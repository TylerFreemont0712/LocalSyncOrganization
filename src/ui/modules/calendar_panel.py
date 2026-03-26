"""Calendar module UI — redesigned with interactive mini-month, rich event dialog,
birthday management, recurring events, and seamless week/day views.

Layout (unchanged positions):
  • Upper-left  → Weekly overview grid
  • Lower-left  → Selected-day detail list
  • Upper-right → Mini month navigator (interactive, dot indicators)
  • Lower-right → Next major events panel
"""

from __future__ import annotations

import calendar
from datetime import date, datetime, timedelta
from typing import Callable

from PyQt6.QtCore import (
    Qt, QDate, QTime, QTimer, pyqtSignal,
    QPropertyAnimation, QEasingCurve, QRect,
)
from PyQt6.QtGui import (
    QColor, QPainter, QPen, QBrush, QFont, QFontMetrics,
    QLinearGradient, QPainterPath, QMouseEvent,
)
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QDialog, QLineEdit, QTextEdit,
    QDateEdit, QTimeEdit, QCheckBox, QFrame, QComboBox,
    QMessageBox, QScrollArea, QSizePolicy, QTabWidget,
    QButtonGroup, QToolButton, QSpinBox, QApplication,
    QGraphicsOpacityEffect,
)

from src.data.calendar_store import (
    CalendarStore, Event, Birthday,
    build_recurrence, expand_recurring_to_range,
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Constants
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EVENT_COLORS: dict[str, str] = {
    "Sky Blue":    "#4a9eff",
    "Mint":        "#a6e3a1",
    "Rose":        "#f38ba8",
    "Peach":       "#fab387",
    "Gold":        "#f9e2af",
    "Lavender":    "#cba6f7",
    "Teal":        "#94e2d5",
    "Pink":        "#f5c2e7",
    "Coral":       "#ff6b6b",
    "Sage":        "#74c7b8",
}

CATEGORY_META: dict[str, dict] = {
    "":         {"label": "General",       "emoji": "📅", "color": "#4a9eff"},
    "work":     {"label": "Work",          "emoji": "💼", "color": "#4a9eff"},
    "birthday": {"label": "Birthday",      "emoji": "🎂", "color": "#f38ba8"},
    "trip":     {"label": "Trip",          "emoji": "✈️",  "color": "#94e2d5"},
    "holiday":  {"label": "Holiday",       "emoji": "🎉", "color": "#f9e2af"},
    "major":    {"label": "Major Event",   "emoji": "⭐", "color": "#cba6f7"},
    "health":   {"label": "Health",        "emoji": "🏥", "color": "#a6e3a1"},
    "social":   {"label": "Social",        "emoji": "🎭", "color": "#fab387"},
}

RECURRENCE_OPTIONS = [
    ("",        "Does not repeat"),
    ("daily",   "Every day"),
    ("weekly",  "Weekly (select days)"),
    ("monthly", "Monthly"),
    ("yearly",  "Yearly"),
]

WEEKDAY_LABELS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def _cat_emoji(category: str) -> str:
    return CATEGORY_META.get(category, CATEGORY_META[""]).get("emoji", "")


def _cat_color(category: str) -> str:
    return CATEGORY_META.get(category, CATEGORY_META[""]).get("color", "#4a9eff")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  EventDialog  — rich add/edit dialog
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ColorButton(QToolButton):
    """A small square color swatch toggle button."""

    def __init__(self, hex_color: str, name: str, parent=None):
        super().__init__(parent)
        self.hex_color = hex_color
        self.setFixedSize(28, 28)
        self.setCheckable(True)
        self.setToolTip(name)
        self._update_style()

    def setChecked(self, checked: bool):
        super().setChecked(checked)
        self._update_style()

    def _update_style(self):
        border = "3px solid white" if self.isChecked() else "2px solid transparent"
        self.setStyleSheet(
            f"QToolButton {{ background-color: {self.hex_color}; "
            f"border: {border}; border-radius: 6px; }}"
        )


class EventDialog(QDialog):
    """Modern add/edit event dialog with tabs for details and recurrence."""

    def __init__(self, parent=None, event: Event | None = None,
                 prefill_date: date | None = None):
        super().__init__(parent)
        self.event = event
        self._delete_requested = False
        self.setWindowTitle("Edit Event" if event else "New Event")
        self.setMinimumWidth(460)
        self.setModal(True)
        self._build_ui(prefill_date)

    # ── UI construction ─────────────────────────────

    def _build_ui(self, prefill_date: date | None):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Color strip header ───────────────────────
        self._header_strip = QFrame()
        self._header_strip.setFixedHeight(6)
        self._header_strip.setStyleSheet(
            f"background-color: {self.event.color if self.event else '#4a9eff'}; "
            "border-radius: 3px 3px 0 0;"
        )
        root.addWidget(self._header_strip)

        # ── Tab widget ───────────────────────────────
        body = QWidget()
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(20, 16, 20, 16)
        body_layout.setSpacing(12)
        root.addWidget(body)

        tabs = QTabWidget()
        tabs.setDocumentMode(True)
        body_layout.addWidget(tabs)

        # Tab 1: Details
        details_tab = QWidget()
        details_layout = QVBoxLayout(details_tab)
        details_layout.setContentsMargins(4, 12, 4, 4)
        details_layout.setSpacing(10)
        tabs.addTab(details_tab, "Details")

        # Title
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Event title…")
        self.title_edit.setStyleSheet("font-size: 15px; padding: 6px; font-weight: bold;")
        if self.event:
            self.title_edit.setText(self.event.title)
        details_layout.addWidget(self.title_edit)

        # Description
        self.desc_edit = QTextEdit()
        self.desc_edit.setMaximumHeight(72)
        self.desc_edit.setPlaceholderText("Optional description or notes…")
        if self.event:
            self.desc_edit.setPlainText(self.event.description)
        details_layout.addWidget(self.desc_edit)

        # Category row
        cat_row = QHBoxLayout()
        cat_row.addWidget(QLabel("Category"))
        self.category_combo = QComboBox()
        for key, meta in CATEGORY_META.items():
            self.category_combo.addItem(f"{meta['emoji']} {meta['label']}", key)
        if self.event:
            idx = self.category_combo.findData(self.event.category)
            if idx >= 0:
                self.category_combo.setCurrentIndex(idx)
        self.category_combo.currentIndexChanged.connect(self._on_category_changed)
        cat_row.addWidget(self.category_combo, 1)
        details_layout.addLayout(cat_row)

        # Color swatches
        color_label = QLabel("Color")
        details_layout.addWidget(color_label)
        color_row = QHBoxLayout()
        color_row.setSpacing(6)
        self._color_group = QButtonGroup(self)
        self._color_group.setExclusive(True)
        self._color_btns: dict[str, ColorButton] = {}
        current_color = self.event.color if self.event else "#4a9eff"
        for name, hex_val in EVENT_COLORS.items():
            btn = ColorButton(hex_val, name)
            btn.setChecked(hex_val == current_color)
            btn.clicked.connect(lambda _, h=hex_val: self._on_color_picked(h))
            self._color_group.addButton(btn)
            self._color_btns[hex_val] = btn
            color_row.addWidget(btn)
        color_row.addStretch()
        details_layout.addLayout(color_row)

        # Date / time
        self.all_day_check = QCheckBox("All-day event")
        if self.event:
            self.all_day_check.setChecked(self.event.all_day)
        self.all_day_check.toggled.connect(self._toggle_time)
        details_layout.addWidget(self.all_day_check)

        dt_row = QHBoxLayout()
        dt_row.setSpacing(8)

        dt_row.addWidget(QLabel("Date"))
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDisplayFormat("dd MMM yyyy")
        if self.event:
            dt = datetime.fromisoformat(self.event.start_time)
            self.date_edit.setDate(QDate(dt.year, dt.month, dt.day))
        elif prefill_date:
            self.date_edit.setDate(QDate(prefill_date.year, prefill_date.month, prefill_date.day))
        else:
            t = date.today()
            self.date_edit.setDate(QDate(t.year, t.month, t.day))
        dt_row.addWidget(self.date_edit, 2)

        dt_row.addWidget(QLabel("Start"))
        self.start_time = QTimeEdit()
        self.start_time.setDisplayFormat("HH:mm")
        if self.event and not self.event.all_day:
            dt = datetime.fromisoformat(self.event.start_time)
            self.start_time.setTime(QTime(dt.hour, dt.minute))
        else:
            self.start_time.setTime(QTime(9, 0))
        dt_row.addWidget(self.start_time, 1)

        dt_row.addWidget(QLabel("End"))
        self.end_time = QTimeEdit()
        self.end_time.setDisplayFormat("HH:mm")
        if self.event and self.event.end_time:
            dt = datetime.fromisoformat(self.event.end_time)
            self.end_time.setTime(QTime(dt.hour, dt.minute))
        else:
            self.end_time.setTime(QTime(10, 0))
        dt_row.addWidget(self.end_time, 1)

        details_layout.addLayout(dt_row)
        self._time_widgets = [self.start_time, self.end_time,
                               details_layout.itemAt(details_layout.count()-1)]
        self._toggle_time(self.all_day_check.isChecked())

        # Tab 2: Recurrence
        rec_tab = QWidget()
        rec_layout = QVBoxLayout(rec_tab)
        rec_layout.setContentsMargins(4, 12, 4, 4)
        rec_layout.setSpacing(10)
        tabs.addTab(rec_tab, "Repeat")

        rec_layout.addWidget(QLabel("Repeat pattern"))
        self.rec_combo = QComboBox()
        for val, label in RECURRENCE_OPTIONS:
            self.rec_combo.addItem(label, val)
        rec_layout.addWidget(self.rec_combo)
        self.rec_combo.currentIndexChanged.connect(self._on_rec_changed)

        # Weekly day pickers
        self._weekday_frame = QFrame()
        wdf_layout = QHBoxLayout(self._weekday_frame)
        wdf_layout.setContentsMargins(0, 4, 0, 0)
        wdf_layout.setSpacing(4)
        self._weekday_btns: list[QToolButton] = []
        for i, label in enumerate(WEEKDAY_LABELS):
            btn = QToolButton()
            btn.setText(label)
            btn.setCheckable(True)
            btn.setFixedSize(42, 30)
            btn.setStyleSheet(
                "QToolButton { border: 1px solid palette(mid); border-radius: 4px; font-size: 11px; }"
                "QToolButton:checked { background-color: #4a9eff; color: #1e1e2e; border-color: #4a9eff; }"
            )
            self._weekday_btns.append(btn)
            wdf_layout.addWidget(btn)
        wdf_layout.addStretch()
        rec_layout.addWidget(self._weekday_frame)
        self._weekday_frame.setVisible(False)

        rec_layout.addStretch()

        # Populate recurrence if editing
        if self.event and self.event.recurrence:
            rec_str = self.event.recurrence
            if rec_str == "daily":
                self.rec_combo.setCurrentIndex(1)
            elif rec_str.startswith("weekly:"):
                self.rec_combo.setCurrentIndex(2)
                days = [int(d) for d in rec_str.split(":")[1].split(",") if d.strip()]
                for d in days:
                    if 0 <= d < len(self._weekday_btns):
                        self._weekday_btns[d].setChecked(True)
            elif rec_str == "monthly":
                self.rec_combo.setCurrentIndex(3)
            elif rec_str == "yearly":
                self.rec_combo.setCurrentIndex(4)

        # ── Action buttons ───────────────────────────
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setObjectName("separator")
        body_layout.addWidget(sep)

        btn_row = QHBoxLayout()
        btn_row.setContentsMargins(0, 0, 0, 0)
        if self.event:
            del_btn = QPushButton("🗑  Delete")
            del_btn.setObjectName("destructive")
            del_btn.clicked.connect(self._on_delete)
            btn_row.addWidget(del_btn)
        btn_row.addStretch()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("secondary")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)
        save_btn = QPushButton("Save Event")
        save_btn.setDefault(True)
        save_btn.clicked.connect(self._on_save)
        btn_row.addWidget(save_btn)
        body_layout.addLayout(btn_row)

    # ── Slots ───────────────────────────────────────

    def _on_color_picked(self, hex_val: str):
        self._header_strip.setStyleSheet(
            f"background-color: {hex_val}; border-radius: 3px 3px 0 0;"
        )

    def _on_category_changed(self, _idx: int):
        cat = self.category_combo.currentData()
        auto_color = _cat_color(cat)
        btn = self._color_btns.get(auto_color)
        if btn:
            # uncheck all, check the matched one
            for b in self._color_btns.values():
                b.setChecked(False)
            btn.setChecked(True)
            self._on_color_picked(auto_color)

    def _on_rec_changed(self, _idx: int):
        val = self.rec_combo.currentData()
        self._weekday_frame.setVisible(val == "weekly")

    def _toggle_time(self, all_day: bool):
        self.start_time.setEnabled(not all_day)
        self.end_time.setEnabled(not all_day)

    def _on_delete(self):
        self._delete_requested = True
        self.reject()

    def _on_save(self):
        if not self.title_edit.text().strip():
            self.title_edit.setFocus()
            self.title_edit.setPlaceholderText("⚠ Title is required")
            return
        self.accept()

    # ── Data extraction ─────────────────────────────

    def _selected_color(self) -> str:
        for hex_val, btn in self._color_btns.items():
            if btn.isChecked():
                return hex_val
        return "#4a9eff"

    def _selected_recurrence(self) -> str:
        val = self.rec_combo.currentData()
        if val == "weekly":
            days = [i for i, btn in enumerate(self._weekday_btns) if btn.isChecked()]
            return build_recurrence("weekly", days) if days else ""
        return build_recurrence(val) if val else ""

    def get_data(self) -> dict:
        qd = self.date_edit.date()
        d = date(qd.year(), qd.month(), qd.day())
        all_day = self.all_day_check.isChecked()
        if all_day:
            start = datetime(d.year, d.month, d.day).isoformat()
            end = None
        else:
            st = self.start_time.time()
            et = self.end_time.time()
            start = datetime(d.year, d.month, d.day, st.hour(), st.minute()).isoformat()
            end   = datetime(d.year, d.month, d.day, et.hour(), et.minute()).isoformat()
        return {
            "title":       self.title_edit.text().strip() or "Untitled",
            "description": self.desc_edit.toPlainText(),
            "start_time":  start,
            "end_time":    end,
            "all_day":     all_day,
            "color":       self._selected_color(),
            "category":    self.category_combo.currentData() or "",
            "recurrence":  self._selected_recurrence(),
        }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  BirthdayDialog
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class BirthdayDialog(QDialog):
    """Simple add/edit dialog for a Birthday entry."""

    def __init__(self, parent=None, birthday: Birthday | None = None):
        super().__init__(parent)
        self.birthday = birthday
        self._delete_requested = False
        self.setWindowTitle("Edit Birthday" if birthday else "Add Birthday")
        self.setMinimumWidth(340)
        self.setModal(True)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 16)
        layout.setSpacing(12)

        # Header
        hdr = QLabel("🎂  Birthday")
        hdr.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(hdr)

        # Name
        layout.addWidget(QLabel("Name"))
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Person's name…")
        if self.birthday:
            self.name_edit.setText(self.birthday.name)
        layout.addWidget(self.name_edit)

        # Month / Day / Year
        mdy_row = QHBoxLayout()

        month_col = QVBoxLayout()
        month_col.addWidget(QLabel("Month"))
        self.month_spin = QSpinBox()
        self.month_spin.setRange(1, 12)
        self.month_spin.setDisplayIntegerBase(10)
        if self.birthday:
            self.month_spin.setValue(self.birthday.month)
        month_col.addWidget(self.month_spin)
        mdy_row.addLayout(month_col)

        day_col = QVBoxLayout()
        day_col.addWidget(QLabel("Day"))
        self.day_spin = QSpinBox()
        self.day_spin.setRange(1, 31)
        if self.birthday:
            self.day_spin.setValue(self.birthday.day)
        day_col.addWidget(self.day_spin)
        mdy_row.addLayout(day_col)

        year_col = QVBoxLayout()
        year_col.addWidget(QLabel("Year (optional)"))
        self.year_spin = QSpinBox()
        self.year_spin.setRange(0, 9999)
        self.year_spin.setSpecialValueText("—")
        self.year_spin.setValue(self.birthday.year if (self.birthday and self.birthday.year) else 0)
        year_col.addWidget(self.year_spin)
        mdy_row.addLayout(year_col)

        layout.addLayout(mdy_row)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setObjectName("separator")
        layout.addWidget(sep)

        btn_row = QHBoxLayout()
        if self.birthday:
            del_btn = QPushButton("Delete")
            del_btn.setObjectName("destructive")
            del_btn.clicked.connect(self._on_delete)
            btn_row.addWidget(del_btn)
        btn_row.addStretch()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("secondary")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)
        save_btn = QPushButton("Save")
        save_btn.setDefault(True)
        save_btn.clicked.connect(self._on_save)
        btn_row.addWidget(save_btn)
        layout.addLayout(btn_row)

    def _on_delete(self):
        self._delete_requested = True
        self.reject()

    def _on_save(self):
        if not self.name_edit.text().strip():
            self.name_edit.setFocus()
            return
        self.accept()

    def get_data(self) -> dict:
        year_val = self.year_spin.value()
        return {
            "name":  self.name_edit.text().strip(),
            "month": self.month_spin.value(),
            "day":   self.day_spin.value(),
            "year":  year_val if year_val > 0 else None,
        }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  MiniMonthCell  — painted single day cell
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class MiniMonthCell(QWidget):
    """Painted day cell for the mini calendar — shows dots for events."""

    clicked = pyqtSignal(int, int, int)   # year, month, day

    CELL_SIZE = 32

    def __init__(self, year: int, month: int, day: int,
                 is_today: bool, is_selected: bool,
                 event_colors: list[str],
                 is_holiday: bool = False,
                 parent=None):
        super().__init__(parent)
        self.year = year
        self.month = month
        self.day = day
        self.is_today = is_today
        self.is_selected = is_selected
        self.event_colors = event_colors[:4]   # max 4 dots
        self.is_holiday = is_holiday
        self._hovered = False

        self.setFixedSize(self.CELL_SIZE, self.CELL_SIZE)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)

        tip_parts = []
        if is_holiday:
            tip_parts.append("Holiday")
        if event_colors:
            tip_parts.append(f"{len(event_colors)} event(s)")
        if tip_parts:
            self.setToolTip(", ".join(tip_parts))

    def enterEvent(self, ev):
        self._hovered = True
        self.update()

    def leaveEvent(self, ev):
        self._hovered = False
        self.update()

    def mousePressEvent(self, ev: QMouseEvent):
        self.clicked.emit(self.year, self.month, self.day)

    def paintEvent(self, ev):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        cx, cy = w / 2, (h - 5) / 2   # centre, leaving 5px for dots

        # Circle background
        if self.is_today:
            p.setBrush(QBrush(QColor("#4a9eff")))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(int(cx - 13), int(cy - 13), 26, 26)
        elif self.is_selected:
            p.setBrush(QBrush(QColor("#4a9eff30")))
            p.setPen(QPen(QColor("#4a9eff"), 1.5))
            p.drawEllipse(int(cx - 13), int(cy - 13), 26, 26)
        elif self._hovered:
            p.setBrush(QBrush(QColor("#ffffff18")))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(int(cx - 13), int(cy - 13), 26, 26)

        # Day number
        font = QFont()
        font.setPixelSize(12)
        if self.is_today or self.is_selected:
            font.setBold(True)
        p.setFont(font)

        if self.is_today:
            p.setPen(QColor("#1e1e2e"))
        elif self.is_holiday:
            p.setPen(QColor("#f38ba8"))
        else:
            p.setPen(QColor("#cdd6f4"))

        p.drawText(0, 0, w, int(h - 7), Qt.AlignmentFlag.AlignCenter, str(self.day))

        # Event dots (bottom row)
        if self.event_colors:
            dot_r = 3
            total_dots = len(self.event_colors)
            spacing = dot_r * 2 + 2
            start_x = cx - (total_dots * spacing - 2) / 2
            dot_y = h - 5
            for i, color in enumerate(self.event_colors):
                p.setBrush(QBrush(QColor(color)))
                p.setPen(Qt.PenStyle.NoPen)
                p.drawEllipse(int(start_x + i * spacing - dot_r),
                              int(dot_y - dot_r), dot_r * 2, dot_r * 2)

        p.end()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  MiniMonth  — compact interactive month navigator
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class MiniMonth(QWidget):
    """Compact month grid — interactive navigation and event dot display."""

    date_selected = pyqtSignal(object)   # emits date

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(240)
        self._selected = date.today()
        self._view_year = self._selected.year
        self._view_month = self._selected.month
        self._events_by_date: dict[date, list[str]] = {}   # date → list[color]
        self._holiday_dates: set[date] = set()
        self._build()

    # ── Public API ──────────────────────────────────

    def set_events(self, by_date: dict[date, list[str]]):
        self._events_by_date = by_date
        self._render()

    def set_holidays(self, holiday_dates: set[date]):
        self._holiday_dates = holiday_dates
        self._render()

    def set_selected(self, d: date):
        self._selected = d
        self._view_year = d.year
        self._view_month = d.month
        self._render()

    def navigate_to(self, d: date):
        self._view_year = d.year
        self._view_month = d.month
        self._render()

    # ── Build structure ─────────────────────────────

    def _build(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(8, 8, 8, 8)
        outer.setSpacing(2)

        # Navigation row
        nav = QHBoxLayout()
        nav.setSpacing(0)

        self._prev_yr_btn = QPushButton("«")
        self._prev_yr_btn.setObjectName("secondary")
        self._prev_yr_btn.setFixedSize(24, 24)
        self._prev_yr_btn.setToolTip("Previous year")
        self._prev_yr_btn.clicked.connect(self._prev_year)
        nav.addWidget(self._prev_yr_btn)

        self._prev_btn = QPushButton("‹")
        self._prev_btn.setObjectName("secondary")
        self._prev_btn.setFixedSize(24, 24)
        self._prev_btn.clicked.connect(self._prev_month)
        nav.addWidget(self._prev_btn)

        self._title_btn = QPushButton()
        self._title_btn.setFlat(True)
        self._title_btn.setStyleSheet(
            "QPushButton { font-weight: bold; font-size: 13px; }"
            "QPushButton:hover { text-decoration: underline; }"
        )
        self._title_btn.clicked.connect(self._go_to_today_month)
        nav.addWidget(self._title_btn, 1)

        self._next_btn = QPushButton("›")
        self._next_btn.setObjectName("secondary")
        self._next_btn.setFixedSize(24, 24)
        self._next_btn.clicked.connect(self._next_month)
        nav.addWidget(self._next_btn)

        self._next_yr_btn = QPushButton("»")
        self._next_yr_btn.setObjectName("secondary")
        self._next_yr_btn.setFixedSize(24, 24)
        self._next_yr_btn.setToolTip("Next year")
        self._next_yr_btn.clicked.connect(self._next_year)
        nav.addWidget(self._next_yr_btn)

        outer.addLayout(nav)

        # Day-of-week header
        dow_row = QHBoxLayout()
        dow_row.setSpacing(0)
        dow_row.setContentsMargins(0, 4, 0, 0)
        for label in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
            lbl = QLabel(label)
            lbl.setFixedSize(MiniMonthCell.CELL_SIZE, 16)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("font-size: 10px; font-weight: bold; color: #6c7086;")
            dow_row.addWidget(lbl)
        outer.addLayout(dow_row)

        # Grid placeholder
        self._grid_widget = QWidget()
        self._grid = QGridLayout(self._grid_widget)
        self._grid.setSpacing(1)
        self._grid.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(self._grid_widget)
        outer.addStretch()

        self._render()

    # ── Rendering ───────────────────────────────────

    def _render(self):
        while self._grid.count():
            child = self._grid.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self._title_btn.setText(
            f"{calendar.month_abbr[self._view_month]} {self._view_year}"
        )

        today = date.today()
        cal = calendar.Calendar(firstweekday=0)   # Monday first
        weeks = cal.monthdayscalendar(self._view_year, self._view_month)

        for row, week in enumerate(weeks):
            for col, day in enumerate(week):
                if day == 0:
                    spacer = QLabel()
                    spacer.setFixedSize(MiniMonthCell.CELL_SIZE, MiniMonthCell.CELL_SIZE)
                    self._grid.addWidget(spacer, row, col)
                else:
                    d = date(self._view_year, self._view_month, day)
                    colors = self._events_by_date.get(d, [])
                    is_holiday = d in self._holiday_dates
                    cell = MiniMonthCell(
                        self._view_year, self._view_month, day,
                        is_today=(d == today),
                        is_selected=(d == self._selected),
                        event_colors=colors,
                        is_holiday=is_holiday,
                    )
                    cell.clicked.connect(self._on_cell_click)
                    self._grid.addWidget(cell, row, col)

    # ── Slots ───────────────────────────────────────

    def _on_cell_click(self, y: int, m: int, d: int):
        self._selected = date(y, m, d)
        self._render()
        self.date_selected.emit(self._selected)

    def _prev_month(self):
        if self._view_month == 1:
            self._view_month = 12
            self._view_year -= 1
        else:
            self._view_month -= 1
        self._render()

    def _next_month(self):
        if self._view_month == 12:
            self._view_month = 1
            self._view_year += 1
        else:
            self._view_month += 1
        self._render()

    def _prev_year(self):
        self._view_year -= 1
        self._render()

    def _next_year(self):
        self._view_year += 1
        self._render()

    def _go_to_today_month(self):
        today = date.today()
        self._view_year = today.year
        self._view_month = today.month
        self._render()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  EventChip  — compact event chip for week grid
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class EventChip(QWidget):
    """A compact, painted event chip for the weekly grid columns."""

    double_clicked = pyqtSignal(object)   # emits Event

    def __init__(self, event: Event, is_birthday: bool = False, parent=None):
        super().__init__(parent)
        self.event = event
        self.is_birthday = is_birthday
        self._hovered = False
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        self.setMinimumHeight(28)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # Build time label
        time_str = ""
        if not event.all_day:
            try:
                dt = datetime.fromisoformat(event.start_time)
                time_str = dt.strftime("%H:%M")
                if event.end_time:
                    et = datetime.fromisoformat(event.end_time)
                    time_str += f"–{et.strftime('%H:%M')}"
            except Exception:
                pass
        self._time_str = time_str

        emoji = _cat_emoji(event.category)
        self._display = f"{emoji} {event.title}" if emoji else event.title

        tip = self._display
        if time_str:
            tip += f"\n{time_str}"
        if event.description:
            tip += f"\n{event.description[:80]}"
        self.setToolTip(tip)

    def enterEvent(self, ev):
        self._hovered = True
        self.update()

    def leaveEvent(self, ev):
        self._hovered = False
        self.update()

    def mouseDoubleClickEvent(self, ev):
        self.double_clicked.emit(self.event)

    def paintEvent(self, ev):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        color = QColor(self.event.color)

        # Background fill
        bg = QColor(color)
        bg.setAlpha(40 if not self._hovered else 70)
        p.setBrush(QBrush(bg))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(0, 0, w, h, 4, 4)

        # Left accent bar
        p.setBrush(QBrush(color))
        p.drawRoundedRect(0, 0, 3, h, 2, 2)

        # Text
        p.setPen(color.lighter(140) if self._hovered else color.lighter(120))
        font = QFont()

        if self._time_str:
            # Two-line: time + title
            font.setPixelSize(9)
            p.setFont(font)
            p.drawText(8, 0, w - 10, h // 2 + 2, Qt.AlignmentFlag.AlignVCenter, self._time_str)
            font.setPixelSize(11)
            font.setBold(True)
            p.setFont(font)
            p.drawText(8, h // 2 - 2, w - 10, h // 2 + 2,
                       Qt.AlignmentFlag.AlignVCenter,
                       QFontMetrics(font).elidedText(
                           self._display, Qt.TextElideMode.ElideRight, w - 14))
        else:
            font.setPixelSize(11)
            font.setBold(True)
            p.setFont(font)
            p.drawText(8, 0, w - 10, h,
                       Qt.AlignmentFlag.AlignVCenter,
                       QFontMetrics(font).elidedText(
                           self._display, Qt.TextElideMode.ElideRight, w - 14))

        p.end()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  DayColumn  — a column in the weekly grid
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class DayColumn(QWidget):
    """A single day column in the weekly overview."""

    request_add   = pyqtSignal(object)    # date
    request_edit  = pyqtSignal(object)    # Event

    def __init__(self, d: date, events: list[Event],
                 birthdays: list[Birthday],
                 is_today: bool, is_selected: bool, parent=None):
        super().__init__(parent)
        self.d = d
        self._hovered = False
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        self._build(events, birthdays, is_today, is_selected)

    def _build(self, events, birthdays, is_today, is_selected):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(3, 4, 3, 4)
        layout.setSpacing(3)

        # ── Day header ───────────────────────────────
        day_name = self.d.strftime("%a").upper()
        day_num  = str(self.d.day)

        header = QWidget()
        header.setFixedHeight(46)
        hdr_layout = QVBoxLayout(header)
        hdr_layout.setContentsMargins(0, 2, 0, 2)
        hdr_layout.setSpacing(0)

        name_lbl = QLabel(day_name)
        name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_lbl.setStyleSheet("font-size: 10px; font-weight: bold; color: #6c7086;")

        num_lbl = QLabel(day_num)
        num_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if is_today:
            num_lbl.setStyleSheet(
                "background-color: #4a9eff; color: #1e1e2e; "
                "border-radius: 13px; font-size: 16px; font-weight: bold; "
                "padding: 0 4px;"
            )
            num_lbl.setFixedSize(26, 26)
            num_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        elif is_selected:
            num_lbl.setStyleSheet(
                "border: 1.5px solid #4a9eff; border-radius: 13px; "
                "font-size: 16px; font-weight: bold; padding: 0 4px;"
            )
            num_lbl.setFixedSize(26, 26)
        else:
            num_lbl.setStyleSheet("font-size: 16px;")

        hdr_layout.addWidget(name_lbl)
        hdr_layout.addWidget(num_lbl, 0, Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(header)

        # ── Thin separator ───────────────────────────
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("border: none; border-top: 1px solid #313244;")
        layout.addWidget(sep)

        # ── Event chips ──────────────────────────────
        sorted_events = sorted(events, key=lambda e: e.start_time)

        # All-day first
        for ev in sorted_events:
            if ev.all_day:
                chip = EventChip(ev)
                chip.double_clicked.connect(self.request_edit.emit)
                layout.addWidget(chip)

        # Birthdays (treated as all-day)
        for b in birthdays:
            today = date.today()
            try:
                age_candidate = date(today.year, b.month, b.day)
            except ValueError:
                age_candidate = None
            age_str = ""
            if b.year and age_candidate:
                age = age_candidate.year - b.year
                if self.d.month == b.month and self.d.day == b.day:
                    age_str = f" ({age})"
            fake_ev = Event(
                id=b.id, title=f"🎂 {b.name}{age_str}",
                start_time=datetime(self.d.year, self.d.month, self.d.day).isoformat(),
                all_day=True, color="#f38ba8", category="birthday",
            )
            chip = EventChip(fake_ev, is_birthday=True)
            chip.double_clicked.connect(lambda _ev: None)   # no-op for birthday
            layout.addWidget(chip)

        # Timed events
        for ev in sorted_events:
            if not ev.all_day:
                chip = EventChip(ev)
                chip.double_clicked.connect(self.request_edit.emit)
                layout.addWidget(chip)

        layout.addStretch()

    def enterEvent(self, ev):
        self._hovered = True
        self.update()

    def leaveEvent(self, ev):
        self._hovered = False
        self.update()

    def mouseDoubleClickEvent(self, ev):
        self.request_add.emit(self.d)

    def paintEvent(self, ev):
        p = QPainter(self)
        if self._hovered:
            p.fillRect(self.rect(), QColor("#ffffff08"))
        p.end()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  MajorEventCard  — lower-right panel card
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class MajorEventCard(QFrame):
    """A single major-event row for the lower-right panel."""

    def __init__(self, ev_date: date, title: str, category: str, color: str, parent=None):
        super().__init__(parent)
        self.setObjectName("majorCard")

        today = date.today()
        delta = (ev_date - today).days

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(10)

        # Colored left bar
        bar = QFrame()
        bar.setFixedWidth(3)
        bar.setStyleSheet(f"background-color: {color}; border-radius: 2px;")
        layout.addWidget(bar)

        # Emoji
        emoji_lbl = QLabel(_cat_emoji(category))
        emoji_lbl.setStyleSheet("font-size: 16px;")
        emoji_lbl.setFixedWidth(22)
        layout.addWidget(emoji_lbl)

        # Text column
        text_col = QVBoxLayout()
        text_col.setSpacing(1)

        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("font-size: 12px; font-weight: bold;")
        title_lbl.setWordWrap(True)
        text_col.addWidget(title_lbl)

        date_str = ev_date.strftime("%b %d, %Y")
        date_lbl = QLabel(date_str)
        date_lbl.setStyleSheet("font-size: 10px; color: #6c7086;")
        text_col.addWidget(date_lbl)

        layout.addLayout(text_col, 1)

        # Countdown badge
        if delta == 0:
            badge_text, badge_color = "Today", color
        elif delta == 1:
            badge_text, badge_color = "Tomorrow", color
        elif delta < 0:
            badge_text, badge_color = f"{abs(delta)}d ago", "#6c7086"
        elif delta <= 7:
            badge_text, badge_color = f"{delta}d", color
        elif delta <= 30:
            badge_text, badge_color = f"{delta}d", "#f9e2af"
        else:
            weeks = delta // 7
            badge_text, badge_color = f"{weeks}w", "#6c7086"

        badge = QLabel(badge_text)
        badge.setStyleSheet(
            f"color: {badge_color}; font-size: 10px; font-weight: bold; "
            f"border: 1px solid {badge_color}; border-radius: 8px; "
            "padding: 2px 7px;"
        )
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(badge)

        self.setStyleSheet(
            "MajorEventCard { border: 1px solid #313244; border-radius: 6px; "
            "background-color: #181825; }"
            "MajorEventCard:hover { border-color: #45475a; background-color: #1e1e2e; }"
        )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  DayEventRow  — row in the selected-day detail list
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class DayEventRow(QFrame):
    """A single event row for the lower-left selected day panel."""

    edit_requested = pyqtSignal(object)   # emits Event

    def __init__(self, event: Event, parent=None):
        super().__init__(parent)
        self.event = event
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setObjectName("dayEventRow")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Color bar
        bar = QFrame()
        bar.setFixedWidth(4)
        bar.setStyleSheet(f"background-color: {event.color}; border-radius: 2px 0 0 2px;")
        layout.addWidget(bar)

        # Body
        body = QWidget()
        body_l = QHBoxLayout(body)
        body_l.setContentsMargins(8, 6, 8, 6)
        body_l.setSpacing(8)

        # Time
        if not event.all_day:
            try:
                t = datetime.fromisoformat(event.start_time).strftime("%H:%M")
            except Exception:
                t = ""
            time_lbl = QLabel(t)
            time_lbl.setStyleSheet("font-size: 11px; color: #6c7086; min-width: 38px;")
            body_l.addWidget(time_lbl)

        # Emoji + title
        emoji = _cat_emoji(event.category)
        display = f"{emoji} {event.title}" if emoji else event.title
        title_lbl = QLabel(display)
        title_lbl.setStyleSheet("font-size: 13px;")
        title_lbl.setWordWrap(True)
        body_l.addWidget(title_lbl, 1)

        # Recurrence indicator
        if event.recurrence:
            rec_lbl = QLabel("↻")
            rec_lbl.setStyleSheet("color: #6c7086; font-size: 14px;")
            rec_lbl.setToolTip("Recurring event")
            body_l.addWidget(rec_lbl)

        layout.addWidget(body, 1)

        self.setStyleSheet(
            "DayEventRow { border: 1px solid #313244; border-radius: 4px; "
            "background-color: #181825; }"
            "DayEventRow:hover { border-color: #45475a; background-color: #1e1e2e; }"
        )

    def mouseDoubleClickEvent(self, ev):
        self.edit_requested.emit(self.event)

    def mousePressEvent(self, ev):
        # Single click selects (visual feedback via hover css)
        pass


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  CalendarPanel  — main panel
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class CalendarPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.store = CalendarStore()
        self._selected_date = date.today()
        self._palette: dict = {}
        self._build_ui()
        self._refresh()

        # Auto-refresh timer (every 60 s) to keep "today" highlight current
        self._auto_timer = QTimer(self)
        self._auto_timer.setInterval(60_000)
        self._auto_timer.timeout.connect(self._refresh)
        self._auto_timer.start()

    def set_palette(self, palette: dict):
        self._palette = palette

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  Build UI
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def _build_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ════════════════════════════════════════════
        #  LEFT COLUMN  (weekly grid + day detail)
        # ════════════════════════════════════════════
        left_col = QWidget()
        left_layout = QVBoxLayout(left_col)
        left_layout.setContentsMargins(14, 10, 8, 10)
        left_layout.setSpacing(0)

        # ── Top bar ──────────────────────────────────
        top_bar = QHBoxLayout()
        top_bar.setSpacing(6)

        title_lbl = QLabel("Calendar")
        title_lbl.setObjectName("sectionTitle")
        top_bar.addWidget(title_lbl)

        top_bar.addStretch()

        self._week_label = QLabel()
        self._week_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._week_label.setStyleSheet("font-size: 13px; font-weight: bold; color: #6c7086;")
        top_bar.addWidget(self._week_label)

        top_bar.addSpacing(8)

        btn_prev = QPushButton("‹")
        btn_prev.setObjectName("secondary")
        btn_prev.setFixedSize(28, 28)
        btn_prev.setToolTip("Previous week")
        btn_prev.clicked.connect(self._prev_week)
        top_bar.addWidget(btn_prev)

        btn_today = QPushButton("Today")
        btn_today.setObjectName("secondary")
        btn_today.setFixedHeight(28)
        btn_today.clicked.connect(self._go_today)
        top_bar.addWidget(btn_today)

        btn_next = QPushButton("›")
        btn_next.setObjectName("secondary")
        btn_next.setFixedSize(28, 28)
        btn_next.setToolTip("Next week")
        btn_next.clicked.connect(self._next_week)
        top_bar.addWidget(btn_next)

        top_bar.addSpacing(8)

        btn_add = QPushButton("＋ Event")
        btn_add.clicked.connect(self._add_event)
        top_bar.addWidget(btn_add)

        left_layout.addLayout(top_bar)
        left_layout.addSpacing(8)

        # ── Weekly grid (upper-left) ──────────────────
        self._week_container = QWidget()
        self._week_grid = QHBoxLayout(self._week_container)
        self._week_grid.setSpacing(0)
        self._week_grid.setContentsMargins(0, 0, 0, 0)

        week_scroll = QScrollArea()
        week_scroll.setWidgetResizable(True)
        week_scroll.setWidget(self._week_container)
        week_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        week_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        week_scroll.setMinimumHeight(220)
        week_scroll.setMaximumHeight(340)
        week_scroll.setFrameShape(QFrame.Shape.NoFrame)
        left_layout.addWidget(week_scroll, 3)

        # ── Divider ─────────────────────────────────
        div = QFrame()
        div.setFrameShape(QFrame.Shape.HLine)
        div.setStyleSheet("border: none; border-top: 1px solid #313244; margin: 8px 0;")
        left_layout.addWidget(div)

        # ── Day detail header ────────────────────────
        detail_bar = QHBoxLayout()
        self._day_title = QLabel("Today")
        self._day_title.setStyleSheet("font-size: 14px; font-weight: bold;")
        detail_bar.addWidget(self._day_title)
        detail_bar.addStretch()
        btn_add_here = QPushButton("＋")
        btn_add_here.setObjectName("secondary")
        btn_add_here.setFixedSize(26, 26)
        btn_add_here.setToolTip("Add event on this day")
        btn_add_here.clicked.connect(lambda: self._add_event_on_date(self._selected_date))
        detail_bar.addWidget(btn_add_here)
        left_layout.addLayout(detail_bar)
        left_layout.addSpacing(4)

        # ── Day detail list (lower-left) ─────────────
        self._day_list_layout = QVBoxLayout()
        self._day_list_layout.setSpacing(4)

        day_list_widget = QWidget()
        day_list_widget.setLayout(self._day_list_layout)

        day_scroll = QScrollArea()
        day_scroll.setWidgetResizable(True)
        day_scroll.setWidget(day_list_widget)
        day_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        day_scroll.setFrameShape(QFrame.Shape.NoFrame)
        left_layout.addWidget(day_scroll, 2)

        root.addWidget(left_col, 1)

        # ════════════════════════════════════════════
        #  RIGHT SIDEBAR  (mini-month + major events)
        # ════════════════════════════════════════════
        right_sidebar = QWidget()
        right_sidebar.setFixedWidth(258)
        right_sidebar.setObjectName("calSidebar")
        right_layout = QVBoxLayout(right_sidebar)
        right_layout.setContentsMargins(0, 10, 12, 10)
        right_layout.setSpacing(0)

        # ── Mini month (upper-right) ──────────────────
        mini_frame = QFrame()
        mini_frame.setObjectName("miniMonthFrame")
        mini_frame.setStyleSheet(
            "#miniMonthFrame { border: 1px solid #313244; border-radius: 8px; "
            "background-color: #181825; }"
        )
        mini_frame_layout = QVBoxLayout(mini_frame)
        mini_frame_layout.setContentsMargins(0, 0, 0, 0)

        self.mini_month = MiniMonth()
        self.mini_month.date_selected.connect(self._on_mini_date_selected)
        mini_frame_layout.addWidget(self.mini_month)

        right_layout.addWidget(mini_frame)
        right_layout.addSpacing(10)

        # ── Sidebar action buttons ────────────────────
        action_row = QHBoxLayout()
        action_row.setSpacing(4)

        btn_birthday = QPushButton("🎂 Birthdays")
        btn_birthday.setObjectName("secondary")
        btn_birthday.clicked.connect(self._manage_birthdays)
        action_row.addWidget(btn_birthday)

        btn_jump = QPushButton("Go to date…")
        btn_jump.setObjectName("secondary")
        btn_jump.clicked.connect(self._jump_to_date)
        action_row.addWidget(btn_jump)

        right_layout.addLayout(action_row)
        right_layout.addSpacing(10)

        # ── Divider ─────────────────────────────────
        div2 = QFrame()
        div2.setFrameShape(QFrame.Shape.HLine)
        div2.setStyleSheet("border: none; border-top: 1px solid #313244;")
        right_layout.addWidget(div2)
        right_layout.addSpacing(8)

        # ── Major events header ──────────────────────
        major_hdr = QHBoxLayout()
        major_title = QLabel("Upcoming Events")
        major_title.setStyleSheet("font-size: 13px; font-weight: bold;")
        major_hdr.addWidget(major_title)
        major_hdr.addStretch()
        self._major_count_lbl = QLabel("")
        self._major_count_lbl.setStyleSheet("font-size: 10px; color: #6c7086;")
        major_hdr.addWidget(self._major_count_lbl)
        right_layout.addLayout(major_hdr)
        right_layout.addSpacing(6)

        # ── Major events list (lower-right) ──────────
        self._major_list_layout = QVBoxLayout()
        self._major_list_layout.setSpacing(5)

        major_list_widget = QWidget()
        major_list_widget.setLayout(self._major_list_layout)

        major_scroll = QScrollArea()
        major_scroll.setWidgetResizable(True)
        major_scroll.setWidget(major_list_widget)
        major_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        major_scroll.setFrameShape(QFrame.Shape.NoFrame)
        right_layout.addWidget(major_scroll, 1)

        root.addWidget(right_sidebar)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  Refresh orchestration
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def _refresh(self):
        self._render_week()
        self._render_day_detail()
        self._render_major_events()
        self._update_mini_month_events()

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  Weekly grid renderer
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def _get_week_start(self) -> date:
        """Monday of the current selected week."""
        d = self._selected_date
        return d - timedelta(days=d.weekday())

    def _render_week(self):
        _clear_layout(self._week_grid)

        week_start = self._get_week_start()
        week_end   = week_start + timedelta(days=6)

        self._week_label.setText(
            f"{week_start.strftime('%b %d')} – {week_end.strftime('%b %d, %Y')}"
        )

        # Fetch regular events
        events = self.store.get_events(
            week_start.isoformat(),
            week_end.isoformat() + "T23:59:59",
        )

        # Also expand recurring events
        recurring = self.store.get_all_recurring_events()
        recurring_expanded: dict[date, list[Event]] = {}
        for ev in recurring:
            for occ_date in expand_recurring_to_range(ev, week_start, week_end):
                recurring_expanded.setdefault(occ_date, []).append(ev)

        # Merge into by-date dict
        events_by_date: dict[date, list[Event]] = {}
        for ev in events:
            try:
                d = datetime.fromisoformat(ev.start_time).date()
            except Exception:
                continue
            events_by_date.setdefault(d, []).append(ev)
        for d, evs in recurring_expanded.items():
            for ev in evs:
                if ev not in events_by_date.get(d, []):
                    events_by_date.setdefault(d, []).append(ev)

        # Birthdays for the week
        all_birthdays = self.store.get_birthdays()
        birthdays_by_date: dict[date, list[Birthday]] = {}
        for b in all_birthdays:
            try:
                bday = date(week_start.year, b.month, b.day)
            except ValueError:
                continue
            if week_start <= bday <= week_end:
                birthdays_by_date.setdefault(bday, []).append(b)

        today = date.today()
        for i in range(7):
            d = week_start + timedelta(days=i)

            if i > 0:
                # Thin vertical separator
                sep = QFrame()
                sep.setFrameShape(QFrame.Shape.VLine)
                sep.setStyleSheet("border: none; border-left: 1px solid #313244;")
                self._week_grid.addWidget(sep)

            day_events    = events_by_date.get(d, [])
            day_birthdays = birthdays_by_date.get(d, [])
            col = DayColumn(
                d, day_events, day_birthdays,
                is_today=(d == today),
                is_selected=(d == self._selected_date),
            )
            col.request_add.connect(self._add_event_on_date)
            col.request_edit.connect(self._edit_event)
            self._week_grid.addWidget(col, 1)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  Day detail renderer
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def _render_day_detail(self):
        _clear_layout(self._day_list_layout)

        d = self._selected_date
        today = date.today()
        if d == today:
            header_text = f"Today  ·  {d.strftime('%A, %B %d')}"
        elif d == today + timedelta(days=1):
            header_text = f"Tomorrow  ·  {d.strftime('%A, %B %d')}"
        elif d == today - timedelta(days=1):
            header_text = f"Yesterday  ·  {d.strftime('%A, %B %d')}"
        else:
            header_text = d.strftime("%A, %B %d, %Y")
        self._day_title.setText(header_text)

        # Regular events
        events = self.store.get_events(
            d.isoformat(), d.isoformat() + "T23:59:59"
        )

        # Recurring occurrences
        recurring = self.store.get_all_recurring_events()
        for ev in recurring:
            for occ in expand_recurring_to_range(ev, d, d):
                if ev not in events:
                    events.append(ev)

        # Birthdays
        bday_events: list[Event] = []
        for b in self.store.get_birthdays():
            if b.month == d.month and b.day == d.day:
                try:
                    age = (d.year - b.year) if b.year else None
                except Exception:
                    age = None
                age_str = f" (turns {age})" if age else ""
                bday_events.append(Event(
                    id=b.id,
                    title=f"🎂 {b.name}{age_str}",
                    start_time=datetime(d.year, d.month, d.day).isoformat(),
                    all_day=True, color="#f38ba8", category="birthday",
                ))

        all_events = sorted(
            bday_events + events,
            key=lambda e: (0 if e.all_day else 1, e.start_time)
        )

        if not all_events:
            empty_lbl = QLabel("No events — double-click a day to add one")
            empty_lbl.setStyleSheet("color: #6c7086; font-size: 12px; padding: 8px 0;")
            self._day_list_layout.addWidget(empty_lbl)
        else:
            for ev in all_events:
                row = DayEventRow(ev)
                row.edit_requested.connect(self._edit_event)
                self._day_list_layout.addWidget(row)

        self._day_list_layout.addStretch()

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  Major events renderer
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def _render_major_events(self):
        _clear_layout(self._major_list_layout)

        major_events = self.store.get_next_major_events(date.today(), limit=8)

        if not major_events:
            lbl = QLabel("No upcoming major events")
            lbl.setStyleSheet("color: #6c7086; font-size: 12px; padding: 8px 0;")
            lbl.setWordWrap(True)
            self._major_list_layout.addWidget(lbl)
            self._major_count_lbl.setText("")
        else:
            self._major_count_lbl.setText(f"{len(major_events)} upcoming")
            for ev_date, title, category, color in major_events:
                card = MajorEventCard(ev_date, title, category, color)
                self._major_list_layout.addWidget(card)

        self._major_list_layout.addStretch()

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  Mini-month event feed
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def _update_mini_month_events(self):
        vy, vm = self.mini_month._view_year, self.mini_month._view_month
        first = date(vy, vm, 1)
        if vm == 12:
            last = date(vy + 1, 1, 1) - timedelta(days=1)
        else:
            last = date(vy, vm + 1, 1) - timedelta(days=1)

        # Regular events
        events = self.store.get_events(first.isoformat(), last.isoformat() + "T23:59:59")
        by_date: dict[date, list[str]] = {}
        for ev in events:
            try:
                d = datetime.fromisoformat(ev.start_time).date()
            except Exception:
                continue
            by_date.setdefault(d, []).append(ev.color)

        # Recurring events
        recurring = self.store.get_all_recurring_events()
        for ev in recurring:
            for occ in expand_recurring_to_range(ev, first, last):
                by_date.setdefault(occ, []).append(ev.color)

        # Birthdays
        all_bdays = self.store.get_birthdays()
        for b in all_bdays:
            if b.month == vm:
                try:
                    d = date(vy, b.month, b.day)
                    if first <= d <= last:
                        by_date.setdefault(d, []).append("#f38ba8")
                except ValueError:
                    pass

        self.mini_month.set_events(by_date)

        # JP holidays (optional enhancement)
        try:
            from src.data.holidays_jp import get_japanese_holidays
            holidays = get_japanese_holidays(vy)
            hday_set = {d for d in holidays.keys() if first <= d <= last}
            self.mini_month.set_holidays(hday_set)
        except Exception:
            pass

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  Navigation
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def _prev_week(self):
        self._selected_date -= timedelta(weeks=1)
        self.mini_month.set_selected(self._selected_date)
        self._refresh()

    def _next_week(self):
        self._selected_date += timedelta(weeks=1)
        self.mini_month.set_selected(self._selected_date)
        self._refresh()

    def _go_today(self):
        self._selected_date = date.today()
        self.mini_month.set_selected(self._selected_date)
        self._refresh()

    def _on_mini_date_selected(self, d: date):
        self._selected_date = d
        self._update_mini_month_events()
        self._render_week()
        self._render_day_detail()

    def _jump_to_date(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Go to date")
        dlg.setModal(True)
        layout = QVBoxLayout(dlg)
        layout.addWidget(QLabel("Jump to date:"))
        de = QDateEdit()
        de.setCalendarPopup(True)
        de.setDisplayFormat("dd MMM yyyy")
        sd = self._selected_date
        de.setDate(QDate(sd.year, sd.month, sd.day))
        layout.addWidget(de)
        btn_row = QHBoxLayout()
        cancel = QPushButton("Cancel")
        cancel.clicked.connect(dlg.reject)
        go = QPushButton("Go")
        go.setDefault(True)
        go.clicked.connect(dlg.accept)
        btn_row.addStretch()
        btn_row.addWidget(cancel)
        btn_row.addWidget(go)
        layout.addLayout(btn_row)
        if dlg.exec():
            qd = de.date()
            self._selected_date = date(qd.year(), qd.month(), qd.day())
            self.mini_month.set_selected(self._selected_date)
            self._refresh()

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  Event CRUD
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def _add_event(self):
        self._add_event_on_date(self._selected_date)

    def _add_event_on_date(self, d: date):
        dlg = EventDialog(self, prefill_date=d)
        if dlg.exec():
            data = dlg.get_data()
            self.store.add_event(**data)
            self._refresh()

    def _edit_event(self, event: Event):
        dlg = EventDialog(self, event=event)
        result = dlg.exec()
        if dlg._delete_requested:
            reply = QMessageBox.question(
                self, "Delete Event",
                f'Delete "{event.title}"?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.store.delete_event(event.id)
                self._refresh()
        elif result:
            data = dlg.get_data()
            event.title       = data["title"]
            event.description = data["description"]
            event.start_time  = data["start_time"]
            event.end_time    = data["end_time"]
            event.all_day     = data["all_day"]
            event.color       = data["color"]
            event.category    = data["category"]
            event.recurrence  = data["recurrence"]
            self.store.update_event(event)
            self._refresh()

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  Birthday management
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def _manage_birthdays(self):
        dlg = BirthdayManagerDialog(self, self.store)
        dlg.exec()
        self._refresh()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  BirthdayManagerDialog
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class BirthdayManagerDialog(QDialog):
    """Lists all birthdays with add/edit/delete capabilities."""

    def __init__(self, parent, store: CalendarStore):
        super().__init__(parent)
        self.store = store
        self.setWindowTitle("Birthday Manager")
        self.setMinimumSize(400, 460)
        self.setModal(True)
        self._build_ui()
        self._load()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        hdr = QHBoxLayout()
        title = QLabel("🎂  Birthdays")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        hdr.addWidget(title)
        hdr.addStretch()
        add_btn = QPushButton("＋ Add")
        add_btn.clicked.connect(self._add_birthday)
        hdr.addWidget(add_btn)
        layout.addLayout(hdr)

        # Search
        self._search = QLineEdit()
        self._search.setPlaceholderText("Search by name…")
        self._search.textChanged.connect(self._filter)
        layout.addWidget(self._search)

        # Scroll list
        self._list_widget = QWidget()
        self._list_layout = QVBoxLayout(self._list_widget)
        self._list_layout.setSpacing(4)
        self._list_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self._list_widget)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        layout.addWidget(scroll, 1)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, 0, Qt.AlignmentFlag.AlignRight)

    def _load(self):
        self._birthdays = self.store.get_birthdays()
        self._filter(self._search.text())

    def _filter(self, text: str):
        _clear_layout(self._list_layout)
        query = text.lower()
        today = date.today()

        filtered = [b for b in self._birthdays if query in b.name.lower()]
        # Sort by upcoming (month, day from today)
        def sort_key(b: Birthday):
            try:
                candidate = date(today.year, b.month, b.day)
                if candidate < today:
                    candidate = date(today.year + 1, b.month, b.day)
                return (candidate - today).days
            except ValueError:
                return 9999
        filtered.sort(key=sort_key)

        if not filtered:
            self._list_layout.addWidget(
                QLabel("No birthdays yet — add one!" if not text else "No matches")
            )
        for b in filtered:
            self._list_layout.addWidget(self._make_row(b))
        self._list_layout.addStretch()

    def _make_row(self, b: Birthday) -> QFrame:
        row = QFrame()
        row.setStyleSheet(
            "QFrame { border: 1px solid #313244; border-radius: 6px; "
            "background-color: #181825; padding: 2px; }"
        )
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(10, 6, 10, 6)
        row_layout.setSpacing(8)

        cake = QLabel("🎂")
        cake.setStyleSheet("font-size: 18px;")
        cake.setFixedWidth(24)
        row_layout.addWidget(cake)

        info = QVBoxLayout()
        info.setSpacing(1)
        name_lbl = QLabel(b.name)
        name_lbl.setStyleSheet("font-size: 13px; font-weight: bold;")
        info.addWidget(name_lbl)

        today = date.today()
        try:
            next_bday = date(today.year, b.month, b.day)
            if next_bday < today:
                next_bday = date(today.year + 1, b.month, b.day)
            days_left = (next_bday - today).days
            suffix = f"  ·  {days_left}d away" if days_left > 0 else "  ·  Today! 🎉"
        except ValueError:
            suffix = ""

        months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        date_str = f"{months[b.month-1]} {b.day}"
        if b.year:
            age = today.year - b.year
            date_str += f", {b.year}  (turns {age})"
        date_str += suffix
        date_lbl = QLabel(date_str)
        date_lbl.setStyleSheet("font-size: 11px; color: #6c7086;")
        info.addWidget(date_lbl)

        row_layout.addLayout(info, 1)

        edit_btn = QPushButton("Edit")
        edit_btn.setObjectName("secondary")
        edit_btn.setFixedHeight(26)
        edit_btn.clicked.connect(lambda _, bd=b: self._edit_birthday(bd))
        row_layout.addWidget(edit_btn)

        return row

    def _add_birthday(self):
        dlg = BirthdayDialog(self)
        if dlg.exec():
            data = dlg.get_data()
            self.store.add_birthday(**data)
            self._load()

    def _edit_birthday(self, birthday: Birthday):
        dlg = BirthdayDialog(self, birthday)
        result = dlg.exec()
        if dlg._delete_requested:
            reply = QMessageBox.question(
                self, "Delete Birthday",
                f"Remove birthday for {birthday.name}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.store.delete_birthday(birthday.id)
                self._load()
        elif result:
            data = dlg.get_data()
            birthday.name  = data["name"]
            birthday.month = data["month"]
            birthday.day   = data["day"]
            birthday.year  = data["year"]
            self.store.update_birthday(birthday)
            self._load()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Utility
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _clear_layout(layout):
    """Remove and delete all widgets from a layout."""
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()
        elif child.layout():
            _clear_layout(child.layout())