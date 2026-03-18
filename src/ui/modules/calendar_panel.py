"""Calendar module UI — weekly main view + mini month navigator + colored dot indicators."""

from datetime import date, datetime, timedelta
import calendar

from PyQt6.QtCore import Qt, QDate, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QDialog, QLineEdit, QTextEdit,
    QDateEdit, QTimeEdit, QCheckBox, QFrame, QComboBox,
    QMessageBox, QScrollArea, QSizePolicy,
)

from src.data.calendar_store import CalendarStore, Event


# ── Event colors ──────────────────────────────────────
EVENT_COLORS = {
    "Blue": "#4a9eff", "Green": "#a6e3a1", "Red": "#f38ba8",
    "Yellow": "#f9e2af", "Purple": "#cba6f7", "Orange": "#fab387",
    "Teal": "#94e2d5", "Pink": "#f5c2e7",
}


class EventDialog(QDialog):
    """Dialog to add/edit an event."""

    def __init__(self, parent=None, event=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Event" if event else "New Event")
        self.setMinimumWidth(380)
        self.event = event
        self._delete_requested = False
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        layout.addWidget(QLabel("Title"))
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Event title...")
        if self.event:
            self.title_edit.setText(self.event.title)
        layout.addWidget(self.title_edit)

        layout.addWidget(QLabel("Description"))
        self.desc_edit = QTextEdit()
        self.desc_edit.setMaximumHeight(80)
        self.desc_edit.setPlaceholderText("Optional description...")
        if self.event:
            self.desc_edit.setPlainText(self.event.description)
        layout.addWidget(self.desc_edit)

        self.all_day_check = QCheckBox("All day event")
        if self.event:
            self.all_day_check.setChecked(self.event.all_day)
        self.all_day_check.toggled.connect(self._toggle_time)
        layout.addWidget(self.all_day_check)

        date_row = QHBoxLayout()
        date_row.addWidget(QLabel("Date"))
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        if self.event:
            dt = datetime.fromisoformat(self.event.start_time)
            self.date_edit.setDate(QDate(dt.year, dt.month, dt.day))
        else:
            today = date.today()
            self.date_edit.setDate(QDate(today.year, today.month, today.day))
        date_row.addWidget(self.date_edit, 1)
        layout.addLayout(date_row)

        from PyQt6.QtCore import QTime
        time_row = QHBoxLayout()
        time_row.addWidget(QLabel("Start"))
        self.start_time = QTimeEdit()
        self.start_time.setDisplayFormat("HH:mm")
        if self.event and not self.event.all_day:
            dt = datetime.fromisoformat(self.event.start_time)
            self.start_time.setTime(QTime(dt.hour, dt.minute))
        else:
            self.start_time.setTime(QTime(9, 0))
        time_row.addWidget(self.start_time, 1)
        time_row.addWidget(QLabel("End"))
        self.end_time = QTimeEdit()
        self.end_time.setDisplayFormat("HH:mm")
        if self.event and self.event.end_time:
            dt = datetime.fromisoformat(self.event.end_time)
            self.end_time.setTime(QTime(dt.hour, dt.minute))
        else:
            self.end_time.setTime(QTime(10, 0))
        time_row.addWidget(self.end_time, 1)
        layout.addLayout(time_row)
        self.time_widgets = [self.start_time, self.end_time]
        self._toggle_time(self.all_day_check.isChecked())

        layout.addWidget(QLabel("Color"))
        self.color_combo = QComboBox()
        for name, hex_val in EVENT_COLORS.items():
            self.color_combo.addItem(name, hex_val)
        if self.event:
            idx = self.color_combo.findData(self.event.color)
            if idx >= 0:
                self.color_combo.setCurrentIndex(idx)
        layout.addWidget(self.color_combo)

        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(sep)

        btn_row = QHBoxLayout()
        if self.event:
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
        save_btn.clicked.connect(self.accept)
        btn_row.addWidget(save_btn)
        layout.addLayout(btn_row)

    def _toggle_time(self, all_day: bool):
        for w in self.time_widgets:
            w.setEnabled(not all_day)

    def _on_delete(self):
        self._delete_requested = True
        self.reject()

    def get_data(self) -> dict:
        qd = self.date_edit.date()
        d = date(qd.year(), qd.month(), qd.day())
        if self.all_day_check.isChecked():
            start = datetime(d.year, d.month, d.day).isoformat()
            end = None
        else:
            st = self.start_time.time()
            et = self.end_time.time()
            start = datetime(d.year, d.month, d.day, st.hour(), st.minute()).isoformat()
            end = datetime(d.year, d.month, d.day, et.hour(), et.minute()).isoformat()
        return {
            "title": self.title_edit.text().strip() or "Untitled",
            "description": self.desc_edit.toPlainText(),
            "start_time": start, "end_time": end,
            "all_day": self.all_day_check.isChecked(),
            "color": self.color_combo.currentData(),
        }


# ── Mini month calendar (for navigation) ──────────────

class MiniMonthCell(QLabel):
    """A single day number in the mini calendar."""
    clicked = pyqtSignal(int, int, int)  # year, month, day

    def __init__(self, year: int, month: int, day: int, is_today: bool,
                 is_selected: bool, has_events: bool, event_colors: list):
        super().__init__(str(day))
        self.year, self.month, self.day = year, month, day
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedSize(28, 28)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        style = "font-size: 11px; border-radius: 14px; "
        if is_today:
            style += "background-color: #4a9eff; color: #1e1e2e; font-weight: bold; "
        elif is_selected:
            style += "border: 1px solid #4a9eff; "

        self.setStyleSheet(style)

        # Colored dots for events
        if has_events and not is_today:
            dots = " ".join(
                f'<span style="color:{c};">\u2022</span>'
                for c in event_colors[:3]
            )
            self.setToolTip(f"{len(event_colors)} event(s)")
            # We'll add dots below via the parent layout
            self._dot_colors = event_colors[:3]
        else:
            self._dot_colors = []

    def mousePressEvent(self, ev):
        self.clicked.emit(self.year, self.month, self.day)


class MiniMonth(QWidget):
    """Compact month grid for date navigation."""
    date_selected = pyqtSignal(object)  # emits a date object

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(230)
        self._selected_date = date.today()
        self._view_year = date.today().year
        self._view_month = date.today().month
        self._events_by_date: dict[date, list] = {}
        self._build()

    def set_events(self, events_by_date: dict):
        self._events_by_date = events_by_date
        self._render()

    def set_selected(self, d: date):
        self._selected_date = d
        self._view_year = d.year
        self._view_month = d.month
        self._render()

    def _build(self):
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(8, 8, 8, 8)
        self._layout.setSpacing(4)

        # Header row
        header = QHBoxLayout()
        self._prev_btn = QPushButton("\u25c0")
        self._prev_btn.setObjectName("secondary")
        self._prev_btn.setFixedSize(24, 24)
        self._prev_btn.clicked.connect(self._prev_month)
        header.addWidget(self._prev_btn)

        self._title = QLabel()
        self._title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._title.setStyleSheet("font-weight: bold; font-size: 13px;")
        header.addWidget(self._title, 1)

        self._next_btn = QPushButton("\u25b6")
        self._next_btn.setObjectName("secondary")
        self._next_btn.setFixedSize(24, 24)
        self._next_btn.clicked.connect(self._next_month)
        header.addWidget(self._next_btn)

        self._layout.addLayout(header)

        # Day-of-week header
        dow_row = QHBoxLayout()
        dow_row.setSpacing(0)
        for d in ["M", "T", "W", "T", "F", "S", "S"]:
            lbl = QLabel(d)
            lbl.setFixedSize(28, 18)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setObjectName("subtitle")
            lbl.setStyleSheet("font-size: 10px; font-weight: bold;")
            dow_row.addWidget(lbl)
        self._layout.addLayout(dow_row)

        # Grid placeholder
        self._grid_widget = QWidget()
        self._grid = QGridLayout(self._grid_widget)
        self._grid.setSpacing(1)
        self._grid.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self._grid_widget)

        self._layout.addStretch()
        self._render()

    def _render(self):
        # Clear grid
        while self._grid.count():
            child = self._grid.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self._title.setText(f"{calendar.month_abbr[self._view_month]} {self._view_year}")

        today = date.today()
        cal = calendar.Calendar(firstweekday=0)
        weeks = cal.monthdayscalendar(self._view_year, self._view_month)

        for row, week in enumerate(weeks):
            for col, day in enumerate(week):
                if day == 0:
                    spacer = QLabel("")
                    spacer.setFixedSize(28, 28)
                    self._grid.addWidget(spacer, row, col)
                else:
                    d = date(self._view_year, self._view_month, day)
                    is_today = (d == today)
                    is_selected = (d == self._selected_date)
                    day_events = self._events_by_date.get(d, [])
                    event_colors = [ev.color for ev in day_events]

                    cell = MiniMonthCell(
                        self._view_year, self._view_month, day,
                        is_today, is_selected, bool(day_events), event_colors,
                    )
                    cell.clicked.connect(self._on_cell_click)
                    self._grid.addWidget(cell, row, col)

                    # Add dot row below if events
                    if event_colors:
                        dot_label = QLabel(
                            " ".join(f'<span style="color:{c};">\u2022</span>'
                                     for c in event_colors[:3])
                        )
                        dot_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        dot_label.setFixedHeight(8)
                        dot_label.setStyleSheet("font-size: 8px;")
                        # We'll overlay it — for simplicity just add tooltips

    def _on_cell_click(self, y, m, d):
        self._selected_date = date(y, m, d)
        self._render()
        self.date_selected.emit(self._selected_date)

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


# ── Weekly view (main content) ─────────────────────────

class WeekEventWidget(QFrame):
    """A single event rendered in the weekly time grid."""

    def __init__(self, event: Event, parent_panel):
        super().__init__()
        self.event = event
        self.parent_panel = parent_panel
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 3, 6, 3)
        layout.setSpacing(6)

        # Color dot
        dot = QLabel("\u25cf")
        dot.setStyleSheet(f"color: {event.color}; font-size: 14px;")
        dot.setFixedWidth(16)
        layout.addWidget(dot)

        # Time + title
        info_layout = QVBoxLayout()
        info_layout.setSpacing(0)
        info_layout.setContentsMargins(0, 0, 0, 0)

        if not event.all_day:
            try:
                dt = datetime.fromisoformat(event.start_time)
                time_str = dt.strftime("%H:%M")
                if event.end_time:
                    et = datetime.fromisoformat(event.end_time)
                    time_str += f" - {et.strftime('%H:%M')}"
            except Exception:
                time_str = ""
            if time_str:
                time_label = QLabel(time_str)
                time_label.setObjectName("subtitle")
                time_label.setStyleSheet("font-size: 11px;")
                info_layout.addWidget(time_label)

        title_label = QLabel(event.title)
        title_label.setStyleSheet("font-weight: bold; font-size: 13px;")
        title_label.setWordWrap(True)
        info_layout.addWidget(title_label)

        if event.description:
            desc = QLabel(event.description[:60])
            desc.setObjectName("subtitle")
            desc.setStyleSheet("font-size: 11px;")
            desc.setWordWrap(True)
            info_layout.addWidget(desc)

        layout.addLayout(info_layout, 1)

        self.setStyleSheet(
            f"WeekEventWidget {{ border-left: 3px solid {event.color}; "
            f"border-radius: 4px; padding: 2px; }}"
        )
        self.setToolTip(
            f"{event.title}\n{event.start_time}"
            + (f" - {event.end_time}" if event.end_time else "")
            + (f"\n{event.description}" if event.description else "")
        )

    def mouseDoubleClickEvent(self, ev):
        self.parent_panel._edit_event(self.event)


class DayColumn(QWidget):
    """A single day column in the weekly view."""

    def __init__(self, d: date, events: list, is_today: bool, parent_panel):
        super().__init__()
        self.d = d
        self.parent_panel = parent_panel
        # Fixed equal-width policy — prevents long text from stretching a column
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)

        # Day header
        day_name = d.strftime("%a")
        day_num = str(d.day)
        header = QLabel(f"{day_name}\n{day_num}")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if is_today:
            header.setStyleSheet(
                "background-color: #4a9eff; color: #1e1e2e; "
                "border-radius: 8px; padding: 4px; font-weight: bold; font-size: 13px;"
            )
        else:
            header.setStyleSheet("font-size: 13px; padding: 4px;")
        layout.addWidget(header)

        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(sep)

        # Events sorted by time
        sorted_events = sorted(events, key=lambda e: e.start_time)

        # All-day events first
        for ev in sorted_events:
            if ev.all_day:
                w = WeekEventWidget(ev, parent_panel)
                layout.addWidget(w)

        # Timed events
        for ev in sorted_events:
            if not ev.all_day:
                w = WeekEventWidget(ev, parent_panel)
                layout.addWidget(w)

        layout.addStretch()

        # Double-click empty space to add event
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mouseDoubleClickEvent(self, ev):
        self.parent_panel._add_event_on_day_date(self.d)


# ── Main calendar panel ───────────────────────────────

class CalendarPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.store = CalendarStore()
        self._selected_date = date.today()
        self._palette = {}
        self._build_ui()
        self._refresh()

    def set_palette(self, palette: dict):
        self._palette = palette

    def _build_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ── Main area: weekly view ────────────────────
        main_area = QWidget()
        main_layout = QVBoxLayout(main_area)
        main_layout.setContentsMargins(16, 12, 8, 12)
        main_layout.setSpacing(8)

        # Week header
        week_header = QHBoxLayout()
        title = QLabel("Calendar")
        title.setObjectName("sectionTitle")
        week_header.addWidget(title)
        week_header.addStretch()

        self.btn_prev_week = QPushButton("\u25c0 Prev")
        self.btn_prev_week.setObjectName("secondary")
        self.btn_prev_week.clicked.connect(self._prev_week)
        week_header.addWidget(self.btn_prev_week)

        self.week_label = QLabel()
        self.week_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.week_label.setMinimumWidth(200)
        self.week_label.setStyleSheet("font-size: 15px; font-weight: bold;")
        week_header.addWidget(self.week_label)

        self.btn_next_week = QPushButton("Next \u25b6")
        self.btn_next_week.setObjectName("secondary")
        self.btn_next_week.clicked.connect(self._next_week)
        week_header.addWidget(self.btn_next_week)

        btn_today = QPushButton("Today")
        btn_today.setObjectName("secondary")
        btn_today.clicked.connect(self._go_today)
        week_header.addWidget(btn_today)

        btn_add = QPushButton("+ Event")
        btn_add.clicked.connect(self._add_event)
        week_header.addWidget(btn_add)

        main_layout.addLayout(week_header)

        # Week grid
        self._week_container = QWidget()
        self._week_grid = QHBoxLayout(self._week_container)
        self._week_grid.setSpacing(2)
        self._week_grid.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self._week_container)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        main_layout.addWidget(scroll, 1)

        layout.addWidget(main_area, 1)

        # ── Right sidebar: mini month + day detail ────
        right_sidebar = QWidget()
        right_sidebar.setFixedWidth(250)
        right_layout = QVBoxLayout(right_sidebar)
        right_layout.setContentsMargins(8, 12, 12, 12)
        right_layout.setSpacing(8)

        self.mini_month = MiniMonth()
        self.mini_month.date_selected.connect(self._on_mini_date_selected)
        right_layout.addWidget(self.mini_month)

        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine)
        right_layout.addWidget(sep)

        # Day detail panel
        self.day_detail_title = QLabel("Today")
        self.day_detail_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        right_layout.addWidget(self.day_detail_title)

        self.day_event_list = QVBoxLayout()
        self.day_event_list.setSpacing(4)
        day_list_widget = QWidget()
        day_list_widget.setLayout(self.day_event_list)

        day_scroll = QScrollArea()
        day_scroll.setWidgetResizable(True)
        day_scroll.setWidget(day_list_widget)
        day_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        right_layout.addWidget(day_scroll, 1)

        layout.addWidget(right_sidebar)

    def _refresh(self):
        self._render_week()
        self._render_day_detail()
        self._update_mini_month_events()

    def _get_week_start(self) -> date:
        """Monday of the selected week."""
        d = self._selected_date
        return d - timedelta(days=d.weekday())

    def _render_week(self):
        # Clear
        while self._week_grid.count():
            child = self._week_grid.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        week_start = self._get_week_start()
        week_end = week_start + timedelta(days=6)
        self.week_label.setText(
            f"{week_start.strftime('%b %d')} - {week_end.strftime('%b %d, %Y')}"
        )

        events = self.store.get_events(
            week_start.isoformat(),
            week_end.isoformat() + "T23:59:59",
        )

        events_by_date: dict[date, list] = {}
        for ev in events:
            d = datetime.fromisoformat(ev.start_time).date()
            events_by_date.setdefault(d, []).append(ev)

        today = date.today()
        for i in range(7):
            d = week_start + timedelta(days=i)
            day_events = events_by_date.get(d, [])
            col = DayColumn(d, day_events, d == today, self)
            self._week_grid.addWidget(col, 1)

    def _render_day_detail(self):
        # Clear
        while self.day_event_list.count():
            child = self.day_event_list.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        d = self._selected_date
        self.day_detail_title.setText(d.strftime("%A, %B %d"))

        events = self.store.get_events(
            d.isoformat(), d.isoformat() + "T23:59:59",
        )

        if not events:
            lbl = QLabel("No events")
            lbl.setObjectName("subtitle")
            self.day_event_list.addWidget(lbl)
        else:
            for ev in sorted(events, key=lambda e: e.start_time):
                row = QHBoxLayout()
                dot = QLabel("\u25cf")
                dot.setStyleSheet(f"color: {ev.color}; font-size: 12px;")
                dot.setFixedWidth(14)
                row.addWidget(dot)

                if not ev.all_day:
                    try:
                        t = datetime.fromisoformat(ev.start_time).strftime("%H:%M")
                    except Exception:
                        t = ""
                    time_lbl = QLabel(t)
                    time_lbl.setObjectName("subtitle")
                    time_lbl.setFixedWidth(42)
                    row.addWidget(time_lbl)

                title_lbl = QLabel(ev.title)
                title_lbl.setStyleSheet("font-size: 12px;")
                row.addWidget(title_lbl, 1)

                container = QWidget()
                container.setLayout(row)
                container.setCursor(Qt.CursorShape.PointingHandCursor)
                self.day_event_list.addWidget(container)

        self.day_event_list.addStretch()

    def _update_mini_month_events(self):
        """Feed the mini month with event data so it can show colored dots."""
        first = date(self.mini_month._view_year, self.mini_month._view_month, 1)
        if self.mini_month._view_month == 12:
            last = date(self.mini_month._view_year + 1, 1, 1) - timedelta(days=1)
        else:
            last = date(self.mini_month._view_year, self.mini_month._view_month + 1, 1) - timedelta(days=1)

        events = self.store.get_events(first.isoformat(), last.isoformat() + "T23:59:59")
        by_date: dict[date, list] = {}
        for ev in events:
            d = datetime.fromisoformat(ev.start_time).date()
            by_date.setdefault(d, []).append(ev)
        self.mini_month.set_events(by_date)

    # ── Navigation ─────────────────────────────────────

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

    def _on_mini_date_selected(self, d):
        self._selected_date = d
        self._refresh()

    # ── Event CRUD ─────────────────────────────────────

    def _add_event(self):
        dlg = EventDialog(self)
        dlg.date_edit.setDate(QDate(
            self._selected_date.year, self._selected_date.month, self._selected_date.day
        ))
        if dlg.exec():
            self.store.add_event(**dlg.get_data())
            self._refresh()

    def _add_event_on_day_date(self, d: date):
        dlg = EventDialog(self)
        dlg.date_edit.setDate(QDate(d.year, d.month, d.day))
        if dlg.exec():
            self.store.add_event(**dlg.get_data())
            self._refresh()

    def _edit_event(self, event: Event):
        dlg = EventDialog(self, event)
        result = dlg.exec()
        if dlg._delete_requested:
            reply = QMessageBox.question(
                self, "Delete Event", f"Delete '{event.title}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.store.delete_event(event.id)
                self._refresh()
        elif result:
            data = dlg.get_data()
            event.title = data["title"]
            event.description = data["description"]
            event.start_time = data["start_time"]
            event.end_time = data["end_time"]
            event.all_day = data["all_day"]
            event.color = data["color"]
            self.store.update_event(event)
            self._refresh()
