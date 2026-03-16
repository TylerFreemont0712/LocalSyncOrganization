"""Financial Tracker module UI — transaction list with summaries."""

from datetime import date

from PyQt6.QtCore import Qt, QDate
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QLabel, QPushButton, QDialog, QLineEdit, QComboBox,
    QDateEdit, QDoubleSpinBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QFrame, QMessageBox,
)

from src.data.finance_store import FinanceStore, DEFAULT_CATEGORIES


class TransactionDialog(QDialog):
    """Dialog to add/edit a transaction."""

    def __init__(self, parent=None, txn=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Transaction" if txn else "New Transaction")
        self.setMinimumWidth(350)
        self.txn = txn
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)

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
        if self.txn:
            self.desc_edit.setText(self.txn.description)
        layout.addWidget(self.desc_edit)

        btn_row = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("secondary")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(save_btn)
        btn_row.addWidget(cancel_btn)
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


class FinancePanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.store = FinanceStore()
        self._build_ui()
        self._refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)

        # Header
        header = QHBoxLayout()
        title = QLabel("Finance")
        title.setObjectName("sectionTitle")
        header.addWidget(title)
        header.addStretch()

        btn_add = QPushButton("+ Transaction")
        btn_add.clicked.connect(self._add_transaction)
        header.addWidget(btn_add)

        btn_delete = QPushButton("Delete")
        btn_delete.setObjectName("destructive")
        btn_delete.clicked.connect(self._delete_transaction)
        header.addWidget(btn_delete)

        layout.addLayout(header)

        # Filters
        filter_row = QHBoxLayout()
        filter_row.addWidget(QLabel("Filter:"))

        self.filter_type = QComboBox()
        self.filter_type.addItems(["All", "income", "expense"])
        self.filter_type.currentTextChanged.connect(self._refresh)
        filter_row.addWidget(self.filter_type)

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
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.doubleClicked.connect(self._edit_transaction)
        content.addWidget(self.table)

        # Summary panel
        summary_widget = QWidget()
        summary_layout = QVBoxLayout(summary_widget)
        summary_layout.setContentsMargins(12, 8, 12, 8)

        summary_title = QLabel("Summary")
        summary_title.setObjectName("sectionTitle")
        summary_layout.addWidget(summary_title)

        self.income_label = QLabel("Income: $0.00")
        self.income_label.setStyleSheet("color: #a6e3a1; font-size: 16px; font-weight: bold;")
        summary_layout.addWidget(self.income_label)

        self.expense_label = QLabel("Expenses: $0.00")
        self.expense_label.setStyleSheet("color: #f38ba8; font-size: 16px; font-weight: bold;")
        summary_layout.addWidget(self.expense_label)

        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine)
        summary_layout.addWidget(sep)

        self.net_label = QLabel("Net: $0.00")
        self.net_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        summary_layout.addWidget(self.net_label)

        sep2 = QFrame()
        sep2.setObjectName("separator")
        sep2.setFrameShape(QFrame.Shape.HLine)
        summary_layout.addWidget(sep2)

        cat_title = QLabel("By Category")
        cat_title.setObjectName("subtitle")
        summary_layout.addWidget(cat_title)

        self.cat_list_label = QLabel("")
        self.cat_list_label.setWordWrap(True)
        summary_layout.addWidget(self.cat_list_label)

        summary_layout.addStretch()
        content.addWidget(summary_widget)
        content.setSizes([500, 250])

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

        # Update table
        self.table.setRowCount(len(txns))
        self._txn_ids = []
        for row, txn in enumerate(txns):
            self._txn_ids.append(txn.id)
            self.table.setItem(row, 0, QTableWidgetItem(txn.date))
            type_item = QTableWidgetItem(txn.type.capitalize())
            if txn.type == "income":
                type_item.setForeground(Qt.GlobalColor.green)
            else:
                type_item.setForeground(Qt.GlobalColor.red)
            self.table.setItem(row, 1, type_item)
            self.table.setItem(row, 2, QTableWidgetItem(txn.category))
            amt_str = f"${txn.amount:,.2f}"
            self.table.setItem(row, 3, QTableWidgetItem(amt_str))
            self.table.setItem(row, 4, QTableWidgetItem(txn.description))

        # Update summary
        summary = self.store.get_summary(start, end)
        self.income_label.setText(f"Income: ${summary['income']:,.2f}")
        self.expense_label.setText(f"Expenses: ${summary['expenses']:,.2f}")
        net = summary['net']
        color = "#a6e3a1" if net >= 0 else "#f38ba8"
        self.net_label.setText(f"Net: ${net:,.2f}")
        self.net_label.setStyleSheet(f"color: {color}; font-size: 18px; font-weight: bold;")

        cat_lines = []
        for cat, amount in sorted(summary['by_category'].items(), key=lambda x: -x[1]):
            cat_lines.append(f"  {cat}: ${amount:,.2f}")
        self.cat_list_label.setText("\n".join(cat_lines) if cat_lines else "No transactions")

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
