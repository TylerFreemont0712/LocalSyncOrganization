"""Earnings Tracker module UI.

Changes in this version:
  • Income categories simplified to "Main Job" / "Side Job"
  • Preset manager: category picker (Main Job / Side Job) per preset
  • log_preset respects preset.category for is_job_pay
  • Monthly Expenses dialog: recurring expense templates with one-click monthly logging
    — tagged [Monthly] for easy 確定申告 filtering
  • GoalEditDialog: JPY/USD currency toggle for goal entry
  • Dropdown QSS fix applied everywhere
"""

import threading
import urllib.request
import json
import csv
from datetime import date, timedelta
from pathlib import Path

from PyQt6.QtCore import Qt, QDate, pyqtSignal, QObject
from PyQt6.QtGui import QColor, QBrush, QPainter, QPen
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QFileDialog,
    QLabel, QPushButton, QDialog, QLineEdit, QComboBox,
    QDateEdit, QDoubleSpinBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QFrame, QMessageBox, QScrollArea,
    QFormLayout, QSizePolicy, QAbstractItemView, QInputDialog,
    QDialogButtonBox, QCheckBox, QGridLayout, QSpinBox, QButtonGroup, QRadioButton
)

from src.config import load_config, save_config
from src.data.finance_store import (
    FinanceStore, Transaction, JobPreset,
    INCOME_CATEGORIES, EXPENSE_CATEGORIES,
)

_FALLBACK_RATE = 150.0

_MONTH_NAMES = ["", "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"]

# ── Default monthly expense templates ─────────────────────────────────────────
# Stored in config key "monthly_expense_presets".  amount=0 means the user
# fills in the actual amount each month (bills vary slightly).
_DEFAULT_MONTHLY_PRESETS: list[dict] = [
    {"name": "Rent",               "amount": 0, "currency": "JPY", "category": "Rent / Housing"},
    {"name": "Kids Extracurriculars","amount": 0, "currency": "JPY", "category": "Education"},
    {"name": "Schooling",          "amount": 0, "currency": "JPY", "category": "Education"},
    {"name": "Power",              "amount": 0, "currency": "JPY", "category": "Utilities"},
    {"name": "Water",              "amount": 0, "currency": "JPY", "category": "Utilities"},
    {"name": "Internet",           "amount": 0, "currency": "JPY", "category": "Subscriptions"},
    {"name": "Phone",              "amount": 0, "currency": "JPY", "category": "Subscriptions"},
    {"name": "Gas",                "amount": 0, "currency": "JPY", "category": "Utilities"},
]

# ── Dropdown / DateEdit QSS ───────────────────────────────────────────────────
_COMBO_QSS = """
QComboBox {
    border: 1px solid palette(mid);
    border-radius: 4px;
    padding: 3px 6px;
    background-color: palette(base);
    color: palette(text);
    min-height: 24px;
}
QComboBox:focus { border-color: palette(highlight); }
QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 22px;
    border-left: 1px solid palette(mid);
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
}
QComboBox QAbstractItemView {
    background-color: palette(base);
    color: palette(text);
    selection-background-color: palette(highlight);
    selection-color: palette(highlighted-text);
    border: 1px solid palette(mid);
    outline: none;
}
QDateEdit {
    border: 1px solid palette(mid);
    border-radius: 4px;
    padding: 3px 6px;
    background-color: palette(base);
    color: palette(text);
    min-height: 24px;
}
QDateEdit::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 22px;
    border-left: 1px solid palette(mid);
}
"""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Exchange Rate Manager
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class RateSignals(QObject):
    updated = pyqtSignal(float)
    error   = pyqtSignal(str)


class ExchangeRateManager:
    _API_URL = "https://open.er-api.com/v6/latest/USD"

    def __init__(self):
        self.signals   = RateSignals()
        self._rate     = _FALLBACK_RATE
        self._fetching = False

    @property
    def rate(self) -> float:
        return self._rate

    def set_fallback(self, rate: float):
        self._rate = max(rate, 1.0)

    def refresh(self):
        if self._fetching: return
        self._fetching = True
        def _fetch():
            try:
                req = urllib.request.Request(
                    self._API_URL, headers={"User-Agent": "LocalSync/1.0"})
                with urllib.request.urlopen(req, timeout=8) as resp:
                    data = json.loads(resp.read().decode())
                rate = float(data["rates"]["JPY"])
                self._rate = rate
                self.signals.updated.emit(rate)
            except Exception as e:
                self.signals.error.emit(str(e))
            finally:
                self._fetching = False
        threading.Thread(target=_fetch, daemon=True).start()


_rate_mgr = ExchangeRateManager()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Goal Progress Bar
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class GoalProgressBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(36)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self._current = 0.0; self._base = 1000.0; self._extra = 2000.0
        self._green = "#a6e3a1"; self._gold = "#f9e2af"; self._accent = "#4a9eff"

    def set_values(self, current, base, extra,
                   green="#a6e3a1", gold="#f9e2af", accent="#4a9eff"):
        self._current = max(current, 0.0)
        self._base    = max(base, 1.0)
        self._extra   = max(extra, self._base + 1.0)
        self._green = green; self._gold = gold; self._accent = accent
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w = self.width(); bar_h = 18; bar_y = (self.height() - bar_h) // 2
        cap = self._extra * 1.05
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor("#313244")))
        painter.drawRoundedRect(0, bar_y, w, bar_h, bar_h // 2, bar_h // 2)
        fill_w = int(w * min(self._current / cap, 1.0))
        if fill_w > 0:
            fc = QColor(self._gold   if self._current >= self._extra else
                        self._green  if self._current >= self._base  else
                        self._accent)
            painter.setBrush(QBrush(fc))
            painter.drawRoundedRect(0, bar_y, fill_w, bar_h, bar_h // 2, bar_h // 2)
        bx = int(w * self._base  / cap)
        ex = int(w * self._extra / cap)
        painter.setPen(QPen(QColor("#cdd6f4"), 2))
        painter.drawLine(bx, bar_y - 3, bx, bar_y + bar_h + 3)
        painter.setPen(QPen(QColor(self._gold), 2))
        painter.drawLine(ex, bar_y - 3, ex, bar_y + bar_h + 3)
        painter.end()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  CategoryBar (summary panel)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class CategoryBar(QWidget):
    def __init__(self, label, amount_usd, max_amount, rate,
                 bar_color="#4a9eff", parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 2, 0, 2); layout.setSpacing(8)
        name_label = QLabel(label); name_label.setFixedWidth(130)
        layout.addWidget(name_label)
        bar = QFrame()
        pct = (amount_usd / max_amount * 100) if max_amount > 0 else 0
        bar.setStyleSheet(
            f"background-color:{bar_color};border-radius:3px;min-height:14px;")
        bar.setFixedWidth(max(int(pct * 1.5), 4))
        layout.addWidget(bar)
        jpy = int(amount_usd * rate)
        amt = QLabel(f"${amount_usd:,.0f}  \u00a5{jpy:,}")
        amt.setObjectName("subtitle")
        amt.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        amt.setFixedWidth(140)
        layout.addWidget(amt); layout.addStretch()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  PresetManagerDialog — with category selector
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class PresetManagerDialog(QDialog):
    def __init__(self, store: FinanceStore, parent=None):
        super().__init__(parent)
        self.store = store
        self.setWindowTitle("Manage Job Presets")
        self.setMinimumSize(480, 380)
        self.setStyleSheet(_COMBO_QSS)
        self._preset_ids: list[str] = []
        self._build_ui(); self._refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self); layout.setSpacing(10)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Name", "Amount (USD)", "Category"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        sep.setObjectName("separator"); layout.addWidget(sep)

        form = QFormLayout(); form.setSpacing(6)

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("e.g. Article Submission")
        form.addRow("Name:", self.name_edit)

        self.amount_spin = QDoubleSpinBox()
        self.amount_spin.setRange(0.01, 999_999.99)
        self.amount_spin.setDecimals(2); self.amount_spin.setPrefix("$ ")
        self.amount_spin.setValue(300.00)
        form.addRow("Amount (USD):", self.amount_spin)

        self.cat_combo = QComboBox()
        self.cat_combo.addItems(INCOME_CATEGORIES)  # Main Job / Side Job
        form.addRow("Category:", self.cat_combo)

        layout.addLayout(form)

        btn_row = QHBoxLayout()
        add_btn = QPushButton("Add Preset"); add_btn.clicked.connect(self._add_preset)
        btn_row.addWidget(add_btn)
        edit_btn = QPushButton("Edit Selected"); edit_btn.setObjectName("secondary")
        edit_btn.clicked.connect(self._edit_selected); btn_row.addWidget(edit_btn)
        del_btn = QPushButton("Delete Selected"); del_btn.setObjectName("destructive")
        del_btn.clicked.connect(self._delete_selected); btn_row.addWidget(del_btn)
        btn_row.addStretch()
        close_btn = QPushButton("Close"); close_btn.setObjectName("secondary")
        close_btn.clicked.connect(self.accept); btn_row.addWidget(close_btn)
        layout.addLayout(btn_row)

    def _refresh(self):
        presets = self.store.get_presets()
        self._preset_ids = [p.id for p in presets]
        self.table.setRowCount(len(presets))
        for i, p in enumerate(presets):
            self.table.setItem(i, 0, QTableWidgetItem(p.name))
            self.table.setItem(i, 1, QTableWidgetItem(f"${p.amount_usd:,.2f}"))
            self.table.setItem(i, 2, QTableWidgetItem(p.category))

    def _add_preset(self):
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Missing Name", "Please enter a preset name.")
            return
        self.store.add_preset(
            name=name,
            amount_usd=self.amount_spin.value(),
            category=self.cat_combo.currentText(),
        )
        self.name_edit.clear(); self._refresh()

    def _edit_selected(self):
        rows = self.table.selectionModel().selectedRows()
        if not rows: return
        idx = rows[0].row()
        if idx >= len(self._preset_ids): return
        presets = self.store.get_presets()
        preset = next((p for p in presets if p.id == self._preset_ids[idx]), None)
        if not preset: return
        self.name_edit.setText(preset.name)
        self.amount_spin.setValue(preset.amount_usd)
        self.cat_combo.setCurrentText(preset.category)
        self.store.delete_preset(preset.id); self._refresh()

    def _delete_selected(self):
        rows = self.table.selectionModel().selectedRows()
        if not rows: return
        if QMessageBox.question(
                self, "Delete Preset", "Delete selected preset(s)?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                ) == QMessageBox.StandardButton.Yes:
            for r in rows:
                if r.row() < len(self._preset_ids):
                    self.store.delete_preset(self._preset_ids[r.row()])
            self._refresh()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  MonthlyExpenseTemplatesDialog — manage the template list
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class MonthlyExpenseTemplatesDialog(QDialog):
    """Add / edit / delete recurring expense templates."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Manage Monthly Expense Templates")
        self.setMinimumSize(560, 420)
        self.setStyleSheet(_COMBO_QSS)
        self._build_ui(); self._refresh()

    @staticmethod
    def _load() -> list[dict]:
        presets = load_config().get("monthly_expense_presets", [])
        return presets if presets else list(_DEFAULT_MONTHLY_PRESETS)

    @staticmethod
    def _save(presets: list[dict]):
        cfg = load_config()
        cfg["monthly_expense_presets"] = presets
        save_config(cfg)

    @staticmethod
    def _load_expense_cats() -> list[str]:
        cats = load_config().get("expense_categories", [])
        return cats if cats else list(EXPENSE_CATEGORIES)

    def _build_ui(self):
        layout = QVBoxLayout(self); layout.setSpacing(10)

        info = QLabel(
            "These templates are used in the Monthly Expenses log dialog.\n"
            "Set your typical amounts here — you can adjust them per month when logging.")
        info.setObjectName("subtitle"); info.setWordWrap(True)
        layout.addWidget(info)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Name", "Default Amount", "Currency", "Category"])
        hh = self.table.horizontalHeader()
        hh.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        hh.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        sep.setObjectName("separator"); layout.addWidget(sep)

        form = QFormLayout(); form.setSpacing(6)

        self._name_edit = QLineEdit()
        self._name_edit.setPlaceholderText("e.g. Gym Membership")
        form.addRow("Name:", self._name_edit)

        amt_row = QHBoxLayout(); amt_row.setSpacing(6)
        self._amount_spin = QDoubleSpinBox()
        self._amount_spin.setRange(0, 9_999_999); self._amount_spin.setDecimals(0)
        self._amount_spin.setSingleStep(1000); self._amount_spin.setValue(0)
        amt_row.addWidget(self._amount_spin, 1)
        self._currency_combo = QComboBox()
        self._currency_combo.addItems(["JPY", "USD"])
        self._currency_combo.currentTextChanged.connect(self._on_currency_changed)
        amt_row.addWidget(self._currency_combo)
        form.addRow("Default Amount:", amt_row)

        self._cat_combo = QComboBox()
        self._cat_combo.addItems(self._load_expense_cats())
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

    def _on_currency_changed(self, cur: str):
        if cur == "JPY":
            self._amount_spin.setDecimals(0); self._amount_spin.setSingleStep(1000)
        else:
            self._amount_spin.setDecimals(2); self._amount_spin.setSingleStep(10)

    def _refresh(self):
        presets = self._load()
        self.table.setRowCount(len(presets))
        for i, p in enumerate(presets):
            self.table.setItem(i, 0, QTableWidgetItem(p["name"]))
            sym = "\u00a5" if p["currency"] == "JPY" else "$"
            amt = int(p["amount"]) if p["currency"] == "JPY" else p["amount"]
            self.table.setItem(i, 1, QTableWidgetItem(f"{sym}{amt:,}"))
            self.table.setItem(i, 2, QTableWidgetItem(p["currency"]))
            self.table.setItem(i, 3, QTableWidgetItem(p["category"]))

    def _add(self):
        name = self._name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Missing Name", "Please enter a template name.")
            return
        presets = self._load()
        presets.append({
            "name":     name,
            "amount":   self._amount_spin.value(),
            "currency": self._currency_combo.currentText(),
            "category": self._cat_combo.currentText(),
        })
        self._save(presets)
        self._name_edit.clear(); self._refresh()

    def _edit_selected(self):
        rows = self.table.selectionModel().selectedRows()
        if not rows: return
        idx = rows[0].row()
        presets = self._load()
        if idx >= len(presets): return
        p = presets[idx]
        self._name_edit.setText(p["name"])
        self._amount_spin.setValue(p["amount"])
        self._currency_combo.setCurrentText(p["currency"])
        self._cat_combo.setCurrentText(p["category"])
        presets.pop(idx); self._save(presets); self._refresh()

    def _delete_selected(self):
        rows = self.table.selectionModel().selectedRows()
        if not rows: return
        if QMessageBox.question(
                self, "Delete", "Delete selected template(s)?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                ) == QMessageBox.StandardButton.Yes:
            presets = self._load()
            for r in sorted(rows, key=lambda x: -x.row()):
                if r.row() < len(presets):
                    presets.pop(r.row())
            self._save(presets); self._refresh()

    def _reset_defaults(self):
        if QMessageBox.question(
                self, "Reset", "Reset templates to defaults? This will remove custom entries.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                ) == QMessageBox.StandardButton.Yes:
            self._save(list(_DEFAULT_MONTHLY_PRESETS)); self._refresh()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  MonthlyExpensesDialog — log a month's expenses in one go
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class MonthlyExpensesDialog(QDialog):
    """One-click monthly expense logger for recurring bills.

    Transactions are tagged [Monthly] <name> in the description field,
    making them easy to filter for 確定申告 year-end reporting.
    """

    def __init__(self, store: FinanceStore, palette: dict = None, parent=None):
        super().__init__(parent)
        self.store = store
        self._palette = palette or {}
        self.setWindowTitle("Monthly Expenses")
        self.setMinimumSize(600, 500)
        self.setStyleSheet(_COMBO_QSS)
        self._year  = date.today().year
        self._month = date.today().month
        self._rows: list[dict] = []   # {check, amount_spin, preset_dict}
        self._build_ui()
        self._reload()

    @staticmethod
    def _load_presets() -> list[dict]:
        presets = load_config().get("monthly_expense_presets", [])
        return presets if presets else list(_DEFAULT_MONTHLY_PRESETS)

    def _build_ui(self):
        layout = QVBoxLayout(self); layout.setSpacing(10)

        # ── Month navigation ──
        nav = QHBoxLayout()
        prev_btn = QPushButton("\u2190"); prev_btn.setObjectName("secondary")
        prev_btn.setFixedSize(28, 28)
        prev_btn.setStyleSheet("QPushButton{font-size:14px;font-weight:bold;}")
        prev_btn.clicked.connect(self._prev_month)
        nav.addWidget(prev_btn)
        self._month_lbl = QLabel()
        self._month_lbl.setStyleSheet("font-size:14px;font-weight:bold;")
        self._month_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nav.addWidget(self._month_lbl, 1)
        next_btn = QPushButton("\u2192"); next_btn.setObjectName("secondary")
        next_btn.setFixedSize(28, 28)
        next_btn.setStyleSheet("QPushButton{font-size:14px;font-weight:bold;}")
        next_btn.clicked.connect(self._next_month)
        nav.addWidget(next_btn)
        layout.addLayout(nav)

        # ── Duplicate warning ──
        self._warn_lbl = QLabel("")
        _warn_color = self._palette.get("yellow", "#f9e2af")
        self._warn_lbl.setStyleSheet(f"color:{_warn_color};font-size:11px;")
        self._warn_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._warn_lbl.setWordWrap(True)
        layout.addWidget(self._warn_lbl)

        # ── Expense rows (scrollable) ──
        scroll = QScrollArea(); scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._rows_widget = QWidget()
        self._rows_layout = QVBoxLayout(self._rows_widget)
        self._rows_layout.setContentsMargins(4, 4, 4, 4); self._rows_layout.setSpacing(6)
        scroll.setWidget(self._rows_widget)
        layout.addWidget(scroll, 1)

        sep = QFrame(); sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine); layout.addWidget(sep)

        # ── Column header labels ──
        hdr = QHBoxLayout(); hdr.setSpacing(0)
        hdr.addWidget(_hdr_lbl("", 24))
        hdr.addWidget(_hdr_lbl("Expense", 0), 1)
        hdr.addWidget(_hdr_lbl("Amount", 120))
        hdr.addWidget(_hdr_lbl("Currency", 60))
        hdr.addWidget(_hdr_lbl("Category", 140))
        layout.insertLayout(2, hdr)   # insert after nav and warn_lbl

        # ── Totals row ──
        totals_row = QHBoxLayout()
        totals_row.addStretch()
        self._total_lbl = QLabel("Total: \u00a50  /  $0.00")
        self._total_lbl.setStyleSheet("font-size:12px;font-weight:bold;")
        totals_row.addWidget(self._total_lbl)
        layout.addLayout(totals_row)

        # ── Action buttons ──
        btn_row = QHBoxLayout()
        manage_btn = QPushButton("\u2699 Manage Templates")
        manage_btn.setObjectName("secondary")
        manage_btn.clicked.connect(self._manage_templates)
        btn_row.addWidget(manage_btn)
        check_all_btn = QPushButton("Check All"); check_all_btn.setObjectName("secondary")
        check_all_btn.clicked.connect(lambda: self._set_all_checked(True))
        btn_row.addWidget(check_all_btn)
        uncheck_btn = QPushButton("Uncheck All"); uncheck_btn.setObjectName("secondary")
        uncheck_btn.clicked.connect(lambda: self._set_all_checked(False))
        btn_row.addWidget(uncheck_btn)
        btn_row.addStretch()
        cancel_btn = QPushButton("Cancel"); cancel_btn.setObjectName("secondary")
        cancel_btn.clicked.connect(self.reject); btn_row.addWidget(cancel_btn)
        self._log_btn = QPushButton("\u2714 Log Selected")
        self._log_btn.clicked.connect(self._log_selected)
        btn_row.addWidget(self._log_btn)
        layout.addLayout(btn_row)

    def _reload(self):
        """Rebuild the expense rows from the current template list."""
        # Clear existing rows
        while self._rows_layout.count():
            child = self._rows_layout.takeAt(0)
            if child.widget(): child.widget().deleteLater()
        self._rows = []

        presets = self._load_presets()
        for p in presets:
            row_widget = QWidget()
            row_l = QHBoxLayout(row_widget)
            row_l.setContentsMargins(0, 2, 0, 2); row_l.setSpacing(8)

            chk = QCheckBox(); chk.setChecked(True); chk.setFixedWidth(24)
            row_l.addWidget(chk)

            name_lbl = QLabel(p["name"]); name_lbl.setStyleSheet("font-size:12px;")
            row_l.addWidget(name_lbl, 1)

            amount_spin = QDoubleSpinBox()
            amount_spin.setFixedWidth(120)
            if p["currency"] == "JPY":
                amount_spin.setRange(0, 9_999_999); amount_spin.setDecimals(0)
                amount_spin.setSingleStep(1000); amount_spin.setPrefix("\u00a5 ")
            else:
                amount_spin.setRange(0, 99_999); amount_spin.setDecimals(2)
                amount_spin.setSingleStep(10); amount_spin.setPrefix("$ ")
            amount_spin.setValue(p["amount"])
            amount_spin.valueChanged.connect(self._update_total)
            chk.toggled.connect(self._update_total)
            row_l.addWidget(amount_spin)

            cur_lbl = QLabel(p["currency"]); cur_lbl.setFixedWidth(60)
            cur_lbl.setObjectName("subtitle"); cur_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            row_l.addWidget(cur_lbl)

            cat_lbl = QLabel(p["category"]); cat_lbl.setFixedWidth(140)
            cat_lbl.setObjectName("subtitle")
            cat_lbl.setStyleSheet("font-size:10px;")
            row_l.addWidget(cat_lbl)

            self._rows_layout.addWidget(row_widget)
            self._rows.append({
                "check":       chk,
                "amount_spin": amount_spin,
                "preset":      p,
            })

        self._rows_layout.addStretch()
        self._update_month_label()
        self._update_total()

    def _update_month_label(self):
        self._month_lbl.setText(f"{_MONTH_NAMES[self._month]} {self._year}")
        already = self.store.has_monthly_tag(self._year, self._month)
        if already:
            self._warn_lbl.setText(
                "\u26a0\ufe0f  Monthly expenses have already been logged for this month. "
                "Logging again will create duplicate entries.")
        else:
            self._warn_lbl.setText("")

    def _update_total(self):
        rate = _rate_mgr.rate
        total_jpy = 0.0
        for r in self._rows:
            if not r["check"].isChecked(): continue
            amt = r["amount_spin"].value()
            if r["preset"]["currency"] == "JPY":
                total_jpy += amt
            else:
                total_jpy += amt * rate
        total_usd = total_jpy / rate if rate > 0 else 0
        self._total_lbl.setText(
            f"Total: \u00a5{int(total_jpy):,}  /  ${total_usd:,.2f}")

    def _set_all_checked(self, state: bool):
        for r in self._rows:
            r["check"].setChecked(state)

    def _prev_month(self):
        if self._month == 1: self._month = 12; self._year -= 1
        else: self._month -= 1
        self._update_month_label()

    def _next_month(self):
        if self._month == 12: self._month = 1; self._year += 1
        else: self._month += 1
        self._update_month_label()

    def _manage_templates(self):
        dlg = MonthlyExpenseTemplatesDialog(self)
        dlg.exec()
        self._reload()

    def _log_selected(self):
        import calendar as _cal
        selected = [r for r in self._rows if r["check"].isChecked()]
        if not selected:
            QMessageBox.warning(self, "Nothing Selected",
                "Please check at least one expense to log."); return

        # Use the last day of the selected month as the transaction date
        last_day = _cal.monthrange(self._year, self._month)[1]
        log_date = date(self._year, self._month, last_day).isoformat()

        count = 0
        for r in selected:
            p = r["preset"]
            amt = r["amount_spin"].value()
            if amt <= 0: continue
            self.store.add_transaction(
                date=log_date,
                amount=amt,
                txn_type="expense",
                category=p["category"],
                description=f"[Monthly] {p['name']}",
                currency=p["currency"],
                is_job_pay=False,
            )
            count += 1

        QMessageBox.information(self, "Logged",
            f"Logged {count} expense(s) for "
            f"{_MONTH_NAMES[self._month]} {self._year}.\n\n"
            f"These are tagged [Monthly] and will appear in the transaction list. "
            f"Filter by description to export for 確定申告.")
        self.accept()


def _hdr_lbl(text: str, width: int) -> QLabel:
    lbl = QLabel(text)
    lbl.setStyleSheet("font-size:10px;font-weight:bold;color:palette(mid);")
    lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
    if width > 0: lbl.setFixedWidth(width)
    return lbl


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  GoalSettingsDialog — USD or JPY input
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class GoalSettingsDialog(QDialog):
    """Set monthly side-income goals.  Input can be in USD or JPY."""

    def __init__(self, base: float, extra: float, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Set Monthly Goals"); self.setMinimumWidth(360)
        self.setStyleSheet(_COMBO_QSS)
        self._rate = _rate_mgr.rate
        layout = QVBoxLayout(self); layout.setSpacing(10)

        info = QLabel(
            "Goals track Side Job income only.\n"
            "Main Job pay does not count toward goals.")
        info.setObjectName("subtitle"); info.setWordWrap(True); layout.addWidget(info)

        # Currency selector
        cur_row = QHBoxLayout()
        cur_row.addWidget(QLabel("Enter goals in:"))
        self._cur_combo = QComboBox()
        self._cur_combo.addItems(["USD ($)", "JPY (\u00a5)"])
        self._cur_combo.currentIndexChanged.connect(self._on_currency_changed)
        cur_row.addWidget(self._cur_combo); cur_row.addStretch()
        layout.addLayout(cur_row)

        form = QFormLayout(); form.setSpacing(8)

        self.min_spin = QDoubleSpinBox()
        self.min_spin.setRange(1, 99_999_999)
        self.min_spin.valueChanged.connect(self._update_hints)
        form.addRow("Minimum Goal:", self.min_spin)

        self._min_hint = QLabel()
        self._min_hint.setObjectName("subtitle")
        self._min_hint.setStyleSheet("font-size:10px;")
        form.addRow("", self._min_hint)

        self.major_spin = QDoubleSpinBox()
        self.major_spin.setRange(1, 99_999_999)
        self.major_spin.valueChanged.connect(self._update_hints)
        form.addRow("Extra Goal:", self.major_spin)

        self._major_hint = QLabel()
        self._major_hint.setObjectName("subtitle")
        self._major_hint.setStyleSheet("font-size:10px;")
        form.addRow("", self._major_hint)

        layout.addLayout(form)

        sep = QFrame(); sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine); layout.addWidget(sep)

        btn_row = QHBoxLayout(); btn_row.addStretch()
        cancel_btn = QPushButton("Cancel"); cancel_btn.setObjectName("secondary")
        cancel_btn.clicked.connect(self.reject); btn_row.addWidget(cancel_btn)
        save_btn = QPushButton("Save"); save_btn.clicked.connect(self._validate_and_accept)
        btn_row.addWidget(save_btn); layout.addLayout(btn_row)

        # Initialise spinboxes with USD values
        self._apply_usd_mode()
        self.min_spin.setValue(base)
        self.major_spin.setValue(extra)
        self._update_hints()

    def _apply_usd_mode(self):
        for sp in (self.min_spin, self.major_spin):
            sp.setDecimals(0); sp.setSingleStep(100); sp.setPrefix("$ ")

    def _apply_jpy_mode(self):
        for sp in (self.min_spin, self.major_spin):
            sp.setDecimals(0); sp.setSingleStep(10_000); sp.setPrefix("\u00a5 ")

    def _on_currency_changed(self, idx: int):
        rate = self._rate
        # Convert current values to the new currency
        base_usd  = self.min_spin.value()
        extra_usd = self.major_spin.value()
        if idx == 0:   # switching to USD
            self._apply_usd_mode()
            # If previous values look like JPY (large), convert; otherwise keep
            if base_usd > 5000:
                self.min_spin.setValue(round(base_usd / rate))
                self.major_spin.setValue(round(extra_usd / rate))
        else:           # switching to JPY
            self._apply_jpy_mode()
            if base_usd < 5000:
                self.min_spin.setValue(round(base_usd * rate))
                self.major_spin.setValue(round(extra_usd * rate))
        self._update_hints()

    def _update_hints(self):
        rate = self._rate
        if self._cur_combo.currentIndex() == 0:  # USD mode
            b_jpy = int(self.min_spin.value() * rate)
            e_jpy = int(self.major_spin.value() * rate)
            self._min_hint.setText(f"\u2248 \u00a5{b_jpy:,} JPY")
            self._major_hint.setText(f"\u2248 \u00a5{e_jpy:,} JPY")
        else:                                     # JPY mode
            b_usd = self.min_spin.value() / rate if rate else 0
            e_usd = self.major_spin.value() / rate if rate else 0
            self._min_hint.setText(f"\u2248 ${b_usd:,.2f} USD")
            self._major_hint.setText(f"\u2248 ${e_usd:,.2f} USD")

    def _validate_and_accept(self):
        if self.major_spin.value() <= self.min_spin.value():
            QMessageBox.warning(self, "Invalid Goals",
                "Major goal must be greater than minimum goal."); return
        self.accept()

    def get_goals(self) -> tuple[float, float]:
        """Always return (min_usd, major_usd)."""
        rate = self._rate if self._rate else _FALLBACK_RATE
        if self._cur_combo.currentIndex() == 1:   # JPY → convert to USD
            return self.min_spin.value() / rate, self.major_spin.value() / rate
        return self.min_spin.value(), self.major_spin.value()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  TransactionDialog
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TransactionDialog(QDialog):
    def __init__(self, parent=None, txn: Transaction | None = None,
                 initial_type: str = "income"):
        super().__init__(parent)
        self.setWindowTitle("Edit Entry" if txn else "New Entry")
        self.setMinimumWidth(420)
        self.txn = txn
        self.setStyleSheet(_COMBO_QSS)
        self._build_ui(initial_type)

    @staticmethod
    def _load_expense_cats() -> list[str]:
        cats = load_config().get("expense_categories", [])
        return cats if cats else list(EXPENSE_CATEGORIES)

    @staticmethod
    def _save_expense_cats(cats: list[str]):
        cfg = load_config(); cfg["expense_categories"] = cats; save_config(cfg)

    def _build_ui(self, initial_type: str):
        layout = QVBoxLayout(self); layout.setSpacing(10)
        form = QFormLayout(); form.setSpacing(8)

        self.type_combo = QComboBox()
        self.type_combo.addItems(["income", "expense"])
        self.type_combo.setCurrentText(self.txn.type if self.txn else initial_type)
        self.type_combo.currentTextChanged.connect(self._on_type_changed)
        form.addRow("Type:", self.type_combo)

        self.currency_combo = QComboBox()
        self.currency_combo.addItems(["USD", "JPY"])
        if self.txn: self.currency_combo.setCurrentText(self.txn.currency)
        self.currency_combo.currentTextChanged.connect(self._on_currency_changed)
        form.addRow("Currency:", self.currency_combo)

        self.amount_spin = QDoubleSpinBox()
        self.amount_spin.setRange(0.01, 99_999_999.99); self.amount_spin.setDecimals(2)
        if self.txn: self.amount_spin.setValue(self.txn.amount)
        form.addRow("Amount:", self.amount_spin)

        self.date_edit = QDateEdit(); self.date_edit.setCalendarPopup(True)
        if self.txn:
            y, mo, d = (int(x) for x in self.txn.date.split("-"))
            self.date_edit.setDate(QDate(y, mo, d))
        else:
            t = date.today()
            self.date_edit.setDate(QDate(t.year, t.month, t.day))
        form.addRow("Date:", self.date_edit)

        self.cat_label = QLabel("Category")
        cat_row = QHBoxLayout(); cat_row.setSpacing(4)
        self.cat_combo = QComboBox(); self.cat_combo.setEditable(False)
        cat_row.addWidget(self.cat_combo, 1)
        self._add_cat_btn = QPushButton("+")
        self._add_cat_btn.setFixedSize(26, 26)
        self._add_cat_btn.setToolTip("Add a new expense category")
        self._add_cat_btn.setObjectName("secondary")
        self._add_cat_btn.clicked.connect(self._add_expense_cat)
        cat_row.addWidget(self._add_cat_btn)
        cat_container = QWidget(); cat_container.setLayout(cat_row)
        form.addRow(self.cat_label, cat_container)

        self.desc_edit = QLineEdit()
        self.desc_edit.setPlaceholderText("Client, project, invoice #\u2026")
        if self.txn: self.desc_edit.setText(self.txn.description)
        form.addRow("Description:", self.desc_edit)

        self.rate_hint = QLabel(""); self.rate_hint.setObjectName("subtitle")
        form.addRow("", self.rate_hint)

        layout.addLayout(form)
        sep = QFrame(); sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine); layout.addWidget(sep)

        btn_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        btn_box.accepted.connect(self.accept); btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)

        self._on_type_changed(self.type_combo.currentText())
        self._on_currency_changed(self.currency_combo.currentText())

        if self.txn:
            idx = self.cat_combo.findText(self.txn.category)
            if idx >= 0: self.cat_combo.setCurrentIndex(idx)
            else:
                self.cat_combo.addItem(self.txn.category)
                self.cat_combo.setCurrentText(self.txn.category)

    def _on_type_changed(self, txn_type: str):
        self.cat_label.setText("Source" if txn_type == "income" else "Category")
        self.cat_combo.clear()
        if txn_type == "income":
            self.cat_combo.addItems(INCOME_CATEGORIES); self._add_cat_btn.setVisible(False)
        else:
            self.cat_combo.addItems(self._load_expense_cats()); self._add_cat_btn.setVisible(True)

    def _on_currency_changed(self, currency: str):
        rate = _rate_mgr.rate
        if currency == "JPY":
            self.amount_spin.setPrefix("\u00a5 "); self.amount_spin.setDecimals(0)
            self.amount_spin.setSingleStep(1000)
            self.rate_hint.setText(f"Rate: 1 USD = \u00a5{rate:,.0f}")
        else:
            self.amount_spin.setPrefix("$ "); self.amount_spin.setDecimals(2)
            self.amount_spin.setSingleStep(10)
            self.rate_hint.setText(f"Rate: \u00a5{rate:,.0f} = 1 USD")

    def _add_expense_cat(self):
        name, ok = QInputDialog.getText(self, "New Expense Category", "Category name:")
        if not ok or not name.strip(): return
        name = name.strip()
        cats = self._load_expense_cats()
        if name not in cats: cats.append(name); self._save_expense_cats(cats)
        self.cat_combo.clear(); self.cat_combo.addItems(cats)
        idx = self.cat_combo.findText(name)
        if idx >= 0: self.cat_combo.setCurrentIndex(idx)

    def get_data(self) -> dict:
        qd = self.date_edit.date()
        txn_type = self.type_combo.currentText()
        category = self.cat_combo.currentText()
        return {
            "date":        f"{qd.year():04d}-{qd.month():02d}-{qd.day():02d}",
            "amount":      self.amount_spin.value(),
            "txn_type":    txn_type,
            "category":    category,
            "description": self.desc_edit.text(),
            "currency":    self.currency_combo.currentText(),
            "is_job_pay":  (txn_type == "income" and category == "Main Job"),
        }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  PresetButton
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class PresetButton(QWidget):
    clicked = pyqtSignal(object)

    def __init__(self, preset: JobPreset, rate: float, parent=None):
        super().__init__(parent)
        self.preset = preset
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6); layout.setSpacing(2)
        name_lbl = QLabel(preset.name)
        name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_lbl.setStyleSheet("font-weight:bold;font-size:12px;")
        layout.addWidget(name_lbl)
        jpy = int(preset.amount_usd * rate)
        amt_lbl = QLabel(f"${preset.amount_usd:,.0f}  \u00a5{jpy:,}")
        amt_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        amt_lbl.setObjectName("subtitle"); layout.addWidget(amt_lbl)
        cat_lbl = QLabel(preset.category)
        cat_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cat_lbl.setStyleSheet("font-size:9px;")
        cat_lbl.setObjectName("subtitle"); layout.addWidget(cat_lbl)
        log_btn = QPushButton("+ Log"); log_btn.setFixedHeight(24)
        log_btn.clicked.connect(lambda: self.clicked.emit(self.preset))
        layout.addWidget(log_btn)
        self.setStyleSheet(
            "PresetButton{border:1px solid #45475a;border-radius:6px;"
            "background-color:#1e1e2e;}"
            "PresetButton:hover{background-color:#313244;}")
        self.setFixedWidth(150)

"""Task 8 Fix C — TaxExportDialog.

Paste this class into finance_panel.py BEFORE the FinancePanel class.
Then add the export button in FinancePanel._build_header() as shown below.
"""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  TaxExportDialog — 確定申告 CSV export
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TaxExportDialog(QDialog):
    """Export transaction data for 確定申告 (annual tax filing)."""

    def __init__(self, parent, finance_store):
        super().__init__(parent)
        self.store = finance_store
        self.setWindowTitle("Export for 確定申告")
        self.setMinimumWidth(400)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 14, 16, 14)

        layout.addWidget(QLabel("Export transaction data for tax filing."))

        # Year selector
        year_row = QHBoxLayout()
        year_row.addWidget(QLabel("Year:"))
        self._year_spin = QSpinBox()
        self._year_spin.setRange(2020, 2035)
        self._year_spin.setValue(date.today().year)
        year_row.addWidget(self._year_spin)
        year_row.addStretch()
        layout.addLayout(year_row)

        # Filter radio buttons
        self._filter_group = QButtonGroup(self)
        self._radio_all = QRadioButton("All transactions")
        self._radio_all.setChecked(True)
        self._radio_monthly = QRadioButton("[Monthly] tagged only")
        self._filter_group.addButton(self._radio_all)
        self._filter_group.addButton(self._radio_monthly)
        layout.addWidget(self._radio_all)
        layout.addWidget(self._radio_monthly)

        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(sep)

        # Export button
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("secondary")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)
        export_btn = QPushButton("Export CSV")
        export_btn.clicked.connect(self._export)
        btn_row.addWidget(export_btn)
        layout.addLayout(btn_row)

    def _export(self):
        year = self._year_spin.value()
        start = f"{year}-01-01"
        end = f"{year}-12-31"

        txns = self.store.get_transactions(start, end)

        # Apply filter
        if self._radio_monthly.isChecked():
            txns = [t for t in txns if "[Monthly]" in t.description]

        if not txns:
            QMessageBox.information(self, "No Data",
                f"No matching transactions found for {year}.")
            return

        # File dialog
        default_name = f"確定申告_{year}.csv"
        path, _ = QFileDialog.getSaveFileName(
            self, "Save CSV", str(Path.home() / default_name),
            "CSV Files (*.csv);;All Files (*)",
        )
        if not path:
            return

        # Get rate for conversion
        from src.config import load_config
        cfg = load_config()
        rate = float(cfg.get("usd_jpy_fallback_rate", 150.0))

        try:
            with open(path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "Date", "Type", "Category", "Description",
                    "Amount (Original)", "Currency",
                    "Amount (USD)", "Amount (JPY)", "Is Job Pay",
                ])
                for t in txns:
                    if t.currency == "JPY":
                        amt_jpy = t.amount
                        amt_usd = t.amount / rate if rate else 0
                    else:
                        amt_usd = t.amount
                        amt_jpy = t.amount * rate
                    writer.writerow([
                        t.date, t.type, t.category, t.description,
                        t.amount, t.currency,
                        f"{amt_usd:.2f}", f"{amt_jpy:.0f}",
                        "Yes" if t.is_job_pay else "No",
                    ])

            QMessageBox.information(self, "Exported",
                f"Exported {len(txns)} transaction(s) to:\n{path}")
            self.accept()
        except OSError as e:
            QMessageBox.warning(self, "Error", f"Failed to write file:\n{e}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  FinancePanel
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class FinancePanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.store = FinanceStore()
        self._palette: dict = {}
        self._cfg = load_config()
        self._txn_ids: list[str] = []
        fallback = float(self._cfg.get("usd_jpy_fallback_rate", _FALLBACK_RATE))
        _rate_mgr.set_fallback(fallback)
        _rate_mgr.signals.updated.connect(self._on_rate_updated)
        _rate_mgr.signals.error.connect(self._on_rate_error)
        self._build_ui()
        self._refresh()
        _rate_mgr.refresh()

    def set_palette(self, palette: dict):
        self._palette = palette; self._refresh()

    def showEvent(self, event):
        super().showEvent(event)
        self._refresh()

    # ── UI Construction ───────────────────────────────────────────────────────

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12); layout.setSpacing(8)
        layout.addLayout(self._build_header())
        layout.addWidget(self._build_quick_log_bar())
        layout.addLayout(self._build_filter_row())
        layout.addWidget(self._build_goal_section())
        content = QSplitter(Qt.Orientation.Horizontal)
        content.addWidget(self._build_table())
        content.addWidget(self._build_summary_panel())
        content.setSizes([560, 300])
        layout.addWidget(content, 1)
        layout.addWidget(self._build_rate_bar())

    def _build_header(self) -> QHBoxLayout:
        header = QHBoxLayout()
        title_col = QVBoxLayout()
        title = QLabel("Earnings Tracker"); title.setObjectName("sectionTitle")
        title_col.addWidget(title)
        sub = QLabel("Freelance income & expenses"); sub.setObjectName("subtitle")
        title_col.addWidget(sub)
        header.addLayout(title_col); header.addStretch()

        badge_col = QVBoxLayout(); badge_col.setSpacing(0)
        self.all_time_usd_label = QLabel("$0")
        self.all_time_usd_label.setStyleSheet(
            "font-size:26px;font-weight:bold;padding:2px 12px 0 12px;")
        badge_col.addWidget(self.all_time_usd_label)
        self.all_time_jpy_label = QLabel("\u00a50")
        self.all_time_jpy_label.setStyleSheet("font-size:13px;padding:0 12px 2px 12px;")
        self.all_time_jpy_label.setObjectName("subtitle")
        badge_col.addWidget(self.all_time_jpy_label)
        header.addLayout(badge_col)
        caption = QLabel("earned\nall-time"); caption.setObjectName("subtitle")
        caption.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        header.addWidget(caption); header.addSpacing(16)

        btn_earn = QPushButton("+ Earning"); btn_earn.setToolTip("Log a new earning")
        btn_earn.clicked.connect(self._add_earning); header.addWidget(btn_earn)
        btn_exp = QPushButton("+ Expense"); btn_exp.setObjectName("secondary")
        btn_exp.setToolTip("Log a new expense")
        btn_exp.clicked.connect(self._add_expense); header.addWidget(btn_exp)
        btn_del = QPushButton("Delete"); btn_del.setObjectName("destructive")
        btn_del.setToolTip("Delete selected row(s)")
        btn_del.clicked.connect(self._delete_transaction); header.addWidget(btn_del)
        export_btn = QPushButton("Export for 確定申告 \U0001f4ca")
        export_btn.setObjectName("secondary")
        export_btn.setToolTip("Export transactions for tax filing")
        export_btn.clicked.connect(self._open_tax_export)
        header.addWidget(export_btn)
        return header

    def _build_quick_log_bar(self) -> QWidget:
        container = QWidget()
        outer = QVBoxLayout(container)
        outer.setContentsMargins(0, 4, 0, 4); outer.setSpacing(4)

        title_row = QHBoxLayout()
        lbl = QLabel("Quick Log \u2014 Job Pay")
        lbl.setStyleSheet("font-weight:bold;font-size:12px;")
        title_row.addWidget(lbl); title_row.addStretch()

        manage_btn = QPushButton("\u2699 Manage Presets")
        manage_btn.setObjectName("secondary"); manage_btn.setFixedHeight(22)
        manage_btn.clicked.connect(self._open_preset_manager)
        title_row.addWidget(manage_btn)

        self._monthly_expenses_btn = QPushButton("\U0001f4cb Monthly Expenses")
        monthly_btn = self._monthly_expenses_btn
        monthly_btn.setObjectName("secondary"); monthly_btn.setFixedHeight(22)
        monthly_btn.setToolTip("Log recurring monthly bills in one go")
        monthly_btn.clicked.connect(self._open_monthly_expenses)
        title_row.addWidget(monthly_btn)

        outer.addLayout(title_row)

        self._preset_scroll = QScrollArea()
        self._preset_scroll.setWidgetResizable(True); self._preset_scroll.setFixedHeight(110)
        self._preset_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self._preset_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._preset_row_widget = QWidget()
        self._preset_row_layout = QHBoxLayout(self._preset_row_widget)
        self._preset_row_layout.setContentsMargins(4, 4, 4, 4)
        self._preset_row_layout.setSpacing(8); self._preset_row_layout.addStretch()
        self._preset_scroll.setWidget(self._preset_row_widget)
        outer.addWidget(self._preset_scroll)

        sep = QFrame(); sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine); outer.addWidget(sep)
        return container

    def _build_filter_row(self) -> QHBoxLayout:
        row = QHBoxLayout(); row.setSpacing(6)
        for label, fn in [("This Month", self._filter_this_month),
                           ("Last Month",  self._filter_last_month),
                           ("This Year",   self._filter_this_year),
                           ("All Time",    self._filter_all_time)]:
            btn = QPushButton(label); btn.setObjectName("secondary")
            btn.setFixedHeight(26); btn.clicked.connect(fn); row.addWidget(btn)
        row.addSpacing(12); row.addWidget(QLabel("Show:"))
        self.filter_type = QComboBox()
        self.filter_type.addItems(["All", "income", "expense"])
        self.filter_type.setStyleSheet(_COMBO_QSS)
        self.filter_type.currentTextChanged.connect(self._refresh)
        row.addWidget(self.filter_type)
        row.addSpacing(8); row.addWidget(QLabel("From:"))
        self.filter_start = QDateEdit(); self.filter_start.setCalendarPopup(True)
        self.filter_start.setStyleSheet(_COMBO_QSS)
        today = date.today()
        self.filter_start.setDate(QDate(today.year, today.month, 1))
        self.filter_start.dateChanged.connect(self._refresh); row.addWidget(self.filter_start)
        row.addWidget(QLabel("To:"))
        self.filter_end = QDateEdit(); self.filter_end.setCalendarPopup(True)
        self.filter_end.setStyleSheet(_COMBO_QSS)
        self.filter_end.setDate(QDate(today.year, today.month, today.day))
        self.filter_end.dateChanged.connect(self._refresh); row.addWidget(self.filter_end)
        row.addStretch()
        return row

    def _build_goal_section(self) -> QWidget:
        container = QFrame(); container.setFrameShape(QFrame.Shape.NoFrame)
        container.setStyleSheet("background-color:#1e1e2e;border-radius:8px;padding:4px;")
        vbox = QVBoxLayout(container)
        vbox.setContentsMargins(12, 8, 12, 8); vbox.setSpacing(6)
        title_row = QHBoxLayout()
        goal_title = QLabel("Month\u2019s Goal \u2014 Side Income")
        goal_title.setStyleSheet("font-weight:bold;font-size:13px;")
        title_row.addWidget(goal_title); title_row.addStretch()
        self.goal_status_label = QLabel(""); self.goal_status_label.setObjectName("subtitle")
        title_row.addWidget(self.goal_status_label)
        set_btn = QPushButton("\u2699 Set Goals"); set_btn.setObjectName("secondary")
        set_btn.setFixedHeight(24); set_btn.clicked.connect(self._open_goal_settings)
        title_row.addWidget(set_btn); vbox.addLayout(title_row)
        self.goal_bar = GoalProgressBar(); vbox.addWidget(self.goal_bar)
        legend_row = QHBoxLayout()
        self.goal_base_label    = QLabel("Base: $0");    self.goal_base_label.setObjectName("subtitle")
        self.goal_extra_label   = QLabel("Extra: $0");   self.goal_extra_label.setObjectName("subtitle")
        self.goal_current_label = QLabel("Progress: $0"); self.goal_current_label.setObjectName("subtitle")
        legend_row.addWidget(self.goal_base_label)
        legend_row.addSpacing(16); legend_row.addWidget(self.goal_extra_label)
        legend_row.addStretch(); legend_row.addWidget(self.goal_current_label)
        vbox.addLayout(legend_row)
        return container

    def _open_tax_export(self):
        TaxExportDialog(self, self.store).exec()

    def _build_table(self) -> QWidget:
        self.table = QTableWidget(); self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["Date", "Type", "Category", "Amount", "\u00a5 Amount", "Description"])
        hh = self.table.horizontalHeader()
        hh.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        for col in (0, 1, 3, 4):
            hh.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.doubleClicked.connect(self._edit_transaction)
        return self.table

    def _build_summary_panel(self) -> QWidget:
        w = QWidget(); self.summary_layout = QVBoxLayout(w)
        self.summary_layout.setContentsMargins(16, 12, 16, 12); self.summary_layout.setSpacing(8)
        period_title = QLabel("Period Summary"); period_title.setObjectName("sectionTitle")
        self.summary_layout.addWidget(period_title)
        self.earned_usd_label = QLabel("Earned: $0")
        self.earned_usd_label.setStyleSheet("font-size:18px;font-weight:bold;")
        self.summary_layout.addWidget(self.earned_usd_label)
        self.earned_jpy_label = QLabel("\u00a50"); self.earned_jpy_label.setObjectName("subtitle")
        self.earned_jpy_label.setStyleSheet("font-size:13px;padding-left:2px;")
        self.summary_layout.addWidget(self.earned_jpy_label)
        self.spent_label = QLabel("Spent: $0")
        self.spent_label.setStyleSheet("font-size:15px;font-weight:bold;")
        self.summary_layout.addWidget(self.spent_label)
        sep = QFrame(); sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine); self.summary_layout.addWidget(sep)
        self.net_label = QLabel("Net: $0")
        self.net_label.setStyleSheet("font-size:20px;font-weight:bold;")
        self.summary_layout.addWidget(self.net_label)
        self.net_jpy_label = QLabel("\u00a50"); self.net_jpy_label.setObjectName("subtitle")
        self.summary_layout.addWidget(self.net_jpy_label)
        self.txn_count_label = QLabel("0 transactions"); self.txn_count_label.setObjectName("subtitle")
        self.summary_layout.addWidget(self.txn_count_label)
        sep2 = QFrame(); sep2.setObjectName("separator")
        sep2.setFrameShape(QFrame.Shape.HLine); self.summary_layout.addWidget(sep2)
        cat_title = QLabel("By Category"); cat_title.setStyleSheet("font-weight:bold;font-size:13px;")
        self.summary_layout.addWidget(cat_title)
        self.cat_bars_container = QWidget()
        self.cat_bars_layout = QVBoxLayout(self.cat_bars_container)
        self.cat_bars_layout.setContentsMargins(0, 0, 0, 0); self.cat_bars_layout.setSpacing(2)
        self.summary_layout.addWidget(self.cat_bars_container)
        self.summary_layout.addStretch()
        return w

    def _build_rate_bar(self) -> QWidget:
        bar = QFrame(); bar.setFrameShape(QFrame.Shape.NoFrame)
        row = QHBoxLayout(bar); row.setContentsMargins(0, 2, 0, 2); row.setSpacing(8)
        self.rate_label = QLabel(f"USD \u2192 JPY: \u00a5{_rate_mgr.rate:,.0f}  (fallback)")
        self.rate_label.setObjectName("subtitle"); row.addWidget(self.rate_label)
        refresh_btn = QPushButton("\u21bb Refresh Rate"); refresh_btn.setObjectName("secondary")
        refresh_btn.setFixedHeight(22); refresh_btn.clicked.connect(self._refresh_rate)
        row.addWidget(refresh_btn); row.addStretch()
        return bar

    # ── Date filters ─────────────────────────────────────────────────────────

    def _set_date_range(self, start: date, end: date):
        self.filter_start.blockSignals(True); self.filter_end.blockSignals(True)
        self.filter_start.setDate(QDate(start.year, start.month, start.day))
        self.filter_end.setDate(QDate(end.year, end.month, end.day))
        self.filter_start.blockSignals(False); self.filter_end.blockSignals(False)
        self._refresh()

    def _filter_this_month(self):
        today = date.today(); self._set_date_range(today.replace(day=1), today)

    def _filter_last_month(self):
        today = date.today(); fp = today.replace(day=1); lp = fp - timedelta(days=1)
        self._set_date_range(lp.replace(day=1), lp)

    def _filter_this_year(self):
        today = date.today(); self._set_date_range(today.replace(month=1, day=1), today)

    def _filter_all_time(self):
        self._set_date_range(date(2000, 1, 1), date.today())

    # ── Rate ─────────────────────────────────────────────────────────────────

    def _refresh_rate(self):
        self.rate_label.setText("Fetching rate\u2026"); _rate_mgr.refresh()

    def _on_rate_updated(self, rate: float):
        self._cfg["usd_jpy_fallback_rate"] = rate; save_config(self._cfg)
        self.rate_label.setText(f"USD \u2192 JPY: \u00a5{rate:,.2f}  (live)")
        self._refresh()

    def _on_rate_error(self, msg: str):
        self.rate_label.setText(
            f"USD \u2192 JPY: \u00a5{_rate_mgr.rate:,.0f}  (offline \u2013 {msg[:40]})")

    # ── Presets ───────────────────────────────────────────────────────────────

    def _rebuild_preset_buttons(self):
        while self._preset_row_layout.count() > 1:
            item = self._preset_row_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        presets = self.store.get_presets(); rate = _rate_mgr.rate
        for preset in presets:
            btn = PresetButton(preset, rate); btn.clicked.connect(self._log_preset)
            self._preset_row_layout.insertWidget(
                self._preset_row_layout.count() - 1, btn)
        if not presets:
            ph = QLabel("No presets yet \u2014 click \u2699 Manage Presets to add one.")
            ph.setObjectName("subtitle"); self._preset_row_layout.insertWidget(0, ph)

    def _update_month_gate(self):
        """Disable Quick Log and Monthly Expenses buttons when viewing a non-current month."""
        qs = self.filter_start.date()
        today = date.today()
        is_current = (qs.year() == today.year and qs.month() == today.month)

        # Gate preset buttons
        for i in range(self._preset_row_layout.count()):
            w = self._preset_row_layout.itemAt(i).widget()
            if w and isinstance(w, PresetButton):
                w.setEnabled(is_current)
                w.setToolTip("" if is_current else "Switch to the current month to log income")

        # Gate monthly expenses button
        self._monthly_expenses_btn.setEnabled(is_current)
        self._monthly_expenses_btn.setToolTip(
            "" if is_current else "Switch to the current month to log income"
        )

    def _log_preset(self, preset: JobPreset):
        self.store.log_preset(preset, count=1, on_date=date.today().isoformat())
        self._refresh()

    def _open_preset_manager(self):
        PresetManagerDialog(self.store, self).exec()
        self._rebuild_preset_buttons(); self._refresh()

    def _open_monthly_expenses(self):
        dlg = MonthlyExpensesDialog(self.store, self._palette, self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self._refresh()

    # ── Goals ─────────────────────────────────────────────────────────────────

    def _open_goal_settings(self):
        base  = float(self._cfg.get("monthly_base_goal",  500.0))
        extra = float(self._cfg.get("monthly_extra_goal", 1000.0))
        dlg = GoalSettingsDialog(base, extra, self)
        if dlg.exec():
            nb, ne = dlg.get_goals()
            self._cfg["monthly_base_goal"] = nb; self._cfg["monthly_extra_goal"] = ne
            save_config(self._cfg); self._refresh()

    def _update_goal_section(self):
        base  = float(self._cfg.get("monthly_base_goal",  500.0))
        extra = float(self._cfg.get("monthly_extra_goal", 1000.0))
        rate  = _rate_mgr.rate
        green  = self._palette.get("green",  "#a6e3a1")
        gold   = "#f9e2af"
        accent = self._palette.get("accent", "#4a9eff")
        today = date.today()
        current = self.store.get_goal_income(
            today.replace(day=1).isoformat(), today.isoformat(), rate)
        self.goal_bar.set_values(current, base, extra, green, gold, accent)
        jpy_b = int(base * rate); jpy_e = int(extra * rate); jpy_c = int(current * rate)
        self.goal_base_label.setText(f"\u25cf Base: ${base:,.0f}  \u00a5{jpy_b:,}")
        self.goal_extra_label.setText(f"\u2605 Extra: ${extra:,.0f}  \u00a5{jpy_e:,}")
        self.goal_current_label.setText(f"Progress: ${current:,.0f}  \u00a5{jpy_c:,}")
        if current >= extra:
            self.goal_status_label.setText("\u2605 Extra goal reached!")
            self.goal_status_label.setStyleSheet(f"color:{gold};font-weight:bold;")
        elif current >= base:
            self.goal_status_label.setText("\u2713 Base goal reached!")
            self.goal_status_label.setStyleSheet(f"color:{green};font-weight:bold;")
        else:
            pct = int(current / base * 100) if base > 0 else 0
            self.goal_status_label.setText(
                f"{pct}% \u2014 ${base - current:,.0f} to base goal")
            self.goal_status_label.setStyleSheet(f"color:{accent};")

    # ── Refresh ───────────────────────────────────────────────────────────────

    def _get_filters(self) -> tuple[str, str, str | None]:
        qs = self.filter_start.date(); qe = self.filter_end.date()
        start = f"{qs.year():04d}-{qs.month():02d}-{qs.day():02d}"
        end   = f"{qe.year():04d}-{qe.month():02d}-{qe.day():02d}"
        t = self.filter_type.currentText()
        return start, end, (None if t == "All" else t)

    def _refresh(self):
        self._cfg = load_config(); rate = _rate_mgr.rate
        start, end, txn_type = self._get_filters()
        txns = self.store.get_transactions(start, end, txn_type)
        green  = self._palette.get("green",  "#a6e3a1")
        red    = self._palette.get("red",    "#f38ba8")
        gold   = "#f9e2af"

        atUSD = self.store.get_all_time_earned_usd(rate)
        self.all_time_usd_label.setText(f"${atUSD:,.0f}")
        self.all_time_usd_label.setStyleSheet(
            f"color:{green};font-size:26px;font-weight:bold;padding:2px 12px 0 12px;")
        self.all_time_jpy_label.setText(f"\u00a5{int(atUSD * rate):,}")

        self.table.setRowCount(len(txns)); self._txn_ids = []
        for ri, txn in enumerate(txns):
            self._txn_ids.append(txn.id)
            self.table.setItem(ri, 0, QTableWidgetItem(txn.date))
            if txn.is_job_pay:
                type_text, clr = "Main Job", QColor(gold)
            elif txn.type == "income":
                type_text, clr = "Side Job", QColor(green)
            else:
                type_text, clr = "Expense",  QColor(red)
            ti = QTableWidgetItem(type_text); ti.setForeground(QBrush(clr))
            self.table.setItem(ri, 1, ti)
            self.table.setItem(ri, 2, QTableWidgetItem(txn.category))
            pfx = "+" if txn.type == "income" else "-"
            sym = "\u00a5" if txn.currency == "JPY" else "$"
            amt_str = (f"{pfx}{sym}{int(txn.amount):,}" if txn.currency == "JPY"
                       else f"{pfx}{sym}{txn.amount:,.2f}")
            ai = QTableWidgetItem(amt_str); ai.setForeground(QBrush(clr))
            ai.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(ri, 3, ai)
            jpy_v = int(txn.amount) if txn.currency == "JPY" else int(txn.amount * rate)
            ji = QTableWidgetItem(f"{pfx}\u00a5{jpy_v:,}"); ji.setForeground(QBrush(clr))
            ji.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(ri, 4, ji)
            self.table.setItem(ri, 5, QTableWidgetItem(txn.description))

        summary = self.store.get_summary(start, end)
        earned_usd = summary["earned"]; spent_usd = summary["spent"]; net_usd = summary["net"]
        self.earned_usd_label.setText(f"Earned: ${earned_usd:,.2f}")
        self.earned_usd_label.setStyleSheet(f"color:{green};font-size:18px;font-weight:bold;")
        self.earned_jpy_label.setText(f"\u00a5{int(earned_usd * rate):,}")
        self.spent_label.setText(f"Spent: ${spent_usd:,.2f}")
        self.spent_label.setStyleSheet(f"color:{red};font-size:15px;font-weight:bold;")
        nc = green if net_usd >= 0 else red; sign = "+" if net_usd >= 0 else ""
        self.net_label.setText(f"Net: {sign}${net_usd:,.2f}")
        self.net_label.setStyleSheet(f"color:{nc};font-size:20px;font-weight:bold;")
        nj = int(net_usd * rate); njs = "+" if nj >= 0 else ""
        self.net_jpy_label.setText(f"{njs}\u00a5{nj:,}")
        self.txn_count_label.setText(f"{summary['count']} transaction(s) in period")

        while self.cat_bars_layout.count():
            child = self.cat_bars_layout.takeAt(0)
            if child.widget(): child.widget().deleteLater()
        by_cat = summary["by_category"]
        if by_cat:
            mx = max(by_cat.values())
            bar_colors = [self._palette.get("accent","#4a9eff"), green,
                          "#cba6f7","#fab387","#f9e2af","#94e2d5",red,"#f5c2e7"]
            for i, (cat, amt) in enumerate(sorted(by_cat.items(), key=lambda x: -x[1])):
                self.cat_bars_layout.addWidget(
                    CategoryBar(cat, amt, mx, rate, bar_colors[i % len(bar_colors)]))
        else:
            nd = QLabel("No transactions in this period"); nd.setObjectName("subtitle")
            self.cat_bars_layout.addWidget(nd)

        self._update_goal_section()
        self._rebuild_preset_buttons()
        self._update_month_gate()

    # ── CRUD ─────────────────────────────────────────────────────────────────

    def _add_earning(self):
        dlg = TransactionDialog(self, initial_type="income")
        if dlg.exec(): self.store.add_transaction(**dlg.get_data()); self._refresh()

    def _add_expense(self):
        dlg = TransactionDialog(self, initial_type="expense")
        if dlg.exec(): self.store.add_transaction(**dlg.get_data()); self._refresh()

    def _edit_transaction(self, index):
        row = index.row()
        if row < 0 or row >= len(self._txn_ids): return
        txn = next((t for t in self.store.get_transactions()
                    if t.id == self._txn_ids[row]), None)
        if not txn: return
        dlg = TransactionDialog(self, txn)
        if dlg.exec():
            d = dlg.get_data()
            txn.date = d["date"]; txn.amount = d["amount"]; txn.type = d["txn_type"]
            txn.category = d["category"]; txn.description = d["description"]
            txn.currency = d["currency"]; txn.is_job_pay = d["is_job_pay"]
            self.store.update_transaction(txn); self._refresh()

    def _delete_transaction(self):
        rows = self.table.selectionModel().selectedRows()
        if not rows: return
        if QMessageBox.question(
                self, "Delete", f"Delete {len(rows)} entry/entries?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                ) == QMessageBox.StandardButton.Yes:
            for idx in rows:
                if idx.row() < len(self._txn_ids):
                    self.store.delete_transaction(self._txn_ids[idx.row()])
            self._refresh()