"""Calendar module UI — monthly view with today highlight and event management."""

from datetime import date, datetime, timedelta
import calendar

from PyQt6.QtCore import Qt, QDate
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QDialog, QLineEdit, QTextEdit,
    QDateEdit, QTimeEdit, QCheckBox, QFrame, QComboBox,
    QMessageBox,
)

from src.data.calendar_store import CalendarStore, Event


class EventDialog(QDialog):
    """Dialog to add/edit an event."""

    def __init__(self, parent=None, event=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Event" if event else "New Event")
        self.setMinimumWidth(380)
        self.event = event
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

        # Date
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

        # Time
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

        self.time_row_widgets = [self.start_time, self.end_time]
        self._toggle_time(self.all_day_check.isChecked())

        # Color
        layout.addWidget(QLabel("Color"))
        self.color_combo = QComboBox()
        colors = {
            "Blue": "#4a9eff", "Green": "#a6e3a1", "Red": "#f38ba8",
            "Yellow": "#f9e2af", "Purple": "#cba6f7", "Orange": "#fab387",
            "Teal": "#94e2d5", "Pink": "#f5c2e7",
        }
        for name, hex_val in colors.items():
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
            delete_btn = QPushButton("Delete")
            delete_btn.setObjectName("destructive")
            delete_btn.clicked.connect(self._on_delete)
            btn_row.addWidget(delete_btn)
        btn_row.addStretch()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("secondary")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        btn_row.addWidget(save_btn)
        layout.addLayout(btn_row)

        self._delete_requested = False

    def _toggle_time(self, all_day: bool):
        for w in self.time_row_widgets:
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
            "start_time": start,
            "end_time": end,
            "all_day": self.all_day_check.isChecked(),
            "color": self.color_combo.currentData(),
        }


class DayCell(QFrame):
    """A single day cell in the monthly grid."""

    def __init__(self, day_num: int, is_today: bool, events: list, parent_panel):
        super().__init__()
        self.day_num = day_num
        self.events = events
        self.parent_panel = parent_panel
        self.setFrameShape(QFrame.Shape.Box)
        self.setMinimumHeight(80)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 3, 4, 3)
        layout.setSpacing(2)

        day_label = QLabel(str(day_num))
        day_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        if is_today:
            day_label.setStyleSheet(
                "background-color: #4a9eff; color: #1e1e2e; "
                "border-radius: 12px; padding: 2px 8px; font-weight: bold; font-size: 13px;"
            )
            day_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            day_label.setFixedWidth(28)
            day_label.setFixedHeight(24)
            # Right-align the label widget
            hlayout = QHBoxLayout()
            hlayout.setContentsMargins(0, 0, 0, 0)
            hlayout.addStretch()
            hlayout.addWidget(day_label)
            layout.addLayout(hlayout)
        else:
            layout.addWidget(day_label)

        for ev in events[:3]:
            ev_label = QLabel(ev.title)
            ev_label.setStyleSheet(
                f"background-color: {ev.color}; color: #1e1e2e; "
                f"border-radius: 3px; padding: 1px 4px; font-size: 11px;"
            )
            ev_label.setToolTip(
                f"{ev.title}\n{ev.start_time}"
                + (f"\n{ev.description}" if ev.description else "")
            )
            layout.addWidget(ev_label)

        if len(events) > 3:
            more = QLabel(f"+{len(events) - 3} more")
            more.setObjectName("subtitle")
            layout.addWidget(more)

        layout.addStretch()

    def mouseDoubleClickEvent(self, event):
        self.parent_panel._add_event_on_day(self.day_num)

    def mousePressEvent(self, event):
        """Single click on an event opens it for editing."""
        if event.button() == Qt.MouseButton.LeftButton and self.events:
            # If there's exactly one event, open it directly
            if len(self.events) == 1:
                self.parent_panel._edit_event(self.events[0])


class CalendarPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.store = CalendarStore()
        self.current_year = date.today().year
        self.current_month = date.today().month
        self._palette = {}
        self._build_ui()
        self._render_month()

    def set_palette(self, palette: dict):
        self._palette = palette
        self._render_month()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)

        # Header
        header = QHBoxLayout()
        title = QLabel("Calendar")
        title.setObjectName("sectionTitle")
        header.addWidget(title)
        header.addStretch()

        self.btn_prev = QPushButton("\u25c0")
        self.btn_prev.setObjectName("secondary")
        self.btn_prev.setFixedSize(36, 36)
        self.btn_prev.setToolTip("Previous month")
        self.btn_prev.clicked.connect(self._prev_month)
        header.addWidget(self.btn_prev)

        self.month_label = QLabel()
        self.month_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.month_label.setMinimumWidth(180)
        self.month_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        header.addWidget(self.month_label)

        self.btn_next = QPushButton("\u25b6")
        self.btn_next.setObjectName("secondary")
        self.btn_next.setFixedSize(36, 36)
        self.btn_next.setToolTip("Next month")
        self.btn_next.clicked.connect(self._next_month)
        header.addWidget(self.btn_next)

        header.addSpacing(12)

        btn_today = QPushButton("Today")
        btn_today.setObjectName("secondary")
        btn_today.setToolTip("Jump to current month")
        btn_today.clicked.connect(self._go_today)
        header.addWidget(btn_today)

        btn_add = QPushButton("+ Event")
        btn_add.setToolTip("Add a new event")
        btn_add.clicked.connect(self._add_event)
        header.addWidget(btn_add)

        layout.addLayout(header)

        # Day-of-week headers
        dow_layout = QGridLayout()
        dow_layout.setSpacing(2)
        for i, name in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]):
            lbl = QLabel(name)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("font-weight: bold; padding: 6px;")
            if i >= 5:  # Weekend
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

        # Today
        today = date.today()
        is_current_month = (today.year == self.current_year and today.month == self.current_month)

        # Build calendar grid
        cal = calendar.Calendar(firstweekday=0)
        weeks = cal.monthdayscalendar(self.current_year, self.current_month)

        for row, week in enumerate(weeks):
            for col, day in enumerate(week):
                if day == 0:
                    cell = QFrame()
                    cell.setMinimumHeight(80)
                else:
                    day_events = events_by_day.get(day, [])
                    is_today = is_current_month and day == today.day
                    cell = DayCell(day, is_today, day_events, self)
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

    def _edit_event(self, event: Event):
        dlg = EventDialog(self, event)
        result = dlg.exec()
        if hasattr(dlg, '_delete_requested') and dlg._delete_requested:
            reply = QMessageBox.question(
                self, "Delete Event",
                f"Delete '{event.title}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.store.delete_event(event.id)
                self._render_month()
        elif result:
            data = dlg.get_data()
            event.title = data["title"]
            event.description = data["description"]
            event.start_time = data["start_time"]
            event.end_time = data["end_time"]
            event.all_day = data["all_day"]
            event.color = data["color"]
            self.store.update_event(event)
            self._render_month()
