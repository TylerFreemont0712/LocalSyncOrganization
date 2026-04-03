"""Activity Tracker panel — quick-tap card interface + weekly 24-hour grid.

Layout:
  Left (scrollable):  7-column × 24-hour painted block grid
  Right (fixed 380px):
    - Quick-tap category cards (2×3 grid)
    - Today's activity log
    - Manual log form with matching pill picker for category selection
"""

from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path

from PyQt6.QtCore import Qt, QRectF, QPointF, QTimer, QTime, pyqtSignal
from PyQt6.QtGui import (
    QPainter, QColor, QFont, QFontMetrics, QPen, QBrush, QMouseEvent,
)
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QComboBox, QTimeEdit, QPlainTextEdit,
    QFrame, QScrollArea, QMessageBox, QSizePolicy,
    QDialog, QGridLayout, QDialogButtonBox, QLineEdit,
)

from src.config import load_config, save_config
from src.data.activity_store import (
    ActivityStore, Activity,
    DEFAULT_ACTIVITIES, ACTIVITY_COLORS, DEFAULT_COLOR, QUICK_CATEGORIES,
)
from src.ui.widgets.nav_button import NavButton


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Layout constants
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HOUR_H    = 52
HEADER_H  = 44
TIME_W    = 52
DAY_COUNT = 7
TOTAL_H   = HEADER_H + 24 * HOUR_H


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Helpers
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _parse_hhmm(s: str) -> float:
    try:
        h, m = map(int, s.split(":"))
        return h + m / 60.0
    except Exception:
        return 0.0

def _hours_to_px(hours: float) -> float:
    return HEADER_H + hours * HOUR_H

def _px_to_hours(py: float) -> float:
    return max(0.0, min(24.0, (py - HEADER_H) / HOUR_H))

def _fmt_hm(total_minutes: int) -> str:
    h, m = divmod(abs(total_minutes), 60)
    return f"{h}h {m}m" if m else f"{h}h"

def _fmt_elapsed(secs: int) -> str:
    h, rem = divmod(secs, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def _resolve_overlaps(activities: list) -> list[tuple]:
    """Resolve overlapping activities using last-created-wins policy.

    Sorts activities by created_at ascending so the most recently added
    activity claims its time slot, clipping any earlier activities that
    overlap it.

    Returns a list of (activity, start_hours, end_hours) tuples,
    sorted by start_hours, with no overlapping segments.
    """
    if not activities:
        return []

    # Oldest first — newest will overwrite overlapping segments below
    sorted_acts = sorted(activities, key=lambda a: a.created_at or "")

    # Each segment: (start_hour, end_hour, activity)
    segments: list[tuple[float, float, object]] = []

    for act in sorted_acts:
        start = _parse_hhmm(act.start_time)
        end   = _parse_hhmm(act.end_time)
        if end <= start:
            end = 24.0          # midnight-overflow: extend to end of day

        new_segments: list[tuple[float, float, object]] = []
        for (s, e, a) in segments:
            if e <= start or s >= end:
                # No overlap — keep as-is
                new_segments.append((s, e, a))
            else:
                # Partial overlap — keep only the non-overlapping tails
                if s < start:
                    new_segments.append((s, start, a))
                if e > end:
                    new_segments.append((end, e, a))
                # The middle portion [start, end] is claimed by the newer act

        new_segments.append((start, end, act))
        segments = new_segments

    segments.sort(key=lambda x: x[0])
    return segments


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ActivityBlock
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ActivityBlock:
    def __init__(self, activity: Activity, col: int,
                 y_start: float, y_end: float, overflow: bool = False):
        self.activity = activity
        self.col      = col
        self.y_start  = y_start
        self.y_end    = y_end
        self.overflow = overflow
        self.rect     = QRectF()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  WeekBlockWidget
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class WeekBlockWidget(QWidget):
    block_clicked = pyqtSignal(object)
    empty_clicked = pyqtSignal(object, float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._palette: dict = {}
        self._blocks:  list[ActivityBlock] = []
        self._week_start = date.today() - timedelta(days=date.today().weekday())
        self._selected: ActivityBlock | None = None
        self._drag_start: QPointF | None = None
        self.setMinimumHeight(TOTAL_H)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setCursor(Qt.CursorShape.CrossCursor)

    def set_palette(self, palette: dict):
        self._palette = palette
        self.update()

    def load_week(self, week_start: date, activities_by_date: dict):
        self._week_start = week_start
        self._blocks = []
        for col, (d, acts) in enumerate(activities_by_date.items()):
            # Resolve overlaps: latest-created wins for any time slot
            segments = _resolve_overlaps(list(acts))
            for (start_h, end_h, act) in segments:
                y0 = _hours_to_px(start_h)
                y1 = _hours_to_px(end_h)
                # Mark overflow only when the original activity wraps midnight
                orig_start = _parse_hhmm(act.start_time)
                orig_end   = _parse_hhmm(act.end_time)
                overflow   = orig_end <= orig_start
                self._blocks.append(ActivityBlock(act, col, y0, y1, overflow))
        self._selected = None
        self.update()

    def mousePressEvent(self, ev: QMouseEvent):
        if ev.button() != Qt.MouseButton.LeftButton:
            return
        pos = ev.position()
        for b in self._blocks:
            if b.rect.contains(pos):
                self._selected = b
                self.update()
                self.block_clicked.emit(b.activity)
                return
        # Empty click — work out which day/hour
        total_w = self.width() - TIME_W
        col_w   = total_w / DAY_COUNT
        col     = int((pos.x() - TIME_W) / col_w)
        col     = max(0, min(DAY_COUNT - 1, col))
        d       = self._week_start + timedelta(days=col)
        hour    = _px_to_hours(pos.y())
        self.empty_clicked.emit(d, hour)

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        w    = self.width()
        bg   = QColor(self._palette.get("bg",      "#1e1e2e"))
        surf = QColor(self._palette.get("surface", "#313244"))
        bord = QColor(self._palette.get("border",  "#45475a"))
        fg   = QColor(self._palette.get("fg",      "#cdd6f4"))
        mut  = QColor(self._palette.get("muted",   "#7f849c"))
        acc  = QColor(self._palette.get("accent",  "#89b4fa"))
        today = date.today()

        total_w = w - TIME_W
        col_w   = total_w / DAY_COUNT

        # Background
        p.fillRect(0, 0, w, TOTAL_H, bg)

        # Hour grid lines + time labels
        time_font = QFont(); time_font.setPixelSize(10)
        p.setFont(time_font)
        for hour in range(25):
            y = int(_hours_to_px(hour))
            p.setPen(QPen(bord, 1))
            p.drawLine(TIME_W, y, w, y)
            if hour < 24:
                p.setPen(mut)
                p.drawText(0, y, TIME_W - 4, HOUR_H,
                           Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop,
                           f"{hour:02d}:00")

        # Column separators + day headers
        day_names  = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        hdr_font   = QFont(); hdr_font.setPixelSize(11); hdr_font.setBold(True)
        p.setFont(hdr_font)
        for col in range(DAY_COUNT):
            x  = TIME_W + col * col_w
            d  = self._week_start + timedelta(days=col)
            is_today = (d == today)

            # Column background
            if is_today:
                today_bg = QColor(acc); today_bg.setAlpha(15)
                p.fillRect(int(x), HEADER_H, int(col_w), TOTAL_H - HEADER_H, today_bg)

            # Vertical separator
            p.setPen(QPen(bord, 1))
            p.drawLine(int(x), 0, int(x), TOTAL_H)

            # Header cell
            hdr_bg = QColor(acc) if is_today else surf
            p.fillRect(int(x) + 1, 0, int(col_w) - 1, HEADER_H, hdr_bg)

            p.setPen(QColor(self._palette.get("accent_fg", "#1e1e2e")) if is_today else fg)
            label = f"{day_names[col]}\n{d.day}"
            p.drawText(int(x), 0, int(col_w), HEADER_H,
                       Qt.AlignmentFlag.AlignCenter, label)

        # Right border
        p.setPen(QPen(bord, 1))
        p.drawLine(w - 1, 0, w - 1, TOTAL_H)

        # Activity blocks — solid fill, latest-wins segments already resolved
        for b in self._blocks:
            x  = TIME_W + b.col * col_w + 2
            bw = col_w - 4
            by = b.y_start + 1
            bh = max(b.y_end - b.y_start - 2, 4)
            b.rect = QRectF(x, by, bw, bh)

            color = QColor(ACTIVITY_COLORS.get(b.activity.activity, DEFAULT_COLOR))
            fill  = QColor(color)

            is_sel = (b is self._selected)
            if is_sel:
                fill.setAlpha(240)
                p.setPen(QPen(color.lighter(140), 2))
            else:
                fill.setAlpha(200)
                p.setPen(QPen(color.darker(130), 1))

            p.setBrush(QBrush(fill))
            p.drawRoundedRect(b.rect, 4, 4)

            if bh >= 14:
                lf = QFont(); lf.setPixelSize(10 if bh < 32 else 11); lf.setBold(True)
                p.setFont(lf)
                # Contrast: dark text on light blocks, light text on dark blocks
                p.setPen(QColor("#11111b") if color.lightness() > 128 else QColor("#cdd6f4"))
                fm   = QFontMetrics(lf)
                text = ("\u2190 " if b.overflow else "") + b.activity.activity
                etext = fm.elidedText(text, Qt.TextElideMode.ElideRight, int(bw - 8))
                tr = b.rect.adjusted(4, 2, -4, -2)
                if bh >= 32:
                    p.drawText(tr, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop, etext)
                    lf.setPixelSize(9); lf.setBold(False); p.setFont(lf)
                    p.drawText(QRectF(x+4, by+13, bw-8, 12),
                               Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop,
                               f"{b.activity.start_time}\u2013{b.activity.end_time}")
                else:
                    p.drawText(tr, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, etext)

        now = datetime.now()
        if self._week_start <= today <= self._week_start + timedelta(days=6):
            nc = (today - self._week_start).days
            ny = _hours_to_px(now.hour + now.minute / 60)
            x0 = TIME_W + nc * col_w; x1 = x0 + col_w
            nc_color = QColor(self._palette.get("red", "#f38ba8"))
            p.setPen(QPen(nc_color, 2))
            p.drawLine(QPointF(x0, ny), QPointF(x1, ny))
            p.setBrush(QBrush(nc_color)); p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(QPointF(x0, ny), 4, 4)
        p.end()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  NotesDialog
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class NotesDialog(QDialog):
    def __init__(self, parent=None, notes: str = "", title: str = "Activity Notes"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumSize(360, 220)
        self.setModal(True)
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.addWidget(QLabel("Notes (optional):"))
        self.edit = QPlainTextEdit()
        self.edit.setPlainText(notes)
        self.edit.setPlaceholderText("What did you do during this time?")
        self.edit.setMinimumHeight(120)
        layout.addWidget(self.edit)
        btn_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)

    def get_notes(self) -> str:
        return self.edit.toPlainText().strip()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  RenameCategoriesDialog
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class RenameCategoriesDialog(QDialog):
    def __init__(self, categories: list[str], parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Quick Categories")
        self.setMinimumWidth(320)
        self.setModal(True)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Rename the 6 quick-tap categories:"))
        self._edits: list[QLineEdit] = []
        form = QGridLayout(); form.setSpacing(6)
        for i, cat in enumerate(categories):
            lbl  = QLabel(f"Card {i + 1}:")
            edit = QLineEdit(cat)
            self._edits.append(edit)
            form.addWidget(lbl, i, 0); form.addWidget(edit, i, 1)
        layout.addLayout(form)
        btn_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)

    def get_categories(self) -> list[str]:
        return [e.text().strip() or "—" for e in self._edits]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  QuickCard — large pill card for one-tap tracking
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class QuickCard(QFrame):
    tapped = pyqtSignal(str)

    def __init__(self, category: str, parent=None):
        super().__init__(parent)
        self._category = category
        self._active   = False
        self._elapsed_secs    = 0
        self._daily_total_mins = 0
        self._color = ACTIVITY_COLORS.get(category, DEFAULT_COLOR)
        self.setMinimumHeight(78)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._build_ui()
        self._apply_style(active=False)

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(3)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        name_row = QHBoxLayout(); name_row.setSpacing(4)
        self._play_lbl = QLabel()
        self._play_lbl.setFixedWidth(16)
        self._play_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_row.addWidget(self._play_lbl)
        self._name_lbl = QLabel(self._category)
        self._name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._name_lbl.setStyleSheet(
            "font-size:13px;font-weight:bold;background:transparent;border:none;")
        name_row.addWidget(self._name_lbl, 1)
        layout.addLayout(name_row)

        self._time_lbl = QLabel("—")
        self._time_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._time_lbl.setStyleSheet(
            "font-size:11px;font-family:monospace;background:transparent;border:none;")
        layout.addWidget(self._time_lbl)

        self._total_lbl = QLabel("")
        self._total_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._total_lbl.setStyleSheet("font-size:9px;background:transparent;border:none;")
        layout.addWidget(self._total_lbl)

    def set_active(self, active: bool, elapsed_secs: int = 0):
        self._active = active
        self._elapsed_secs = elapsed_secs
        self._refresh_display()
        self._apply_style(active)

    def set_daily_total(self, minutes: int):
        self._daily_total_mins = minutes
        self._refresh_display()

    def tick(self, elapsed_secs: int):
        self._elapsed_secs = elapsed_secs
        self._refresh_display()

    def _refresh_display(self):
        if self._active:
            self._play_lbl.setText("\u25b6")
            self._play_lbl.setStyleSheet(
                f"color:{self._color};font-size:11px;background:transparent;border:none;")
            self._time_lbl.setText(_fmt_elapsed(self._elapsed_secs))
            self._time_lbl.setStyleSheet(
                f"font-size:13px;font-weight:bold;font-family:monospace;"
                f"color:{self._color};background:transparent;border:none;")
            total = self._daily_total_mins + self._elapsed_secs // 60
            self._total_lbl.setText(f"Today: {_fmt_hm(total)}" if total else "Today: just started")
        else:
            self._play_lbl.setText("")
            self._play_lbl.setStyleSheet("background:transparent;border:none;")
            if self._daily_total_mins > 0:
                self._time_lbl.setText(_fmt_hm(self._daily_total_mins))
                self._time_lbl.setStyleSheet(
                    "font-size:12px;font-family:monospace;background:transparent;border:none;")
                self._total_lbl.setText("today")
            else:
                self._time_lbl.setText("—")
                self._time_lbl.setStyleSheet(
                    "font-size:11px;font-family:monospace;background:transparent;border:none;")
                self._total_lbl.setText("")

    def _apply_style(self, active: bool):
        color = self._color
        if active:
            c = QColor(color); c.setAlpha(45)
            bg = c.name(QColor.NameFormat.HexArgb)
            self.setStyleSheet(
                f"QuickCard{{border:2px solid {color};border-radius:12px;"
                f"background-color:{bg};}}")
        else:
            self.setStyleSheet(
                f"QuickCard{{border:1px solid {color}55;border-radius:12px;"
                f"background-color:transparent;}}"
                f"QuickCard:hover{{border:1px solid {color};"
                f"background-color:{color}18;}}")

    def update_category(self, new_name: str):
        self._category = new_name
        self._color    = ACTIVITY_COLORS.get(new_name, DEFAULT_COLOR)
        self._name_lbl.setText(new_name)
        self._apply_style(self._active)

    def mousePressEvent(self, ev):
        if ev.button() == Qt.MouseButton.LeftButton:
            self.tapped.emit(self._category)
        super().mousePressEvent(ev)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  TodayBreakdown
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _make_lbl(text: str, style: str) -> QLabel:
    l = QLabel(text); l.setStyleSheet(style); return l


class TodayBreakdown(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._palette: dict = {}
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(2)

    def set_palette(self, palette: dict):
        self._palette = palette

    def refresh(self, activities: list, active_category=None, session_start=None):
        while self._layout.count():
            child = self._layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        muted = self._palette.get("muted", "#7f849c")

        if not activities and not active_category:
            self._layout.addWidget(_make_lbl(
                "No activity logged today.", f"font-size:10px;color:{muted};"))
            return

        if active_category and session_start:
            color = ACTIVITY_COLORS.get(active_category, DEFAULT_COLOR)
            elapsed_mins = int((datetime.now() - session_start).total_seconds() // 60)
            row = QHBoxLayout(); row.setSpacing(6); row.setContentsMargins(0, 1, 0, 1)
            dot = QLabel("\u25b6"); dot.setFixedWidth(12)
            dot.setStyleSheet(f"color:{color};font-size:10px;")
            row.addWidget(dot)
            name = QLabel(active_category)
            name.setStyleSheet(f"font-size:10px;font-weight:bold;color:{color};")
            row.addWidget(name, 1)
            row.addWidget(_make_lbl(f"{elapsed_mins}m\u2026", f"font-size:10px;color:{color};"))
            w = QWidget(); w.setLayout(row)
            self._layout.addWidget(w)

        for act in reversed(activities):
            color = ACTIVITY_COLORS.get(act.activity, DEFAULT_COLOR)
            row = QHBoxLayout(); row.setSpacing(6); row.setContentsMargins(0, 1, 0, 1)
            dot = QLabel("\u25cf"); dot.setFixedWidth(12)
            dot.setStyleSheet(f"color:{color};font-size:10px;")
            row.addWidget(dot)
            row.addWidget(_make_lbl(act.activity, "font-size:10px;font-weight:bold;"), 1)
            dur = act.duration_minutes
            row.addWidget(_make_lbl(_fmt_hm(dur) if dur > 0 else "\u2014",
                                    f"font-size:10px;color:{muted};"))
            row.addWidget(_make_lbl(f"{act.start_time}\u2013{act.end_time}",
                                    f"font-size:9px;color:{muted};"))
            w = QWidget(); w.setLayout(row)
            self._layout.addWidget(w)

        self._layout.addStretch()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  CategoryPillPicker — compact pill grid for LogForm
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class _SmallPill(QFrame):
    """A single small pill inside CategoryPillPicker."""

    tapped = pyqtSignal(str)

    def __init__(self, category: str, parent=None):
        super().__init__(parent)
        self._category = category
        self._selected = False
        self._color = ACTIVITY_COLORS.get(category, DEFAULT_COLOR)
        self.setMinimumHeight(40)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 4, 6, 4)
        layout.setSpacing(1)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._name_lbl = QLabel(category)
        self._name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._name_lbl.setStyleSheet(
            "font-size:11px;font-weight:bold;background:transparent;border:none;")
        layout.addWidget(self._name_lbl)

        self._apply_style()

    def set_selected(self, selected: bool):
        self._selected = selected
        self._apply_style()

    def update_category(self, name: str):
        self._category = name
        self._color = ACTIVITY_COLORS.get(name, DEFAULT_COLOR)
        self._name_lbl.setText(name)
        self._apply_style()

    def _apply_style(self):
        color = self._color
        if self._selected:
            c = QColor(color); c.setAlpha(50)
            bg = c.name(QColor.NameFormat.HexArgb)
            self.setStyleSheet(
                f"_SmallPill{{border:2px solid {color};border-radius:8px;"
                f"background-color:{bg};}}")
            self._name_lbl.setStyleSheet(
                f"font-size:11px;font-weight:bold;color:{color};"
                "background:transparent;border:none;")
        else:
            self.setStyleSheet(
                f"_SmallPill{{border:1px solid {color}44;border-radius:8px;"
                f"background-color:transparent;}}"
                f"_SmallPill:hover{{border:1px solid {color}aa;"
                f"background-color:{color}15;}}")
            self._name_lbl.setStyleSheet(
                "font-size:11px;font-weight:bold;background:transparent;border:none;")

    def mousePressEvent(self, ev):
        if ev.button() == Qt.MouseButton.LeftButton:
            self.tapped.emit(self._category)
        super().mousePressEvent(ev)


class CategoryPillPicker(QWidget):
    """2×3 grid of small pills + optional custom text field."""

    def __init__(self, categories: list[str], parent=None):
        super().__init__(parent)
        self._pills: list[_SmallPill] = []
        self._selected_cat: str | None = None
        self._build_ui(categories)

    def _build_ui(self, categories: list[str]):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(4)

        grid = QGridLayout(); grid.setSpacing(5)
        for i, cat in enumerate(categories):
            pill = _SmallPill(cat)
            pill.tapped.connect(self._on_pill_tapped)
            self._pills.append(pill)
            grid.addWidget(pill, i // 3, i % 3)
        root.addLayout(grid)

        self._custom = QLineEdit()
        self._custom.setPlaceholderText("Other activity\u2026")
        self._custom.setFixedHeight(26)
        self._custom.setStyleSheet("font-size:11px;")
        self._custom.textChanged.connect(self._on_custom_changed)
        root.addWidget(self._custom)

    def _on_pill_tapped(self, category: str):
        self._custom.blockSignals(True)
        self._custom.clear()
        self._custom.blockSignals(False)
        if self._selected_cat == category:
            self._selected_cat = None
        else:
            self._selected_cat = category
        self._sync_pill_styles()

    def _on_custom_changed(self, text: str):
        if text.strip():
            self._selected_cat = None
            self._sync_pill_styles()

    def _sync_pill_styles(self):
        for pill in self._pills:
            pill.set_selected(pill._category == self._selected_cat)

    def get_activity(self) -> str:
        custom = self._custom.text().strip()
        if custom:
            return custom
        return self._selected_cat or ""

    def set_activity(self, name: str):
        self._custom.blockSignals(True)
        self._custom.clear()
        self._custom.blockSignals(False)
        self._selected_cat = None
        for pill in self._pills:
            if pill._category == name:
                self._selected_cat = name
                break
        if self._selected_cat is None and name:
            self._custom.setText(name)
        self._sync_pill_styles()

    def clear(self):
        self._selected_cat = None
        self._custom.blockSignals(True)
        self._custom.clear()
        self._custom.blockSignals(False)
        self._sync_pill_styles()

    def update_categories(self, categories: list[str]):
        for pill, cat in zip(self._pills, categories):
            pill.update_category(cat)
        if self._selected_cat not in categories:
            self._selected_cat = None
            self._sync_pill_styles()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  LogForm — manual activity entry / edit form
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class LogForm(QWidget):
    activity_added   = pyqtSignal(object)
    activity_updated = pyqtSignal(object)
    activity_deleted = pyqtSignal(str)

    def __init__(self, week_start: date, quick_cats: list[str], parent=None):
        super().__init__(parent)
        self._week_start   = week_start
        self._quick_cats   = quick_cats
        self._editing: Activity | None = None
        self._pending_notes = ""
        self._timer: QTimer | None = None
        self._timer_start: datetime | None = None
        self._palette: dict = {}
        self._build_ui()

    def set_palette(self, palette: dict):
        self._palette = palette

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(5)

        hdr = QHBoxLayout()
        self._form_title = QLabel("Log Activity")
        self._form_title.setStyleSheet("font-size:12px;font-weight:bold;")
        hdr.addWidget(self._form_title); hdr.addStretch()
        self._cancel_btn = QPushButton("Cancel")
        self._cancel_btn.setObjectName("secondary")
        self._cancel_btn.setFixedHeight(24)
        self._cancel_btn.clicked.connect(self._cancel_edit)
        self._cancel_btn.setVisible(False)
        hdr.addWidget(self._cancel_btn)
        root.addLayout(hdr)

        self._pill_picker = CategoryPillPicker(self._quick_cats)
        root.addWidget(self._pill_picker)

        self.day_combo = QComboBox()
        self._rebuild_day_combo()
        root.addWidget(self.day_combo)

        time_row = QHBoxLayout(); time_row.setSpacing(6)
        self._start_lbl = QLabel("Start"); self._start_lbl.setFixedWidth(30)
        muted = "#7f849c"
        self._start_lbl.setStyleSheet(f"font-size:10px;color:{muted};")
        time_row.addWidget(self._start_lbl)
        self.start_edit = QTimeEdit()
        self.start_edit.setDisplayFormat("HH:mm")
        now = datetime.now()
        self.start_edit.setTime(QTime(now.hour, 0))
        time_row.addWidget(self.start_edit, 1)
        time_row.addSpacing(4)
        self._end_lbl = QLabel("End"); self._end_lbl.setFixedWidth(24)
        self._end_lbl.setStyleSheet(f"font-size:10px;color:{muted};")
        time_row.addWidget(self._end_lbl)
        self.end_edit = QTimeEdit()
        self.end_edit.setDisplayFormat("HH:mm")
        self.end_edit.setTime(QTime(min(now.hour + 1, 23), 0))
        time_row.addWidget(self.end_edit, 1)
        root.addLayout(time_row)

        timer_row = QHBoxLayout(); timer_row.setSpacing(6)
        timer_icon = QLabel("\u23f1"); timer_icon.setStyleSheet("font-size:13px;")
        timer_icon.setFixedWidth(18); timer_row.addWidget(timer_icon)
        self._timer_label = QLabel("00:00")
        self._timer_label.setStyleSheet(
            "font-family:monospace;font-size:13px;font-weight:bold;")
        self._timer_label.setMinimumWidth(52)
        timer_row.addWidget(self._timer_label); timer_row.addStretch()
        self._start_btn = QPushButton("Start")
        self._start_btn.setFixedHeight(26)
        self._start_btn.setStyleSheet(
            "background-color:#a6e3a1;color:#1e1e2e;font-weight:bold;"
            "border-radius:4px;padding:2px 10px;font-size:11px;")
        self._start_btn.clicked.connect(self._start_timer)
        timer_row.addWidget(self._start_btn)
        self._stop_btn = QPushButton("Stop")
        self._stop_btn.setFixedHeight(26)
        self._stop_btn.setStyleSheet(
            "background-color:#f38ba8;color:#1e1e2e;font-weight:bold;"
            "border-radius:4px;padding:2px 10px;font-size:11px;")
        self._stop_btn.setEnabled(False)
        self._stop_btn.clicked.connect(self._stop_timer)
        timer_row.addWidget(self._stop_btn)
        root.addLayout(timer_row)

        action_row = QHBoxLayout(); action_row.setSpacing(5)
        self._notes_btn = QPushButton("Notes\u2026")
        self._notes_btn.setObjectName("secondary")
        self._notes_btn.setFixedHeight(26)
        self._notes_btn.clicked.connect(self._open_notes)
        action_row.addWidget(self._notes_btn); action_row.addStretch()
        self._delete_btn = QPushButton("Delete")
        self._delete_btn.setObjectName("destructive")
        self._delete_btn.setFixedHeight(26)
        self._delete_btn.clicked.connect(self._delete)
        self._delete_btn.setVisible(False)
        action_row.addWidget(self._delete_btn)
        self._action_btn = QPushButton("Add")
        self._action_btn.setFixedHeight(26)
        self._action_btn.clicked.connect(self._submit)
        action_row.addWidget(self._action_btn)
        root.addLayout(action_row)

    def set_week_start(self, week_start: date):
        self._week_start = week_start
        self._rebuild_day_combo()

    def update_categories(self, categories: list[str]):
        self._quick_cats = categories
        self._pill_picker.update_categories(categories)

    def prefill(self, d: date, hour: float):
        self._cancel_edit()
        idx = (d - self._week_start).days
        if 0 <= idx < 7: self.day_combo.setCurrentIndex(idx)
        h = int(hour); m = int((hour - h) * 60)
        self.start_edit.setTime(QTime(h, m))
        self.end_edit.setTime(QTime(min(h + 1, 23), m))

    def load_for_edit(self, activity: Activity):
        self._editing       = activity
        self._pending_notes = activity.notes or ""
        self._pill_picker.set_activity(activity.activity)

        act_date = date.fromisoformat(activity.date)
        day_idx  = (act_date - self._week_start).days
        if 0 <= day_idx < 7: self.day_combo.setCurrentIndex(day_idx)

        sh, sm = map(int, activity.start_time.split(":"))
        eh, em = map(int, activity.end_time.split(":"))
        self.start_edit.setTime(QTime(sh, sm))
        self.end_edit.setTime(QTime(eh, em))

        self._form_title.setText("Edit Activity")
        self._action_btn.setText("Update")
        self._cancel_btn.setVisible(True)
        self._delete_btn.setVisible(True)
        self._notes_btn.setText("Notes \u2713" if self._pending_notes else "Notes\u2026")

    def _rebuild_day_combo(self):
        self.day_combo.clear()
        day_names = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        today = date.today()
        for i in range(7):
            d = self._week_start + timedelta(days=i)
            label = f"{day_names[i]} {d.day}" + (" \u2605" if d == today else "")
            self.day_combo.addItem(label, d)
        idx = (today - self._week_start).days
        if 0 <= idx < 7: self.day_combo.setCurrentIndex(idx)

    def _selected_date(self) -> date:
        d = self.day_combo.currentData()
        return d if isinstance(d, date) else self._week_start

    def _submit(self):
        name = self._pill_picker.get_activity().strip()
        if not name: return
        self._stop_timer()
        start = self.start_edit.time().toString("HH:mm")
        end   = self.end_edit.time().toString("HH:mm")
        d     = self._selected_date()
        if self._editing:
            self._editing.activity   = name
            self._editing.date       = d.isoformat()
            self._editing.start_time = start
            self._editing.end_time   = end
            self._editing.notes      = self._pending_notes
            self.activity_updated.emit(self._editing)
            self._cancel_edit()
        else:
            act = ActivityStore().add(date=d.isoformat(), activity=name,
                                      start_time=start, end_time=end,
                                      notes=self._pending_notes)
            self._pending_notes = ""
            self._notes_btn.setText("Notes\u2026")
            self.activity_added.emit(act)

    def _delete(self):
        if not self._editing: return
        reply = QMessageBox.question(
            self, "Delete Activity",
            f"Delete '{self._editing.activity}' "
            f"({self._editing.start_time}\u2013{self._editing.end_time})?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.activity_deleted.emit(self._editing.id)
            self._cancel_edit()

    def _cancel_edit(self):
        self._editing = None
        self._pending_notes = ""
        self._pill_picker.clear()
        self._form_title.setText("Log Activity")
        self._action_btn.setText("Add")
        self._cancel_btn.setVisible(False)
        self._delete_btn.setVisible(False)
        self._notes_btn.setText("Notes\u2026")

    def _open_notes(self):
        dlg = NotesDialog(self, self._pending_notes)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self._pending_notes = dlg.get_notes()
            self._notes_btn.setText(
                "Notes \u2713" if self._pending_notes else "Notes\u2026")

    def _start_timer(self):
        now = datetime.now()
        self._timer_start = now
        self.start_edit.setTime(QTime(now.hour, now.minute))
        self.end_edit.setTime(QTime(now.hour, now.minute))
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(1000)
        self._start_btn.setEnabled(False); self._stop_btn.setEnabled(True)
        self._timer_label.setStyleSheet(
            "font-family:monospace;font-size:13px;font-weight:bold;color:#a6e3a1;")

    def _stop_timer(self):
        if self._timer: self._timer.stop(); self._timer = None
        if self._timer_start:
            now = datetime.now()
            self.end_edit.setTime(QTime(now.hour, now.minute))
        self._timer_start = None
        self._start_btn.setEnabled(True); self._stop_btn.setEnabled(False)
        self._timer_label.setStyleSheet(
            "font-family:monospace;font-size:13px;font-weight:bold;")

    def _tick(self):
        if not self._timer_start: return
        secs = int((datetime.now() - self._timer_start).total_seconds())
        h, s = divmod(secs, 3600); m, s = divmod(s, 60)
        self._timer_label.setText(f"{h:02d}:{m:02d}" if h else f"{m:02d}:{s:02d}")
        now = datetime.now()
        self.end_edit.setTime(QTime(now.hour, now.minute))


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ActivityPanel — main panel
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ActivityPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._palette: dict = {}
        self.store = ActivityStore()
        self._week_start = date.today() - timedelta(days=date.today().weekday())
        self._activities_by_date: dict[date, list[Activity]] = {}

        self._active_category: str | None = None
        self._session_start: datetime | None = None
        self._card_timer: QTimer | None = None

        # NavButton references stored for palette refresh
        self._prev_week_btn: NavButton | None = None
        self._next_week_btn: NavButton | None = None

        self._quick_cats = self._load_quick_cats()
        self._build_ui()
        self._refresh()
        self._schedule_midnight_refresh()

    def _load_quick_cats(self) -> list[str]:
        cfg = load_config()
        saved = cfg.get("activity_quick_categories", [])
        return saved if len(saved) == 6 else list(QUICK_CATEGORIES)

    def _save_quick_cats(self):
        cfg = load_config()
        cfg["activity_quick_categories"] = self._quick_cats
        save_config(cfg)

    # ── Midnight rollover ───────────────────────────

    def _schedule_midnight_refresh(self):
        """Schedule a one-shot timer that fires 5 s after midnight."""
        now = datetime.now()
        next_midnight = (now + timedelta(days=1)).replace(
            hour=0, minute=0, second=5, microsecond=0)
        ms = max(int((next_midnight - now).total_seconds() * 1000), 1000)
        QTimer.singleShot(ms, self._midnight_refresh)

    def _midnight_refresh(self):
        """Called at midnight: snap the week view to contain today, then refresh."""
        today = date.today()
        current_week_start = today - timedelta(days=today.weekday())
        # If the panel is still showing a week that no longer contains today, advance it
        if self._week_start < current_week_start:
            self._week_start = current_week_start
            self._log_form.set_week_start(self._week_start)
        self._refresh()
        self._schedule_midnight_refresh()   # re-arm for the next midnight

    # ── Palette ─────────────────────────────────────

    def set_palette(self, palette: dict):
        self._palette = palette
        self._grid.set_palette(palette)
        self._today_breakdown.set_palette(palette)
        muted   = palette.get("muted",     "#7f849c")
        green   = palette.get("green",     "#a6e3a1")
        red     = palette.get("red",       "#f38ba8")
        acc_fg  = palette.get("accent_fg", "#1e1e2e")
        btn_css = "font-weight:bold;border-radius:4px;padding:2px 10px;font-size:11px;"
        if self._prev_week_btn:
            self._prev_week_btn.refresh(palette)
        if self._next_week_btn:
            self._next_week_btn.refresh(palette)
        if hasattr(self, "_log_form"):
            self._log_form.set_palette(palette)
            if hasattr(self._log_form, "_start_lbl"):
                self._log_form._start_lbl.setStyleSheet(f"font-size:10px;color:{muted};")
                self._log_form._end_lbl.setStyleSheet(f"font-size:10px;color:{muted};")
            if hasattr(self._log_form, "_start_btn"):
                self._log_form._start_btn.setStyleSheet(
                    f"background-color:{green};color:{acc_fg};" + btn_css)
                self._log_form._stop_btn.setStyleSheet(
                    f"background-color:{red};color:{acc_fg};" + btn_css)

    def _build_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0); root.setSpacing(0)

        # ── LEFT: week grid ──
        left = QWidget()
        left_l = QVBoxLayout(left)
        left_l.setContentsMargins(0, 10, 0, 10); left_l.setSpacing(8)

        top_bar = QHBoxLayout(); top_bar.setContentsMargins(14, 0, 8, 0)
        title = QLabel("Activity Tracker"); title.setObjectName("sectionTitle")
        top_bar.addWidget(title); top_bar.addStretch()
        self._week_label = QLabel()
        self._week_label.setStyleSheet("font-size:12px;font-weight:bold;")
        top_bar.addWidget(self._week_label); top_bar.addSpacing(8)

        self._prev_week_btn = NavButton("left", size=28, tooltip="Previous week")
        self._prev_week_btn.clicked.connect(self._prev_week)
        top_bar.addWidget(self._prev_week_btn)

        today_btn = QPushButton("Today")
        today_btn.setObjectName("secondary")
        today_btn.setFixedHeight(28)
        today_btn.clicked.connect(self._go_today)
        top_bar.addWidget(today_btn)

        self._next_week_btn = NavButton("right", size=28, tooltip="Next week")
        self._next_week_btn.clicked.connect(self._next_week)
        top_bar.addWidget(self._next_week_btn)

        top_bar.addSpacing(8)
        btn_exp = QPushButton("Export\u2026"); btn_exp.setObjectName("secondary")
        btn_exp.setFixedHeight(28); btn_exp.clicked.connect(self._export)
        top_bar.addWidget(btn_exp)
        left_l.addLayout(top_bar)

        self._grid = WeekBlockWidget()
        self._grid.block_clicked.connect(self._on_block_clicked)
        self._grid.empty_clicked.connect(self._on_empty_clicked)
        scroll = QScrollArea(); scroll.setWidgetResizable(True)
        scroll.setWidget(self._grid)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        left_l.addWidget(scroll, 1)
        root.addWidget(left, 1)

        # ── RIGHT: cards + breakdown + form ──
        right = QWidget(); right.setFixedWidth(385)
        right_l = QVBoxLayout(right)
        right_l.setContentsMargins(8, 10, 12, 10); right_l.setSpacing(8)

        cards_hdr = QHBoxLayout()
        cards_title = QLabel("Quick Track")
        cards_title.setStyleSheet("font-size:12px;font-weight:bold;")
        cards_hdr.addWidget(cards_title); cards_hdr.addStretch()
        rename_btn = QPushButton("\u2699"); rename_btn.setObjectName("secondary")
        rename_btn.setFixedSize(24, 24)
        rename_btn.setToolTip("Edit category names")
        rename_btn.clicked.connect(self._rename_categories)
        cards_hdr.addWidget(rename_btn)
        right_l.addLayout(cards_hdr)

        cards_grid = QGridLayout(); cards_grid.setSpacing(8)
        self._cards: list[QuickCard] = []
        for i, cat in enumerate(self._quick_cats):
            card = QuickCard(cat); card.tapped.connect(self._on_card_tapped)
            self._cards.append(card)
            cards_grid.addWidget(card, i // 3, i % 3)
        right_l.addLayout(cards_grid)

        div1 = QFrame(); div1.setFrameShape(QFrame.Shape.HLine)
        div1.setObjectName("separator"); right_l.addWidget(div1)

        self._today_breakdown = TodayBreakdown()
        right_l.addWidget(self._today_breakdown)

        div2 = QFrame(); div2.setFrameShape(QFrame.Shape.HLine)
        div2.setObjectName("separator"); right_l.addWidget(div2)

        self._log_form = LogForm(self._week_start, self._quick_cats)
        self._log_form.activity_added.connect(self._on_activity_added)
        self._log_form.activity_updated.connect(self._on_activity_updated)
        self._log_form.activity_deleted.connect(self._on_activity_deleted)
        right_l.addWidget(self._log_form)
        right_l.addStretch()

        root.addWidget(right)

        self._auto_timer = QTimer(self)
        self._auto_timer.setInterval(60_000)
        self._auto_timer.timeout.connect(self._refresh)
        self._auto_timer.start()

    # ── Quick card session management ────────────────

    def _on_card_tapped(self, category: str):
        if self._active_category == category:
            self._stop_session(prompt_notes=True)
        else:
            self._stop_session(prompt_notes=False)
            self._start_session(category)

    def _start_session(self, category: str):
        self._active_category = category
        self._session_start   = datetime.now()
        self._card_timer = QTimer(self)
        self._card_timer.timeout.connect(self._card_tick)
        self._card_timer.start(1000)
        self._update_card_states()
        self._today_breakdown.refresh(
            self._activities_by_date.get(date.today(), []),
            self._active_category, self._session_start)

    def _stop_session(self, prompt_notes: bool = True):
        if not self._active_category or not self._session_start: return
        if self._card_timer:
            self._card_timer.stop(); self._card_timer = None

        category  = self._active_category
        start_dt  = self._session_start
        end_dt    = datetime.now()
        start_str = start_dt.strftime("%H:%M")
        end_str   = "23:59" if end_dt.date() > start_dt.date() else end_dt.strftime("%H:%M")

        notes = ""
        if prompt_notes:
            dlg = NotesDialog(self, title=f"Notes for {category}")
            if dlg.exec() == QDialog.DialogCode.Accepted:
                notes = dlg.get_notes()

        if int((end_dt - start_dt).total_seconds() // 60) >= 1:
            self.store.add(date=start_dt.date().isoformat(), activity=category,
                           start_time=start_str, end_time=end_str, notes=notes)

        self._active_category = None
        self._session_start   = None
        for card in self._cards: card.set_active(False)
        self._refresh()

    def _card_tick(self):
        if not self._session_start or not self._active_category: return
        elapsed = int((datetime.now() - self._session_start).total_seconds())
        for card in self._cards:
            if card._category == self._active_category:
                card.tick(elapsed); break
        self._today_breakdown.refresh(
            self._activities_by_date.get(date.today(), []),
            self._active_category, self._session_start)

    def _update_card_states(self):
        today_acts = self._activities_by_date.get(date.today(), [])
        for card in self._cards:
            cat = card._category
            total_mins = sum(a.duration_minutes for a in today_acts if a.activity == cat)
            card.set_daily_total(total_mins)
            if cat == self._active_category:
                elapsed = int((datetime.now() - self._session_start).total_seconds()) \
                    if self._session_start else 0
                card.set_active(True, elapsed)
            else:
                card.set_active(False)

    def _rename_categories(self):
        dlg = RenameCategoriesDialog(self._quick_cats, self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            new_cats = dlg.get_categories()
            self._quick_cats = new_cats
            self._save_quick_cats()
            for card, cat in zip(self._cards, new_cats):
                card.update_category(cat)
            self._log_form.update_categories(new_cats)
            self._update_card_states()

    # ── Navigation ──────────────────────────────────

    def _prev_week(self):
        self._week_start -= timedelta(weeks=1)
        self._log_form.set_week_start(self._week_start)
        self._refresh()

    def _next_week(self):
        self._week_start += timedelta(weeks=1)
        self._log_form.set_week_start(self._week_start)
        self._refresh()

    def _go_today(self):
        today = date.today()
        self._week_start = today - timedelta(days=today.weekday())
        self._log_form.set_week_start(self._week_start)
        self._refresh()

    # ── Refresh ─────────────────────────────────────

    def _refresh(self):
        we = self._week_start + timedelta(days=6)
        self._week_label.setText(
            f"{self._week_start.strftime('%b %d')} \u2013 {we.strftime('%b %d, %Y')}")
        self._activities_by_date = {}
        for i in range(7):
            d = self._week_start + timedelta(days=i)
            self._activities_by_date[d] = self.store.get_for_date(d.isoformat())
        self._grid.load_week(self._week_start, self._activities_by_date)
        self._update_card_states()
        self._today_breakdown.refresh(
            self._activities_by_date.get(date.today(), []),
            self._active_category, self._session_start)

    # ── Grid callbacks ──────────────────────────────

    def _on_block_clicked(self, activity: Activity):
        self._log_form.load_for_edit(activity)

    def _on_empty_clicked(self, d: date, hour: float):
        self._log_form.prefill(d, hour)

    # ── CRUD callbacks ──────────────────────────────

    def _on_activity_added(self, _: Activity):  self._refresh()

    def _on_activity_updated(self, activity: Activity):
        self.store.update(activity); self._refresh()

    def _on_activity_deleted(self, activity_id: str):
        self.store.delete(activity_id); self._refresh()

    # ── Export ──────────────────────────────────────

    def _export(self):
        cfg = load_config()
        vault_path = cfg.get("obsidian_vault_path", "")
        if not vault_path or not Path(vault_path).is_dir():
            QMessageBox.warning(self, "No Vault",
                "Set an Obsidian vault path first (Notes \u2192 Set Vault).")
            return
        vault = Path(vault_path)
        exported = 0
        for d, activities in self._activities_by_date.items():
            if not activities: continue
            base = (vault / "Activity Tracker" / str(d.year)
                    / f"{d.month:02d} - {d.strftime('%B')}"
                    / f"{d.day:02d} - {d.strftime('%A')}")
            base.mkdir(parents=True, exist_ok=True)
            total_mins = sum(a.duration_minutes for a in activities)
            h, m = divmod(total_mins, 60)
            lines = [
                f"# Activity Summary \u2014 {d.strftime('%A, %B %d, %Y')}",
                "", f"**Total tracked:** {h}h {m}m", "",
                "| Time | Activity | Duration | Notes |",
                "|------|----------|----------|-------|",
            ]
            for a in activities:
                notes = (a.notes or "").replace("\n", " ").replace("|", "/")
                lines.append(f"| {a.start_time}\u2013{a.end_time} | {a.activity} "
                             f"| {a.duration_minutes}m | {notes} |")
            (base / "_Daily Summary.md").write_text("\n".join(lines), encoding="utf-8")
            exported += len(activities)
        we = self._week_start + timedelta(days=6)
        QMessageBox.information(self, "Exported",
            f"Exported {exported} activities for week of "
            f"{self._week_start.strftime('%b %d')} \u2013 {we.strftime('%b %d')}.")