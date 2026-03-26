"""Calendar module UI — weekly view + mini-month navigator + major events.

All colors read from the active theme palette so the panel adapts when the
user switches themes.  No hardcoded hex values remain in inline stylesheets
or paintEvent code.

Layout (positions unchanged):
  Upper-left  → Weekly overview grid (7 day columns)
  Lower-left  → Selected-day detail list
  Upper-right → Mini month navigator (interactive dot indicators)
  Lower-right → Next major events panel
"""

from __future__ import annotations

import calendar
from datetime import date, datetime, timedelta

from PyQt6.QtCore import Qt, QDate, QTime, QTimer, pyqtSignal
from PyQt6.QtGui import QColor, QPainter, QPen, QBrush, QFont, QFontMetrics, QMouseEvent
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QDialog, QLineEdit, QTextEdit,
    QDateEdit, QTimeEdit, QCheckBox, QFrame, QComboBox,
    QMessageBox, QScrollArea, QSizePolicy, QTabWidget,
    QButtonGroup, QToolButton, QSpinBox,
)

from src.data.calendar_store import (
    CalendarStore, Event, Birthday,
    build_recurrence, expand_recurring_to_range,
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Module-level palette  (updated by CalendarPanel.set_palette)
#  Defaults = Catppuccin Dark so the panel renders correctly before
#  MainWindow calls set_palette() for the first time.
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

_PALETTE: dict = {
    "bg":        "#1e1e2e", "surface":   "#313244", "border": "#45475a",
    "fg":        "#cdd6f4", "muted":     "#7f849c",  "hover":  "#3b3d54",
    "accent":    "#89b4fa", "accent_fg": "#1e1e2e",
    "header_bg": "#181825", "alt_row":   "#252538",
    "red":       "#f38ba8", "green":     "#a6e3a1",  "yellow": "#f9e2af",
}


def _p(key: str, fallback: str = "#888888") -> str:
    """Return current palette value for *key*."""
    return _PALETTE.get(key, fallback)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Category / color constants
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EVENT_COLORS: dict[str, str] = {
    "Sky Blue": "#4a9eff", "Mint":     "#a6e3a1", "Rose":    "#f38ba8",
    "Peach":    "#fab387", "Gold":     "#f9e2af", "Lavender":"#cba6f7",
    "Teal":     "#94e2d5", "Pink":     "#f5c2e7", "Coral":   "#ff6b6b",
    "Sage":     "#74c7b8",
}

CATEGORY_META: dict[str, dict] = {
    "":         {"label": "General",     "emoji": "📅", "color": "#4a9eff"},
    "work":     {"label": "Work",        "emoji": "💼", "color": "#4a9eff"},
    "birthday": {"label": "Birthday",    "emoji": "🎂", "color": "#f38ba8"},
    "trip":     {"label": "Trip",        "emoji": "✈️",  "color": "#94e2d5"},
    "holiday":  {"label": "Holiday",     "emoji": "🎉", "color": "#f9e2af"},
    "major":    {"label": "Major Event", "emoji": "⭐", "color": "#cba6f7"},
    "health":   {"label": "Health",      "emoji": "🏥", "color": "#a6e3a1"},
    "social":   {"label": "Social",      "emoji": "🎭", "color": "#fab387"},
}

RECURRENCE_OPTIONS = [
    ("",        "Does not repeat"), ("daily",   "Every day"),
    ("weekly",  "Weekly (select days)"), ("monthly", "Monthly"),
    ("yearly",  "Yearly"),
]

WEEKDAY_LABELS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def _cat_emoji(cat: str) -> str:
    return CATEGORY_META.get(cat, CATEGORY_META[""]).get("emoji", "")

def _cat_color(cat: str) -> str:
    return CATEGORY_META.get(cat, CATEGORY_META[""]).get("color", "#4a9eff")

def _clear_layout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():   child.widget().deleteLater()
        elif child.layout(): _clear_layout(child.layout())


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ColorButton
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ColorButton(QToolButton):
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


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  EventDialog
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class EventDialog(QDialog):
    def __init__(self, parent=None, event: Event | None = None,
                 prefill_date: date | None = None):
        super().__init__(parent)
        self.event = event
        self._delete_requested = False
        self.setWindowTitle("Edit Event" if event else "New Event")
        self.setMinimumWidth(460)
        self.setModal(True)
        self._build_ui(prefill_date)

    def _build_ui(self, prefill_date):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        init_color = self.event.color if self.event else _p("accent")
        self._header_strip = QFrame()
        self._header_strip.setFixedHeight(6)
        self._header_strip.setStyleSheet(
            f"background-color: {init_color}; border-radius: 3px 3px 0 0;")
        root.addWidget(self._header_strip)

        body = QWidget()
        body_l = QVBoxLayout(body)
        body_l.setContentsMargins(20, 16, 20, 16)
        body_l.setSpacing(12)
        root.addWidget(body)

        tabs = QTabWidget()
        tabs.setDocumentMode(True)
        body_l.addWidget(tabs)

        # ── Details tab ──
        det_tab = QWidget()
        det = QVBoxLayout(det_tab)
        det.setContentsMargins(4, 12, 4, 4)
        det.setSpacing(10)
        tabs.addTab(det_tab, "Details")

        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Event title…")
        self.title_edit.setStyleSheet("font-size: 15px; padding: 6px; font-weight: bold;")
        if self.event: self.title_edit.setText(self.event.title)
        det.addWidget(self.title_edit)

        self.desc_edit = QTextEdit()
        self.desc_edit.setMaximumHeight(68)
        self.desc_edit.setPlaceholderText("Optional description…")
        if self.event: self.desc_edit.setPlainText(self.event.description)
        det.addWidget(self.desc_edit)

        cat_row = QHBoxLayout()
        cat_row.addWidget(QLabel("Category"))
        self.category_combo = QComboBox()
        for key, meta in CATEGORY_META.items():
            self.category_combo.addItem(f"{meta['emoji']} {meta['label']}", key)
        if self.event:
            idx = self.category_combo.findData(self.event.category)
            if idx >= 0: self.category_combo.setCurrentIndex(idx)
        self.category_combo.currentIndexChanged.connect(self._on_category_changed)
        cat_row.addWidget(self.category_combo, 1)
        det.addLayout(cat_row)

        det.addWidget(QLabel("Color"))
        color_row = QHBoxLayout()
        color_row.setSpacing(6)
        self._color_group = QButtonGroup(self)
        self._color_group.setExclusive(True)
        self._color_btns: dict[str, ColorButton] = {}
        current_color = self.event.color if self.event else _p("accent")
        for name, hex_val in EVENT_COLORS.items():
            btn = ColorButton(hex_val, name)
            btn.setChecked(hex_val == current_color)
            btn.clicked.connect(lambda _, h=hex_val: self._on_color_picked(h))
            self._color_group.addButton(btn)
            self._color_btns[hex_val] = btn
            color_row.addWidget(btn)
        color_row.addStretch()
        det.addLayout(color_row)

        self.all_day_check = QCheckBox("All-day event")
        if self.event: self.all_day_check.setChecked(self.event.all_day)
        self.all_day_check.toggled.connect(self._toggle_time)
        det.addWidget(self.all_day_check)

        dt_row = QHBoxLayout()
        dt_row.setSpacing(8)
        dt_row.addWidget(QLabel("Date"))
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDisplayFormat("dd MMM yyyy")
        if self.event:
            d0 = datetime.fromisoformat(self.event.start_time)
            self.date_edit.setDate(QDate(d0.year, d0.month, d0.day))
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
            d0 = datetime.fromisoformat(self.event.start_time)
            self.start_time.setTime(QTime(d0.hour, d0.minute))
        else:
            self.start_time.setTime(QTime(9, 0))
        dt_row.addWidget(self.start_time, 1)

        dt_row.addWidget(QLabel("End"))
        self.end_time = QTimeEdit()
        self.end_time.setDisplayFormat("HH:mm")
        if self.event and self.event.end_time:
            d0 = datetime.fromisoformat(self.event.end_time)
            self.end_time.setTime(QTime(d0.hour, d0.minute))
        else:
            self.end_time.setTime(QTime(10, 0))
        dt_row.addWidget(self.end_time, 1)
        det.addLayout(dt_row)
        self._toggle_time(self.all_day_check.isChecked())

        # ── Repeat tab ──
        rec_tab = QWidget()
        rec = QVBoxLayout(rec_tab)
        rec.setContentsMargins(4, 12, 4, 4)
        rec.setSpacing(10)
        tabs.addTab(rec_tab, "Repeat")

        rec.addWidget(QLabel("Repeat pattern"))
        self.rec_combo = QComboBox()
        for val, label in RECURRENCE_OPTIONS:
            self.rec_combo.addItem(label, val)
        rec.addWidget(self.rec_combo)
        self.rec_combo.currentIndexChanged.connect(
            lambda _: self._weekday_frame.setVisible(
                self.rec_combo.currentData() == "weekly"))

        self._weekday_frame = QFrame()
        wdf = QHBoxLayout(self._weekday_frame)
        wdf.setContentsMargins(0, 4, 0, 0)
        wdf.setSpacing(4)
        self._weekday_btns: list[QToolButton] = []
        for label in WEEKDAY_LABELS:
            btn = QToolButton()
            btn.setText(label)
            btn.setCheckable(True)
            btn.setFixedSize(42, 30)
            self._weekday_btns.append(btn)
            wdf.addWidget(btn)
        wdf.addStretch()
        rec.addWidget(self._weekday_frame)
        self._weekday_frame.setVisible(False)
        rec.addStretch()

        if self.event and self.event.recurrence:
            r = self.event.recurrence
            if r == "daily":      self.rec_combo.setCurrentIndex(1)
            elif r.startswith("weekly:"):
                self.rec_combo.setCurrentIndex(2)
                for d in [int(x) for x in r.split(":")[1].split(",") if x.strip()]:
                    if 0 <= d < len(self._weekday_btns):
                        self._weekday_btns[d].setChecked(True)
            elif r == "monthly":  self.rec_combo.setCurrentIndex(3)
            elif r == "yearly":   self.rec_combo.setCurrentIndex(4)

        # ── Buttons ──
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setObjectName("separator")
        body_l.addWidget(sep)

        btn_row = QHBoxLayout()
        if self.event:
            del_btn = QPushButton("🗑  Delete")
            del_btn.setObjectName("destructive")
            del_btn.clicked.connect(self._on_delete)
            btn_row.addWidget(del_btn)
        btn_row.addStretch()
        cancel = QPushButton("Cancel")
        cancel.setObjectName("secondary")
        cancel.clicked.connect(self.reject)
        btn_row.addWidget(cancel)
        save = QPushButton("Save Event")
        save.setDefault(True)
        save.clicked.connect(self._on_save)
        btn_row.addWidget(save)
        body_l.addLayout(btn_row)

    def _on_color_picked(self, hex_val: str):
        self._header_strip.setStyleSheet(
            f"background-color: {hex_val}; border-radius: 3px 3px 0 0;")

    def _on_category_changed(self, _):
        auto = _cat_color(self.category_combo.currentData())
        btn = self._color_btns.get(auto)
        if btn:
            for b in self._color_btns.values(): b.setChecked(False)
            btn.setChecked(True)
            self._on_color_picked(auto)

    def _toggle_time(self, all_day: bool):
        self.start_time.setEnabled(not all_day)
        self.end_time.setEnabled(not all_day)

    def _on_delete(self):
        self._delete_requested = True; self.reject()

    def _on_save(self):
        if not self.title_edit.text().strip():
            self.title_edit.setFocus()
            self.title_edit.setPlaceholderText("⚠ Title is required")
            return
        self.accept()

    def _selected_color(self) -> str:
        for hex_val, btn in self._color_btns.items():
            if btn.isChecked(): return hex_val
        return _p("accent")

    def _selected_recurrence(self) -> str:
        val = self.rec_combo.currentData()
        if val == "weekly":
            days = [i for i, b in enumerate(self._weekday_btns) if b.isChecked()]
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
            st = self.start_time.time(); et = self.end_time.time()
            start = datetime(d.year, d.month, d.day, st.hour(), st.minute()).isoformat()
            end   = datetime(d.year, d.month, d.day, et.hour(), et.minute()).isoformat()
        return {
            "title":       self.title_edit.text().strip() or "Untitled",
            "description": self.desc_edit.toPlainText(),
            "start_time":  start, "end_time": end,
            "all_day":     all_day, "color": self._selected_color(),
            "category":    self.category_combo.currentData() or "",
            "recurrence":  self._selected_recurrence(),
        }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  BirthdayDialog
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class BirthdayDialog(QDialog):
    def __init__(self, parent=None, birthday: Birthday | None = None):
        super().__init__(parent)
        self.birthday = birthday
        self._delete_requested = False
        self.setWindowTitle("Edit Birthday" if birthday else "Add Birthday")
        self.setMinimumWidth(340); self.setModal(True)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 16)
        layout.setSpacing(12)

        hdr = QLabel("🎂  Birthday")
        hdr.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(hdr)

        layout.addWidget(QLabel("Name"))
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Person's name…")
        if self.birthday: self.name_edit.setText(self.birthday.name)
        layout.addWidget(self.name_edit)

        mdy = QHBoxLayout()
        for label, attr, lo, hi in [("Month","month",1,12), ("Day","day",1,31)]:
            col = QVBoxLayout()
            col.addWidget(QLabel(label))
            spin = QSpinBox(); spin.setRange(lo, hi)
            if self.birthday: spin.setValue(getattr(self.birthday, attr))
            col.addWidget(spin); mdy.addLayout(col)
            setattr(self, f"{attr}_spin", spin)
        yr_col = QVBoxLayout()
        yr_col.addWidget(QLabel("Year (optional)"))
        self.year_spin = QSpinBox()
        self.year_spin.setRange(0, 9999)
        self.year_spin.setSpecialValueText("—")
        self.year_spin.setValue(self.birthday.year if (self.birthday and self.birthday.year) else 0)
        yr_col.addWidget(self.year_spin); mdy.addLayout(yr_col)
        layout.addLayout(mdy)

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine); sep.setObjectName("separator")
        layout.addWidget(sep)

        btn_row = QHBoxLayout()
        if self.birthday:
            del_btn = QPushButton("Delete"); del_btn.setObjectName("destructive")
            del_btn.clicked.connect(self._on_delete); btn_row.addWidget(del_btn)
        btn_row.addStretch()
        cancel = QPushButton("Cancel"); cancel.setObjectName("secondary")
        cancel.clicked.connect(self.reject); btn_row.addWidget(cancel)
        save = QPushButton("Save"); save.setDefault(True)
        save.clicked.connect(self._on_save); btn_row.addWidget(save)
        layout.addLayout(btn_row)

    def _on_delete(self): self._delete_requested = True; self.reject()
    def _on_save(self):
        if not self.name_edit.text().strip(): self.name_edit.setFocus(); return
        self.accept()
    def get_data(self) -> dict:
        y = self.year_spin.value()
        return {"name": self.name_edit.text().strip(),
                "month": self.month_spin.value(), "day": self.day_spin.value(),
                "year": y if y > 0 else None}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  MiniMonthCell  — fully painted using current palette
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class MiniMonthCell(QWidget):
    clicked = pyqtSignal(int, int, int)
    CELL = 32

    def __init__(self, year, month, day, is_today, is_selected,
                 event_colors: list[str], is_holiday: bool = False, parent=None):
        super().__init__(parent)
        self.year, self.month, self.day = year, month, day
        self.is_today = is_today; self.is_selected = is_selected
        self.event_colors = event_colors[:4]; self.is_holiday = is_holiday
        self._hovered = False
        self.setFixedSize(self.CELL, self.CELL)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        if event_colors or is_holiday:
            parts = (["Holiday"] if is_holiday else []) + ([f"{len(event_colors)} event(s)"] if event_colors else [])
            self.setToolTip(", ".join(parts))

    def enterEvent(self, ev): self._hovered = True;  self.update()
    def leaveEvent(self, ev): self._hovered = False; self.update()
    def mousePressEvent(self, ev): self.clicked.emit(self.year, self.month, self.day)

    def paintEvent(self, ev):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        cx, cy = w / 2, (h - 6) / 2

        accent = QColor(_p("accent"))
        fg     = QColor(_p("fg"))
        muted  = QColor(_p("muted"))
        hover_c= QColor(_p("hover"))
        red    = QColor(_p("red"))

        if self.is_today:
            p.setBrush(QBrush(accent)); p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(int(cx-13), int(cy-13), 26, 26)
        elif self.is_selected:
            c = QColor(accent); c.setAlpha(45)
            p.setBrush(QBrush(c)); p.setPen(QPen(accent, 1.5))
            p.drawEllipse(int(cx-13), int(cy-13), 26, 26)
        elif self._hovered:
            p.setBrush(QBrush(hover_c)); p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(int(cx-13), int(cy-13), 26, 26)

        font = QFont(); font.setPixelSize(12)
        if self.is_today or self.is_selected: font.setBold(True)
        p.setFont(font)
        if self.is_today:        p.setPen(QColor(_p("accent_fg")))
        elif self.is_holiday:    p.setPen(red)
        else:                    p.setPen(fg)
        p.drawText(0, 0, w, int(h-7), Qt.AlignmentFlag.AlignCenter, str(self.day))

        if self.event_colors:
            dr=3; n=len(self.event_colors); sp=dr*2+2
            sx = cx - (n*sp-2)/2; dy = h-5
            for i, color in enumerate(self.event_colors):
                p.setBrush(QBrush(QColor(color))); p.setPen(Qt.PenStyle.NoPen)
                p.drawEllipse(int(sx+i*sp-dr), int(dy-dr), dr*2, dr*2)
        p.end()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  MiniMonth
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class MiniMonth(QWidget):
    date_selected = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(240)
        self._selected    = date.today()
        self._view_year   = self._selected.year
        self._view_month  = self._selected.month
        self._events:    dict[date, list[str]] = {}
        self._holidays:  set[date]             = set()
        self._nav_buttons: list[QPushButton]   = []
        self._dow_labels:  list[QLabel]        = []
        self._title_btn:   QPushButton         = None  # type: ignore
        self._build()

    # ── Public ──────────────────────────────────────

    def set_events(self, by_date: dict[date, list[str]]):
        self._events = by_date; self._render()

    def set_holidays(self, holidays: set[date]):
        self._holidays = holidays; self._render()

    def set_selected(self, d: date):
        self._selected = d
        self._view_year = d.year; self._view_month = d.month
        self._render()

    def refresh_styles(self):
        """Re-apply palette colors to navigation buttons/labels."""
        nav_style = (
            f"QPushButton {{ background-color: {_p('surface')}; color: {_p('fg')}; "
            f"border: 1px solid {_p('border')}; border-radius: 4px; "
            f"font-weight: bold; font-size: 14px; padding: 0px; }}"
            f"QPushButton:hover {{ background-color: {_p('hover')}; "
            f"border-color: {_p('accent')}; color: {_p('accent')}; }}"
            f"QPushButton:pressed {{ background-color: {_p('border')}; }}"
        )
        for btn in self._nav_buttons:
            btn.setStyleSheet(nav_style)
        if self._title_btn:
            self._title_btn.setStyleSheet(
                f"QPushButton {{ background-color: transparent; color: {_p('fg')}; "
                f"border: none; font-weight: bold; font-size: 13px; }}"
                f"QPushButton:hover {{ color: {_p('accent')}; }}"
            )
        for lbl in self._dow_labels:
            lbl.setStyleSheet(f"font-size: 10px; font-weight: bold; color: {_p('muted')};")
        self._render()

    # ── Build ────────────────────────────────────────

    def _nav_style(self) -> str:
        return (
            f"QPushButton {{ background-color: {_p('surface')}; color: {_p('fg')}; "
            f"border: 1px solid {_p('border')}; border-radius: 4px; "
            f"font-weight: bold; font-size: 14px; padding: 0px; }}"
            f"QPushButton:hover {{ background-color: {_p('hover')}; "
            f"border-color: {_p('accent')}; color: {_p('accent')}; }}"
            f"QPushButton:pressed {{ background-color: {_p('border')}; }}"
        )

    def _build(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(8, 8, 8, 8); outer.setSpacing(2)

        nav = QHBoxLayout(); nav.setSpacing(0)
        for symbol, tip, handler in [
            ("«","Previous year", self._prev_year),
            ("‹","Previous month",self._prev_month),
        ]:
            btn = QPushButton(symbol); btn.setFixedSize(26, 26)
            btn.setToolTip(tip); btn.clicked.connect(handler)
            btn.setStyleSheet(self._nav_style())
            self._nav_buttons.append(btn); nav.addWidget(btn)

        self._title_btn = QPushButton()
        self._title_btn.setFlat(True)
        self._title_btn.clicked.connect(self._go_today_month)
        self._title_btn.setStyleSheet(
            f"QPushButton {{ background-color: transparent; color: {_p('fg')}; "
            f"border: none; font-weight: bold; font-size: 13px; }}"
            f"QPushButton:hover {{ color: {_p('accent')}; }}"
        )
        nav.addWidget(self._title_btn, 1)

        for symbol, tip, handler in [
            ("›","Next month",self._next_month),
            ("»","Next year", self._next_year),
        ]:
            btn = QPushButton(symbol); btn.setFixedSize(26, 26)
            btn.setToolTip(tip); btn.clicked.connect(handler)
            btn.setStyleSheet(self._nav_style())
            self._nav_buttons.append(btn); nav.addWidget(btn)

        outer.addLayout(nav)

        dow_row = QHBoxLayout(); dow_row.setSpacing(0)
        dow_row.setContentsMargins(0, 4, 0, 0)
        for label in ["Mo","Tu","We","Th","Fr","Sa","Su"]:
            lbl = QLabel(label)
            lbl.setFixedSize(MiniMonthCell.CELL, 16)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet(f"font-size: 10px; font-weight: bold; color: {_p('muted')};")
            self._dow_labels.append(lbl); dow_row.addWidget(lbl)
        outer.addLayout(dow_row)

        self._grid_w = QWidget()
        self._grid   = QGridLayout(self._grid_w)
        self._grid.setSpacing(1); self._grid.setContentsMargins(0,0,0,0)
        outer.addWidget(self._grid_w)
        outer.addStretch()
        self._render()

    def _render(self):
        _clear_layout(self._grid)
        self._title_btn.setText(
            f"{calendar.month_abbr[self._view_month]} {self._view_year}"
        )
        today = date.today()
        for row, week in enumerate(
                calendar.Calendar(firstweekday=0).monthdayscalendar(
                    self._view_year, self._view_month)):
            for col, day in enumerate(week):
                if day == 0:
                    sp = QLabel(); sp.setFixedSize(MiniMonthCell.CELL, MiniMonthCell.CELL)
                    self._grid.addWidget(sp, row, col)
                else:
                    d = date(self._view_year, self._view_month, day)
                    cell = MiniMonthCell(
                        self._view_year, self._view_month, day,
                        is_today=(d==today), is_selected=(d==self._selected),
                        event_colors=self._events.get(d,[]),
                        is_holiday=(d in self._holidays),
                    )
                    cell.clicked.connect(self._on_cell_click)
                    self._grid.addWidget(cell, row, col)

    def _on_cell_click(self, y, m, d):
        self._selected = date(y,m,d); self._render()
        self.date_selected.emit(self._selected)

    def _prev_month(self):
        if self._view_month==1: self._view_month=12; self._view_year-=1
        else: self._view_month-=1
        self._render()
    def _next_month(self):
        if self._view_month==12: self._view_month=1; self._view_year+=1
        else: self._view_month+=1
        self._render()
    def _prev_year(self): self._view_year-=1; self._render()
    def _next_year(self): self._view_year+=1; self._render()
    def _go_today_month(self):
        t=date.today(); self._view_year=t.year; self._view_month=t.month; self._render()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  EventChip  — painted event chip in week grid
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class EventChip(QWidget):
    double_clicked = pyqtSignal(object)

    def __init__(self, event: Event, parent=None):
        super().__init__(parent)
        self.event = event; self._hovered = False
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        self.setMinimumHeight(28)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        time_str = ""
        if not event.all_day:
            try:
                dt = datetime.fromisoformat(event.start_time)
                time_str = dt.strftime("%H:%M")
                if event.end_time:
                    et = datetime.fromisoformat(event.end_time)
                    time_str += f"–{et.strftime('%H:%M')}"
            except Exception: pass
        self._time_str = time_str
        emoji = _cat_emoji(event.category)
        self._display = f"{emoji} {event.title}" if emoji else event.title
        tip = self._display
        if time_str: tip += f"\n{time_str}"
        if event.description: tip += f"\n{event.description[:80]}"
        self.setToolTip(tip)

    def enterEvent(self, ev): self._hovered=True;  self.update()
    def leaveEvent(self, ev): self._hovered=False; self.update()
    def mouseDoubleClickEvent(self, ev): self.double_clicked.emit(self.event)

    def paintEvent(self, ev):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        color = QColor(self.event.color)
        bg = QColor(color); bg.setAlpha(55 if self._hovered else 35)
        p.setBrush(QBrush(bg)); p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(0,0,w,h,4,4)
        p.setBrush(QBrush(color)); p.drawRoundedRect(0,0,3,h,2,2)
        text_c = color.lighter(145 if self._hovered else 128)
        p.setPen(text_c)
        font = QFont()
        if self._time_str:
            font.setPixelSize(9); p.setFont(font)
            p.drawText(8,0,w-10,h//2+2,Qt.AlignmentFlag.AlignVCenter,self._time_str)
            font.setPixelSize(11); font.setBold(True); p.setFont(font)
            fm = QFontMetrics(font)
            p.drawText(8,h//2-2,w-10,h//2+2,Qt.AlignmentFlag.AlignVCenter,
                       fm.elidedText(self._display,Qt.TextElideMode.ElideRight,w-14))
        else:
            font.setPixelSize(11); font.setBold(True); p.setFont(font)
            fm = QFontMetrics(font)
            p.drawText(8,0,w-10,h,Qt.AlignmentFlag.AlignVCenter,
                       fm.elidedText(self._display,Qt.TextElideMode.ElideRight,w-14))
        p.end()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  DayColumn
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class DayColumn(QWidget):
    request_add  = pyqtSignal(object)
    request_edit = pyqtSignal(object)

    def __init__(self, d: date, events: list[Event], birthdays: list[Birthday],
                 is_today: bool, is_selected: bool, parent=None):
        super().__init__(parent)
        self.d = d; self._hovered = False
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        self._build(events, birthdays, is_today, is_selected)

    def _build(self, events, birthdays, is_today, is_selected):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(3,4,3,4); layout.setSpacing(3)

        header = QWidget(); header.setFixedHeight(46)
        hl = QVBoxLayout(header); hl.setContentsMargins(0,2,0,2); hl.setSpacing(0)

        name_lbl = QLabel(self.d.strftime("%a").upper())
        name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_lbl.setStyleSheet(f"font-size:10px; font-weight:bold; color:{_p('muted')};")
        hl.addWidget(name_lbl)

        num_lbl = QLabel(str(self.d.day))
        num_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if is_today:
            num_lbl.setStyleSheet(
                f"background-color:{_p('accent')};color:{_p('accent_fg')};"
                "border-radius:13px;font-size:16px;font-weight:bold;padding:0 4px;")
            num_lbl.setFixedSize(26,26)
        elif is_selected:
            num_lbl.setStyleSheet(
                f"border:1.5px solid {_p('accent')};border-radius:13px;"
                "font-size:16px;font-weight:bold;padding:0 4px;")
            num_lbl.setFixedSize(26,26)
        else:
            num_lbl.setStyleSheet(f"font-size:16px;color:{_p('fg')};")
        hl.addWidget(num_lbl, 0, Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(header)

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"border:none;border-top:1px solid {_p('border')};")
        layout.addWidget(sep)

        for ev in sorted(events, key=lambda e: e.start_time):
            if ev.all_day:
                chip = EventChip(ev)
                chip.double_clicked.connect(self.request_edit.emit)
                layout.addWidget(chip)

        for b in birthdays:
            try: age = (self.d.year-b.year) if b.year else None
            except Exception: age = None
            age_str = f" ({age})" if age else ""
            fake = Event(id=b.id, title=f"🎂 {b.name}{age_str}",
                         start_time=datetime(self.d.year,self.d.month,self.d.day).isoformat(),
                         all_day=True, color=_p("red"), category="birthday")
            layout.addWidget(EventChip(fake))

        for ev in sorted(events, key=lambda e: e.start_time):
            if not ev.all_day:
                chip = EventChip(ev)
                chip.double_clicked.connect(self.request_edit.emit)
                layout.addWidget(chip)

        layout.addStretch()

    def enterEvent(self, ev): self._hovered=True;  self.update()
    def leaveEvent(self, ev): self._hovered=False; self.update()
    def mouseDoubleClickEvent(self, ev): self.request_add.emit(self.d)
    def paintEvent(self, ev):
        p=QPainter(self)
        if self._hovered: p.fillRect(self.rect(), QColor(_p("hover")))
        p.end()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  MajorEventCard
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class MajorEventCard(QFrame):
    def __init__(self, ev_date: date, title: str, category: str, color: str, parent=None):
        super().__init__(parent)
        today = date.today(); delta = (ev_date-today).days
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10,8,10,8); layout.setSpacing(10)

        bar = QFrame(); bar.setFixedWidth(3)
        bar.setStyleSheet(f"background-color:{color};border-radius:2px;")
        layout.addWidget(bar)

        emoji_lbl = QLabel(_cat_emoji(category))
        emoji_lbl.setStyleSheet("font-size:16px;"); emoji_lbl.setFixedWidth(22)
        layout.addWidget(emoji_lbl)

        text_col = QVBoxLayout(); text_col.setSpacing(1)
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(f"font-size:12px;font-weight:bold;color:{_p('fg')};")
        title_lbl.setWordWrap(True); text_col.addWidget(title_lbl)
        date_lbl = QLabel(ev_date.strftime("%b %d, %Y"))
        date_lbl.setStyleSheet(f"font-size:10px;color:{_p('muted')};")
        text_col.addWidget(date_lbl); layout.addLayout(text_col,1)

        if   delta==0:    bt,bc="Today",    color
        elif delta==1:    bt,bc="Tomorrow", color
        elif delta<0:     bt,bc=f"{abs(delta)}d ago", _p("muted")
        elif delta<=7:    bt,bc=f"{delta}d", color
        elif delta<=30:   bt,bc=f"{delta}d", _p("yellow")
        else:             bt,bc=f"{delta//7}w",_p("muted")

        badge=QLabel(bt)
        badge.setStyleSheet(
            f"color:{bc};font-size:10px;font-weight:bold;"
            f"border:1px solid {bc};border-radius:8px;padding:2px 7px;")
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter); layout.addWidget(badge)

        self.setStyleSheet(
            f"QFrame{{border:1px solid {_p('border')};border-radius:6px;"
            f"background-color:{_p('header_bg')};}}"
            f"QFrame:hover{{border-color:{_p('muted')};"
            f"background-color:{_p('surface')};}}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  DayEventRow
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class DayEventRow(QFrame):
    edit_requested = pyqtSignal(object)

    def __init__(self, event: Event, parent=None):
        super().__init__(parent)
        self.event = event
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0,0,0,0); layout.setSpacing(0)

        bar = QFrame(); bar.setFixedWidth(4)
        bar.setStyleSheet(f"background-color:{event.color};border-radius:2px 0 0 2px;")
        layout.addWidget(bar)

        body = QWidget(); bl = QHBoxLayout(body)
        bl.setContentsMargins(8,6,8,6); bl.setSpacing(8)

        if not event.all_day:
            try: t = datetime.fromisoformat(event.start_time).strftime("%H:%M")
            except Exception: t=""
            tl = QLabel(t)
            tl.setStyleSheet(f"font-size:11px;color:{_p('muted')};min-width:38px;")
            bl.addWidget(tl)

        emoji = _cat_emoji(event.category)
        display = f"{emoji} {event.title}" if emoji else event.title
        tl2 = QLabel(display)
        tl2.setStyleSheet(f"font-size:13px;color:{_p('fg')};")
        tl2.setWordWrap(True); bl.addWidget(tl2,1)

        if event.recurrence:
            rl=QLabel("↻")
            rl.setStyleSheet(f"color:{_p('muted')};font-size:14px;")
            rl.setToolTip("Recurring event"); bl.addWidget(rl)

        layout.addWidget(body,1)
        self.setStyleSheet(
            f"QFrame{{border:1px solid {_p('border')};border-radius:4px;"
            f"background-color:{_p('header_bg')};}}"
            f"QFrame:hover{{border-color:{_p('muted')};"
            f"background-color:{_p('surface')};}}")

    def mouseDoubleClickEvent(self, ev): self.edit_requested.emit(self.event)
    def mousePressEvent(self, ev): pass


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  CalendarPanel — main widget
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class CalendarPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.store = CalendarStore()
        self._selected_date = date.today()
        self._build_ui(); self._refresh()
        self._auto_timer = QTimer(self)
        self._auto_timer.setInterval(60_000)
        self._auto_timer.timeout.connect(self._refresh)
        self._auto_timer.start()

    # ── Palette ─────────────────────────────────────

    def set_palette(self, palette: dict):
        global _PALETTE
        _PALETTE = palette
        # Update static structural labels/dividers built once in _build_ui
        self._week_label.setStyleSheet(
            f"font-size:13px;font-weight:bold;color:{_p('muted')};")
        self._left_div.setStyleSheet(
            f"border:none;border-top:1px solid {_p('border')};margin:8px 0;")
        self._mini_frame.setStyleSheet(
            f"#miniMonthFrame{{border:1px solid {_p('border')};"
            f"border-radius:8px;background-color:{_p('header_bg')};}}")
        self._major_count_lbl.setStyleSheet(f"font-size:10px;color:{_p('muted')};")
        self.mini_month.refresh_styles()
        self._refresh()

    # ── Build UI ────────────────────────────────────

    def _build_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(0,0,0,0); root.setSpacing(0)

        # Left column
        left = QWidget()
        left_l = QVBoxLayout(left)
        left_l.setContentsMargins(14,10,8,10); left_l.setSpacing(0)

        top_bar = QHBoxLayout(); top_bar.setSpacing(6)
        title = QLabel("Calendar"); title.setObjectName("sectionTitle")
        top_bar.addWidget(title); top_bar.addStretch()

        self._week_label = QLabel()
        self._week_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._week_label.setStyleSheet(f"font-size:13px;font-weight:bold;color:{_p('muted')};")
        top_bar.addWidget(self._week_label); top_bar.addSpacing(8)

        for text, tip, slot in [("‹","Previous week",self._prev_week),
                                  ("›","Next week",   self._next_week)]:
            if text == "›": top_bar.addWidget(self._today_btn())
            btn = QPushButton(text); btn.setObjectName("secondary")
            btn.setFixedSize(28,28); btn.setToolTip(tip); btn.clicked.connect(slot)
            top_bar.addWidget(btn)

        top_bar.addSpacing(8)
        btn_add = QPushButton("＋ Event"); btn_add.clicked.connect(self._add_event)
        top_bar.addWidget(btn_add)
        left_l.addLayout(top_bar); left_l.addSpacing(8)

        self._week_container = QWidget()
        self._week_grid = QHBoxLayout(self._week_container)
        self._week_grid.setSpacing(0); self._week_grid.setContentsMargins(0,0,0,0)
        week_scroll = QScrollArea()
        week_scroll.setWidgetResizable(True); week_scroll.setWidget(self._week_container)
        week_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        week_scroll.setMinimumHeight(220); week_scroll.setMaximumHeight(340)
        week_scroll.setFrameShape(QFrame.Shape.NoFrame)
        left_l.addWidget(week_scroll, 3)

        self._left_div = QFrame(); self._left_div.setFrameShape(QFrame.Shape.HLine)
        self._left_div.setStyleSheet(
            f"border:none;border-top:1px solid {_p('border')};margin:8px 0;")
        left_l.addWidget(self._left_div)

        detail_bar = QHBoxLayout()
        self._day_title = QLabel("Today")
        self._day_title.setStyleSheet("font-size:14px;font-weight:bold;")
        detail_bar.addWidget(self._day_title); detail_bar.addStretch()
        btn_add_here = QPushButton("＋"); btn_add_here.setObjectName("secondary")
        btn_add_here.setFixedSize(26,26); btn_add_here.setToolTip("Add event on this day")
        btn_add_here.clicked.connect(lambda: self._add_event_on_date(self._selected_date))
        detail_bar.addWidget(btn_add_here); left_l.addLayout(detail_bar)
        left_l.addSpacing(4)

        self._day_list_layout = QVBoxLayout(); self._day_list_layout.setSpacing(4)
        day_list_w = QWidget(); day_list_w.setLayout(self._day_list_layout)
        day_scroll = QScrollArea(); day_scroll.setWidgetResizable(True)
        day_scroll.setWidget(day_list_w)
        day_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        day_scroll.setFrameShape(QFrame.Shape.NoFrame)
        left_l.addWidget(day_scroll,2)
        root.addWidget(left,1)

        # Right sidebar
        right = QWidget(); right.setFixedWidth(258)
        right_l = QVBoxLayout(right)
        right_l.setContentsMargins(0,10,12,10); right_l.setSpacing(0)

        self._mini_frame = QFrame(); self._mini_frame.setObjectName("miniMonthFrame")
        self._mini_frame.setStyleSheet(
            f"#miniMonthFrame{{border:1px solid {_p('border')};"
            f"border-radius:8px;background-color:{_p('header_bg')};}}")
        mf_l = QVBoxLayout(self._mini_frame); mf_l.setContentsMargins(0,0,0,0)
        self.mini_month = MiniMonth()
        self.mini_month.date_selected.connect(self._on_mini_date_selected)
        mf_l.addWidget(self.mini_month); right_l.addWidget(self._mini_frame)
        right_l.addSpacing(8)

        action_row = QHBoxLayout(); action_row.setSpacing(4)
        btn_bday = QPushButton("🎂 Birthdays"); btn_bday.setObjectName("secondary")
        btn_bday.clicked.connect(self._manage_birthdays); action_row.addWidget(btn_bday)
        btn_jump = QPushButton("Go to date…"); btn_jump.setObjectName("secondary")
        btn_jump.clicked.connect(self._jump_to_date); action_row.addWidget(btn_jump)
        right_l.addLayout(action_row); right_l.addSpacing(8)

        rdiv1 = QFrame(); rdiv1.setFrameShape(QFrame.Shape.HLine)
        rdiv1.setStyleSheet(f"border:none;border-top:1px solid {_p('border')};")
        right_l.addWidget(rdiv1); right_l.addSpacing(8)

        major_hdr = QHBoxLayout()
        major_title = QLabel("Upcoming Events")
        major_title.setStyleSheet("font-size:13px;font-weight:bold;")
        major_hdr.addWidget(major_title); major_hdr.addStretch()
        self._major_count_lbl = QLabel("")
        self._major_count_lbl.setStyleSheet(f"font-size:10px;color:{_p('muted')};")
        major_hdr.addWidget(self._major_count_lbl); right_l.addLayout(major_hdr)
        right_l.addSpacing(6)

        self._major_list_layout = QVBoxLayout(); self._major_list_layout.setSpacing(5)
        major_list_w = QWidget(); major_list_w.setLayout(self._major_list_layout)
        major_scroll = QScrollArea(); major_scroll.setWidgetResizable(True)
        major_scroll.setWidget(major_list_w)
        major_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        major_scroll.setFrameShape(QFrame.Shape.NoFrame)
        right_l.addWidget(major_scroll,1)
        root.addWidget(right)

    def _today_btn(self) -> QPushButton:
        btn = QPushButton("Today"); btn.setObjectName("secondary")
        btn.setFixedHeight(28); btn.clicked.connect(self._go_today)
        return btn

    # ── Refresh ─────────────────────────────────────

    def _refresh(self):
        self._render_week(); self._render_day_detail()
        self._render_major_events(); self._update_mini_month_events()

    def _get_week_start(self) -> date:
        d = self._selected_date; return d - timedelta(days=d.weekday())

    def _render_week(self):
        _clear_layout(self._week_grid)
        ws = self._get_week_start(); we = ws + timedelta(days=6)
        self._week_label.setText(
            f"{ws.strftime('%b %d')} – {we.strftime('%b %d, %Y')}")

        events = self.store.get_events(ws.isoformat(), we.isoformat()+"T23:59:59")
        ebd: dict[date,list[Event]] = {}
        for ev in events:
            try: d=datetime.fromisoformat(ev.start_time).date()
            except Exception: continue
            ebd.setdefault(d,[]).append(ev)
        for ev in self.store.get_all_recurring_events():
            for occ in expand_recurring_to_range(ev,ws,we):
                if ev not in ebd.get(occ,[]): ebd.setdefault(occ,[]).append(ev)

        bbd: dict[date,list[Birthday]] = {}
        for b in self.store.get_birthdays():
            try: bd=date(ws.year,b.month,b.day)
            except ValueError: continue
            if ws<=bd<=we: bbd.setdefault(bd,[]).append(b)

        today = date.today()
        for i in range(7):
            d = ws+timedelta(days=i)
            if i>0:
                sep=QFrame(); sep.setFrameShape(QFrame.Shape.VLine)
                sep.setStyleSheet(f"border:none;border-left:1px solid {_p('border')};")
                self._week_grid.addWidget(sep)
            col = DayColumn(d, ebd.get(d,[]), bbd.get(d,[]),
                            is_today=(d==today), is_selected=(d==self._selected_date))
            col.request_add.connect(self._add_event_on_date)
            col.request_edit.connect(self._edit_event)
            self._week_grid.addWidget(col,1)

    def _render_day_detail(self):
        _clear_layout(self._day_list_layout)
        d=self._selected_date; today=date.today()
        if   d==today:               hdr=f"Today  ·  {d.strftime('%A, %B %d')}"
        elif d==today+timedelta(1):  hdr=f"Tomorrow  ·  {d.strftime('%A, %B %d')}"
        elif d==today-timedelta(1):  hdr=f"Yesterday  ·  {d.strftime('%A, %B %d')}"
        else:                        hdr=d.strftime("%A, %B %d, %Y")
        self._day_title.setText(hdr)

        events=self.store.get_events(d.isoformat(),d.isoformat()+"T23:59:59")
        for ev in self.store.get_all_recurring_events():
            if expand_recurring_to_range(ev,d,d) and ev not in events:
                events.append(ev)

        bday_evs: list[Event]=[]
        for b in self.store.get_birthdays():
            if b.month==d.month and b.day==d.day:
                age=(d.year-b.year) if b.year else None
                age_str=f" (turns {age})" if age else ""
                bday_evs.append(Event(id=b.id, title=f"🎂 {b.name}{age_str}",
                    start_time=datetime(d.year,d.month,d.day).isoformat(),
                    all_day=True, color=_p("red"), category="birthday"))

        all_evs=sorted(bday_evs+events,
                       key=lambda e:(0 if e.all_day else 1, e.start_time))
        if not all_evs:
            lbl=QLabel("No events — double-click a day to add one")
            lbl.setStyleSheet(f"color:{_p('muted')};font-size:12px;padding:8px 0;")
            self._day_list_layout.addWidget(lbl)
        else:
            for ev in all_evs:
                row=DayEventRow(ev); row.edit_requested.connect(self._edit_event)
                self._day_list_layout.addWidget(row)
        self._day_list_layout.addStretch()

    def _render_major_events(self):
        _clear_layout(self._major_list_layout)
        majors=self.store.get_next_major_events(date.today(),limit=8)
        if not majors:
            lbl=QLabel("No upcoming major events")
            lbl.setStyleSheet(f"color:{_p('muted')};font-size:12px;padding:8px 0;")
            lbl.setWordWrap(True); self._major_list_layout.addWidget(lbl)
            self._major_count_lbl.setText("")
        else:
            self._major_count_lbl.setText(f"{len(majors)} upcoming")
            for ev_date,title,category,color in majors:
                self._major_list_layout.addWidget(
                    MajorEventCard(ev_date,title,category,color))
        self._major_list_layout.addStretch()

    def _update_mini_month_events(self):
        vy,vm=self.mini_month._view_year,self.mini_month._view_month
        first=date(vy,vm,1)
        last=date(vy+(vm==12), 1 if vm==12 else vm+1, 1)-timedelta(days=1)
        by_date: dict[date,list[str]]={}
        for ev in self.store.get_events(first.isoformat(),last.isoformat()+"T23:59:59"):
            try: d=datetime.fromisoformat(ev.start_time).date()
            except Exception: continue
            by_date.setdefault(d,[]).append(ev.color)
        for ev in self.store.get_all_recurring_events():
            for occ in expand_recurring_to_range(ev,first,last):
                by_date.setdefault(occ,[]).append(ev.color)
        for b in self.store.get_birthdays():
            if b.month==vm:
                try:
                    d=date(vy,b.month,b.day)
                    if first<=d<=last: by_date.setdefault(d,[]).append(_p("red"))
                except ValueError: pass
        self.mini_month.set_events(by_date)
        try:
            from src.data.holidays_jp import get_japanese_holidays
            hset={d for d in get_japanese_holidays(vy) if first<=d<=last}
            self.mini_month.set_holidays(hset)
        except Exception: pass

    # ── Navigation ──────────────────────────────────

    def _prev_week(self):
        self._selected_date-=timedelta(weeks=1)
        self.mini_month.set_selected(self._selected_date); self._refresh()

    def _next_week(self):
        self._selected_date+=timedelta(weeks=1)
        self.mini_month.set_selected(self._selected_date); self._refresh()

    def _go_today(self):
        self._selected_date=date.today()
        self.mini_month.set_selected(self._selected_date); self._refresh()

    def _on_mini_date_selected(self,d:date):
        self._selected_date=d
        self._update_mini_month_events(); self._render_week(); self._render_day_detail()

    def _jump_to_date(self):
        dlg=QDialog(self); dlg.setWindowTitle("Go to date"); dlg.setModal(True)
        layout=QVBoxLayout(dlg); layout.addWidget(QLabel("Jump to date:"))
        de=QDateEdit(); de.setCalendarPopup(True); de.setDisplayFormat("dd MMM yyyy")
        sd=self._selected_date; de.setDate(QDate(sd.year,sd.month,sd.day))
        layout.addWidget(de)
        br=QHBoxLayout()
        cancel=QPushButton("Cancel"); cancel.setObjectName("secondary"); cancel.clicked.connect(dlg.reject)
        go=QPushButton("Go"); go.setDefault(True); go.clicked.connect(dlg.accept)
        br.addStretch(); br.addWidget(cancel); br.addWidget(go); layout.addLayout(br)
        if dlg.exec():
            qd=de.date(); self._selected_date=date(qd.year(),qd.month(),qd.day())
            self.mini_month.set_selected(self._selected_date); self._refresh()

    # ── Event CRUD ───────────────────────────────────

    def _add_event(self): self._add_event_on_date(self._selected_date)

    def _add_event_on_date(self,d:date):
        dlg=EventDialog(self,prefill_date=d)
        if dlg.exec(): self.store.add_event(**dlg.get_data()); self._refresh()

    def _edit_event(self,event:Event):
        dlg=EventDialog(self,event=event); result=dlg.exec()
        if dlg._delete_requested:
            if QMessageBox.question(
                self,"Delete Event",f'Delete "{event.title}"?',
                QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No,
            )==QMessageBox.StandardButton.Yes:
                self.store.delete_event(event.id); self._refresh()
        elif result:
            data=dlg.get_data()
            event.title=data["title"]; event.description=data["description"]
            event.start_time=data["start_time"]; event.end_time=data["end_time"]
            event.all_day=data["all_day"]; event.color=data["color"]
            event.category=data["category"]; event.recurrence=data["recurrence"]
            self.store.update_event(event); self._refresh()

    def _manage_birthdays(self):
        BirthdayManagerDialog(self,self.store).exec(); self._refresh()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  BirthdayManagerDialog
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class BirthdayManagerDialog(QDialog):
    def __init__(self,parent,store:CalendarStore):
        super().__init__(parent); self.store=store
        self.setWindowTitle("Birthday Manager")
        self.setMinimumSize(400,460); self.setModal(True)
        self._build_ui(); self._load()

    def _build_ui(self):
        layout=QVBoxLayout(self); layout.setContentsMargins(16,16,16,16); layout.setSpacing(10)
        hdr=QHBoxLayout(); title=QLabel("🎂  Birthdays")
        title.setStyleSheet("font-size:16px;font-weight:bold;"); hdr.addWidget(title)
        hdr.addStretch(); add_btn=QPushButton("＋ Add"); add_btn.clicked.connect(self._add_birthday)
        hdr.addWidget(add_btn); layout.addLayout(hdr)
        self._search=QLineEdit(); self._search.setPlaceholderText("Search by name…")
        self._search.textChanged.connect(self._filter); layout.addWidget(self._search)
        self._list_widget=QWidget(); self._list_layout=QVBoxLayout(self._list_widget)
        self._list_layout.setSpacing(4); self._list_layout.setContentsMargins(0,0,0,0)
        scroll=QScrollArea(); scroll.setWidgetResizable(True)
        scroll.setWidget(self._list_widget); scroll.setFrameShape(QFrame.Shape.NoFrame)
        layout.addWidget(scroll,1)
        close_btn=QPushButton("Close"); close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn,0,Qt.AlignmentFlag.AlignRight)

    def _load(self):
        self._birthdays=self.store.get_birthdays(); self._filter(self._search.text())

    def _filter(self,text:str):
        _clear_layout(self._list_layout); q=text.lower(); today=date.today()
        filtered=[b for b in self._birthdays if q in b.name.lower()]
        def sk(b):
            try:
                c=date(today.year,b.month,b.day)
                if c<today: c=date(today.year+1,b.month,b.day)
                return (c-today).days
            except ValueError: return 9999
        filtered.sort(key=sk)
        if not filtered:
            self._list_layout.addWidget(
                QLabel("No birthdays yet — add one!" if not text else "No matches"))
        for b in filtered: self._list_layout.addWidget(self._make_row(b))
        self._list_layout.addStretch()

    def _make_row(self,b:Birthday)->QFrame:
        row=QFrame()
        row.setStyleSheet(
            f"QFrame{{border:1px solid {_p('border')};border-radius:6px;"
            f"background-color:{_p('header_bg')};padding:2px;}}")
        rl=QHBoxLayout(row); rl.setContentsMargins(10,6,10,6); rl.setSpacing(8)
        cake=QLabel("🎂"); cake.setStyleSheet("font-size:18px;"); cake.setFixedWidth(24)
        rl.addWidget(cake)
        info=QVBoxLayout(); info.setSpacing(1)
        name_lbl=QLabel(b.name)
        name_lbl.setStyleSheet(f"font-size:13px;font-weight:bold;color:{_p('fg')};")
        info.addWidget(name_lbl)
        today=date.today()
        try:
            nb=date(today.year,b.month,b.day)
            if nb<today: nb=date(today.year+1,b.month,b.day)
            suffix=f"  ·  {(nb-today).days}d away" if (nb-today).days>0 else "  ·  Today! 🎉"
        except ValueError: suffix=""
        months=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        ds=f"{months[b.month-1]} {b.day}"
        if b.year: ds+=f", {b.year}  (turns {today.year-b.year})"
        ds+=suffix
        dl=QLabel(ds); dl.setStyleSheet(f"font-size:11px;color:{_p('muted')};")
        info.addWidget(dl); rl.addLayout(info,1)
        edit_btn=QPushButton("Edit"); edit_btn.setObjectName("secondary")
        edit_btn.setFixedHeight(26)
        edit_btn.clicked.connect(lambda _,bd=b: self._edit_birthday(bd))
        rl.addWidget(edit_btn); return row

    def _add_birthday(self):
        dlg=BirthdayDialog(self)
        if dlg.exec(): self.store.add_birthday(**dlg.get_data()); self._load()

    def _edit_birthday(self,birthday:Birthday):
        dlg=BirthdayDialog(self,birthday); result=dlg.exec()
        if dlg._delete_requested:
            if QMessageBox.question(self,"Delete Birthday",
                f"Remove birthday for {birthday.name}?",
                QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No,
            )==QMessageBox.StandardButton.Yes:
                self.store.delete_birthday(birthday.id); self._load()
        elif result:
            data=dlg.get_data(); birthday.name=data["name"]
            birthday.month=data["month"]; birthday.day=data["day"]; birthday.year=data["year"]
            self.store.update_birthday(birthday); self._load()