"""QA Dashboard panel — overview of tasks, upcoming deadlines, and productivity stats."""

from datetime import date, datetime, timedelta

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QFrame, QScrollArea, QProgressBar,
)

from src.data.todo_store import TodoStore, PRIORITY_LABELS
from src.data.calendar_store import CalendarStore
from src.data.finance_store import FinanceStore


PRIORITY_COLORS = {0: "#a6adc8", 1: "#a6e3a1", 2: "#f9e2af", 3: "#f38ba8"}


class StatCard(QFrame):
    """A compact stat card with a big number and label."""

    def __init__(self, value: str, label: str, color: str = "#cdd6f4", parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            f"StatCard {{ border: 1px solid palette(mid); border-radius: 6px; padding: 8px; }}"
        )
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(2)

        val = QLabel(value)
        val.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {color};")
        val.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(val)
        self._value_label = val

        lbl = QLabel(label)
        lbl.setObjectName("subtitle")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("font-size: 11px;")
        layout.addWidget(lbl)
        self._label = lbl

    def update_value(self, value: str, color: str | None = None):
        self._value_label.setText(value)
        if color:
            self._value_label.setStyleSheet(
                f"font-size: 24px; font-weight: bold; color: {color};"
            )


class UpcomingItem(QFrame):
    """A single upcoming deadline / event in the dashboard."""

    def __init__(self, title: str, subtitle: str, color: str, days_label: str, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(8)

        dot = QLabel("\u25cf")
        dot.setStyleSheet(f"color: {color}; font-size: 14px;")
        dot.setFixedWidth(16)
        layout.addWidget(dot)

        info = QVBoxLayout()
        info.setSpacing(0)
        t = QLabel(title)
        t.setStyleSheet("font-weight: bold; font-size: 12px;")
        info.addWidget(t)
        s = QLabel(subtitle)
        s.setObjectName("subtitle")
        s.setStyleSheet("font-size: 10px;")
        info.addWidget(s)
        layout.addLayout(info, 1)

        badge = QLabel(days_label)
        badge.setStyleSheet(
            f"color: {color}; font-size: 10px; font-weight: bold; "
            f"padding: 2px 6px; border: 1px solid {color}; border-radius: 3px;"
        )
        layout.addWidget(badge)


class DashboardPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.todo_store = TodoStore()
        self.calendar_store = CalendarStore()
        self.finance_store = FinanceStore()
        self._palette: dict = {}
        self._build_ui()
        self._refresh()

    def set_palette(self, palette: dict):
        self._palette = palette
        self._refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)

        # Header
        header = QHBoxLayout()
        title = QLabel("Dashboard")
        title.setObjectName("sectionTitle")
        header.addWidget(title)
        header.addStretch()
        self.date_label = QLabel("")
        self.date_label.setObjectName("subtitle")
        header.addWidget(self.date_label)
        layout.addLayout(header)

        # Stat cards row
        self._cards_layout = QHBoxLayout()
        self._cards_layout.setSpacing(10)

        self.card_pending = StatCard("0", "Pending Tasks")
        self.card_done_today = StatCard("0", "Done Today")
        self.card_overdue = StatCard("0", "Overdue", "#f38ba8")
        self.card_events_week = StatCard("0", "Events This Week")
        self.card_earned_month = StatCard("$0", "Earned This Month")

        for card in [self.card_pending, self.card_done_today, self.card_overdue,
                     self.card_events_week, self.card_earned_month]:
            self._cards_layout.addWidget(card)

        layout.addLayout(self._cards_layout)

        # Progress bar for task completion
        progress_row = QHBoxLayout()
        progress_row.setSpacing(8)
        progress_lbl = QLabel("Task Completion:")
        progress_lbl.setObjectName("subtitle")
        progress_row.addWidget(progress_lbl)
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(18)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p% complete")
        progress_row.addWidget(self.progress_bar, 1)
        self.progress_pct_label = QLabel("")
        self.progress_pct_label.setObjectName("subtitle")
        progress_row.addWidget(self.progress_pct_label)
        layout.addLayout(progress_row)

        # Two-column area: upcoming deadlines + priority breakdown
        columns = QHBoxLayout()
        columns.setSpacing(12)

        # Left: upcoming deadlines
        left = QVBoxLayout()
        upcoming_title = QLabel("Upcoming Deadlines & Events")
        upcoming_title.setStyleSheet("font-weight: bold; font-size: 13px;")
        left.addWidget(upcoming_title)

        self._upcoming_container = QWidget()
        self._upcoming_layout = QVBoxLayout(self._upcoming_container)
        self._upcoming_layout.setContentsMargins(0, 0, 0, 0)
        self._upcoming_layout.setSpacing(3)

        upcoming_scroll = QScrollArea()
        upcoming_scroll.setWidgetResizable(True)
        upcoming_scroll.setWidget(self._upcoming_container)
        upcoming_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        left.addWidget(upcoming_scroll, 1)
        columns.addLayout(left, 3)

        # Right: priority breakdown + category breakdown
        right = QVBoxLayout()

        priority_title = QLabel("Tasks by Priority")
        priority_title.setStyleSheet("font-weight: bold; font-size: 13px;")
        right.addWidget(priority_title)

        self._priority_container = QWidget()
        self._priority_layout = QVBoxLayout(self._priority_container)
        self._priority_layout.setContentsMargins(0, 0, 0, 0)
        self._priority_layout.setSpacing(4)
        right.addWidget(self._priority_container)

        right.addSpacing(12)

        cat_title = QLabel("Tasks by Category")
        cat_title.setStyleSheet("font-weight: bold; font-size: 13px;")
        right.addWidget(cat_title)

        self._category_container = QWidget()
        self._category_layout = QVBoxLayout(self._category_container)
        self._category_layout.setContentsMargins(0, 0, 0, 0)
        self._category_layout.setSpacing(4)
        right.addWidget(self._category_container)

        right.addStretch()
        columns.addLayout(right, 2)

        layout.addLayout(columns, 1)

    def _refresh(self):
        green = self._palette.get("green", "#a6e3a1")
        red = self._palette.get("red", "#f38ba8")
        accent = self._palette.get("accent", "#4a9eff")
        yellow = self._palette.get("yellow", "#f9e2af")

        today = date.today()
        self.date_label.setText(today.strftime("%A, %B %d, %Y"))

        # Task stats
        counts = self.todo_store.get_counts()
        all_tasks = self.todo_store.get_all(include_done=True)
        pending_tasks = [t for t in all_tasks if not t.done and not t.deleted]
        done_tasks = [t for t in all_tasks if t.done and not t.deleted]

        overdue = [
            t for t in pending_tasks
            if t.due_date and t.due_date < today.isoformat()
        ]

        # Done today
        today_str = today.isoformat()
        done_today = [
            t for t in done_tasks
            if t.updated_at and t.updated_at[:10] == today_str
        ]

        self.card_pending.update_value(str(counts["pending"]), accent)
        self.card_done_today.update_value(str(len(done_today)), green)
        self.card_overdue.update_value(str(len(overdue)), red if overdue else green)

        # Events this week
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        week_events = self.calendar_store.get_events(
            week_start.isoformat(), week_end.isoformat() + "T23:59:59"
        )
        self.card_events_week.update_value(str(len(week_events)), accent)

        # Earned this month
        month_start = today.replace(day=1).isoformat()
        month_earned = self.finance_store.get_summary(month_start, today.isoformat())
        self.card_earned_month.update_value(
            f"${month_earned['earned']:,.0f}", green
        )

        # Progress bar
        total = counts["total"]
        done = counts["done"]
        if total > 0:
            pct = int(done / total * 100)
            self.progress_bar.setValue(pct)
            self.progress_pct_label.setText(f"{done}/{total}")
        else:
            self.progress_bar.setValue(0)
            self.progress_pct_label.setText("No tasks")

        # Style the progress bar
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid palette(mid);
                border-radius: 4px;
                text-align: center;
                font-size: 11px;
            }}
            QProgressBar::chunk {{
                background-color: {accent};
                border-radius: 3px;
            }}
        """)

        # Upcoming deadlines (tasks with due dates + events in next 7 days)
        self._clear_layout(self._upcoming_layout)

        upcoming_items = []

        # Tasks with due dates (sorted by date)
        for task in sorted(pending_tasks, key=lambda t: t.due_date or "9999"):
            if task.due_date:
                try:
                    due = date.fromisoformat(task.due_date)
                    delta = (due - today).days
                    if delta < 0:
                        days_text = f"{-delta}d overdue"
                        color = red
                    elif delta == 0:
                        days_text = "Today"
                        color = yellow
                    elif delta == 1:
                        days_text = "Tomorrow"
                        color = yellow
                    elif delta <= 7:
                        days_text = f"In {delta}d"
                        color = accent
                    else:
                        days_text = f"In {delta}d"
                        color = green
                    cat = f"Task \u00b7 {task.category}" if task.category else "Task"
                    upcoming_items.append((delta, UpcomingItem(
                        task.title, cat, color, days_text
                    )))
                except ValueError:
                    pass

        # Events in next 7 days
        next_week = today + timedelta(days=7)
        upcoming_events = self.calendar_store.get_events(
            today.isoformat(), next_week.isoformat() + "T23:59:59"
        )
        for ev in upcoming_events:
            try:
                ev_date = datetime.fromisoformat(ev.start_time).date()
                delta = (ev_date - today).days
                if delta == 0:
                    days_text = "Today"
                elif delta == 1:
                    days_text = "Tomorrow"
                else:
                    days_text = f"In {delta}d"
                time_str = ""
                if not ev.all_day:
                    time_str = datetime.fromisoformat(ev.start_time).strftime("%H:%M")
                sub = f"Event \u00b7 {time_str}" if time_str else "Event \u00b7 All day"
                upcoming_items.append((delta, UpcomingItem(
                    ev.title, sub, ev.color, days_text
                )))
            except (ValueError, AttributeError):
                pass

        # Sort by urgency
        for _, widget in sorted(upcoming_items, key=lambda x: x[0]):
            self._upcoming_layout.addWidget(widget)

        if not upcoming_items:
            no_items = QLabel("No upcoming deadlines or events")
            no_items.setObjectName("subtitle")
            self._upcoming_layout.addWidget(no_items)

        self._upcoming_layout.addStretch()

        # Priority breakdown
        self._clear_layout(self._priority_layout)
        priority_counts = {0: 0, 1: 0, 2: 0, 3: 0}
        for task in pending_tasks:
            priority_counts[task.priority] = priority_counts.get(task.priority, 0) + 1

        max_count = max(priority_counts.values()) if any(priority_counts.values()) else 1
        for pri in [3, 2, 1, 0]:
            count = priority_counts[pri]
            row = QHBoxLayout()
            label = QLabel(PRIORITY_LABELS[pri])
            label.setFixedWidth(55)
            label.setStyleSheet(f"font-size: 11px; color: {PRIORITY_COLORS[pri]};")
            row.addWidget(label)

            bar = QFrame()
            width = max(int(count / max_count * 120), 2) if max_count > 0 else 2
            bar.setFixedSize(width, 14)
            bar.setStyleSheet(
                f"background-color: {PRIORITY_COLORS[pri]}; border-radius: 2px;"
            )
            row.addWidget(bar)

            cnt = QLabel(str(count))
            cnt.setObjectName("subtitle")
            cnt.setFixedWidth(25)
            row.addWidget(cnt)
            row.addStretch()

            container = QWidget()
            container.setLayout(row)
            self._priority_layout.addWidget(container)

        # Category breakdown
        self._clear_layout(self._category_layout)
        cat_counts: dict[str, int] = {}
        for task in pending_tasks:
            cat = task.category or "Uncategorized"
            cat_counts[cat] = cat_counts.get(cat, 0) + 1

        if cat_counts:
            max_cat = max(cat_counts.values())
            bar_colors = [accent, green, "#cba6f7", "#fab387", yellow, "#94e2d5"]
            for i, (cat, count) in enumerate(sorted(cat_counts.items(), key=lambda x: -x[1])):
                row = QHBoxLayout()
                label = QLabel(cat)
                label.setFixedWidth(80)
                label.setStyleSheet("font-size: 11px;")
                row.addWidget(label)

                bar = QFrame()
                width = max(int(count / max_cat * 100), 2) if max_cat > 0 else 2
                bar.setFixedSize(width, 14)
                color = bar_colors[i % len(bar_colors)]
                bar.setStyleSheet(f"background-color: {color}; border-radius: 2px;")
                row.addWidget(bar)

                cnt = QLabel(str(count))
                cnt.setObjectName("subtitle")
                cnt.setFixedWidth(25)
                row.addWidget(cnt)
                row.addStretch()

                container = QWidget()
                container.setLayout(row)
                self._category_layout.addWidget(container)
        else:
            no_cats = QLabel("No pending tasks")
            no_cats.setObjectName("subtitle")
            self._category_layout.addWidget(no_cats)

    @staticmethod
    def _clear_layout(layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
