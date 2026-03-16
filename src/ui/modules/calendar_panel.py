"""Calendar module UI — monthly view with event management."""

from datetime import date, datetime, timedelta
import calendar

from PyQt6.QtCore import Qt, QDate
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QDialog, QLineEdit, QTextEdit,
    QDateEdit, QTimeEdit, QCheckBox, QListWidget, QListWidgetItem,
    QFrame, QScrollArea, QComboBox,
)

from src.data.calendar_store import CalendarStore


class EventDialog(QDialog):
    """Dialog to add/edit an event."""

    def __init__(self, parent=None, event=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Event" if event else "New Event")
        self.setMinimumWidth(350)
        self.event = event
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Title"))
        self.title_edit = QLineEdit()
        if self.event:
            self.title_edit.setText(self.event.title)
        layout.addWidget(self.title_edit)

        layout.addWidget(QLabel("Description"))
        self.desc_edit = QTextEdit()
        self.desc_edit.setMaximumHeight(80)
        if self.event:
            self.desc_edit.setPlainText(self.event.description)
        layout.addWidget(self.desc_edit)

        self.all_day_check = QCheckBox("All day")
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
        date_row.addWidget(self.date_edit)
        layout.addLayout(date_row)

        time_row = QHBoxLayout()
        time_row.addWidget(QLabel("Start"))
        self.start_time = QTimeEdit()
        if self.event and not self.event.all_day:
            dt = datetime.fromisoformat(self.event.start_time)
            from PyQt6.QtCore import QTime
            self.start_time.setTime(QTime(dt.hour, dt.minute))
        time_row.addWidget(self.start_time)
        time_row.addWidget(QLabel("End"))
        self.end_time = QTimeEdit()
        if self.event and self.event.end_time:
            dt = datetime.fromisoformat(self.event.end_time)
            from PyQt6.QtCore import QTime
            self.end_time.setTime(QTime(dt.hour, dt.minute))
        time_row.addWidget(self.end_time)
        layout.addLayout(time_row)

        self.time_row_widgets = [self.start_time, self.end_time]
        self._toggle_time(self.all_day_check.isChecked())

        layout.addWidget(QLabel("Color"))
        self.color_combo = QComboBox()
        colors = {
            "Blue": "#4a9eff", "Green": "#a6e3a1", "Red": "#f38ba8",
            "Yellow": "#f9e2af", "Purple": "#cba6f7", "Orange": "#fab387",
        }
        for name, hex_val in colors.items():
            self.color_combo.addItem(name, hex_val)
        if self.event:
            idx = self.color_combo.findData(self.event.color)
            if idx >= 0:
                self.color_combo.setCurrentIndex(idx)
        layout.addWidget(self.color_combo)

        btn_row = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("secondary")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(save_btn)
        btn_row.addWidget(cancel_btn)
        layout.addLayout(btn_row)

    def _toggle_time(self, all_day: bool):
        for w in self.time_row_widgets:
            w.setEnabled(not all_day)

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
            "start_time": start,
            "end_time": end,
            "all_day": self.all_day_check.isChecked(),
            "color": self.color_combo.currentData(),
        }


class DayCell(QFrame):
    """A single day cell in the monthly grid."""

    def __init__(self, day_num: int, is_current_month: bool, events: list, parent_panel):
        super().__init__()
        self.day_num = day_num
        self.parent_panel = parent_panel
        self.setFrameShape(QFrame.Shape.Box)
        self.setMinimumHeight(80)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 2, 4, 2)
        layout.setSpacing(1)

        day_label = QLabel(str(day_num))
        if not is_current_month:
            day_label.setObjectName("subtitle")
        day_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(day_label)

        for ev in events[:3]:  # Show max 3 events
            ev_label = QLabel(ev.title)
            ev_label.setStyleSheet(
                f"background-color: {ev.color}; color: #1e1e2e; "
                f"border-radius: 3px; padding: 1px 4px; font-size: 11px;"
            )
            layout.addWidget(ev_label)

        if len(events) > 3:
            more = QLabel(f"+{len(events) - 3} more")
            more.setObjectName("subtitle")
            layout.addWidget(more)

        layout.addStretch()

    def mouseDoubleClickEvent(self, event):
        self.parent_panel._add_event_on_day(self.day_num)


class CalendarPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.store = CalendarStore()
        self.current_year = date.today().year
        self.current_month = date.today().month
        self._build_ui()
        self._render_month()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)

        # Header
        header = QHBoxLayout()
        title = QLabel("Calendar")
        title.setObjectName("sectionTitle")
        header.addWidget(title)
        header.addStretch()

        self.btn_prev = QPushButton("<")
        self.btn_prev.setObjectName("secondary")
        self.btn_prev.setFixedWidth(40)
        self.btn_prev.clicked.connect(self._prev_month)
        header.addWidget(self.btn_prev)

        self.month_label = QLabel()
        self.month_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.month_label.setMinimumWidth(160)
        header.addWidget(self.month_label)

        self.btn_next = QPushButton(">")
        self.btn_next.setObjectName("secondary")
        self.btn_next.setFixedWidth(40)
        self.btn_next.clicked.connect(self._next_month)
        header.addWidget(self.btn_next)

        btn_today = QPushButton("Today")
        btn_today.setObjectName("secondary")
        btn_today.clicked.connect(self._go_today)
        header.addWidget(btn_today)

        btn_add = QPushButton("+ Event")
        btn_add.clicked.connect(self._add_event)
        header.addWidget(btn_add)

        layout.addLayout(header)

        # Day-of-week headers
        dow_layout = QGridLayout()
        for i, name in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]):
            lbl = QLabel(name)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setObjectName("subtitle")
            dow_layout.addWidget(lbl, 0, i)
        layout.addLayout(dow_layout)

        # Grid container
        self.grid_container = QWidget()
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setSpacing(2)
        layout.addWidget(self.grid_container, 1)

    def _render_month(self):
        # Clear grid
        while self.grid_layout.count():
            child = self.grid_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.month_label.setText(
            f"{calendar.month_name[self.current_month]} {self.current_year}"
        )

        # Get events for the month
        first_day = date(self.current_year, self.current_month, 1)
        if self.current_month == 12:
            last_day = date(self.current_year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day = date(self.current_year, self.current_month + 1, 1) - timedelta(days=1)

        events = self.store.get_events(first_day.isoformat(), last_day.isoformat() + "T23:59:59")

        # Group events by day
        events_by_day: dict[int, list] = {}
        for ev in events:
            day = datetime.fromisoformat(ev.start_time).day
            events_by_day.setdefault(day, []).append(ev)

        # Build calendar grid (Monday-start)
        cal = calendar.Calendar(firstweekday=0)
        weeks = cal.monthdayscalendar(self.current_year, self.current_month)

        for row, week in enumerate(weeks):
            for col, day in enumerate(week):
                if day == 0:
                    cell = QFrame()
                    cell.setMinimumHeight(80)
                else:
                    day_events = events_by_day.get(day, [])
                    cell = DayCell(day, True, day_events, self)
                self.grid_layout.addWidget(cell, row, col)

    def _prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self._render_month()

    def _next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self._render_month()

    def _go_today(self):
        today = date.today()
        self.current_year = today.year
        self.current_month = today.month
        self._render_month()

    def _add_event(self):
        dlg = EventDialog(self)
        if dlg.exec():
            data = dlg.get_data()
            self.store.add_event(**data)
            self._render_month()

    def _add_event_on_day(self, day: int):
        dlg = EventDialog(self)
        dlg.date_edit.setDate(QDate(self.current_year, self.current_month, day))
        if dlg.exec():
            data = dlg.get_data()
            self.store.add_event(**data)
            self._render_month()
