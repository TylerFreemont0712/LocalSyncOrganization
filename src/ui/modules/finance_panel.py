"""Financial Tracker module UI — transaction list with summaries and category bars."""

from datetime import date

from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor, QBrush
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QLabel, QPushButton, QDialog, QLineEdit, QComboBox,
    QDateEdit, QDoubleSpinBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QFrame, QMessageBox,
)

from src.data.finance_store import FinanceStore, Transaction, DEFAULT_CATEGORIES


class TransactionDialog(QDialog):
    """Dialog to add/edit a transaction."""

    def __init__(self, parent=None, txn=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Transaction" if txn else "New Transaction")
        self.setMinimumWidth(380)
        self.txn = txn
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        layout.addWidget(QLabel("Type"))
        self.type_combo = QComboBox()
        self.type_combo.addItems(["income", "expense"])
        if self.txn:
            self.type_combo.setCurrentText(self.txn.type)
        layout.addWidget(self.type_combo)

        layout.addWidget(QLabel("Amount"))
        self.amount_spin = QDoubleSpinBox()
        self.amount_spin.setRange(0.01, 9999999.99)
        self.amount_spin.setDecimals(2)
        self.amount_spin.setPrefix("$ ")
        if self.txn:
            self.amount_spin.setValue(self.txn.amount)
        layout.addWidget(self.amount_spin)

        layout.addWidget(QLabel("Date"))
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        if self.txn:
            parts = self.txn.date.split("-")
            self.date_edit.setDate(QDate(int(parts[0]), int(parts[1]), int(parts[2])))
        else:
            today = date.today()
            self.date_edit.setDate(QDate(today.year, today.month, today.day))
        layout.addWidget(self.date_edit)

        layout.addWidget(QLabel("Category"))
        self.cat_combo = QComboBox()
        self.cat_combo.addItems(DEFAULT_CATEGORIES)
        self.cat_combo.setEditable(True)
        if self.txn:
            self.cat_combo.setCurrentText(self.txn.category)
        layout.addWidget(self.cat_combo)

        layout.addWidget(QLabel("Description"))
        self.desc_edit = QLineEdit()
        self.desc_edit.setPlaceholderText("Optional description...")
        if self.txn:
            self.desc_edit.setText(self.txn.description)
        layout.addWidget(self.desc_edit)

        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(sep)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("secondary")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        btn_row.addWidget(save_btn)
        layout.addLayout(btn_row)

    def get_data(self) -> dict:
        qd = self.date_edit.date()
        return {
            "date": f"{qd.year():04d}-{qd.month():02d}-{qd.day():02d}",
            "amount": self.amount_spin.value(),
            "txn_type": self.type_combo.currentText(),
            "category": self.cat_combo.currentText(),
            "description": self.desc_edit.text(),
        }


class CategoryBar(QWidget):
    """A simple horizontal bar showing category proportion."""

    def __init__(self, label: str, amount: float, max_amount: float,
                 bar_color: str = "#4a9eff", parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 2, 0, 2)
        layout.setSpacing(8)

        name_label = QLabel(label)
        name_label.setFixedWidth(110)
        layout.addWidget(name_label)

        # Bar
        bar_frame = QFrame()
        width_pct = (amount / max_amount * 100) if max_amount > 0 else 0
        bar_frame.setStyleSheet(
            f"background-color: {bar_color}; border-radius: 3px; min-height: 16px;"
        )
        bar_frame.setFixedWidth(max(int(width_pct * 1.5), 4))
        layout.addWidget(bar_frame)

        amt_label = QLabel(f"${amount:,.2f}")
        amt_label.setObjectName("subtitle")
        amt_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        amt_label.setFixedWidth(90)
        layout.addWidget(amt_label)

        layout.addStretch()


class FinancePanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.store = FinanceStore()
        self._palette: dict = {}
        self._build_ui()
        self._refresh()

    def set_palette(self, palette: dict):
        self._palette = palette
        self._refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)

        # Header
        header = QHBoxLayout()
        title = QLabel("Finance")
        title.setObjectName("sectionTitle")
        header.addWidget(title)
        header.addStretch()

        btn_add = QPushButton("+ Transaction")
        btn_add.setToolTip("Add a new transaction")
        btn_add.clicked.connect(self._add_transaction)
        header.addWidget(btn_add)

        btn_delete = QPushButton("Delete")
        btn_delete.setObjectName("destructive")
        btn_delete.setToolTip("Delete selected transactions")
        btn_delete.clicked.connect(self._delete_transaction)
        header.addWidget(btn_delete)

        layout.addLayout(header)

        # Filters
        filter_row = QHBoxLayout()
        filter_row.setSpacing(8)
        filter_row.addWidget(QLabel("Show:"))

        self.filter_type = QComboBox()
        self.filter_type.addItems(["All", "income", "expense"])
        self.filter_type.currentTextChanged.connect(self._refresh)
        filter_row.addWidget(self.filter_type)

        filter_row.addSpacing(12)
        filter_row.addWidget(QLabel("From:"))
        self.filter_start = QDateEdit()
        self.filter_start.setCalendarPopup(True)
        today = date.today()
        self.filter_start.setDate(QDate(today.year, today.month, 1))
        self.filter_start.dateChanged.connect(self._refresh)
        filter_row.addWidget(self.filter_start)

        filter_row.addWidget(QLabel("To:"))
        self.filter_end = QDateEdit()
        self.filter_end.setCalendarPopup(True)
        self.filter_end.setDate(QDate(today.year, today.month, today.day))
        self.filter_end.dateChanged.connect(self._refresh)
        filter_row.addWidget(self.filter_end)

        filter_row.addStretch()
        layout.addLayout(filter_row)

        # Content: table + summary
        content = QSplitter(Qt.Orientation.Horizontal)

        # Transaction table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Date", "Type", "Category", "Amount", "Description"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.doubleClicked.connect(self._edit_transaction)
        content.addWidget(self.table)

        # Summary panel
        summary_widget = QWidget()
        self.summary_layout = QVBoxLayout(summary_widget)
        self.summary_layout.setContentsMargins(16, 12, 16, 12)
        self.summary_layout.setSpacing(8)

        summary_title = QLabel("Summary")
        summary_title.setObjectName("sectionTitle")
        self.summary_layout.addWidget(summary_title)

        self.income_label = QLabel("Income: $0.00")
        self.income_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.summary_layout.addWidget(self.income_label)

        self.expense_label = QLabel("Expenses: $0.00")
        self.expense_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.summary_layout.addWidget(self.expense_label)

        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine)
        self.summary_layout.addWidget(sep)

        self.net_label = QLabel("Net: $0.00")
        self.net_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.summary_layout.addWidget(self.net_label)

        sep2 = QFrame()
        sep2.setObjectName("separator")
        sep2.setFrameShape(QFrame.Shape.HLine)
        self.summary_layout.addWidget(sep2)

        cat_title = QLabel("By Category")
        cat_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.summary_layout.addWidget(cat_title)

        # Container for category bars (dynamically rebuilt)
        self.cat_bars_container = QWidget()
        self.cat_bars_layout = QVBoxLayout(self.cat_bars_container)
        self.cat_bars_layout.setContentsMargins(0, 0, 0, 0)
        self.cat_bars_layout.setSpacing(2)
        self.summary_layout.addWidget(self.cat_bars_container)

        self.summary_layout.addStretch()
        content.addWidget(summary_widget)
        content.setSizes([520, 280])

        layout.addWidget(content, 1)

    def _get_filters(self) -> tuple:
        qs = self.filter_start.date()
        qe = self.filter_end.date()
        start = f"{qs.year():04d}-{qs.month():02d}-{qs.day():02d}"
        end = f"{qe.year():04d}-{qe.month():02d}-{qe.day():02d}"
        txn_type = self.filter_type.currentText()
        if txn_type == "All":
            txn_type = None
        return start, end, txn_type

    def _refresh(self):
        start, end, txn_type = self._get_filters()
        txns = self.store.get_transactions(start, end, txn_type)

        green = self._palette.get("green", "#a6e3a1")
        red = self._palette.get("red", "#f38ba8")
        accent = self._palette.get("accent", "#4a9eff")

        # Update table
        self.table.setRowCount(len(txns))
        self._txn_ids = []
        for row, txn in enumerate(txns):
            self._txn_ids.append(txn.id)
            self.table.setItem(row, 0, QTableWidgetItem(txn.date))

            type_item = QTableWidgetItem(txn.type.capitalize())
            color = QColor(green if txn.type == "income" else red)
            type_item.setForeground(QBrush(color))
            self.table.setItem(row, 1, type_item)

            self.table.setItem(row, 2, QTableWidgetItem(txn.category))

            prefix = "+" if txn.type == "income" else "-"
            amt_item = QTableWidgetItem(f"{prefix}${txn.amount:,.2f}")
            amt_item.setForeground(QBrush(color))
            amt_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row, 3, amt_item)

            self.table.setItem(row, 4, QTableWidgetItem(txn.description))

        # Update summary
        summary = self.store.get_summary(start, end)
        self.income_label.setText(f"Income: ${summary['income']:,.2f}")
        self.income_label.setStyleSheet(f"color: {green}; font-size: 16px; font-weight: bold;")
        self.expense_label.setText(f"Expenses: ${summary['expenses']:,.2f}")
        self.expense_label.setStyleSheet(f"color: {red}; font-size: 16px; font-weight: bold;")

        net = summary['net']
        net_color = green if net >= 0 else red
        sign = "+" if net >= 0 else ""
        self.net_label.setText(f"Net: {sign}${net:,.2f}")
        self.net_label.setStyleSheet(f"color: {net_color}; font-size: 20px; font-weight: bold;")

        # Rebuild category bars
        while self.cat_bars_layout.count():
            child = self.cat_bars_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        by_cat = summary['by_category']
        if by_cat:
            max_amount = max(by_cat.values())
            # Cycle through some colors
            bar_colors = [accent, green, "#cba6f7", "#fab387", "#f9e2af", "#94e2d5", red, "#f5c2e7"]
            for i, (cat, amount) in enumerate(sorted(by_cat.items(), key=lambda x: -x[1])):
                bar = CategoryBar(cat, amount, max_amount, bar_colors[i % len(bar_colors)])
                self.cat_bars_layout.addWidget(bar)
        else:
            no_data = QLabel("No transactions in this period")
            no_data.setObjectName("subtitle")
            self.cat_bars_layout.addWidget(no_data)

    def _add_transaction(self):
        dlg = TransactionDialog(self)
        if dlg.exec():
            data = dlg.get_data()
            self.store.add_transaction(**data)
            self._refresh()

    def _edit_transaction(self, index):
        row = index.row()
        if row < 0 or row >= len(self._txn_ids):
            return
        txn_id = self._txn_ids[row]
        txns = self.store.get_transactions()
        txn = next((t for t in txns if t.id == txn_id), None)
        if not txn:
            return
        dlg = TransactionDialog(self, txn)
        if dlg.exec():
            data = dlg.get_data()
            txn.date = data["date"]
            txn.amount = data["amount"]
            txn.type = data["txn_type"]
            txn.category = data["category"]
            txn.description = data["description"]
            self.store.update_transaction(txn)
            self._refresh()

    def _delete_transaction(self):
        rows = self.table.selectionModel().selectedRows()
        if not rows:
            return
        reply = QMessageBox.question(
            self, "Delete Transaction",
            f"Delete {len(rows)} transaction(s)?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            for idx in rows:
                txn_id = self._txn_ids[idx.row()]
                self.store.delete_transaction(txn_id)
            self._refresh()
