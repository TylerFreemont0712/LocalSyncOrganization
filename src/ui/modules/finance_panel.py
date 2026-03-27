"""Earnings Tracker module UI — freelance income tracking with summaries.

Features:
- Quick-log preset jobs with one click (job pay, does not count toward goals)
- Manual earning / expense entry with USD or JPY currency selection
- Live USD→JPY exchange rate via open.er-api.com with offline fallback
- Dual-currency display throughout (USD + ¥JPY)
- Month's Goal section: Base Goal + Extra Goal progress bars
  (only additional income, not job pay, counts toward goals)
- Quick date-range buttons (This Month / Last Month / This Year / All Time)
- Period summary panel with category bars
"""

import threading
import urllib.request
import urllib.error
import json
from datetime import date, timedelta

from PyQt6.QtCore import Qt, QDate, QTimer, pyqtSignal, QObject
from PyQt6.QtGui import QColor, QBrush, QPainter, QPen, QFont
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QLabel, QPushButton, QDialog, QLineEdit, QComboBox,
    QDateEdit, QDoubleSpinBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QFrame, QMessageBox, QScrollArea, QSpinBox,
    QFormLayout, QSizePolicy, QAbstractItemView,
)

from src.config import load_config, save_config
from src.data.finance_store import FinanceStore, Transaction, JobPreset, DEFAULT_CATEGORIES

# ── Default fallback exchange rate ────────────────────────────────────────────
_FALLBACK_RATE = 150.0


# ── Exchange Rate Manager ─────────────────────────────────────────────────────

class RateSignals(QObject):
    updated = pyqtSignal(float)
    error = pyqtSignal(str)


class ExchangeRateManager:
    """Fetches USD→JPY rate in a background thread. Thread-safe."""

    _API_URL = "https://open.er-api.com/v6/latest/USD"

    def __init__(self):
        self.signals = RateSignals()
        self._rate: float = _FALLBACK_RATE
        self._fetching = False

    @property
    def rate(self) -> float:
        return self._rate

    def set_fallback(self, rate: float):
        self._rate = max(rate, 1.0)

    def refresh(self):
        if self._fetching:
            return
        self._fetching = True

        def _fetch():
            try:
                req = urllib.request.Request(
                    self._API_URL,
                    headers={"User-Agent": "LocalSync/1.0"},
                )
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


# Module-level singleton so the panel and dialogs share one rate
_rate_mgr = ExchangeRateManager()


# ── Goal Progress Bar ─────────────────────────────────────────────────────────

class GoalProgressBar(QWidget):
    """Paints a two-tier progress bar: base goal and extra goal."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(36)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self._current = 0.0
        self._base = 1000.0
        self._extra = 2000.0
        self._green = "#a6e3a1"
        self._gold = "#f9e2af"
        self._accent = "#4a9eff"

    def set_values(self, current: float, base: float, extra: float,
                   green: str = "#a6e3a1", gold: str = "#f9e2af",
                   accent: str = "#4a9eff"):
        self._current = max(current, 0.0)
        self._base = max(base, 1.0)
        self._extra = max(extra, self._base + 1.0)
        self._green = green
        self._gold = gold
        self._accent = accent
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        bar_h = 18
        bar_y = (self.height() - bar_h) // 2

        cap = self._extra * 1.05   # a little breathing room past extra goal
        fill_ratio = min(self._current / cap, 1.0)
        base_ratio = self._base / cap
        extra_ratio = self._extra / cap

        # Background track
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor("#313244")))
        painter.drawRoundedRect(0, bar_y, w, bar_h, bar_h // 2, bar_h // 2)

        # Filled portion — colour shifts from accent → green (base) → gold (extra)
        fill_w = int(w * fill_ratio)
        if fill_w > 0:
            if self._current >= self._extra:
                fill_color = QColor(self._gold)
            elif self._current >= self._base:
                fill_color = QColor(self._green)
            else:
                fill_color = QColor(self._accent)
            painter.setBrush(QBrush(fill_color))
            painter.drawRoundedRect(0, bar_y, fill_w, bar_h, bar_h // 2, bar_h // 2)

        # Base goal marker
        base_x = int(w * base_ratio)
        pen = QPen(QColor("#cdd6f4"), 2)
        painter.setPen(pen)
        painter.drawLine(base_x, bar_y - 3, base_x, bar_y + bar_h + 3)

        # Extra goal marker
        extra_x = int(w * extra_ratio)
        pen.setColor(QColor(self._gold))
        painter.setPen(pen)
        painter.drawLine(extra_x, bar_y - 3, extra_x, bar_y + bar_h + 3)

        painter.end()


# ── Category Bar ──────────────────────────────────────────────────────────────

class CategoryBar(QWidget):

    def __init__(self, label: str, amount_usd: float, max_amount: float,
                 rate: float, bar_color: str = "#4a9eff", parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 2, 0, 2)
        layout.setSpacing(8)

        name_label = QLabel(label)
        name_label.setFixedWidth(110)
        layout.addWidget(name_label)

        bar_frame = QFrame()
        width_pct = (amount_usd / max_amount * 100) if max_amount > 0 else 0
        bar_frame.setStyleSheet(
            f"background-color: {bar_color}; border-radius: 3px; min-height: 14px;"
        )
        bar_frame.setFixedWidth(max(int(width_pct * 1.5), 4))
        layout.addWidget(bar_frame)

        jpy = int(amount_usd * rate)
        amt_label = QLabel(f"${amount_usd:,.0f}  ¥{jpy:,}")
        amt_label.setObjectName("subtitle")
        amt_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        amt_label.setFixedWidth(140)
        layout.addWidget(amt_label)

        layout.addStretch()


# ── Preset Manager Dialog ─────────────────────────────────────────────────────

class PresetManagerDialog(QDialog):
    """Add / edit / delete job presets."""

    def __init__(self, store: FinanceStore, parent=None):
        super().__init__(parent)
        self.store = store
        self.setWindowTitle("Manage Job Presets")
        self.setMinimumSize(460, 360)
        self._build_ui()
        self._refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # List
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Name", "Amount (USD)", "Category"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)

        # Add row
        add_frame = QFrame()
        add_frame.setObjectName("separator")
        add_frame.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(add_frame)

        form = QFormLayout()
        form.setSpacing(6)
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("e.g. Submission")
        form.addRow("Name:", self.name_edit)

        self.amount_spin = QDoubleSpinBox()
        self.amount_spin.setRange(0.01, 999999.99)
        self.amount_spin.setDecimals(2)
        self.amount_spin.setPrefix("$ ")
        self.amount_spin.setValue(300.00)
        form.addRow("Amount (USD):", self.amount_spin)

        self.cat_combo = QComboBox()
        self.cat_combo.addItems(DEFAULT_CATEGORIES)
        self.cat_combo.setCurrentText("Contract")
        self.cat_combo.setEditable(True)
        form.addRow("Category:", self.cat_combo)

        layout.addLayout(form)

        btn_row = QHBoxLayout()
        add_btn = QPushButton("Add Preset")
        add_btn.clicked.connect(self._add_preset)
        btn_row.addWidget(add_btn)

        edit_btn = QPushButton("Edit Selected")
        edit_btn.setObjectName("secondary")
        edit_btn.clicked.connect(self._edit_selected)
        btn_row.addWidget(edit_btn)

        del_btn = QPushButton("Delete Selected")
        del_btn.setObjectName("destructive")
        del_btn.clicked.connect(self._delete_selected)
        btn_row.addWidget(del_btn)

        btn_row.addStretch()
        close_btn = QPushButton("Close")
        close_btn.setObjectName("secondary")
        close_btn.clicked.connect(self.accept)
        btn_row.addWidget(close_btn)
        layout.addLayout(btn_row)

        self._preset_ids: list[str] = []

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
        self.name_edit.clear()
        self._refresh()

    def _edit_selected(self):
        rows = self.table.selectionModel().selectedRows()
        if not rows:
            return
        idx = rows[0].row()
        if idx >= len(self._preset_ids):
            return
        presets = self.store.get_presets()
        preset = next((p for p in presets if p.id == self._preset_ids[idx]), None)
        if not preset:
            return
        self.name_edit.setText(preset.name)
        self.amount_spin.setValue(preset.amount_usd)
        self.cat_combo.setCurrentText(preset.category)
        # Remove old and add updated
        self.store.delete_preset(preset.id)
        self._refresh()

    def _delete_selected(self):
        rows = self.table.selectionModel().selectedRows()
        if not rows:
            return
        reply = QMessageBox.question(
            self, "Delete Preset", "Delete selected preset(s)?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            for r in rows:
                if r.row() < len(self._preset_ids):
                    self.store.delete_preset(self._preset_ids[r.row()])
            self._refresh()


# ── Goal Settings Dialog ──────────────────────────────────────────────────────

class GoalSettingsDialog(QDialog):
    """Set base and extra monthly income goals (USD)."""

    def __init__(self, base: float, extra: float, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Set Monthly Goals")
        self.setMinimumWidth(320)
        self._build_ui(base, extra)

    def _build_ui(self, base: float, extra: float):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        info = QLabel(
            "Goals track additional income only.\n"
            "Job Pay (preset completions) does not count."
        )
        info.setObjectName("subtitle")
        info.setWordWrap(True)
        layout.addWidget(info)

        form = QFormLayout()
        form.setSpacing(8)

        self.base_spin = QDoubleSpinBox()
        self.base_spin.setRange(1.0, 9999999.0)
        self.base_spin.setDecimals(0)
        self.base_spin.setPrefix("$ ")
        self.base_spin.setSingleStep(100)
        self.base_spin.setValue(base)
        form.addRow("Base Goal (USD):", self.base_spin)

        self.extra_spin = QDoubleSpinBox()
        self.extra_spin.setRange(1.0, 9999999.0)
        self.extra_spin.setDecimals(0)
        self.extra_spin.setPrefix("$ ")
        self.extra_spin.setSingleStep(100)
        self.extra_spin.setValue(extra)
        form.addRow("Extra Goal (USD):", self.extra_spin)

        layout.addLayout(form)

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
        save_btn.clicked.connect(self._validate_and_accept)
        btn_row.addWidget(save_btn)
        layout.addLayout(btn_row)

    def _validate_and_accept(self):
        if self.extra_spin.value() <= self.base_spin.value():
            QMessageBox.warning(
                self, "Invalid Goals",
                "Extra goal must be greater than base goal.",
            )
            return
        self.accept()

    def get_goals(self) -> tuple[float, float]:
        return self.base_spin.value(), self.extra_spin.value()


# ── Transaction Dialog ────────────────────────────────────────────────────────

class TransactionDialog(QDialog):
    """Dialog to add/edit a transaction (earning or expense)."""

    def __init__(self, parent=None, txn: Transaction | None = None):
        super().__init__(parent)
        self.setWindowTitle("Edit Entry" if txn else "New Entry")
        self.setMinimumWidth(400)
        self.txn = txn
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        form = QFormLayout()
        form.setSpacing(8)

        # Type
        self.type_combo = QComboBox()
        self.type_combo.addItems(["income", "expense"])
        if self.txn:
            self.type_combo.setCurrentText(self.txn.type)
        self.type_combo.currentTextChanged.connect(self._on_type_changed)
        form.addRow("Type:", self.type_combo)

        # Currency
        self.currency_combo = QComboBox()
        self.currency_combo.addItems(["USD", "JPY"])
        if self.txn:
            self.currency_combo.setCurrentText(self.txn.currency)
        self.currency_combo.currentTextChanged.connect(self._on_currency_changed)
        form.addRow("Currency:", self.currency_combo)

        # Amount
        self.amount_spin = QDoubleSpinBox()
        self.amount_spin.setRange(0.01, 99999999.99)
        self.amount_spin.setDecimals(2)
        if self.txn:
            self.amount_spin.setValue(self.txn.amount)
        form.addRow("Amount:", self.amount_spin)

        # Date
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        if self.txn:
            parts = self.txn.date.split("-")
            self.date_edit.setDate(QDate(int(parts[0]), int(parts[1]), int(parts[2])))
        else:
            today = date.today()
            self.date_edit.setDate(QDate(today.year, today.month, today.day))
        form.addRow("Date:", self.date_edit)

        # Category
        self.cat_label = QLabel("Source")
        self.cat_combo = QComboBox()
        self.cat_combo.addItems(DEFAULT_CATEGORIES)
        self.cat_combo.setEditable(True)
        if self.txn:
            self.cat_combo.setCurrentText(self.txn.category)
        form.addRow(self.cat_label, self.cat_combo)

        # Description
        self.desc_edit = QLineEdit()
        self.desc_edit.setPlaceholderText("Client name, project, invoice #...")
        if self.txn:
            self.desc_edit.setText(self.txn.description)
        form.addRow("Description:", self.desc_edit)

        # Rate hint
        self.rate_hint = QLabel("")
        self.rate_hint.setObjectName("subtitle")
        form.addRow("", self.rate_hint)

        layout.addLayout(form)

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

        self._on_type_changed(self.type_combo.currentText())
        self._on_currency_changed(self.currency_combo.currentText())

    def _on_type_changed(self, txn_type: str):
        self.cat_label.setText("Source" if txn_type == "income" else "Category")

    def _on_currency_changed(self, currency: str):
        rate = _rate_mgr.rate
        if currency == "JPY":
            self.amount_spin.setPrefix("¥ ")
            self.amount_spin.setDecimals(0)
            self.amount_spin.setSingleStep(1000)
            self.rate_hint.setText(f"Rate: 1 USD = ¥{rate:,.0f}")
        else:
            self.amount_spin.setPrefix("$ ")
            self.amount_spin.setDecimals(2)
            self.amount_spin.setSingleStep(10)
            self.rate_hint.setText(f"Rate: ¥{rate:,.0f} = 1 USD")

    def get_data(self) -> dict:
        qd = self.date_edit.date()
        return {
            "date": f"{qd.year():04d}-{qd.month():02d}-{qd.day():02d}",
            "amount": self.amount_spin.value(),
            "txn_type": self.type_combo.currentText(),
            "category": self.cat_combo.currentText(),
            "description": self.desc_edit.text(),
            "currency": self.currency_combo.currentText(),
            "is_job_pay": False,
        }


# ── Quick Log Button ──────────────────────────────────────────────────────────

class PresetButton(QWidget):
    """A card-style button for one-click job logging."""

    clicked = pyqtSignal(object)  # emits JobPreset

    def __init__(self, preset: JobPreset, rate: float, parent=None):
        super().__init__(parent)
        self.preset = preset
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(2)

        name_lbl = QLabel(preset.name)
        name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_lbl.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(name_lbl)

        jpy = int(preset.amount_usd * rate)
        amt_lbl = QLabel(f"${preset.amount_usd:,.0f}  ¥{jpy:,}")
        amt_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        amt_lbl.setObjectName("subtitle")
        layout.addWidget(amt_lbl)

        log_btn = QPushButton("+ Log")
        log_btn.setFixedHeight(26)
        log_btn.clicked.connect(lambda: self.clicked.emit(self.preset))
        layout.addWidget(log_btn)

        self.setStyleSheet(
            "PresetButton { border: 1px solid #45475a; border-radius: 6px;"
            " background-color: #1e1e2e; }"
            "PresetButton:hover { background-color: #313244; }"
        )
        self.setFixedWidth(150)


# ── Main Finance Panel ────────────────────────────────────────────────────────

class FinancePanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.store = FinanceStore()
        self._palette: dict = {}
        self._cfg = load_config()
        self._txn_ids: list[str] = []

        # Load fallback rate from config
        fallback = float(self._cfg.get("usd_jpy_fallback_rate", _FALLBACK_RATE))
        _rate_mgr.set_fallback(fallback)
        _rate_mgr.signals.updated.connect(self._on_rate_updated)
        _rate_mgr.signals.error.connect(self._on_rate_error)

        self._build_ui()
        self._refresh()

        # Fetch rate on startup (non-blocking)
        _rate_mgr.refresh()

    def set_palette(self, palette: dict):
        self._palette = palette
        self._refresh()

    # ── UI Construction ───────────────────────────────────────────────────────

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)

        layout.addLayout(self._build_header())
        layout.addWidget(self._build_quick_log_bar())
        layout.addLayout(self._build_filter_row())
        layout.addWidget(self._build_goal_section())

        # Main content: table + summary
        content = QSplitter(Qt.Orientation.Horizontal)
        content.addWidget(self._build_table())
        content.addWidget(self._build_summary_panel())
        content.setSizes([560, 300])
        layout.addWidget(content, 1)

        layout.addWidget(self._build_rate_bar())

    def _build_header(self) -> QHBoxLayout:
        header = QHBoxLayout()

        title_col = QVBoxLayout()
        title = QLabel("Earnings Tracker")
        title.setObjectName("sectionTitle")
        title_col.addWidget(title)
        subtitle = QLabel("Freelance income & expenses")
        subtitle.setObjectName("subtitle")
        title_col.addWidget(subtitle)
        header.addLayout(title_col)

        header.addStretch()

        # All-time badge (stacked USD + JPY)
        badge_col = QVBoxLayout()
        badge_col.setSpacing(0)
        self.all_time_usd_label = QLabel("$0")
        self.all_time_usd_label.setStyleSheet(
            "font-size: 26px; font-weight: bold; padding: 2px 12px 0 12px;"
        )
        self.all_time_usd_label.setToolTip("Total earned all-time (USD)")
        badge_col.addWidget(self.all_time_usd_label)
        self.all_time_jpy_label = QLabel("¥0")
        self.all_time_jpy_label.setStyleSheet(
            "font-size: 13px; padding: 0 12px 2px 12px;"
        )
        self.all_time_jpy_label.setObjectName("subtitle")
        badge_col.addWidget(self.all_time_jpy_label)
        header.addLayout(badge_col)

        caption = QLabel("earned\nall-time")
        caption.setObjectName("subtitle")
        caption.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        header.addWidget(caption)

        header.addSpacing(16)

        btn_add_income = QPushButton("+ Earning")
        btn_add_income.setToolTip("Log a new earning")
        btn_add_income.clicked.connect(self._add_earning)
        header.addWidget(btn_add_income)

        btn_add_expense = QPushButton("+ Expense")
        btn_add_expense.setObjectName("secondary")
        btn_add_expense.setToolTip("Log a new expense")
        btn_add_expense.clicked.connect(self._add_expense)
        header.addWidget(btn_add_expense)

        btn_delete = QPushButton("Delete")
        btn_delete.setObjectName("destructive")
        btn_delete.setToolTip("Delete selected row(s)")
        btn_delete.clicked.connect(self._delete_transaction)
        header.addWidget(btn_delete)

        return header

    def _build_quick_log_bar(self) -> QWidget:
        container = QWidget()
        outer = QVBoxLayout(container)
        outer.setContentsMargins(0, 4, 0, 4)
        outer.setSpacing(4)

        title_row = QHBoxLayout()
        lbl = QLabel("Quick Log — Job Pay")
        lbl.setStyleSheet("font-weight: bold; font-size: 12px;")
        title_row.addWidget(lbl)
        title_row.addStretch()
        manage_btn = QPushButton("⚙ Manage Presets")
        manage_btn.setObjectName("secondary")
        manage_btn.setFixedHeight(22)
        manage_btn.clicked.connect(self._open_preset_manager)
        title_row.addWidget(manage_btn)
        outer.addLayout(title_row)

        # Scrollable row of preset buttons
        self._preset_scroll = QScrollArea()
        self._preset_scroll.setWidgetResizable(True)
        self._preset_scroll.setFixedHeight(100)
        self._preset_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self._preset_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self._preset_row_widget = QWidget()
        self._preset_row_layout = QHBoxLayout(self._preset_row_widget)
        self._preset_row_layout.setContentsMargins(4, 4, 4, 4)
        self._preset_row_layout.setSpacing(8)
        self._preset_row_layout.addStretch()

        self._preset_scroll.setWidget(self._preset_row_widget)
        outer.addWidget(self._preset_scroll)

        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine)
        outer.addWidget(sep)

        return container

    def _build_filter_row(self) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setSpacing(6)

        # Quick range buttons
        for label, fn in [
            ("This Month", self._filter_this_month),
            ("Last Month", self._filter_last_month),
            ("This Year", self._filter_this_year),
            ("All Time", self._filter_all_time),
        ]:
            btn = QPushButton(label)
            btn.setObjectName("secondary")
            btn.setFixedHeight(26)
            btn.clicked.connect(fn)
            row.addWidget(btn)

        row.addSpacing(12)
        row.addWidget(QLabel("Show:"))
        self.filter_type = QComboBox()
        self.filter_type.addItems(["All", "income", "expense"])
        self.filter_type.currentTextChanged.connect(self._refresh)
        row.addWidget(self.filter_type)

        row.addSpacing(8)
        row.addWidget(QLabel("From:"))
        self.filter_start = QDateEdit()
        self.filter_start.setCalendarPopup(True)
        today = date.today()
        self.filter_start.setDate(QDate(today.year, today.month, 1))
        self.filter_start.dateChanged.connect(self._refresh)
        row.addWidget(self.filter_start)

        row.addWidget(QLabel("To:"))
        self.filter_end = QDateEdit()
        self.filter_end.setCalendarPopup(True)
        self.filter_end.setDate(QDate(today.year, today.month, today.day))
        self.filter_end.dateChanged.connect(self._refresh)
        row.addWidget(self.filter_end)

        row.addStretch()
        return row

    def _build_goal_section(self) -> QWidget:
        container = QFrame()
        container.setObjectName("separator")
        container.setFrameShape(QFrame.Shape.NoFrame)
        container.setStyleSheet("background-color: #1e1e2e; border-radius: 8px; padding: 4px;")

        vbox = QVBoxLayout(container)
        vbox.setContentsMargins(12, 8, 12, 8)
        vbox.setSpacing(6)

        title_row = QHBoxLayout()
        goal_title = QLabel("Month's Goal  —  Additional Income")
        goal_title.setStyleSheet("font-weight: bold; font-size: 13px;")
        title_row.addWidget(goal_title)
        title_row.addStretch()

        self.goal_status_label = QLabel("")
        self.goal_status_label.setObjectName("subtitle")
        title_row.addWidget(self.goal_status_label)

        set_btn = QPushButton("⚙ Set Goals")
        set_btn.setObjectName("secondary")
        set_btn.setFixedHeight(24)
        set_btn.clicked.connect(self._open_goal_settings)
        title_row.addWidget(set_btn)
        vbox.addLayout(title_row)

        self.goal_bar = GoalProgressBar()
        vbox.addWidget(self.goal_bar)

        legend_row = QHBoxLayout()
        self.goal_base_label = QLabel("Base: $0")
        self.goal_base_label.setObjectName("subtitle")
        legend_row.addWidget(self.goal_base_label)
        legend_row.addSpacing(16)
        self.goal_extra_label = QLabel("Extra: $0")
        self.goal_extra_label.setObjectName("subtitle")
        legend_row.addWidget(self.goal_extra_label)
        legend_row.addStretch()
        self.goal_current_label = QLabel("Progress: $0")
        self.goal_current_label.setObjectName("subtitle")
        legend_row.addWidget(self.goal_current_label)
        vbox.addLayout(legend_row)

        return container

    def _build_table(self) -> QWidget:
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["Date", "Type", "Source", "Amount", "¥ Amount", "Description"]
        )
        hh = self.table.horizontalHeader()
        hh.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        hh.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.doubleClicked.connect(self._edit_transaction)
        return self.table

    def _build_summary_panel(self) -> QWidget:
        summary_widget = QWidget()
        self.summary_layout = QVBoxLayout(summary_widget)
        self.summary_layout.setContentsMargins(16, 12, 16, 12)
        self.summary_layout.setSpacing(8)

        period_title = QLabel("Period Summary")
        period_title.setObjectName("sectionTitle")
        self.summary_layout.addWidget(period_title)

        self.earned_usd_label = QLabel("Earned: $0")
        self.earned_usd_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.summary_layout.addWidget(self.earned_usd_label)

        self.earned_jpy_label = QLabel("¥0")
        self.earned_jpy_label.setObjectName("subtitle")
        self.earned_jpy_label.setStyleSheet("font-size: 13px; padding-left: 2px;")
        self.summary_layout.addWidget(self.earned_jpy_label)

        self.spent_label = QLabel("Spent: $0")
        self.spent_label.setStyleSheet("font-size: 15px; font-weight: bold;")
        self.summary_layout.addWidget(self.spent_label)

        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine)
        self.summary_layout.addWidget(sep)

        self.net_label = QLabel("Net: $0")
        self.net_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.summary_layout.addWidget(self.net_label)

        self.net_jpy_label = QLabel("¥0")
        self.net_jpy_label.setObjectName("subtitle")
        self.summary_layout.addWidget(self.net_jpy_label)

        self.txn_count_label = QLabel("0 transactions")
        self.txn_count_label.setObjectName("subtitle")
        self.summary_layout.addWidget(self.txn_count_label)

        sep2 = QFrame()
        sep2.setObjectName("separator")
        sep2.setFrameShape(QFrame.Shape.HLine)
        self.summary_layout.addWidget(sep2)

        cat_title = QLabel("By Source / Category")
        cat_title.setStyleSheet("font-weight: bold; font-size: 13px;")
        self.summary_layout.addWidget(cat_title)

        self.cat_bars_container = QWidget()
        self.cat_bars_layout = QVBoxLayout(self.cat_bars_container)
        self.cat_bars_layout.setContentsMargins(0, 0, 0, 0)
        self.cat_bars_layout.setSpacing(2)
        self.summary_layout.addWidget(self.cat_bars_container)

        self.summary_layout.addStretch()
        return summary_widget

    def _build_rate_bar(self) -> QWidget:
        bar = QFrame()
        bar.setFrameShape(QFrame.Shape.NoFrame)
        row = QHBoxLayout(bar)
        row.setContentsMargins(0, 2, 0, 2)
        row.setSpacing(8)

        self.rate_label = QLabel(f"USD → JPY: ¥{_rate_mgr.rate:,.0f}  (fallback)")
        self.rate_label.setObjectName("subtitle")
        row.addWidget(self.rate_label)

        refresh_btn = QPushButton("↻ Refresh Rate")
        refresh_btn.setObjectName("secondary")
        refresh_btn.setFixedHeight(22)
        refresh_btn.clicked.connect(self._refresh_rate)
        row.addWidget(refresh_btn)

        row.addStretch()
        return bar

    # ── Quick date range helpers ───────────────────────────────────────────────

    def _set_date_range(self, start: date, end: date):
        # Block signals while setting both to avoid double-refresh
        self.filter_start.blockSignals(True)
        self.filter_end.blockSignals(True)
        self.filter_start.setDate(QDate(start.year, start.month, start.day))
        self.filter_end.setDate(QDate(end.year, end.month, end.day))
        self.filter_start.blockSignals(False)
        self.filter_end.blockSignals(False)
        self._refresh()

    def _filter_this_month(self):
        today = date.today()
        self._set_date_range(today.replace(day=1), today)

    def _filter_last_month(self):
        today = date.today()
        first_this = today.replace(day=1)
        last_prev = first_this - timedelta(days=1)
        self._set_date_range(last_prev.replace(day=1), last_prev)

    def _filter_this_year(self):
        today = date.today()
        self._set_date_range(today.replace(month=1, day=1), today)

    def _filter_all_time(self):
        self._set_date_range(date(2000, 1, 1), date.today())

    # ── Rate helpers ──────────────────────────────────────────────────────────

    def _refresh_rate(self):
        self.rate_label.setText("Fetching rate…")
        _rate_mgr.refresh()

    def _on_rate_updated(self, rate: float):
        # Save as new fallback
        self._cfg["usd_jpy_fallback_rate"] = rate
        save_config(self._cfg)
        self.rate_label.setText(f"USD → JPY: ¥{rate:,.2f}  (live)")
        self._refresh()

    def _on_rate_error(self, msg: str):
        rate = _rate_mgr.rate
        self.rate_label.setText(f"USD → JPY: ¥{rate:,.0f}  (offline – {msg[:40]})")

    # ── Preset helpers ────────────────────────────────────────────────────────

    def _rebuild_preset_buttons(self):
        """Clear and repopulate the Quick Log button row."""
        # Remove all except the trailing stretch
        while self._preset_row_layout.count() > 1:
            item = self._preset_row_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        presets = self.store.get_presets()
        rate = _rate_mgr.rate
        for preset in presets:
            btn = PresetButton(preset, rate)
            btn.clicked.connect(self._log_preset)
            self._preset_row_layout.insertWidget(
                self._preset_row_layout.count() - 1, btn
            )

        if not presets:
            placeholder = QLabel("No presets yet — click ⚙ Manage Presets to add one.")
            placeholder.setObjectName("subtitle")
            self._preset_row_layout.insertWidget(0, placeholder)

    def _log_preset(self, preset: JobPreset):
        today_str = date.today().isoformat()
        self.store.log_preset(preset, count=1, on_date=today_str)
        self._refresh()

    def _open_preset_manager(self):
        dlg = PresetManagerDialog(self.store, self)
        dlg.exec()
        self._rebuild_preset_buttons()
        self._refresh()

    # ── Goal helpers ──────────────────────────────────────────────────────────

    def _open_goal_settings(self):
        base = float(self._cfg.get("monthly_base_goal", 500.0))
        extra = float(self._cfg.get("monthly_extra_goal", 1000.0))
        dlg = GoalSettingsDialog(base, extra, self)
        if dlg.exec():
            new_base, new_extra = dlg.get_goals()
            self._cfg["monthly_base_goal"] = new_base
            self._cfg["monthly_extra_goal"] = new_extra
            save_config(self._cfg)
            self._refresh()

    def _update_goal_section(self):
        base = float(self._cfg.get("monthly_base_goal", 500.0))
        extra = float(self._cfg.get("monthly_extra_goal", 1000.0))
        rate = _rate_mgr.rate
        green = self._palette.get("green", "#a6e3a1")
        gold = "#f9e2af"
        accent = self._palette.get("accent", "#4a9eff")

        today = date.today()
        month_start = today.replace(day=1).isoformat()
        month_end = today.isoformat()
        current = self.store.get_goal_income(month_start, month_end, rate)

        self.goal_bar.set_values(current, base, extra, green, gold, accent)

        jpy_base = int(base * rate)
        jpy_extra = int(extra * rate)
        self.goal_base_label.setText(f"● Base: ${base:,.0f}  ¥{jpy_base:,}")
        self.goal_extra_label.setText(f"★ Extra: ${extra:,.0f}  ¥{jpy_extra:,}")

        jpy_current = int(current * rate)
        self.goal_current_label.setText(
            f"Progress: ${current:,.0f}  ¥{jpy_current:,}"
        )

        if current >= extra:
            self.goal_status_label.setText("★ Extra goal reached!")
            self.goal_status_label.setStyleSheet(f"color: {gold}; font-weight: bold;")
        elif current >= base:
            self.goal_status_label.setText("✓ Base goal reached!")
            self.goal_status_label.setStyleSheet(f"color: {green}; font-weight: bold;")
        else:
            remaining = base - current
            pct = int(current / base * 100) if base > 0 else 0
            self.goal_status_label.setText(
                f"{pct}% — ${remaining:,.0f} to base goal"
            )
            self.goal_status_label.setStyleSheet(f"color: {accent};")

    # ── Main refresh ──────────────────────────────────────────────────────────

    def _get_filters(self) -> tuple[str, str, str | None]:
        qs = self.filter_start.date()
        qe = self.filter_end.date()
        start = f"{qs.year():04d}-{qs.month():02d}-{qs.day():02d}"
        end = f"{qe.year():04d}-{qe.month():02d}-{qe.day():02d}"
        txn_type = self.filter_type.currentText()
        if txn_type == "All":
            txn_type = None
        return start, end, txn_type

    def _refresh(self):
        self._cfg = load_config()
        rate = _rate_mgr.rate
        start, end, txn_type = self._get_filters()
        txns = self.store.get_transactions(start, end, txn_type)

        green = self._palette.get("green", "#a6e3a1")
        red = self._palette.get("red", "#f38ba8")
        accent = self._palette.get("accent", "#4a9eff")
        gold = "#f9e2af"

        # ── All-time badge ────────────────────────────────────────────────────
        all_time_usd = self.store.get_all_time_earned_usd(rate)
        all_time_jpy = int(all_time_usd * rate)
        self.all_time_usd_label.setText(f"${all_time_usd:,.0f}")
        self.all_time_usd_label.setStyleSheet(
            f"color: {green}; font-size: 26px; font-weight: bold;"
            " padding: 2px 12px 0 12px;"
        )
        self.all_time_jpy_label.setText(f"¥{all_time_jpy:,}")

        # ── Table ─────────────────────────────────────────────────────────────
        self.table.setRowCount(len(txns))
        self._txn_ids = []
        for row_idx, txn in enumerate(txns):
            self._txn_ids.append(txn.id)

            self.table.setItem(row_idx, 0, QTableWidgetItem(txn.date))

            type_text = "Earned" if txn.type == "income" else "Spent"
            if txn.is_job_pay:
                type_text = "Job Pay"
            type_item = QTableWidgetItem(type_text)
            color = QColor(green if txn.type == "income" else red)
            if txn.is_job_pay:
                color = QColor(gold)
            type_item.setForeground(QBrush(color))
            self.table.setItem(row_idx, 1, type_item)

            self.table.setItem(row_idx, 2, QTableWidgetItem(txn.category))

            # USD amount column
            prefix = "+" if txn.type == "income" else "-"
            curr_sym = "¥" if txn.currency == "JPY" else "$"
            if txn.currency == "JPY":
                amt_str = f"{prefix}{curr_sym}{int(txn.amount):,}"
            else:
                amt_str = f"{prefix}{curr_sym}{txn.amount:,.2f}"
            amt_item = QTableWidgetItem(amt_str)
            amt_item.setForeground(QBrush(color))
            amt_item.setTextAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )
            self.table.setItem(row_idx, 3, amt_item)

            # JPY column
            if txn.currency == "JPY":
                jpy_val = int(txn.amount)
            else:
                jpy_val = int(txn.amount * rate)
            jpy_item = QTableWidgetItem(f"{prefix}¥{jpy_val:,}")
            jpy_item.setForeground(QBrush(color))
            jpy_item.setTextAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )
            self.table.setItem(row_idx, 4, jpy_item)

            self.table.setItem(row_idx, 5, QTableWidgetItem(txn.description))

        # ── Summary panel ─────────────────────────────────────────────────────
        summary = self.store.get_summary(start, end)
        earned_usd = summary["earned"]
        spent_usd = summary["spent"]
        net_usd = summary["net"]

        earned_jpy = int(earned_usd * rate)
        spent_jpy = int(spent_usd * rate)
        net_jpy = int(net_usd * rate)

        self.earned_usd_label.setText(f"Earned: ${earned_usd:,.2f}")
        self.earned_usd_label.setStyleSheet(
            f"color: {green}; font-size: 18px; font-weight: bold;"
        )
        self.earned_jpy_label.setText(f"¥{earned_jpy:,}")

        self.spent_label.setText(f"Spent: ${spent_usd:,.2f}")
        self.spent_label.setStyleSheet(
            f"color: {red}; font-size: 15px; font-weight: bold;"
        )

        net_color = green if net_usd >= 0 else red
        sign = "+" if net_usd >= 0 else ""
        self.net_label.setText(f"Net: {sign}${net_usd:,.2f}")
        self.net_label.setStyleSheet(
            f"color: {net_color}; font-size: 20px; font-weight: bold;"
        )
        net_sign_jpy = "+" if net_jpy >= 0 else ""
        self.net_jpy_label.setText(f"{net_sign_jpy}¥{net_jpy:,}")

        self.txn_count_label.setText(f"{summary['count']} transaction(s) in period")

        # Category bars
        while self.cat_bars_layout.count():
            child = self.cat_bars_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        by_cat = summary["by_category"]
        if by_cat:
            max_amount = max(by_cat.values())
            bar_colors = [
                accent, green, "#cba6f7", "#fab387",
                "#f9e2af", "#94e2d5", red, "#f5c2e7",
            ]
            for i, (cat, amount) in enumerate(
                sorted(by_cat.items(), key=lambda x: -x[1])
            ):
                bar = CategoryBar(
                    cat, amount, max_amount, rate,
                    bar_colors[i % len(bar_colors)],
                )
                self.cat_bars_layout.addWidget(bar)
        else:
            no_data = QLabel("No transactions in this period")
            no_data.setObjectName("subtitle")
            self.cat_bars_layout.addWidget(no_data)

        # ── Goal section ──────────────────────────────────────────────────────
        self._update_goal_section()

        # ── Preset buttons ────────────────────────────────────────────────────
        self._rebuild_preset_buttons()

    # ── CRUD actions ──────────────────────────────────────────────────────────

    def _add_earning(self):
        dlg = TransactionDialog(self)
        dlg.type_combo.setCurrentText("income")
        if dlg.exec():
            self.store.add_transaction(**dlg.get_data())
            self._refresh()

    def _add_expense(self):
        dlg = TransactionDialog(self)
        dlg.type_combo.setCurrentText("expense")
        if dlg.exec():
            self.store.add_transaction(**dlg.get_data())
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
            txn.currency = data["currency"]
            self.store.update_transaction(txn)
            self._refresh()

    def _delete_transaction(self):
        rows = self.table.selectionModel().selectedRows()
        if not rows:
            return
        reply = QMessageBox.question(
            self, "Delete",
            f"Delete {len(rows)} entry/entries?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            for idx in rows:
                if idx.row() < len(self._txn_ids):
                    self.store.delete_transaction(self._txn_ids[idx.row()])
            self._refresh()