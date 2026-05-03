"""Expenses panel — receipts, ledger, item-price catalogue, monthly templates.

Three sub-tabs:

  Ledger      One-row-per-expense table with period/category filters and a
              quick-add bar at the top for fast non-receipt entries (rent,
              utilities, etc.). Double-click a row to edit; rows that came
              from a receipt open the receipt editor with line items.

  Receipts    Full receipt editor with a line-item table. Item-name fields
              autocomplete from the catalogue, autofilling unit_price from
              the last seen price. Subtotal/tax/total are computed live.
              Save writes the receipt + a mirrored ledger transaction.

  Catalogue   Searchable view of every expense item we've ever seen,
              with last/avg/min/max price stats so the user can quickly
              answer "what did eggs cost last time?".

Receipts mirror into `transactions` (`type='expense'`) so existing
summary, goal, and chart aggregates continue to work without changes.
Standalone expenses go through the same FinanceStore.add_transaction
path used by the earlier Earnings panel.
"""

from __future__ import annotations

import calendar as _cal
from datetime import date, timedelta

from PyQt6.QtCore import Qt, QDate, QStringListModel, pyqtSignal
from PyQt6.QtGui import QColor, QBrush
from PyQt6.QtWidgets import (
    QAbstractItemView, QCheckBox, QComboBox, QCompleter, QDateEdit, QDialog,
    QDialogButtonBox, QDoubleSpinBox, QFormLayout, QFrame, QGridLayout,
    QHBoxLayout, QHeaderView, QInputDialog, QLabel, QLineEdit, QMessageBox,
    QPlainTextEdit, QPushButton, QScrollArea, QSizePolicy, QSpinBox,
    QSplitter, QTabWidget, QTableWidget, QTableWidgetItem, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget,
)

from src.config import load_config, save_config
from src.data.finance_store import FinanceStore, Transaction
from src.data.expenses_store import (
    ExpensesStore, Receipt, ReceiptItem, ExpenseItem,
    EXPENSE_CATEGORIES, PAYMENT_METHODS,
)


_FALLBACK_RATE = 150.0
_MONTH_NAMES = ["", "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"]


# ── Default monthly recurring expense templates (moved from finance_panel) ────
_DEFAULT_MONTHLY_PRESETS: list[dict] = [
    {"name": "Rent",                "amount": 0, "currency": "JPY", "category": "Rent / Housing"},
    {"name": "Kids Extracurriculars","amount": 0, "currency": "JPY", "category": "Education"},
    {"name": "Schooling",           "amount": 0, "currency": "JPY", "category": "Education"},
    {"name": "Power",               "amount": 0, "currency": "JPY", "category": "Utilities"},
    {"name": "Water",               "amount": 0, "currency": "JPY", "category": "Utilities"},
    {"name": "Internet",            "amount": 0, "currency": "JPY", "category": "Subscriptions"},
    {"name": "Phone",               "amount": 0, "currency": "JPY", "category": "Subscriptions"},
    {"name": "Gas",                 "amount": 0, "currency": "JPY", "category": "Utilities"},
]


def _load_categories() -> list[str]:
    cats = load_config().get("expense_categories_v2", [])
    return cats if cats else list(EXPENSE_CATEGORIES)


def _save_categories(cats: list[str]) -> None:
    cfg = load_config()
    cfg["expense_categories_v2"] = cats
    save_config(cfg)


def _vendor_history(store: ExpensesStore, limit: int = 200) -> list[str]:
    """Distinct list of vendors we've seen, most recent first."""
    seen: dict[str, str] = {}   # vendor -> latest date
    for r in store.get_receipts():
        v = (r.vendor or "").strip()
        if not v:
            continue
        prev = seen.get(v)
        if prev is None or r.date > prev:
            seen[v] = r.date
    return [v for v, _ in sorted(seen.items(), key=lambda kv: kv[1], reverse=True)][:limit]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Item-name field with catalog autocomplete + price autofill
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ItemNameEdit(QLineEdit):
    """Line edit that autocompletes against the expense-item catalogue.

    When the user picks a known item from the dropdown, the configured
    `price_target` spinbox autofills with that item's last-seen price.
    """
    item_picked = pyqtSignal(object)   # emits ExpenseItem on selection

    def __init__(self, store: ExpensesStore, parent=None):
        super().__init__(parent)
        self._store = store
        self._items: list[ExpenseItem] = []
        self._model = QStringListModel(self)
        completer = QCompleter(self._model, self)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.setCompleter(completer)
        completer.activated.connect(self._on_completer_activated)
        self.textEdited.connect(self._refresh_suggestions)
        self.price_target: QDoubleSpinBox | None = None
        self._refresh_suggestions("")

    def _refresh_suggestions(self, text: str):
        # When the completer inserts a full label (e.g. "Eggs  ·  ¥298") into
        # the field, textEdited fires with that label string.  Refreshing with
        # it would clobber _label_map before _on_completer_activated can use it,
        # leaving the price text stuck in the field.  The "  ·  " separator only
        # ever appears in labels we build, never in a user-typed query.
        if "  ·  " in text:
            return
        self._items = self._store.search_items(text or "", limit=20)
        self._label_map: dict[str, ExpenseItem] = {}
        labels = []
        for it in self._items:
            sym = "¥" if it.last_currency == "JPY" else "$"
            lbl = f"{it.name}  ·  {sym}{it.last_price:,.0f}"
            labels.append(lbl)
            self._label_map[lbl] = it
        self._model.setStringList(labels)

    def _on_completer_activated(self, label: str):
        it = getattr(self, "_label_map", {}).get(label)
        if it is None:
            # Fallback: linear scan in case the map is stale
            for candidate in self._items:
                if label.startswith(candidate.name + "  ·  "):
                    it = candidate
                    break
        if it is None:
            return
        self.setText(it.name)
        if self.price_target:
            self.price_target.setValue(float(it.last_price))
        self.item_picked.emit(it)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Receipt editor dialog (used for both New and Edit)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ReceiptEditorDialog(QDialog):
    """Header + line-item editor for a single receipt.

    Use `Receipt(...)` for a fresh receipt or pass in an existing one.
    `result_receipt` is None until the dialog is accepted.
    """

    def __init__(self, store: ExpensesStore, receipt: Receipt | None = None,
                 categories: list[str] | None = None, parent=None):
        super().__init__(parent)
        self._store = store
        self._categories = categories or _load_categories()
        self._editing = receipt is not None
        self._receipt = receipt or Receipt(
            id="", date=date.today().isoformat(),
        )
        self.result_receipt: Receipt | None = None

        self.setWindowTitle("Edit Receipt" if self._editing else "New Receipt")
        self.setMinimumSize(720, 540)
        self._build_ui()
        self._populate()
        self._recompute_totals()

    # ── UI ─────────────────────────────────────────────────────────────────────

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setSpacing(10)

        # ── Header form: 2-column grid for fast tabbing ────────────────
        hdr = QGridLayout()
        hdr.setHorizontalSpacing(10); hdr.setVerticalSpacing(6)

        self.date_edit = QDateEdit(); self.date_edit.setCalendarPopup(True)
        self.date_edit.setDisplayFormat("yyyy-MM-dd")
        hdr.addWidget(QLabel("Date:"),     0, 0)
        hdr.addWidget(self.date_edit,      0, 1)

        self.vendor_edit = QLineEdit()
        self.vendor_edit.setPlaceholderText("e.g. Aeon, Lawson, JR East…")
        # Autocomplete vendor from history
        v_completer = QCompleter(_vendor_history(self._store), self)
        v_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        v_completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.vendor_edit.setCompleter(v_completer)
        hdr.addWidget(QLabel("Vendor:"),   0, 2)
        hdr.addWidget(self.vendor_edit,    0, 3)

        self.cat_combo = QComboBox()
        self.cat_combo.addItems(self._categories)
        hdr.addWidget(QLabel("Category:"), 1, 0)
        hdr.addWidget(self.cat_combo,      1, 1)

        self.cur_combo = QComboBox()
        self.cur_combo.addItems(["JPY", "USD"])
        self.cur_combo.currentTextChanged.connect(self._on_currency_changed)
        hdr.addWidget(QLabel("Currency:"), 1, 2)
        hdr.addWidget(self.cur_combo,      1, 3)

        self.pay_combo = QComboBox()
        self.pay_combo.addItems(PAYMENT_METHODS)
        hdr.addWidget(QLabel("Paid by:"),  2, 0)
        hdr.addWidget(self.pay_combo,      2, 1)

        self.tax_spin = QDoubleSpinBox()
        self.tax_spin.setRange(0.0, 9_999_999.0)
        self.tax_spin.setDecimals(0)
        self.tax_spin.setPrefix("¥ ")
        self.tax_spin.valueChanged.connect(self._recompute_totals)
        hdr.addWidget(QLabel("Tax (incl.):"), 2, 2)
        hdr.addWidget(self.tax_spin,          2, 3)

        root.addLayout(hdr)

        # ── Items table ──────────────────────────────────────────────
        itm_lbl = QLabel("Items"); itm_lbl.setObjectName("subtitle")
        root.addWidget(itm_lbl)

        self.items_table = QTableWidget()
        self.items_table.setColumnCount(5)
        self.items_table.setHorizontalHeaderLabels(
            ["Item", "Qty", "Unit Price", "Line Total", ""]
        )
        hh = self.items_table.horizontalHeader()
        hh.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        hh.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.items_table.verticalHeader().setVisible(False)
        self.items_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        # Cells host inline widgets, so disable inline editing (we provide
        # the widgets directly).
        self.items_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        root.addWidget(self.items_table, 1)

        row_btns = QHBoxLayout()
        add_btn = QPushButton("+ Add Item"); add_btn.setObjectName("secondary")
        add_btn.clicked.connect(lambda: self._append_row(ReceiptItem(
            id="", receipt_id="", name="", qty=1.0, unit_price=0.0)))
        row_btns.addWidget(add_btn)

        paste_btn = QPushButton("Paste Lines…"); paste_btn.setObjectName("secondary")
        paste_btn.setToolTip(
            "Paste a block of text — one item per line, "
            "tab- or comma-separated: name, qty, unit_price"
        )
        paste_btn.clicked.connect(self._paste_lines)
        row_btns.addWidget(paste_btn)

        row_btns.addStretch()

        self.subtotal_lbl = QLabel("Subtotal: ¥0")
        self.subtotal_lbl.setObjectName("subtitle")
        row_btns.addWidget(self.subtotal_lbl)

        self.total_lbl = QLabel("Total: ¥0")
        self.total_lbl.setStyleSheet("font-size:15px;font-weight:bold;")
        row_btns.addWidget(self.total_lbl)
        root.addLayout(row_btns)

        # ── Notes ─────────────────────────────────────────────────────
        self.notes_edit = QPlainTextEdit()
        self.notes_edit.setPlaceholderText(
            "Notes (optional) — e.g. trip name, project tag, splitwise reference…"
        )
        self.notes_edit.setMaximumHeight(60)
        root.addWidget(self.notes_edit)

        # ── Action buttons ────────────────────────────────────────────
        btns = QHBoxLayout(); btns.addStretch()
        if self._editing:
            del_btn = QPushButton("Delete"); del_btn.setObjectName("destructive")
            del_btn.clicked.connect(self._delete)
            btns.addWidget(del_btn)
        cancel = QPushButton("Cancel"); cancel.setObjectName("secondary")
        cancel.clicked.connect(self.reject)
        btns.addWidget(cancel)
        save_new = QPushButton("Save && New"); save_new.setObjectName("secondary")
        save_new.setToolTip("Save this receipt and start a fresh one")
        save_new.clicked.connect(self._save_and_new)
        if self._editing:
            save_new.setVisible(False)
        btns.addWidget(save_new)
        save = QPushButton("Save"); save.setDefault(True)
        save.clicked.connect(self._save_and_close)
        btns.addWidget(save)
        root.addLayout(btns)

    # ── Population / state ─────────────────────────────────────────────────────

    def _populate(self):
        r = self._receipt
        try:
            y, m, d = (int(x) for x in r.date.split("-"))
            self.date_edit.setDate(QDate(y, m, d))
        except Exception:
            self.date_edit.setDate(QDate.currentDate())
        self.vendor_edit.setText(r.vendor)
        idx = self.cat_combo.findText(r.category)
        if idx >= 0:
            self.cat_combo.setCurrentIndex(idx)
        elif r.category:
            self.cat_combo.addItem(r.category)
            self.cat_combo.setCurrentText(r.category)
        self.cur_combo.setCurrentText(r.currency or "JPY")
        if r.payment_method:
            self.pay_combo.setCurrentText(r.payment_method)
        self.tax_spin.setValue(float(r.tax or 0.0))
        self.notes_edit.setPlainText(r.notes or "")

        # Items: ensure at least one editable row exists
        items = list(r.items) or [ReceiptItem(
            id="", receipt_id="", name="", qty=1.0, unit_price=0.0)]
        for item in items:
            self._append_row(item)

        # Apply currency to spinbox prefixes after populating
        self._on_currency_changed(self.cur_combo.currentText())

    def _on_currency_changed(self, cur: str):
        prefix = "¥ " if cur == "JPY" else "$ "
        decimals = 0 if cur == "JPY" else 2
        step     = 1 if cur == "JPY" else 0.10
        self.tax_spin.setPrefix(prefix)
        self.tax_spin.setDecimals(decimals)
        self.tax_spin.setSingleStep(step)
        for r in range(self.items_table.rowCount()):
            up_spin = self.items_table.cellWidget(r, 2)
            if isinstance(up_spin, QDoubleSpinBox):
                up_spin.setPrefix(prefix)
                up_spin.setDecimals(decimals)
                up_spin.setSingleStep(step)
        self._recompute_totals()

    def _append_row(self, item: ReceiptItem):
        cur = self.cur_combo.currentText() if hasattr(self, "cur_combo") else "JPY"
        prefix = "¥ " if cur == "JPY" else "$ "
        decimals = 0 if cur == "JPY" else 2
        step     = 1 if cur == "JPY" else 0.10

        row = self.items_table.rowCount()
        self.items_table.insertRow(row)

        name_edit = ItemNameEdit(self._store)
        name_edit.setText(item.name)
        self.items_table.setCellWidget(row, 0, name_edit)

        qty_spin = QDoubleSpinBox()
        qty_spin.setRange(0.0, 9_999.0); qty_spin.setDecimals(2)
        qty_spin.setSingleStep(1.0); qty_spin.setValue(float(item.qty or 1.0))
        qty_spin.setMinimumWidth(70)
        self.items_table.setCellWidget(row, 1, qty_spin)

        up_spin = QDoubleSpinBox()
        up_spin.setRange(0.0, 9_999_999.0)
        up_spin.setDecimals(decimals); up_spin.setSingleStep(step)
        up_spin.setPrefix(prefix); up_spin.setValue(float(item.unit_price or 0.0))
        up_spin.setMinimumWidth(110)
        self.items_table.setCellWidget(row, 2, up_spin)
        # Wire item-name picker to autofill price
        name_edit.price_target = up_spin

        line_lbl = QLabel("0")
        line_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        line_lbl.setMinimumWidth(80)
        self.items_table.setCellWidget(row, 3, line_lbl)

        del_btn = QPushButton("✕")
        del_btn.setFixedSize(26, 26)
        del_btn.setObjectName("secondary")
        del_btn.setToolTip("Remove this row")
        del_btn.clicked.connect(lambda _=False, w=name_edit: self._remove_row(w))
        self.items_table.setCellWidget(row, 4, del_btn)

        # Stash the original ReceiptItem so we keep its id on save
        name_edit.setProperty("_orig_id", item.id or "")

        qty_spin.valueChanged.connect(self._recompute_totals)
        up_spin.valueChanged.connect(self._recompute_totals)
        # Recompute when item-name picker fills the price
        name_edit.item_picked.connect(lambda _=None: self._recompute_totals())
        self._recompute_totals()

    def _remove_row(self, name_edit_widget):
        for r in range(self.items_table.rowCount()):
            if self.items_table.cellWidget(r, 0) is name_edit_widget:
                self.items_table.removeRow(r)
                break
        if self.items_table.rowCount() == 0:
            self._append_row(ReceiptItem(
                id="", receipt_id="", name="", qty=1.0, unit_price=0.0))
        self._recompute_totals()

    def _paste_lines(self):
        """Bulk-paste a block of items. Each line may be tab- or comma-
        separated; missing fields default to qty=1, unit_price=0."""
        text, ok = QInputDialog.getMultiLineText(
            self, "Paste Items",
            "One item per line. Format:  name [, qty [, unit_price]]\n"
            "Tab or comma-separated. Lines starting with # are ignored.",
            "",
        )
        if not ok or not text.strip():
            return
        added = 0
        for raw in text.splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in (line.split("\t")
                     if "\t" in line else line.split(","))]
            name = parts[0] if parts else ""
            if not name:
                continue
            try:
                qty = float(parts[1]) if len(parts) > 1 and parts[1] else 1.0
            except ValueError:
                qty = 1.0
            try:
                up = float(parts[2]) if len(parts) > 2 and parts[2] else 0.0
            except ValueError:
                up = 0.0
            self._append_row(ReceiptItem(
                id="", receipt_id="", name=name, qty=qty, unit_price=up))
            added += 1
        if added == 0:
            QMessageBox.information(self, "Paste Items", "No usable lines found.")

    # ── Totals ─────────────────────────────────────────────────────────────────

    def _recompute_totals(self):
        cur = self.cur_combo.currentText() if hasattr(self, "cur_combo") else "JPY"
        sym = "¥" if cur == "JPY" else "$"
        decimals = 0 if cur == "JPY" else 2

        subtotal = 0.0
        for r in range(self.items_table.rowCount()):
            qty_spin = self.items_table.cellWidget(r, 1)
            up_spin  = self.items_table.cellWidget(r, 2)
            line_lbl = self.items_table.cellWidget(r, 3)
            if not (qty_spin and up_spin and line_lbl):
                continue
            line = float(qty_spin.value()) * float(up_spin.value())
            subtotal += line
            line_lbl.setText(
                f"{sym}{line:,.0f}" if decimals == 0 else f"{sym}{line:,.2f}"
            )
        tax = float(self.tax_spin.value())
        total = subtotal + tax
        self.subtotal_lbl.setText(
            f"Subtotal: {sym}{subtotal:,.0f}" if decimals == 0
            else f"Subtotal: {sym}{subtotal:,.2f}"
        )
        self.total_lbl.setText(
            f"Total: {sym}{total:,.0f}" if decimals == 0
            else f"Total: {sym}{total:,.2f}"
        )

    # ── Save / Delete ──────────────────────────────────────────────────────────

    def _collect(self) -> tuple[Receipt, list[ReceiptItem]]:
        qd = self.date_edit.date()
        cur = self.cur_combo.currentText()
        items: list[ReceiptItem] = []
        for r in range(self.items_table.rowCount()):
            name_edit = self.items_table.cellWidget(r, 0)
            qty_spin  = self.items_table.cellWidget(r, 1)
            up_spin   = self.items_table.cellWidget(r, 2)
            if not (name_edit and qty_spin and up_spin):
                continue
            name = name_edit.text().strip()
            if not name:
                continue
            qty = float(qty_spin.value())
            up  = float(up_spin.value())
            items.append(ReceiptItem(
                id=name_edit.property("_orig_id") or "",
                receipt_id=self._receipt.id or "",
                name=name, qty=qty, unit_price=up,
                line_total=qty * up,
                sort_order=r,
            ))
        subtotal = sum(it.line_total for it in items)
        tax = float(self.tax_spin.value())
        total = subtotal + tax
        rec = Receipt(
            id=self._receipt.id,
            date=f"{qd.year():04d}-{qd.month():02d}-{qd.day():02d}",
            vendor=self.vendor_edit.text().strip(),
            category=self.cat_combo.currentText(),
            currency=cur,
            subtotal=subtotal,
            tax=tax,
            total=total,
            payment_method=self.pay_combo.currentText(),
            notes=self.notes_edit.toPlainText().strip(),
            transaction_id=self._receipt.transaction_id,
        )
        return rec, items

    def _validate(self, rec: Receipt, items: list[ReceiptItem]) -> bool:
        if rec.total <= 0 and not items:
            QMessageBox.warning(self, "Empty Receipt",
                "Add at least one line item or a non-zero total.")
            return False
        return True

    def _save_and_close(self):
        rec, items = self._collect()
        if not self._validate(rec, items):
            return
        self.result_receipt = self._store.save_receipt(rec, items)
        self.accept()

    def _save_and_new(self):
        rec, items = self._collect()
        if not self._validate(rec, items):
            return
        self._store.save_receipt(rec, items)
        # Reset for a fresh entry without closing the dialog
        self._receipt = Receipt(id="", date=date.today().isoformat(),
                                category=rec.category, currency=rec.currency,
                                payment_method=rec.payment_method)
        self.vendor_edit.clear()
        self.tax_spin.setValue(0.0)
        self.notes_edit.clear()
        self.items_table.setRowCount(0)
        self._append_row(ReceiptItem(
            id="", receipt_id="", name="", qty=1.0, unit_price=0.0))
        self._recompute_totals()

    def _delete(self):
        if QMessageBox.question(self, "Delete Receipt",
                "Permanently remove this receipt?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                ) != QMessageBox.StandardButton.Yes:
            return
        if self._receipt.id:
            self._store.delete_receipt(self._receipt.id)
        self.result_receipt = None
        self.reject()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Quick-expense dialog (single-line, no receipt detail)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class QuickExpenseDialog(QDialog):
    """A minimal one-shot expense entry — date, amount, currency, category,
    description. For things like rent, gas, or any bill that doesn't need
    line-item breakdown."""

    def __init__(self, categories: list[str], txn: Transaction | None = None,
                 parent=None):
        super().__init__(parent)
        self._editing = txn is not None
        self.txn = txn
        self.setWindowTitle("Edit Expense" if self._editing else "Quick Expense")
        self.setMinimumWidth(380)

        layout = QVBoxLayout(self)
        form = QFormLayout(); form.setSpacing(8)

        self.date_edit = QDateEdit(); self.date_edit.setCalendarPopup(True)
        self.date_edit.setDisplayFormat("yyyy-MM-dd")
        if txn:
            try:
                y, m, d = (int(x) for x in txn.date.split("-"))
                self.date_edit.setDate(QDate(y, m, d))
            except Exception:
                self.date_edit.setDate(QDate.currentDate())
        else:
            self.date_edit.setDate(QDate.currentDate())
        form.addRow("Date:", self.date_edit)

        self.cur_combo = QComboBox(); self.cur_combo.addItems(["JPY", "USD"])
        if txn:
            self.cur_combo.setCurrentText(txn.currency)
        self.cur_combo.currentTextChanged.connect(self._on_currency_changed)
        form.addRow("Currency:", self.cur_combo)

        self.amount_spin = QDoubleSpinBox()
        self.amount_spin.setRange(0.0, 99_999_999.0)
        if txn:
            self.amount_spin.setValue(txn.amount)
        form.addRow("Amount:", self.amount_spin)

        self.cat_combo = QComboBox(); self.cat_combo.addItems(categories)
        if txn:
            idx = self.cat_combo.findText(txn.category)
            if idx >= 0:
                self.cat_combo.setCurrentIndex(idx)
            else:
                self.cat_combo.addItem(txn.category)
                self.cat_combo.setCurrentText(txn.category)
        form.addRow("Category:", self.cat_combo)

        self.desc_edit = QLineEdit()
        self.desc_edit.setPlaceholderText("e.g. Rent November, Gas — round trip")
        if txn:
            self.desc_edit.setText(txn.description)
        form.addRow("Description:", self.desc_edit)

        layout.addLayout(form)

        sep = QFrame(); sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine); layout.addWidget(sep)

        btns = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        btns.accepted.connect(self.accept); btns.rejected.connect(self.reject)
        layout.addWidget(btns)

        self._on_currency_changed(self.cur_combo.currentText())

    def _on_currency_changed(self, cur: str):
        if cur == "JPY":
            self.amount_spin.setPrefix("¥ "); self.amount_spin.setDecimals(0)
            self.amount_spin.setSingleStep(100)
        else:
            self.amount_spin.setPrefix("$ "); self.amount_spin.setDecimals(2)
            self.amount_spin.setSingleStep(1.0)

    def get_data(self) -> dict:
        qd = self.date_edit.date()
        return {
            "date":        f"{qd.year():04d}-{qd.month():02d}-{qd.day():02d}",
            "amount":      float(self.amount_spin.value()),
            "txn_type":    "expense",
            "category":    self.cat_combo.currentText(),
            "description": self.desc_edit.text().strip(),
            "currency":    self.cur_combo.currentText(),
            "is_job_pay":  False,
        }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Monthly recurring expense templates (moved from finance_panel)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class MonthlyExpenseTemplatesDialog(QDialog):
    """Add / edit / delete recurring expense templates."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Manage Monthly Expense Templates")
        self.setMinimumSize(560, 420)
        self._build_ui(); self._refresh()

    @staticmethod
    def _load() -> list[dict]:
        presets = load_config().get("monthly_expense_presets", [])
        return presets if presets else list(_DEFAULT_MONTHLY_PRESETS)

    @staticmethod
    def _save(presets: list[dict]):
        cfg = load_config(); cfg["monthly_expense_presets"] = presets
        save_config(cfg)

    def _build_ui(self):
        layout = QVBoxLayout(self); layout.setSpacing(10)
        info = QLabel(
            "These templates power the Monthly Expenses bulk-log dialog.\n"
            "Set typical amounts here — adjust per-month when logging.")
        info.setObjectName("subtitle"); info.setWordWrap(True)
        layout.addWidget(info)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["Name", "Default Amount", "Currency", "Category"])
        hh = self.table.horizontalHeader()
        hh.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        hh.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table, 1)

        sep = QFrame(); sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine); layout.addWidget(sep)

        form = QFormLayout(); form.setSpacing(6)
        self._name_edit = QLineEdit()
        self._name_edit.setPlaceholderText("e.g. Gym Membership")
        form.addRow("Name:", self._name_edit)
        amt_row = QHBoxLayout(); amt_row.setSpacing(6)
        self._amount_spin = QDoubleSpinBox()
        self._amount_spin.setRange(0, 9_999_999); self._amount_spin.setDecimals(0)
        self._amount_spin.setSingleStep(1000); self._amount_spin.setValue(0)
        amt_row.addWidget(self._amount_spin, 1)
        self._currency_combo = QComboBox(); self._currency_combo.addItems(["JPY", "USD"])
        self._currency_combo.currentTextChanged.connect(self._on_cur)
        amt_row.addWidget(self._currency_combo)
        form.addRow("Default Amount:", amt_row)
        self._cat_combo = QComboBox(); self._cat_combo.addItems(_load_categories())
        form.addRow("Category:", self._cat_combo)
        layout.addLayout(form)

        btn_row = QHBoxLayout()
        add_btn = QPushButton("Add Template"); add_btn.clicked.connect(self._add)
        btn_row.addWidget(add_btn)
        edit_btn = QPushButton("Edit Selected"); edit_btn.setObjectName("secondary")
        edit_btn.clicked.connect(self._edit_selected); btn_row.addWidget(edit_btn)
        del_btn = QPushButton("Delete Selected"); del_btn.setObjectName("destructive")
        del_btn.clicked.connect(self._delete_selected); btn_row.addWidget(del_btn)
        btn_row.addStretch()
        reset_btn = QPushButton("Reset Defaults"); reset_btn.setObjectName("secondary")
        reset_btn.clicked.connect(self._reset_defaults); btn_row.addWidget(reset_btn)
        close_btn = QPushButton("Done"); close_btn.clicked.connect(self.accept)
        btn_row.addWidget(close_btn)
        layout.addLayout(btn_row)

    def _on_cur(self, cur: str):
        if cur == "JPY":
            self._amount_spin.setDecimals(0); self._amount_spin.setSingleStep(1000)
        else:
            self._amount_spin.setDecimals(2); self._amount_spin.setSingleStep(10)

    def _refresh(self):
        ps = self._load()
        self.table.setRowCount(len(ps))
        for i, p in enumerate(ps):
            self.table.setItem(i, 0, QTableWidgetItem(p["name"]))
            sym = "¥" if p["currency"] == "JPY" else "$"
            amt = int(p["amount"]) if p["currency"] == "JPY" else p["amount"]
            self.table.setItem(i, 1, QTableWidgetItem(f"{sym}{amt:,}"))
            self.table.setItem(i, 2, QTableWidgetItem(p["currency"]))
            self.table.setItem(i, 3, QTableWidgetItem(p["category"]))

    def _add(self):
        name = self._name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Missing Name", "Please enter a name."); return
        ps = self._load()
        ps.append({
            "name": name,
            "amount": self._amount_spin.value(),
            "currency": self._currency_combo.currentText(),
            "category": self._cat_combo.currentText(),
        })
        self._save(ps); self._name_edit.clear(); self._refresh()

    def _edit_selected(self):
        rows = self.table.selectionModel().selectedRows()
        if not rows: return
        idx = rows[0].row()
        ps = self._load()
        if idx >= len(ps): return
        p = ps[idx]
        self._name_edit.setText(p["name"])
        self._amount_spin.setValue(p["amount"])
        self._currency_combo.setCurrentText(p["currency"])
        self._cat_combo.setCurrentText(p["category"])
        ps.pop(idx); self._save(ps); self._refresh()

    def _delete_selected(self):
        rows = self.table.selectionModel().selectedRows()
        if not rows: return
        if QMessageBox.question(
            self, "Delete", "Delete selected template(s)?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        ) == QMessageBox.StandardButton.Yes:
            ps = self._load()
            for r in sorted(rows, key=lambda x: -x.row()):
                if r.row() < len(ps): ps.pop(r.row())
            self._save(ps); self._refresh()

    def _reset_defaults(self):
        if QMessageBox.question(
            self, "Reset", "Reset templates to defaults?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        ) == QMessageBox.StandardButton.Yes:
            self._save(list(_DEFAULT_MONTHLY_PRESETS)); self._refresh()


class MonthlyExpensesDialog(QDialog):
    """Bulk-log a month of recurring bills, tagged [Monthly] for tax export."""

    def __init__(self, finance_store: FinanceStore, parent=None):
        super().__init__(parent)
        self.fs = finance_store
        self.setWindowTitle("Monthly Expenses")
        self.setMinimumSize(620, 480)
        self._year  = date.today().year
        self._month = date.today().month
        self._rows: list[dict] = []
        self._build_ui(); self._reload()

    def _build_ui(self):
        layout = QVBoxLayout(self); layout.setSpacing(10)
        nav = QHBoxLayout()
        prev_btn = QPushButton("←"); prev_btn.setObjectName("secondary")
        prev_btn.setFixedSize(28, 28); prev_btn.clicked.connect(self._prev)
        nav.addWidget(prev_btn)
        self._month_lbl = QLabel(); self._month_lbl.setStyleSheet("font-weight:bold;")
        self._month_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nav.addWidget(self._month_lbl, 1)
        next_btn = QPushButton("→"); next_btn.setObjectName("secondary")
        next_btn.setFixedSize(28, 28); next_btn.clicked.connect(self._next)
        nav.addWidget(next_btn)
        layout.addLayout(nav)

        self._warn_lbl = QLabel(""); self._warn_lbl.setObjectName("subtitle")
        self._warn_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._warn_lbl)

        scroll = QScrollArea(); scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        self._rows_widget = QWidget()
        self._rows_layout = QVBoxLayout(self._rows_widget)
        self._rows_layout.setSpacing(4)
        scroll.setWidget(self._rows_widget)
        layout.addWidget(scroll, 1)

        sep = QFrame(); sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine); layout.addWidget(sep)

        totals_row = QHBoxLayout(); totals_row.addStretch()
        self._total_lbl = QLabel("Total: ¥0  /  $0.00")
        self._total_lbl.setStyleSheet("font-weight:bold;")
        totals_row.addWidget(self._total_lbl)
        layout.addLayout(totals_row)

        btn_row = QHBoxLayout()
        manage_btn = QPushButton("Manage Templates"); manage_btn.setObjectName("secondary")
        manage_btn.clicked.connect(self._manage); btn_row.addWidget(manage_btn)
        check_all = QPushButton("Check All"); check_all.setObjectName("secondary")
        check_all.clicked.connect(lambda: self._set_all(True)); btn_row.addWidget(check_all)
        uncheck = QPushButton("Uncheck All"); uncheck.setObjectName("secondary")
        uncheck.clicked.connect(lambda: self._set_all(False)); btn_row.addWidget(uncheck)
        btn_row.addStretch()
        cancel = QPushButton("Cancel"); cancel.setObjectName("secondary")
        cancel.clicked.connect(self.reject); btn_row.addWidget(cancel)
        log_btn = QPushButton("Log Selected"); log_btn.clicked.connect(self._log)
        btn_row.addWidget(log_btn)
        layout.addLayout(btn_row)

    def _reload(self):
        while self._rows_layout.count():
            item = self._rows_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        self._rows = []
        for p in MonthlyExpenseTemplatesDialog._load():
            row = QWidget(); rl = QHBoxLayout(row)
            rl.setContentsMargins(0, 0, 0, 0); rl.setSpacing(8)
            chk = QCheckBox(); chk.setChecked(True); chk.setFixedWidth(22)
            rl.addWidget(chk)
            name = QLabel(p["name"]); rl.addWidget(name, 1)
            amt = QDoubleSpinBox()
            if p["currency"] == "JPY":
                amt.setRange(0, 9_999_999); amt.setDecimals(0); amt.setPrefix("¥ ")
                amt.setSingleStep(1000)
            else:
                amt.setRange(0, 99_999); amt.setDecimals(2); amt.setPrefix("$ ")
                amt.setSingleStep(10)
            amt.setValue(p["amount"]); amt.setMinimumWidth(120)
            amt.valueChanged.connect(self._update_total)
            chk.toggled.connect(self._update_total)
            rl.addWidget(amt)
            cur = QLabel(p["currency"]); cur.setFixedWidth(40); rl.addWidget(cur)
            cat = QLabel(p["category"]); cat.setObjectName("subtitle")
            cat.setFixedWidth(140); rl.addWidget(cat)
            self._rows_layout.addWidget(row)
            self._rows.append({"check": chk, "amount": amt, "preset": p})
        self._rows_layout.addStretch()
        self._update_label(); self._update_total()

    def _update_label(self):
        self._month_lbl.setText(f"{_MONTH_NAMES[self._month]} {self._year}")
        if self.fs.has_monthly_tag(self._year, self._month):
            self._warn_lbl.setText("⚠ Already logged for this month — duplicates may be created.")
        else:
            self._warn_lbl.setText("")

    def _update_total(self):
        total_jpy = 0.0
        rate = float(load_config().get("usd_jpy_fallback_rate", _FALLBACK_RATE)) or _FALLBACK_RATE
        for r in self._rows:
            if not r["check"].isChecked(): continue
            v = r["amount"].value()
            total_jpy += v if r["preset"]["currency"] == "JPY" else v * rate
        total_usd = total_jpy / rate if rate else 0
        self._total_lbl.setText(f"Total: ¥{int(total_jpy):,}  /  ${total_usd:,.2f}")

    def _set_all(self, state: bool):
        for r in self._rows: r["check"].setChecked(state)

    def _prev(self):
        if self._month == 1: self._month = 12; self._year -= 1
        else: self._month -= 1
        self._update_label()

    def _next(self):
        if self._month == 12: self._month = 1; self._year += 1
        else: self._month += 1
        self._update_label()

    def _manage(self):
        MonthlyExpenseTemplatesDialog(self).exec(); self._reload()

    def _log(self):
        sel = [r for r in self._rows if r["check"].isChecked()]
        if not sel:
            QMessageBox.warning(self, "Nothing Selected", "Check at least one row."); return
        last_day = _cal.monthrange(self._year, self._month)[1]
        log_date = date(self._year, self._month, last_day).isoformat()
        n = 0
        for r in sel:
            v = r["amount"].value()
            if v <= 0: continue
            p = r["preset"]
            self.fs.add_transaction(
                date=log_date, amount=v, txn_type="expense",
                category=p["category"], description=f"[Monthly] {p['name']}",
                currency=p["currency"], is_job_pay=False,
            )
            n += 1
        QMessageBox.information(self, "Logged",
            f"Logged {n} expense(s) for {_MONTH_NAMES[self._month]} {self._year}.")
        self.accept()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ExpensesPanel — top-level UI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ExpensesPanel(QWidget):
    """The dedicated Expenses tab — receipts, ledger, and item catalogue."""

    def __init__(self, finance_store: FinanceStore | None = None,
                 expenses_store: ExpensesStore | None = None,
                 parent=None):
        super().__init__(parent)
        self.fs = finance_store or FinanceStore()
        self.store = expenses_store or ExpensesStore(self.fs)
        self._palette: dict = {}
        self._txn_ids: list[str] = []
        self._build_ui()
        self._refresh()

    def set_palette(self, palette: dict):
        self._palette = palette
        self._refresh()

    def showEvent(self, event):
        super().showEvent(event); self._refresh()

    # ── UI ─────────────────────────────────────────────────────────────────────

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(16, 12, 16, 12); outer.setSpacing(8)

        header = QHBoxLayout()
        title = QLabel("Expenses"); title.setObjectName("sectionTitle")
        header.addWidget(title)
        sub = QLabel("All outgoing transactions, receipts, and item history")
        sub.setObjectName("subtitle")
        header.addWidget(sub); header.addStretch()

        new_rec_btn = QPushButton("+ Receipt")
        new_rec_btn.setToolTip("Open the receipt editor (line items, vendor, etc.)")
        new_rec_btn.clicked.connect(self._new_receipt)
        header.addWidget(new_rec_btn)

        new_exp_btn = QPushButton("+ Quick Expense")
        new_exp_btn.setObjectName("secondary")
        new_exp_btn.setToolTip("Log a one-line expense without line items (rent, gas, etc.)")
        new_exp_btn.clicked.connect(self._new_quick_expense)
        header.addWidget(new_exp_btn)

        monthly_btn = QPushButton("Monthly Bills")
        monthly_btn.setObjectName("secondary")
        monthly_btn.setToolTip("Bulk-log recurring monthly expenses (rent, utilities…)")
        monthly_btn.clicked.connect(self._open_monthly)
        header.addWidget(monthly_btn)

        cats_btn = QPushButton("Categories")
        cats_btn.setObjectName("secondary")
        cats_btn.setToolTip("Add or remove expense categories")
        cats_btn.clicked.connect(self._manage_categories)
        header.addWidget(cats_btn)

        outer.addLayout(header)

        self._tabs = QTabWidget()
        self._tabs.addTab(self._build_ledger_tab(),  "Ledger")
        self._tabs.addTab(self._build_receipts_tab(),"Receipts")
        self._tabs.addTab(self._build_catalog_tab(), "Item Catalogue")
        outer.addWidget(self._tabs, 1)

    # ── Ledger tab ─────────────────────────────────────────────────────────────

    def _build_ledger_tab(self) -> QWidget:
        w = QWidget(); v = QVBoxLayout(w)
        v.setContentsMargins(0, 8, 0, 0); v.setSpacing(6)

        # Filters — search first (far left), then period pills, then date range
        f = QHBoxLayout(); f.setSpacing(6)

        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search vendor / description…")
        self.search_edit.setMinimumWidth(180)
        self.search_edit.setMaximumWidth(240)
        self.search_edit.textChanged.connect(self._refresh)
        f.addWidget(self.search_edit)

        f.addSpacing(4)

        # Compact acronym period pills
        _pill_style = (
            "QPushButton{border-radius:10px;padding:0 8px;"
            "font-size:11px;font-weight:bold;min-width:32px;max-width:42px;}"
        )
        for label, tip, fn in [
            ("TM", "This Month", self._filter_this_month),
            ("LM", "Last Month", self._filter_last_month),
            ("TY", "This Year",  self._filter_this_year),
            ("AT", "All Time",   self._filter_all_time),
        ]:
            b = QPushButton(label); b.setObjectName("secondary")
            b.setFixedHeight(24); b.setToolTip(tip)
            b.setStyleSheet(_pill_style)
            b.clicked.connect(fn); f.addWidget(b)

        f.addSpacing(6); f.addWidget(QLabel("Cat:"))
        self.cat_filter = QComboBox()
        self.cat_filter.addItem("All")
        self.cat_filter.addItems(_load_categories())
        self.cat_filter.currentTextChanged.connect(self._refresh)
        f.addWidget(self.cat_filter)

        f.addSpacing(6); f.addWidget(QLabel("From:"))
        today = date.today()
        self.from_edit = QDateEdit(); self.from_edit.setCalendarPopup(True)
        self.from_edit.setDisplayFormat("yyyy-MM-dd")
        self.from_edit.setMinimumWidth(108)
        self.from_edit.setDate(QDate(today.year, today.month, 1))
        self.from_edit.dateChanged.connect(self._refresh)
        f.addWidget(self.from_edit)
        f.addWidget(QLabel("To:"))
        self.to_edit = QDateEdit(); self.to_edit.setCalendarPopup(True)
        self.to_edit.setDisplayFormat("yyyy-MM-dd")
        self.to_edit.setMinimumWidth(108)
        self.to_edit.setDate(QDate(today.year, today.month, today.day))
        self.to_edit.dateChanged.connect(self._refresh)
        f.addWidget(self.to_edit)
        f.addStretch()
        v.addLayout(f)

        # Splitter: table | summary panel
        split = QSplitter(Qt.Orientation.Horizontal)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ["Date", "Category", "Amount", "¥ Amount", "Description", "Receipt", ""]
        )
        hh = self.table.horizontalHeader()
        hh.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        for col in (0, 1, 2, 3, 5, 6):
            hh.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.doubleClicked.connect(self._edit_row)
        split.addWidget(self.table)

        summary = QWidget(); sl = QVBoxLayout(summary)
        sl.setContentsMargins(12, 8, 12, 8); sl.setSpacing(6)
        st = QLabel("Period Summary"); st.setObjectName("sectionTitle")
        sl.addWidget(st)
        self.total_lbl = QLabel("Total: $0")
        self.total_lbl.setStyleSheet("font-size:18px;font-weight:bold;")
        sl.addWidget(self.total_lbl)
        self.count_lbl = QLabel("0 entries"); self.count_lbl.setObjectName("subtitle")
        sl.addWidget(self.count_lbl)
        sep = QFrame(); sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine); sl.addWidget(sep)
        ct = QLabel("By Category"); ct.setStyleSheet("font-weight:bold;")
        sl.addWidget(ct)
        self._cat_box = QWidget(); self._cat_layout = QVBoxLayout(self._cat_box)
        self._cat_layout.setContentsMargins(0, 0, 0, 0); self._cat_layout.setSpacing(2)
        sl.addWidget(self._cat_box)
        sl.addStretch()
        split.addWidget(summary)
        split.setSizes([700, 280])
        v.addWidget(split, 1)

        # Bottom: delete, export
        bot = QHBoxLayout()
        del_btn = QPushButton("Delete Selected"); del_btn.setObjectName("destructive")
        del_btn.clicked.connect(self._delete_selected)
        bot.addWidget(del_btn); bot.addStretch()
        v.addLayout(bot)

        return w

    # ── Receipts tab ───────────────────────────────────────────────────────────

    def _build_receipts_tab(self) -> QWidget:
        w = QWidget(); v = QVBoxLayout(w)
        v.setContentsMargins(0, 8, 0, 0); v.setSpacing(6)

        bar = QHBoxLayout()
        bar.addWidget(QLabel("Filter:"))
        self.rcpt_search = QLineEdit()
        self.rcpt_search.setPlaceholderText("Vendor or category…")
        self.rcpt_search.textChanged.connect(self._refresh_receipts)
        bar.addWidget(self.rcpt_search, 1)
        new_btn = QPushButton("+ New Receipt")
        new_btn.clicked.connect(self._new_receipt); bar.addWidget(new_btn)
        v.addLayout(bar)

        self.rcpt_table = QTableWidget()
        self.rcpt_table.setColumnCount(6)
        self.rcpt_table.setHorizontalHeaderLabels(
            ["Date", "Vendor", "Category", "Items", "Total", "Currency"]
        )
        hh = self.rcpt_table.horizontalHeader()
        hh.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        for col in (0, 3, 4, 5):
            hh.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)
        self.rcpt_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.rcpt_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.rcpt_table.setAlternatingRowColors(True)
        self.rcpt_table.doubleClicked.connect(self._edit_receipt_row)
        v.addWidget(self.rcpt_table, 1)

        return w

    # ── Catalogue tab ──────────────────────────────────────────────────────────

    def _build_catalog_tab(self) -> QWidget:
        w = QWidget(); v = QVBoxLayout(w)
        v.setContentsMargins(0, 8, 0, 0); v.setSpacing(6)

        bar = QHBoxLayout()
        bar.addWidget(QLabel("Search:"))
        self.cat_search = QLineEdit()
        self.cat_search.setPlaceholderText("Item name (e.g. eggs, milk, rent)…")
        self.cat_search.textChanged.connect(self._refresh_catalog)
        bar.addWidget(self.cat_search, 1)
        bar.addWidget(QLabel("Sort:"))
        self.cat_sort = QComboBox()
        self.cat_sort.addItems(["Name", "Most Seen", "Most Recent", "Highest Price"])
        self.cat_sort.currentTextChanged.connect(self._refresh_catalog)
        bar.addWidget(self.cat_sort)
        v.addLayout(bar)

        # Tree widget: top-level rows are items; child rows are per-vendor
        # price breakdowns, loaded lazily on first expand.
        self.cat_tree = QTreeWidget()
        self.cat_tree.setColumnCount(7)
        self.cat_tree.setHeaderLabels(
            ["Item", "Last Price", "Avg", "Min", "Max", "Times Seen", "Last Date"]
        )
        hh = self.cat_tree.header()
        hh.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        for col in (1, 2, 3, 4, 5, 6):
            hh.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)
        self.cat_tree.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.cat_tree.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.cat_tree.setAlternatingRowColors(True)
        self.cat_tree.setRootIsDecorated(True)
        self.cat_tree.itemExpanded.connect(self._on_catalog_item_expanded)
        v.addWidget(self.cat_tree, 1)

        bot = QHBoxLayout()
        del_btn = QPushButton("Remove Selected"); del_btn.setObjectName("destructive")
        del_btn.setToolTip("Drop this item from the catalogue (won't affect past receipts)")
        del_btn.clicked.connect(self._delete_catalog_item)
        bot.addWidget(del_btn); bot.addStretch()
        v.addLayout(bot)

        return w

    # ── Filters ────────────────────────────────────────────────────────────────

    def _set_range(self, start: date, end: date):
        self.from_edit.blockSignals(True); self.to_edit.blockSignals(True)
        self.from_edit.setDate(QDate(start.year, start.month, start.day))
        self.to_edit.setDate(QDate(end.year, end.month, end.day))
        self.from_edit.blockSignals(False); self.to_edit.blockSignals(False)
        self._refresh()

    def _filter_this_month(self):
        t = date.today(); self._set_range(t.replace(day=1), t)

    def _filter_last_month(self):
        t = date.today(); first = t.replace(day=1)
        last_prev = first - timedelta(days=1)
        self._set_range(last_prev.replace(day=1), last_prev)

    def _filter_this_year(self):
        t = date.today(); self._set_range(t.replace(month=1, day=1), t)

    def _filter_all_time(self):
        self._set_range(date(2000, 1, 1), date.today())

    # ── Refreshers ─────────────────────────────────────────────────────────────

    def _refresh(self):
        self._refresh_ledger()
        self._refresh_receipts()
        self._refresh_catalog()

    def _refresh_ledger(self):
        rate = float(load_config().get("usd_jpy_fallback_rate", _FALLBACK_RATE)) or _FALLBACK_RATE
        qs = self.from_edit.date(); qe = self.to_edit.date()
        start = f"{qs.year():04d}-{qs.month():02d}-{qs.day():02d}"
        end   = f"{qe.year():04d}-{qe.month():02d}-{qe.day():02d}"
        cat = self.cat_filter.currentText()
        query = self.search_edit.text().strip().lower()

        txns = [t for t in self.fs.get_transactions(start, end, "expense")]
        if cat != "All":
            txns = [t for t in txns if t.category == cat]
        if query:
            txns = [t for t in txns
                    if query in t.description.lower()
                    or query in t.category.lower()]

        red = self._palette.get("red", "#f38ba8")
        receipt_clr = self._palette.get("accent", "#89b4fa")

        self.table.setRowCount(len(txns)); self._txn_ids = []
        for i, t in enumerate(txns):
            self._txn_ids.append(t.id)
            self.table.setItem(i, 0, QTableWidgetItem(t.date))
            self.table.setItem(i, 1, QTableWidgetItem(t.category))

            sym = "¥" if t.currency == "JPY" else "$"
            amt_str = (f"-{sym}{int(t.amount):,}" if t.currency == "JPY"
                       else f"-{sym}{t.amount:,.2f}")
            ai = QTableWidgetItem(amt_str)
            ai.setForeground(QBrush(QColor(red)))
            ai.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(i, 2, ai)

            jpy_v = int(t.amount) if t.currency == "JPY" else int(t.amount * rate)
            ji = QTableWidgetItem(f"-¥{jpy_v:,}")
            ji.setForeground(QBrush(QColor(red)))
            ji.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(i, 3, ji)

            self.table.setItem(i, 4, QTableWidgetItem(t.description))

            # Receipt indicator: pull receipt_id from the row directly
            from src.data.database import get_connection
            conn = get_connection()
            try:
                row = conn.execute(
                    "SELECT receipt_id FROM transactions WHERE id=?", (t.id,)
                ).fetchone()
            finally:
                conn.close()
            rid = row["receipt_id"] if row and row["receipt_id"] else ""
            label = "● View" if rid else ""
            ri = QTableWidgetItem(label)
            if rid:
                ri.setForeground(QBrush(QColor(receipt_clr)))
            self.table.setItem(i, 5, ri)
            # Stash the receipt id on the row so double-click can find it
            self.table.setItem(i, 6, QTableWidgetItem(rid))

        # Hide the receipt-id helper column
        self.table.setColumnHidden(6, True)

        # Summary
        total_usd = 0.0
        by_cat: dict[str, float] = {}
        for t in txns:
            usd = t.amount / rate if t.currency == "JPY" else t.amount
            total_usd += usd
            by_cat[t.category] = by_cat.get(t.category, 0.0) + usd
        self.total_lbl.setText(f"Total: ${total_usd:,.2f}  /  ¥{int(total_usd * rate):,}")
        self.total_lbl.setStyleSheet(f"font-size:18px;font-weight:bold;color:{red};")
        self.count_lbl.setText(f"{len(txns)} entries")
        while self._cat_layout.count():
            child = self._cat_layout.takeAt(0)
            if child.widget(): child.widget().deleteLater()
        if by_cat:
            mx = max(by_cat.values()) or 1.0
            for cat_name, amt in sorted(by_cat.items(), key=lambda kv: -kv[1]):
                pct = int(amt / mx * 100)
                lbl = QLabel(
                    f"{cat_name:<22}  ${amt:,.2f}   {pct:>3}%"
                )
                lbl.setStyleSheet("font-family:monospace;font-size:11px;")
                self._cat_layout.addWidget(lbl)
        else:
            ph = QLabel("No expenses in this period")
            ph.setObjectName("subtitle"); self._cat_layout.addWidget(ph)

    def _refresh_receipts(self):
        if not hasattr(self, "rcpt_table"):
            return
        q = self.rcpt_search.text().strip().lower() if hasattr(self, "rcpt_search") else ""
        receipts = self.store.get_receipts()
        if q:
            receipts = [r for r in receipts
                        if q in (r.vendor or "").lower()
                        or q in (r.category or "").lower()
                        or any(q in (it.name or "").lower() for it in r.items)]
        self.rcpt_table.setRowCount(len(receipts))
        self._receipt_ids: list[str] = []
        for i, r in enumerate(receipts):
            self._receipt_ids.append(r.id)
            self.rcpt_table.setItem(i, 0, QTableWidgetItem(r.date))
            self.rcpt_table.setItem(i, 1, QTableWidgetItem(r.vendor))
            self.rcpt_table.setItem(i, 2, QTableWidgetItem(r.category))
            self.rcpt_table.setItem(i, 3, QTableWidgetItem(str(len(r.items))))
            sym = "¥" if r.currency == "JPY" else "$"
            tot = (f"{sym}{int(r.total):,}" if r.currency == "JPY"
                   else f"{sym}{r.total:,.2f}")
            ti = QTableWidgetItem(tot)
            ti.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.rcpt_table.setItem(i, 4, ti)
            self.rcpt_table.setItem(i, 5, QTableWidgetItem(r.currency))

    # ── Catalogue helpers ──────────────────────────────────────────────────────

    @staticmethod
    def _fmt_price(val: float, currency: str) -> str:
        sym = "¥" if currency == "JPY" else "$"
        return f"{sym}{val:,.0f}" if currency == "JPY" else f"{sym}{val:,.2f}"

    def _refresh_catalog(self):
        if not hasattr(self, "cat_tree"):
            return
        q = self.cat_search.text().strip() if hasattr(self, "cat_search") else ""
        sort_label = self.cat_sort.currentText() if hasattr(self, "cat_sort") else "Name"
        sort_key = {
            "Name": "name", "Most Seen": "seen",
            "Most Recent": "recent", "Highest Price": "price",
        }.get(sort_label, "name")
        items = self.store.search_items(q, limit=500) if q else self.store.get_all_items(sort_by=sort_key)

        self.cat_tree.blockSignals(True)
        self.cat_tree.clear()

        for it in items:
            fp = self._fmt_price
            node = QTreeWidgetItem([
                it.name,
                fp(it.last_price, it.last_currency),
                fp(it.avg_price,  it.last_currency),
                fp(it.min_price,  it.last_currency),
                fp(it.max_price,  it.last_currency),
                str(it.times_seen),
                it.last_seen_date,
            ])
            node.setData(0, Qt.ItemDataRole.UserRole, it.id)
            node.setData(0, Qt.ItemDataRole.UserRole + 1, it.name)
            # Placeholder child so Qt shows the expand arrow; populated lazily.
            node.setData(0, Qt.ItemDataRole.UserRole + 2, False)  # expanded flag
            if it.times_seen > 0:
                placeholder = QTreeWidgetItem(["Loading…"])
                node.addChild(placeholder)
            self.cat_tree.addTopLevelItem(node)

        self.cat_tree.blockSignals(False)

    def _on_catalog_item_expanded(self, node: QTreeWidgetItem):
        already_loaded = node.data(0, Qt.ItemDataRole.UserRole + 2)
        if already_loaded:
            return
        node.setData(0, Qt.ItemDataRole.UserRole + 2, True)
        item_name = node.data(0, Qt.ItemDataRole.UserRole + 1)
        if not item_name:
            return

        vendors = self.store.get_item_all_prices(item_name)

        # Remove placeholder
        while node.childCount():
            node.removeChild(node.child(0))

        if not vendors:
            empty = QTreeWidgetItem(["  (no receipt data found)"])
            node.addChild(empty)
            return

        for v in vendors:
            sym = "¥" if v["currency"] == "JPY" else "$"
            fmt_p = lambda x: f"{x:,.0f}" if v["currency"] == "JPY" else f"{x:,.2f}"

            # Individual prices as a compact space-separated list in the "Last Price" column
            price_list = "  ".join(f"{sym}{fmt_p(p)}" for p in v["prices"])

            child = QTreeWidgetItem([
                f"  ▸ {v['vendor']}",
                price_list,
                f"{sym}{fmt_p(v['avg_price'])}",
                f"{sym}{fmt_p(v['min_price'])}",
                f"{sym}{fmt_p(v['max_price'])}",
                str(v["times_seen"]),
                v["last_date"],
            ])
            node.addChild(child)

    # ── Actions ────────────────────────────────────────────────────────────────

    def _new_receipt(self):
        dlg = ReceiptEditorDialog(self.store, parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self._refresh()

    def _new_quick_expense(self):
        dlg = QuickExpenseDialog(_load_categories(), parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self.fs.add_transaction(**dlg.get_data())
            self._refresh()

    def _open_monthly(self):
        if MonthlyExpensesDialog(self.fs, self).exec() == QDialog.DialogCode.Accepted:
            self._refresh()

    def _manage_categories(self):
        cats = _load_categories()
        text, ok = QInputDialog.getMultiLineText(
            self, "Expense Categories",
            "One category per line. Empty lines are ignored.",
            "\n".join(cats),
        )
        if not ok:
            return
        new_cats = [c.strip() for c in text.splitlines() if c.strip()]
        if not new_cats:
            QMessageBox.warning(self, "Empty", "At least one category is required.")
            return
        _save_categories(new_cats)
        # Rebuild filter combo
        self.cat_filter.blockSignals(True)
        self.cat_filter.clear(); self.cat_filter.addItem("All")
        self.cat_filter.addItems(new_cats)
        self.cat_filter.blockSignals(False)
        self._refresh()

    def _edit_row(self, index):
        row = index.row()
        if row < 0 or row >= len(self._txn_ids):
            return
        rid = (self.table.item(row, 6) or QTableWidgetItem("")).text()
        if rid:
            rec = self.store.get_receipt(rid)
            if rec:
                dlg = ReceiptEditorDialog(self.store, receipt=rec, parent=self)
                if dlg.exec() == QDialog.DialogCode.Accepted:
                    self._refresh()
                return
        # Standalone transaction — open the quick-expense editor
        txn = next((t for t in self.fs.get_transactions()
                    if t.id == self._txn_ids[row]), None)
        if not txn:
            return
        dlg = QuickExpenseDialog(_load_categories(), txn=txn, parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            d = dlg.get_data()
            txn.date = d["date"]; txn.amount = d["amount"]
            txn.category = d["category"]; txn.description = d["description"]
            txn.currency = d["currency"]
            self.fs.update_transaction(txn)
            self._refresh()

    def _edit_receipt_row(self, index):
        row = index.row()
        if row < 0 or row >= len(self._receipt_ids):
            return
        rec = self.store.get_receipt(self._receipt_ids[row])
        if not rec:
            return
        dlg = ReceiptEditorDialog(self.store, receipt=rec, parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted or dlg.result_receipt is None:
            self._refresh()

    def _delete_selected(self):
        rows = self.table.selectionModel().selectedRows()
        if not rows: return
        if QMessageBox.question(
            self, "Delete", f"Delete {len(rows)} entry/entries?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        ) != QMessageBox.StandardButton.Yes:
            return
        for idx in rows:
            r = idx.row()
            if r >= len(self._txn_ids): continue
            rid = (self.table.item(r, 6) or QTableWidgetItem("")).text()
            if rid:
                self.store.delete_receipt(rid)
            else:
                self.fs.delete_transaction(self._txn_ids[r])
        self._refresh()

    def _delete_catalog_item(self):
        selected = [
            node for node in self.cat_tree.selectedItems()
            if node.parent() is None  # top-level items only
        ]
        if not selected:
            return
        if QMessageBox.question(
            self, "Remove",
            f"Remove {len(selected)} item(s) from the catalogue?\n"
            "Past receipts won't be affected, but the price history is dropped.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        ) != QMessageBox.StandardButton.Yes:
            return
        for node in selected:
            item_id = node.data(0, Qt.ItemDataRole.UserRole)
            if item_id:
                self.store.delete_item(item_id)
        self._refresh_catalog()
