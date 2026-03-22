"""Activity Tracker panel — Gantt-style single-row day view with manual timer input.

Tracks daily activities with start/end times, a dropdown of common activities,
and a small notes section. Exports activities to the Obsidian vault.
"""

from datetime import date, datetime, timedelta
from pathlib import Path, PurePosixPath

from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QBrush, QMouseEvent
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QComboBox, QTimeEdit, QPlainTextEdit,
    QFrame, QScrollArea, QMessageBox, QSizePolicy,
)

from src.config import load_config
from src.data.activity_store import (
    ActivityStore, Activity, DEFAULT_ACTIVITIES, ACTIVITY_COLORS, DEFAULT_COLOR,
)


# Day view spans 0:00 to 30:00 (6 AM previous to noon next day conceptually,
# but we display 0-30 hours so users can log late-night activity)
DAY_START_HOUR = 0
DAY_END_HOUR = 30
HOUR_COUNT = DAY_END_HOUR - DAY_START_HOUR


class GanttBar:
    """Represents a single activity block on the Gantt chart."""

    def __init__(self, activity: Activity):
        self.activity = activity
        self.rect = QRectF()  # Set during painting


class GanttWidget(QWidget):
    """Custom-painted Gantt chart showing a single day's activities."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.bars: list[GanttBar] = []
        self.selected_bar: GanttBar | None = None
        self._palette: dict = {}
        self.setMinimumHeight(100)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(100)
        self.setMouseTracking(True)
        self._hover_bar: GanttBar | None = None
        self._on_select = None  # callback

    def set_palette(self, palette: dict):
        self._palette = palette
        self.update()

    def set_bars(self, activities: list[Activity]):
        self.bars = [GanttBar(a) for a in activities]
        self.selected_bar = None
        self.update()

    def set_on_select(self, callback):
        self._on_select = callback

    def _time_to_x(self, time_str: str, width: float, margin: float) -> float:
        """Convert HH:MM to x coordinate."""
        try:
            h, m = map(int, time_str.split(":"))
            total_minutes = h * 60 + m
            chart_width = width - 2 * margin
            return margin + (total_minutes / (HOUR_COUNT * 60)) * chart_width
        except (ValueError, AttributeError):
            return margin

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()
        margin_left = 40
        margin_right = 10
        margin_top = 18
        bar_height = 36
        chart_width = w - margin_left - margin_right

        bg = QColor(self._palette.get("bg", "#1e1e2e"))
        fg = QColor(self._palette.get("fg", "#cdd6f4"))
        grid_color = QColor(self._palette.get("border", "#45475a"))

        # Background
        painter.fillRect(0, 0, w, h, bg)

        # Hour grid lines and labels
        painter.setPen(QPen(grid_color, 1))
        label_font = QFont()
        label_font.setPixelSize(9)
        painter.setFont(label_font)

        for hour in range(DAY_START_HOUR, DAY_END_HOUR + 1):
            x = margin_left + (hour / HOUR_COUNT) * chart_width
            # Major lines every 6 hours, minor every hour
            if hour % 6 == 0:
                painter.setPen(QPen(grid_color, 1))
                painter.drawLine(QPointF(x, margin_top - 2), QPointF(x, margin_top + bar_height + 4))
                # Label
                display_h = hour % 24
                label = f"{display_h:02d}:00"
                painter.setPen(fg)
                painter.drawText(QRectF(x - 18, 0, 36, margin_top - 2),
                                 Qt.AlignmentFlag.AlignCenter, label)
            elif hour % 3 == 0:
                painter.setPen(QPen(grid_color, 1, Qt.PenStyle.DotLine))
                painter.drawLine(QPointF(x, margin_top), QPointF(x, margin_top + bar_height))

        # Track background
        track_rect = QRectF(margin_left, margin_top, chart_width, bar_height)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(grid_color.red(), grid_color.green(),
                                        grid_color.blue(), 80)))
        painter.drawRoundedRect(track_rect, 4, 4)

        # Activity bars
        for bar in self.bars:
            x1 = self._time_to_x(bar.activity.start_time, w, margin_left)
            x2 = self._time_to_x(bar.activity.end_time, w, margin_left)
            bar_w = max(x2 - x1, 2)
            bar.rect = QRectF(x1, margin_top + 2, bar_w, bar_height - 4)

            color = QColor(bar.activity.color)
            if bar == self.selected_bar:
                color = color.lighter(130)
            elif bar == self._hover_bar:
                color = color.lighter(115)

            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawRoundedRect(bar.rect, 3, 3)

            # Label inside bar if wide enough
            if bar_w > 40:
                painter.setPen(QColor("#11111b"))
                text_font = QFont()
                text_font.setPixelSize(10)
                text_font.setBold(True)
                painter.setFont(text_font)
                text_rect = bar.rect.adjusted(4, 0, -4, 0)
                painter.drawText(text_rect, Qt.AlignmentFlag.AlignVCenter |
                                 Qt.AlignmentFlag.AlignLeft,
                                 bar.activity.activity)

        # "Now" indicator if viewing today
        now = datetime.now()
        now_minutes = now.hour * 60 + now.minute
        if 0 <= now_minutes <= HOUR_COUNT * 60:
            now_x = margin_left + (now_minutes / (HOUR_COUNT * 60)) * chart_width
            painter.setPen(QPen(QColor("#f38ba8"), 2))
            painter.drawLine(QPointF(now_x, margin_top - 4),
                             QPointF(now_x, margin_top + bar_height + 4))

        # Bottom time summary
        total = sum(b.activity.duration_minutes for b in self.bars)
        hours = total // 60
        mins = total % 60
        painter.setPen(fg)
        summary_font = QFont()
        summary_font.setPixelSize(10)
        painter.setFont(summary_font)
        painter.drawText(QRectF(margin_left, margin_top + bar_height + 6,
                                chart_width, 20),
                         Qt.AlignmentFlag.AlignLeft,
                         f"Total tracked: {hours}h {mins}m")

        painter.end()

    def mousePressEvent(self, event: QMouseEvent):
        pos = event.position()
        clicked = None
        for bar in self.bars:
            if bar.rect.contains(pos):
                clicked = bar
                break
        self.selected_bar = clicked
        self.update()
        if self._on_select and clicked:
            self._on_select(clicked.activity)

    def mouseMoveEvent(self, event: QMouseEvent):
        pos = event.position()
        hover = None
        for bar in self.bars:
            if bar.rect.contains(pos):
                hover = bar
                break
        if hover != self._hover_bar:
            self._hover_bar = hover
            if hover:
                a = hover.activity
                self.setToolTip(
                    f"{a.activity}\n{a.start_time} – {a.end_time} "
                    f"({a.duration_minutes}m)\n{a.notes}" if a.notes
                    else f"{a.activity}\n{a.start_time} – {a.end_time} ({a.duration_minutes}m)"
                )
            else:
                self.setToolTip("")
            self.update()


class ActivityPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.store = ActivityStore()
        self._palette: dict = {}
        self._current_date = date.today()
        self._editing_activity: Activity | None = None
        self._build_ui()
        self._refresh()

    def set_palette(self, palette: dict):
        self._palette = palette
        self.gantt.set_palette(palette)
        self._refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(10)

        # Header
        header = QHBoxLayout()
        title = QLabel("Activity Tracker")
        title.setObjectName("sectionTitle")
        header.addWidget(title)
        header.addStretch()

        btn_prev = QPushButton("\u25c0")
        btn_prev.setFixedSize(28, 28)
        btn_prev.clicked.connect(self._prev_day)
        header.addWidget(btn_prev)

        self.date_label = QLabel("")
        self.date_label.setStyleSheet("font-weight: bold; font-size: 13px;")
        header.addWidget(self.date_label)

        btn_next = QPushButton("\u25b6")
        btn_next.setFixedSize(28, 28)
        btn_next.clicked.connect(self._next_day)
        header.addWidget(btn_next)

        btn_today = QPushButton("Today")
        btn_today.setObjectName("secondary")
        btn_today.clicked.connect(self._go_today)
        header.addWidget(btn_today)

        layout.addLayout(header)

        # Gantt chart
        self.gantt = GanttWidget()
        self.gantt.set_on_select(self._on_bar_selected)
        layout.addWidget(self.gantt)

        # Input form — quick entry
        form_frame = QFrame()
        form_frame.setStyleSheet(
            "QFrame { border: 1px solid palette(mid); border-radius: 6px; padding: 8px; }"
        )
        form_layout = QVBoxLayout(form_frame)
        form_layout.setContentsMargins(10, 8, 10, 8)
        form_layout.setSpacing(6)

        form_title = QLabel("Log Activity")
        form_title.setStyleSheet("font-weight: bold; font-size: 12px; border: none;")
        form_layout.addWidget(form_title)

        # Row 1: Activity + times
        row1 = QHBoxLayout()
        row1.setSpacing(8)

        self.activity_combo = QComboBox()
        self.activity_combo.setEditable(True)
        self.activity_combo.addItems(DEFAULT_ACTIVITIES)
        self.activity_combo.setMinimumWidth(140)
        self.activity_combo.setPlaceholderText("Activity...")
        row1.addWidget(QLabel("Activity:"))
        row1.addWidget(self.activity_combo, 1)

        row1.addWidget(QLabel("Start:"))
        self.start_edit = QTimeEdit()
        self.start_edit.setDisplayFormat("HH:mm")
        self.start_edit.setWrapping(True)
        # Default to current hour
        now = datetime.now()
        from PyQt6.QtCore import QTime
        self.start_edit.setTime(QTime(now.hour, 0))
        row1.addWidget(self.start_edit)

        row1.addWidget(QLabel("End:"))
        self.end_edit = QTimeEdit()
        self.end_edit.setDisplayFormat("HH:mm")
        self.end_edit.setWrapping(True)
        self.end_edit.setTime(QTime(min(now.hour + 1, 23), 0))
        row1.addWidget(self.end_edit)

        form_layout.addLayout(row1)

        # Row 2: Notes + buttons
        row2 = QHBoxLayout()
        row2.setSpacing(8)

        self.notes_edit = QPlainTextEdit()
        self.notes_edit.setPlaceholderText("Notes (optional)...")
        self.notes_edit.setMaximumHeight(50)
        self.notes_edit.setStyleSheet("border: 1px solid palette(mid); border-radius: 3px;")
        row2.addWidget(self.notes_edit, 1)

        btn_col = QVBoxLayout()
        btn_col.setSpacing(3)

        self.btn_add = QPushButton("Add")
        self.btn_add.setFixedWidth(70)
        self.btn_add.clicked.connect(self._add_activity)
        btn_col.addWidget(self.btn_add)

        self.btn_update = QPushButton("Update")
        self.btn_update.setObjectName("secondary")
        self.btn_update.setFixedWidth(70)
        self.btn_update.clicked.connect(self._update_activity)
        self.btn_update.setVisible(False)
        btn_col.addWidget(self.btn_update)

        self.btn_delete = QPushButton("Delete")
        self.btn_delete.setObjectName("destructive")
        self.btn_delete.setFixedWidth(70)
        self.btn_delete.clicked.connect(self._delete_activity)
        self.btn_delete.setVisible(False)
        btn_col.addWidget(self.btn_delete)

        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setObjectName("secondary")
        self.btn_cancel.setFixedWidth(70)
        self.btn_cancel.clicked.connect(self._cancel_edit)
        self.btn_cancel.setVisible(False)
        btn_col.addWidget(self.btn_cancel)

        row2.addLayout(btn_col)
        form_layout.addLayout(row2)

        layout.addWidget(form_frame)

        # Activity list for the day (scrollable)
        list_header = QHBoxLayout()
        list_title = QLabel("Today's Activities")
        list_title.setStyleSheet("font-weight: bold; font-size: 13px;")
        list_header.addWidget(list_title)
        list_header.addStretch()

        self.total_label = QLabel("")
        self.total_label.setObjectName("subtitle")
        list_header.addWidget(self.total_label)

        btn_export = QPushButton("Export to Vault")
        btn_export.setObjectName("secondary")
        btn_export.clicked.connect(self._export_to_vault)
        list_header.addWidget(btn_export)

        layout.addLayout(list_header)

        self._list_container = QWidget()
        self._list_layout = QVBoxLayout(self._list_container)
        self._list_layout.setContentsMargins(0, 0, 0, 0)
        self._list_layout.setSpacing(3)

        list_scroll = QScrollArea()
        list_scroll.setWidgetResizable(True)
        list_scroll.setWidget(self._list_container)
        list_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        layout.addWidget(list_scroll, 1)

    # ── Navigation ──────────────────────────────────────

    def _prev_day(self):
        self._current_date -= timedelta(days=1)
        self._refresh()

    def _next_day(self):
        self._current_date += timedelta(days=1)
        self._refresh()

    def _go_today(self):
        self._current_date = date.today()
        self._refresh()

    # ── Refresh ─────────────────────────────────────────

    def _refresh(self):
        self.date_label.setText(self._current_date.strftime("%A, %B %d, %Y"))

        activities = self.store.get_for_date(self._current_date.isoformat())
        self.gantt.set_bars(activities)

        # Populate list
        self._clear_layout(self._list_layout)

        total_mins = 0
        for act in activities:
            total_mins += act.duration_minutes
            row = self._make_activity_row(act)
            self._list_layout.addWidget(row)

        if not activities:
            empty = QLabel("No activities logged for this day")
            empty.setObjectName("subtitle")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self._list_layout.addWidget(empty)

        self._list_layout.addStretch()

        hours = total_mins // 60
        mins = total_mins % 60
        self.total_label.setText(f"Total: {hours}h {mins}m")

        # Reset edit state
        self._cancel_edit()

    def _make_activity_row(self, act: Activity) -> QFrame:
        row = QFrame()
        row.setStyleSheet(
            "QFrame { border: 1px solid palette(mid); border-radius: 4px; padding: 4px; }"
        )
        layout = QHBoxLayout(row)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(8)

        # Color dot
        dot = QLabel("\u25cf")
        dot.setStyleSheet(f"color: {act.color}; font-size: 16px; border: none;")
        dot.setFixedWidth(18)
        layout.addWidget(dot)

        # Name
        name = QLabel(act.activity)
        name.setStyleSheet("font-weight: bold; font-size: 12px; border: none;")
        layout.addWidget(name)

        # Time range
        time_lbl = QLabel(f"{act.start_time} – {act.end_time}")
        time_lbl.setObjectName("subtitle")
        time_lbl.setStyleSheet("font-size: 11px; border: none;")
        layout.addWidget(time_lbl)

        # Duration
        dur = QLabel(f"{act.duration_minutes}m")
        dur.setObjectName("subtitle")
        dur.setStyleSheet("font-size: 11px; border: none;")
        dur.setFixedWidth(40)
        layout.addWidget(dur)

        # Notes preview
        if act.notes:
            notes_lbl = QLabel(act.notes[:50] + ("..." if len(act.notes) > 50 else ""))
            notes_lbl.setObjectName("subtitle")
            notes_lbl.setStyleSheet("font-size: 10px; font-style: italic; border: none;")
            layout.addWidget(notes_lbl, 1)
        else:
            layout.addStretch(1)

        # Edit button
        edit_btn = QPushButton("Edit")
        edit_btn.setObjectName("secondary")
        edit_btn.setFixedSize(40, 22)
        edit_btn.setStyleSheet("font-size: 10px; border: 1px solid palette(mid); border-radius: 3px;")
        edit_btn.clicked.connect(lambda _, a=act: self._start_edit(a))
        layout.addWidget(edit_btn)

        return row

    # ── CRUD ────────────────────────────────────────────

    def _add_activity(self):
        activity_name = self.activity_combo.currentText().strip()
        if not activity_name:
            return

        start = self.start_edit.time().toString("HH:mm")
        end = self.end_edit.time().toString("HH:mm")

        if start >= end:
            QMessageBox.warning(self, "Invalid Time", "End time must be after start time.")
            return

        self.store.add(
            date=self._current_date.isoformat(),
            activity=activity_name,
            start_time=start,
            end_time=end,
            notes=self.notes_edit.toPlainText().strip(),
        )
        self._refresh()

    def _start_edit(self, act: Activity):
        self._editing_activity = act
        # Populate form
        idx = self.activity_combo.findText(act.activity)
        if idx >= 0:
            self.activity_combo.setCurrentIndex(idx)
        else:
            self.activity_combo.setCurrentText(act.activity)

        from PyQt6.QtCore import QTime
        sh, sm = map(int, act.start_time.split(":"))
        eh, em = map(int, act.end_time.split(":"))
        self.start_edit.setTime(QTime(sh, sm))
        self.end_edit.setTime(QTime(eh, em))
        self.notes_edit.setPlainText(act.notes)

        self.btn_add.setVisible(False)
        self.btn_update.setVisible(True)
        self.btn_delete.setVisible(True)
        self.btn_cancel.setVisible(True)

    def _update_activity(self):
        if not self._editing_activity:
            return
        act = self._editing_activity
        act.activity = self.activity_combo.currentText().strip()
        act.start_time = self.start_edit.time().toString("HH:mm")
        act.end_time = self.end_edit.time().toString("HH:mm")
        act.notes = self.notes_edit.toPlainText().strip()

        if act.start_time >= act.end_time:
            QMessageBox.warning(self, "Invalid Time", "End time must be after start time.")
            return

        self.store.update(act)
        self._refresh()

    def _delete_activity(self):
        if not self._editing_activity:
            return
        reply = QMessageBox.question(
            self, "Delete Activity",
            f"Delete '{self._editing_activity.activity}' ({self._editing_activity.start_time}–{self._editing_activity.end_time})?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.store.delete(self._editing_activity.id)
            self._refresh()

    def _cancel_edit(self):
        self._editing_activity = None
        self.btn_add.setVisible(True)
        self.btn_update.setVisible(False)
        self.btn_delete.setVisible(False)
        self.btn_cancel.setVisible(False)
        self.notes_edit.clear()

    def _on_bar_selected(self, activity: Activity):
        """Called when user clicks a bar in the Gantt chart."""
        self._start_edit(activity)

    # ── Obsidian export ─────────────────────────────────

    def _export_to_vault(self):
        cfg = load_config()
        vault_path = cfg.get("obsidian_vault_path", "")
        if not vault_path or not Path(vault_path).is_dir():
            QMessageBox.warning(
                self, "No Vault",
                "Set an Obsidian vault path first (Notes > Set Vault).",
            )
            return

        activities = self.store.get_for_date(self._current_date.isoformat())
        if not activities:
            QMessageBox.information(self, "Nothing to Export", "No activities logged for this day.")
            return

        vault = Path(vault_path)
        d = self._current_date
        # Structure: Activity Tracker / YYYY / MM - MonthName / DD - DayName / ActivityName.md
        year_folder = f"{d.year}"
        month_folder = f"{d.month:02d} - {d.strftime('%B')}"
        day_folder = f"{d.day:02d} - {d.strftime('%A')}"

        base = vault / "Activity Tracker" / year_folder / month_folder / day_folder
        base.mkdir(parents=True, exist_ok=True)

        # Write a summary file
        summary_path = base / "_Daily Summary.md"
        total_mins = sum(a.duration_minutes for a in activities)
        hours, mins = divmod(total_mins, 60)

        lines = [
            f"# Activity Summary — {d.strftime('%A, %B %d, %Y')}",
            "",
            f"**Total tracked:** {hours}h {mins}m",
            "",
            "| Time | Activity | Duration | Notes |",
            "|------|----------|----------|-------|",
        ]
        for a in activities:
            dur = f"{a.duration_minutes}m"
            notes = a.notes.replace("\n", " ").replace("|", "/") if a.notes else ""
            lines.append(f"| {a.start_time}–{a.end_time} | {a.activity} | {dur} | {notes} |")

        lines.append("")
        summary_path.write_text("\n".join(lines), encoding="utf-8")

        # Write individual activity files
        for a in activities:
            safe_name = a.activity.replace("/", "-").replace("\\", "-")
            act_path = base / f"{safe_name}.md"
            content = [
                f"# {a.activity}",
                "",
                f"**Date:** {d.isoformat()}",
                f"**Time:** {a.start_time} – {a.end_time}",
                f"**Duration:** {a.duration_minutes} minutes",
                "",
            ]
            if a.notes:
                content.extend(["## Notes", "", a.notes, ""])
            act_path.write_text("\n".join(content), encoding="utf-8")

        QMessageBox.information(
            self, "Exported",
            f"Exported {len(activities)} activities to:\n{base}",
        )

    # ── Helpers ─────────────────────────────────────────

    @staticmethod
    def _clear_layout(layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
