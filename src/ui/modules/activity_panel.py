"""Activity Tracker panel — weekly 24-hour time-block view with efficiency totals.

Layout:
  Left (scrollable):  7-column × 24-hour painted block grid
  Right (fixed 310px): Efficiency panel + compact log form

Features:
  • Stacked colored blocks showing activities proportionally across 24 h
  • Cross-midnight activities drawn across the day boundary
  • "Now" horizontal line on today's column
  • Click a block to select / edit it in the log form
  • Double-click empty space to open add form for that day+time
  • Compact multi-row log form (activity, date, start, end, timer, add)
  • Notes are a pop-out dialog — not shown by default
  • Efficiency panel: weekly totals by activity category + per-day bar chart
"""

from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

from PyQt6.QtCore import Qt, QRectF, QPointF, QTimer, QTime, pyqtSignal
from PyQt6.QtGui import (
    QPainter, QColor, QFont, QFontMetrics, QPen, QBrush,
    QLinearGradient, QMouseEvent,
)
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QComboBox, QTimeEdit, QPlainTextEdit,
    QFrame, QScrollArea, QMessageBox, QSizePolicy,
    QDialog, QGridLayout,
)

from src.config import load_config
from src.data.activity_store import (
    ActivityStore, Activity,
    DEFAULT_ACTIVITIES, ACTIVITY_COLORS, DEFAULT_COLOR,
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Layout constants
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HOUR_H    = 52      # px per hour → 52 × 24 = 1248 px total height
HEADER_H  = 44      # day-name row height
TIME_W    = 52      # left column for hour labels
DAY_COUNT = 7       # Mon–Sun
TOTAL_H   = HEADER_H + 24 * HOUR_H   # 1292


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Helpers
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _parse_hhmm(s: str) -> float:
    """Convert 'HH:MM' to float hours (e.g. '09:30' → 9.5)."""
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


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ActivityBlock  — one drawn block on the grid
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ActivityBlock:
    """Represents one painted rectangle on the weekly grid."""
    def __init__(self, activity: Activity, col: int,
                 y_start: float, y_end: float, overflow: bool = False):
        self.activity  = activity
        self.col       = col
        self.y_start   = y_start   # pixel y of top
        self.y_end     = y_end     # pixel y of bottom
        self.overflow  = overflow  # True = this is the continuation from prev day
        self.rect      = QRectF()  # set during paint (includes column x offset)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  WeekBlockWidget  — fully-painted main calendar body
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class WeekBlockWidget(QWidget):
    """Custom-painted weekly time-block grid."""

    block_clicked  = pyqtSignal(object)    # Activity
    empty_clicked  = pyqtSignal(object, float)  # date, hour_float

    def __init__(self, parent=None):
        super().__init__(parent)
        self._palette: dict = {}
        self._blocks:  list[ActivityBlock] = []
        self._week_start: date = date.today() - timedelta(days=date.today().weekday())
        self._selected: ActivityBlock | None = None
        self._hovered:  ActivityBlock | None = None
        self.setFixedHeight(TOTAL_H)
        self.setMinimumWidth(400)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMouseTracking(True)

    # ── Public API ───────────────────────────────────

    def set_palette(self, palette: dict):
        self._palette = palette; self.update()

    def load_week(self, week_start: date, activities_by_date: dict[date, list[Activity]]):
        self._week_start = week_start
        self._blocks = []
        self._selected = None

        for col in range(DAY_COUNT):
            day = week_start + timedelta(days=col)
            acts = activities_by_date.get(day, [])

            # Also check previous day for any cross-midnight overflows
            prev_day = day - timedelta(days=1)
            for prev_act in activities_by_date.get(prev_day, []):
                sh = _parse_hhmm(prev_act.start_time)
                eh = _parse_hhmm(prev_act.end_time)
                if eh < sh:   # crosses midnight
                    y0 = _hours_to_px(0.0)
                    y1 = _hours_to_px(eh)
                    if y1 > y0:
                        self._blocks.append(ActivityBlock(
                            prev_act, col, y0, y1, overflow=True))

            for act in acts:
                sh = _parse_hhmm(act.start_time)
                eh = _parse_hhmm(act.end_time)
                if eh < sh:
                    # Crosses midnight: draw to bottom of this column
                    self._blocks.append(ActivityBlock(
                        act, col, _hours_to_px(sh), _hours_to_px(24.0)))
                else:
                    self._blocks.append(ActivityBlock(
                        act, col, _hours_to_px(sh), _hours_to_px(eh)))

        self.update()

    def select_activity(self, activity: Activity | None):
        if activity is None:
            self._selected = None
        else:
            for b in self._blocks:
                if b.activity.id == activity.id:
                    self._selected = b; break
        self.update()

    # ── Mouse ────────────────────────────────────────

    def _col_x(self, col: int) -> float:
        col_w = (self.width() - TIME_W) / DAY_COUNT
        return TIME_W + col * col_w

    def _col_width(self) -> float:
        return (self.width() - TIME_W) / DAY_COUNT

    def _block_at(self, pos: QPointF) -> ActivityBlock | None:
        for b in reversed(self._blocks):   # top = last drawn = front
            if b.rect.contains(pos):
                return b
        return None

    def _pos_to_col_hour(self, pos: QPointF):
        cw = self._col_width()
        col = int((pos.x() - TIME_W) / cw)
        col = max(0, min(DAY_COUNT - 1, col))
        hour = _px_to_hours(pos.y())
        return col, hour

    def mousePressEvent(self, ev: QMouseEvent):
        b = self._block_at(ev.position())
        if b:
            self._selected = b; self.update()
            self.block_clicked.emit(b.activity)
        else:
            self._selected = None; self.update()

    def mouseDoubleClickEvent(self, ev: QMouseEvent):
        b = self._block_at(ev.position())
        if not b:
            col, hour = self._pos_to_col_hour(ev.position())
            d = self._week_start + timedelta(days=col)
            self.empty_clicked.emit(d, hour)

    def mouseMoveEvent(self, ev: QMouseEvent):
        b = self._block_at(ev.position())
        if b != self._hovered:
            self._hovered = b
            if b:
                a = b.activity
                tip = f"{a.activity}\n{a.start_time} – {a.end_time}  ({a.duration_minutes}m)"
                if a.notes: tip += f"\n{a.notes}"
                self.setToolTip(tip)
            else:
                self.setToolTip("")
            self.update()

    # ── Paint ────────────────────────────────────────

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w = self.width()

        bg     = QColor(self._palette.get("bg",        "#1e1e2e"))
        surf   = QColor(self._palette.get("surface",   "#313244"))
        border = QColor(self._palette.get("border",    "#45475a"))
        fg     = QColor(self._palette.get("fg",        "#cdd6f4"))
        muted  = QColor(self._palette.get("muted",     "#7f849c"))
        accent = QColor(self._palette.get("accent",    "#89b4fa"))
        hdr_bg = QColor(self._palette.get("header_bg", "#181825"))

        col_w  = self._col_width()

        # ── Background ───────────────────────────────
        p.fillRect(0, 0, w, TOTAL_H, bg)
        p.fillRect(0, 0, w, HEADER_H, hdr_bg)

        # ── Hour grid lines ──────────────────────────
        hour_font = QFont(); hour_font.setPixelSize(9)
        p.setFont(hour_font)
        for h in range(25):
            y = _hours_to_px(h)
            is_major = (h % 6 == 0)
            c = QColor(border)
            if is_major: c.setAlpha(200)
            else:        c.setAlpha(80)
            p.setPen(QPen(c, 1 if is_major else 0.5))
            p.drawLine(QPointF(TIME_W, y), QPointF(w, y))

            if h < 24:
                lbl = f"{h:02d}:00"
                p.setPen(muted if h % 6 else fg)
                p.drawText(QRectF(0, y + 1, TIME_W - 4, HOUR_H - 2),
                           Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop, lbl)

        # ── Column dividers + day headers ─────────────
        today = date.today()
        day_font = QFont(); day_font.setPixelSize(11); day_font.setBold(True)
        num_font  = QFont(); num_font.setPixelSize(15); num_font.setBold(True)

        for col in range(DAY_COUNT):
            x = TIME_W + col * col_w
            d = self._week_start + timedelta(days=col)
            is_today = (d == today)
            is_weekend = (col >= 5)

            # Column background (weekend slightly tinted)
            if is_weekend:
                tint = QColor(surf)
                tint.setAlpha(30)
                p.fillRect(QRectF(x, HEADER_H, col_w, TOTAL_H - HEADER_H), QBrush(tint))

            # Column divider
            if col > 0:
                p.setPen(QPen(border, 1))
                p.drawLine(QPointF(x, 0), QPointF(x, TOTAL_H))

            # Day header
            if is_today:
                p.fillRect(QRectF(x, 0, col_w, HEADER_H), QBrush(accent))
                text_c = QColor(self._palette.get("accent_fg", "#1e1e2e"))
            else:
                text_c = fg

            p.setPen(text_c)
            p.setFont(day_font)
            p.drawText(QRectF(x, 4, col_w, 18),
                       Qt.AlignmentFlag.AlignCenter, d.strftime("%a").upper())
            p.setFont(num_font)
            p.drawText(QRectF(x, 20, col_w, 22),
                       Qt.AlignmentFlag.AlignCenter, str(d.day))

        # Time-label column border
        p.setPen(QPen(border, 1))
        p.drawLine(QPointF(TIME_W, 0), QPointF(TIME_W, TOTAL_H))

        # ── Activity blocks ──────────────────────────
        for b in self._blocks:
            x    = TIME_W + b.col * col_w
            bx   = x + 2
            bw   = col_w - 4
            by   = b.y_start
            bh   = b.y_end - b.y_start
            if bh < 1: continue
            b.rect = QRectF(bx, by, bw, bh)

            color = QColor(b.activity.color)
            is_sel = (b is self._selected)
            is_hov = (b is self._hovered)

            if b.overflow:
                color.setAlpha(160)
            if is_sel:   color = color.lighter(135)
            elif is_hov: color = color.lighter(115)

            p.setBrush(QBrush(color))
            p.setPen(QPen(color.lighter(160), 1) if is_sel else Qt.PenStyle.NoPen)
            p.drawRoundedRect(b.rect, 3, 3)

            # Label
            if bh >= 18:
                lbl_font = QFont()
                lbl_font.setPixelSize(10 if bh < 32 else 11)
                lbl_font.setBold(True)
                p.setFont(lbl_font)
                # Dark text on light block
                p.setPen(QColor("#11111b") if color.lightness() > 128
                         else QColor("#cdd6f4"))
                fm = QFontMetrics(lbl_font)
                text = b.activity.activity
                if b.overflow: text = "← " + text
                etext = fm.elidedText(text, Qt.TextElideMode.ElideRight, int(bw - 8))
                text_rect = b.rect.adjusted(4, 2, -4, -2)
                if bh >= 32:
                    p.drawText(text_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop, etext)
                    # Time hint on second line
                    lbl_font.setPixelSize(9); lbl_font.setBold(False); p.setFont(lbl_font)
                    time_lbl = f"{b.activity.start_time}–{b.activity.end_time}"
                    time_rect = QRectF(b.rect.x()+4, b.rect.y()+13, bw-8, 12)
                    p.drawText(time_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop, time_lbl)
                else:
                    p.drawText(text_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, etext)

        # ── "Now" indicator ──────────────────────────
        now = datetime.now()
        if self._week_start <= today <= self._week_start + timedelta(days=6):
            now_col = (today - self._week_start).days
            now_y   = _hours_to_px(now.hour + now.minute / 60)
            x0 = TIME_W + now_col * col_w
            x1 = x0 + col_w
            now_color = QColor(self._palette.get("red", "#f38ba8"))
            p.setPen(QPen(now_color, 2))
            p.drawLine(QPointF(x0, now_y), QPointF(x1, now_y))
            # Small circle at left edge
            p.setBrush(QBrush(now_color)); p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(QPointF(x0, now_y), 4, 4)

        p.end()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  NotesDialog
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class NotesDialog(QDialog):
    def __init__(self, parent=None, notes: str = ""):
        super().__init__(parent)
        self.setWindowTitle("Activity Notes")
        self.setMinimumSize(340, 200)
        self.setModal(True)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Notes (optional):"))
        self.edit = QPlainTextEdit()
        self.edit.setPlainText(notes)
        self.edit.setPlaceholderText("Add notes for this activity…")
        layout.addWidget(self.edit)
        btn_row = QHBoxLayout()
        cancel = QPushButton("Cancel"); cancel.setObjectName("secondary")
        cancel.clicked.connect(self.reject)
        ok = QPushButton("OK"); ok.setDefault(True); ok.clicked.connect(self.accept)
        btn_row.addStretch(); btn_row.addWidget(cancel); btn_row.addWidget(ok)
        layout.addLayout(btn_row)

    def get_notes(self) -> str:
        return self.edit.toPlainText().strip()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  FillBar — a proper auto-resizing percentage bar
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class FillBar(QWidget):
    """A horizontal bar that fills to a percentage of its parent width."""

    def __init__(self, ratio: float, fill_color: str, bg_color: str,
                 height: int = 6, parent=None):
        super().__init__(parent)
        self._ratio = max(0.0, min(1.0, ratio))
        self._fill_color = fill_color
        self._bg_color = bg_color
        self.setFixedHeight(height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def paintEvent(self, ev):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        r = h / 2

        # Background track
        p.setBrush(QBrush(QColor(self._bg_color)))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(0, 0, w, h, r, r)

        # Fill
        if self._ratio > 0:
            fill_w = max(h, int(w * self._ratio))  # at least pill-shaped
            p.setBrush(QBrush(QColor(self._fill_color)))
            p.drawRoundedRect(0, 0, fill_w, h, r, r)

        p.end()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  EfficiencyPanel  — right-side totals + mini bar chart
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class EfficiencyPanel(QWidget):
    """Shows weekly activity totals and a per-day summary."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._palette: dict = {}
        self._build_ui()

    def set_palette(self, palette: dict):
        self._palette = palette; self.update()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        hdr = QLabel("Week Efficiency")
        hdr.setStyleSheet("font-size:13px;font-weight:bold;")
        layout.addWidget(hdr)

        self._totals_lbl  = QLabel("—")
        self._totals_lbl.setStyleSheet("font-size:11px;")
        layout.addWidget(self._totals_lbl)

        self._today_lbl = QLabel("")
        self._today_lbl.setStyleSheet("font-size:10px;font-weight:bold;")
        layout.addWidget(self._today_lbl)

        div = QFrame(); div.setFrameShape(QFrame.Shape.HLine)
        div.setObjectName("separator"); layout.addWidget(div)

        self._bar_container = QWidget()
        self._bar_layout    = QVBoxLayout(self._bar_container)
        self._bar_layout.setContentsMargins(0, 0, 0, 0)
        self._bar_layout.setSpacing(4)
        layout.addWidget(self._bar_container)

        div2 = QFrame(); div2.setFrameShape(QFrame.Shape.HLine)
        div2.setObjectName("separator"); layout.addWidget(div2)

        daily_hdr = QLabel("Daily totals")
        daily_hdr.setStyleSheet("font-size:11px;font-weight:bold;")
        layout.addWidget(daily_hdr)

        self._daily_container = QWidget()
        self._daily_layout    = QVBoxLayout(self._daily_container)
        self._daily_layout.setContentsMargins(0, 0, 0, 0)
        self._daily_layout.setSpacing(3)
        layout.addWidget(self._daily_container)
        layout.addStretch()

    def update_data(self, week_start: date, activities_by_date: dict[date, list[Activity]]):
        # ── Category totals ──────────────────────────
        by_name: dict[str, int] = defaultdict(int)
        total_mins = 0
        for acts in activities_by_date.values():
            for a in acts:
                by_name[a.activity] += a.duration_minutes
                total_mins += a.duration_minutes

        # Proper average per day
        avg_mins_per_day = total_mins / 7
        avg_h = int(avg_mins_per_day) // 60
        avg_m = int(avg_mins_per_day) % 60
        avg_str = f"{avg_h}h {avg_m}m" if avg_m else f"{avg_h}h"

        self._totals_lbl.setText(
            f"Tracked: {_fmt_hm(total_mins)}  ·  ~{avg_str}/day"
        )

        # Today's total
        today = date.today()
        today_acts = activities_by_date.get(today, [])
        today_mins = sum(a.duration_minutes for a in today_acts)
        accent = self._palette.get("accent", "#89b4fa")
        green = self._palette.get("green", "#a6e3a1")
        if today_mins > 0:
            self._today_lbl.setText(f"Today: {_fmt_hm(today_mins)}")
            self._today_lbl.setStyleSheet(
                f"font-size:10px;font-weight:bold;color:{green};")
        else:
            self._today_lbl.setText("Today: —")
            self._today_lbl.setStyleSheet(
                f"font-size:10px;font-weight:bold;color:{self._palette.get('muted','#7f849c')};")

        # Clear bar rows
        while self._bar_layout.count():
            child = self._bar_layout.takeAt(0)
            if child.widget(): child.widget().deleteLater()

        max_mins = max(by_name.values(), default=1)
        for name, mins in sorted(by_name.items(), key=lambda x: -x[1])[:10]:
            color = ACTIVITY_COLORS.get(name, DEFAULT_COLOR)
            row = self._make_bar_row(name, mins, max_mins, color)
            self._bar_layout.addWidget(row)

        # ── Daily totals ─────────────────────────────
        while self._daily_layout.count():
            child = self._daily_layout.takeAt(0)
            if child.widget(): child.widget().deleteLater()

        day_labels = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        day_totals = []
        for i in range(7):
            d = week_start + timedelta(days=i)
            acts = activities_by_date.get(d, [])
            day_totals.append(sum(a.duration_minutes for a in acts))

        max_day = max(day_totals, default=1) or 1
        for i, (label, mins) in enumerate(zip(day_labels, day_totals)):
            d = week_start + timedelta(days=i)
            is_today = (d == today)
            row = self._make_day_row(label, mins, max_day, is_today)
            self._daily_layout.addWidget(row)

    def _make_bar_row(self, name: str, mins: int, max_mins: int, color: str) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w); layout.setContentsMargins(0,2,0,0); layout.setSpacing(1)

        top_row = QHBoxLayout(); top_row.setSpacing(4)
        name_lbl = QLabel(name)
        name_lbl.setStyleSheet("font-size:11px;")
        top_row.addWidget(name_lbl, 1)
        mins_lbl = QLabel(_fmt_hm(mins))
        mins_lbl.setStyleSheet("font-size:10px;font-weight:bold;")
        top_row.addWidget(mins_lbl)
        layout.addLayout(top_row)

        ratio = mins / max(max_mins, 1)
        bg_c = self._palette.get('border', '#45475a')
        bar = FillBar(ratio, color, bg_c, height=6)
        layout.addWidget(bar)

        return w

    def _make_day_row(self, label: str, mins: int, max_mins: int,
                      is_today: bool) -> QWidget:
        w = QWidget(); layout = QHBoxLayout(w)
        layout.setContentsMargins(0,1,0,1); layout.setSpacing(6)

        lbl = QLabel(label)
        lbl.setFixedWidth(28)
        lbl.setStyleSheet(
            f"font-size:10px;font-weight:bold;"
            f"color:{self._palette.get('accent','#89b4fa') if is_today else self._palette.get('muted','#7f849c')};")
        layout.addWidget(lbl)

        ratio = mins / max(max_mins, 1)
        accent_c = self._palette.get("accent","#89b4fa") if is_today else \
                   self._palette.get("green","#a6e3a1")
        bg_c = self._palette.get('border', '#45475a')
        bar = FillBar(ratio if mins > 0 else 0, accent_c, bg_c, height=8)
        layout.addWidget(bar, 1)

        time_lbl = QLabel(_fmt_hm(mins) if mins else "—")
        time_lbl.setFixedWidth(40)
        time_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        time_lbl.setStyleSheet("font-size:10px;")
        layout.addWidget(time_lbl)
        return w


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  LogForm  — redesigned multi-row activity entry
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class LogForm(QWidget):
    """Compact activity log form docked at the bottom of the right panel."""

    activity_added   = pyqtSignal(object)   # Activity
    activity_updated = pyqtSignal(object)   # Activity
    activity_deleted = pyqtSignal(str)      # id

    def __init__(self, week_start: date, parent=None):
        super().__init__(parent)
        self._week_start = week_start
        self._editing: Activity | None = None
        self._pending_notes: str = ""
        self._timer: QTimer | None = None
        self._timer_start: datetime | None = None
        self._build_ui()

    # ── Build ────────────────────────────────────────

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(6)

        # ── Header row ──
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

        # ── Row 1: Activity name (full width) ──
        self.activity_combo = QComboBox()
        self.activity_combo.setEditable(True)
        self.activity_combo.addItems(DEFAULT_ACTIVITIES)
        self.activity_combo.setPlaceholderText("Activity…")
        root.addWidget(self.activity_combo)

        # ── Row 2: Day selector (full width) ──
        self.day_combo = QComboBox()
        self._rebuild_day_combo()
        root.addWidget(self.day_combo)

        # ── Row 3: Start + End times ──
        time_row = QHBoxLayout(); time_row.setSpacing(6)

        start_lbl = QLabel("Start")
        start_lbl.setStyleSheet("font-size:10px;color:palette(mid);")
        start_lbl.setFixedWidth(30)
        time_row.addWidget(start_lbl)
        self.start_edit = QTimeEdit()
        self.start_edit.setDisplayFormat("HH:mm")
        now = datetime.now()
        self.start_edit.setTime(QTime(now.hour, 0))
        time_row.addWidget(self.start_edit, 1)

        time_row.addSpacing(4)

        end_lbl = QLabel("End")
        end_lbl.setStyleSheet("font-size:10px;color:palette(mid);")
        end_lbl.setFixedWidth(24)
        time_row.addWidget(end_lbl)
        self.end_edit = QTimeEdit()
        self.end_edit.setDisplayFormat("HH:mm")
        self.end_edit.setTime(QTime(min(now.hour + 1, 23), 0))
        time_row.addWidget(self.end_edit, 1)

        root.addLayout(time_row)

        # ── Row 4: Timer (dedicated row) ──
        timer_row = QHBoxLayout(); timer_row.setSpacing(6)

        timer_icon = QLabel("⏱")
        timer_icon.setStyleSheet("font-size:13px;")
        timer_icon.setFixedWidth(18)
        timer_row.addWidget(timer_icon)

        self._timer_label = QLabel("00:00")
        self._timer_label.setStyleSheet(
            "font-family:monospace;font-size:13px;font-weight:bold;")
        self._timer_label.setMinimumWidth(52)
        timer_row.addWidget(self._timer_label)

        timer_row.addStretch()

        self._start_btn = QPushButton("▶ Start")
        self._start_btn.setToolTip("Start timer")
        self._start_btn.setFixedHeight(26)
        self._start_btn.setStyleSheet(
            "background-color:#a6e3a1;color:#1e1e2e;font-weight:bold;"
            "border-radius:4px;padding:2px 10px;font-size:11px;")
        self._start_btn.clicked.connect(self._start_timer)
        timer_row.addWidget(self._start_btn)

        self._stop_btn = QPushButton("■ Stop")
        self._stop_btn.setToolTip("Stop timer")
        self._stop_btn.setFixedHeight(26)
        self._stop_btn.setStyleSheet(
            "background-color:#f38ba8;color:#1e1e2e;font-weight:bold;"
            "border-radius:4px;padding:2px 10px;font-size:11px;")
        self._stop_btn.setEnabled(False)
        self._stop_btn.clicked.connect(self._stop_timer)
        timer_row.addWidget(self._stop_btn)

        root.addLayout(timer_row)

        # ── Row 5: Notes + action buttons ──
        action_row = QHBoxLayout(); action_row.setSpacing(5)

        self._notes_btn = QPushButton("Notes…")
        self._notes_btn.setObjectName("secondary")
        self._notes_btn.setFixedHeight(26)
        self._notes_btn.clicked.connect(self._open_notes)
        action_row.addWidget(self._notes_btn)

        action_row.addStretch()

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

    # ── Public ───────────────────────────────────────

    def set_week_start(self, week_start: date):
        self._week_start = week_start
        self._rebuild_day_combo()

    def prefill(self, d: date, hour: float):
        """Called when user double-clicks empty space on the grid."""
        self._cancel_edit()
        idx = (d - self._week_start).days
        if 0 <= idx < 7:
            self.day_combo.setCurrentIndex(idx)
        h = int(hour); m = int((hour - h) * 60)
        self.start_edit.setTime(QTime(h, m))
        self.end_edit.setTime(QTime(min(h + 1, 23), m))

    def load_for_edit(self, activity: Activity):
        """Populate form fields with an existing activity for editing."""
        self._editing = activity
        self._pending_notes = activity.notes or ""

        idx = self.activity_combo.findText(activity.activity)
        if idx >= 0: self.activity_combo.setCurrentIndex(idx)
        else:        self.activity_combo.setCurrentText(activity.activity)

        act_date = date.fromisoformat(activity.date)
        day_idx = (act_date - self._week_start).days
        if 0 <= day_idx < 7: self.day_combo.setCurrentIndex(day_idx)

        sh, sm = map(int, activity.start_time.split(":"))
        eh, em = map(int, activity.end_time.split(":"))
        self.start_edit.setTime(QTime(sh, sm))
        self.end_edit.setTime(QTime(eh, em))

        self._form_title.setText("Edit Activity")
        self._action_btn.setText("Update")
        self._cancel_btn.setVisible(True)
        self._delete_btn.setVisible(True)

    # ── Private ──────────────────────────────────────

    def _rebuild_day_combo(self):
        self.day_combo.clear()
        day_names = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        today = date.today()
        for i in range(7):
            d = self._week_start + timedelta(days=i)
            label = f"{day_names[i]} {d.day}"
            if d == today: label += " ★"
            self.day_combo.addItem(label, d)
        # Default to today if in range
        idx = (today - self._week_start).days
        if 0 <= idx < 7: self.day_combo.setCurrentIndex(idx)

    def _selected_date(self) -> date:
        d = self.day_combo.currentData()
        return d if isinstance(d, date) else self._week_start

    def _submit(self):
        name = self.activity_combo.currentText().strip()
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
            store = ActivityStore()
            act = store.add(date=d.isoformat(), activity=name,
                            start_time=start, end_time=end,
                            notes=self._pending_notes)
            self._pending_notes = ""
            self.activity_added.emit(act)

    def _delete(self):
        if not self._editing: return
        reply = QMessageBox.question(
            self, "Delete Activity",
            f"Delete '{self._editing.activity}' ({self._editing.start_time}–{self._editing.end_time})?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.activity_deleted.emit(self._editing.id)
            self._cancel_edit()

    def _cancel_edit(self):
        self._editing = None
        self._pending_notes = ""
        self._form_title.setText("Log Activity")
        self._action_btn.setText("Add")
        self._cancel_btn.setVisible(False)
        self._delete_btn.setVisible(False)

    def _open_notes(self):
        dlg = NotesDialog(self, self._pending_notes)
        if dlg.exec():
            self._pending_notes = dlg.get_notes()

    def _start_timer(self):
        now = datetime.now()
        self._timer_start = now
        self.start_edit.setTime(QTime(now.hour, now.minute))
        self.end_edit.setTime(QTime(now.hour, now.minute))
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(1000)
        self._start_btn.setEnabled(False)
        self._stop_btn.setEnabled(True)
        self._timer_label.setStyleSheet(
            "font-family:monospace;font-size:13px;font-weight:bold;color:#a6e3a1;")

    def _stop_timer(self):
        if self._timer:
            self._timer.stop(); self._timer = None
        if self._timer_start:
            now = datetime.now()
            self.end_edit.setTime(QTime(now.hour, now.minute))
        self._timer_start = None
        self._start_btn.setEnabled(True)
        self._stop_btn.setEnabled(False)
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
#  ActivityPanel  — main panel
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ActivityPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.store = ActivityStore()
        self._palette: dict = {}
        self._week_start = date.today() - timedelta(days=date.today().weekday())
        self._activities_by_date: dict[date, list[Activity]] = {}
        self._build_ui()
        self._refresh()

    # ── Palette ─────────────────────────────────────

    def set_palette(self, palette: dict):
        self._palette = palette
        self._grid.set_palette(palette)
        self._efficiency.set_palette(palette)

    # ── Build UI ────────────────────────────────────

    def _build_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ══ LEFT: scrollable week grid ══
        left = QWidget()
        left_l = QVBoxLayout(left)
        left_l.setContentsMargins(0, 10, 0, 10)
        left_l.setSpacing(8)

        # Top bar
        top_bar = QHBoxLayout(); top_bar.setContentsMargins(14, 0, 8, 0)
        title = QLabel("Activity Tracker"); title.setObjectName("sectionTitle")
        top_bar.addWidget(title); top_bar.addStretch()

        self._week_label = QLabel()
        self._week_label.setStyleSheet("font-size:12px;font-weight:bold;")
        top_bar.addWidget(self._week_label); top_bar.addSpacing(8)

        btn_prev = QPushButton("‹"); btn_prev.setObjectName("secondary")
        btn_prev.setFixedSize(28, 28); btn_prev.setToolTip("Previous week")
        btn_prev.clicked.connect(self._prev_week); top_bar.addWidget(btn_prev)

        btn_today = QPushButton("Today"); btn_today.setObjectName("secondary")
        btn_today.setFixedHeight(28); btn_today.clicked.connect(self._go_today)
        top_bar.addWidget(btn_today)

        btn_next = QPushButton("›"); btn_next.setObjectName("secondary")
        btn_next.setFixedSize(28, 28); btn_next.setToolTip("Next week")
        btn_next.clicked.connect(self._next_week); top_bar.addWidget(btn_next)

        top_bar.addSpacing(8)
        btn_export = QPushButton("Export…"); btn_export.setObjectName("secondary")
        btn_export.setFixedHeight(28); btn_export.clicked.connect(self._export)
        top_bar.addWidget(btn_export)

        left_l.addLayout(top_bar)

        # Grid inside scroll area
        self._grid = WeekBlockWidget()
        self._grid.block_clicked.connect(self._on_block_clicked)
        self._grid.empty_clicked.connect(self._on_empty_clicked)

        scroll = QScrollArea(); scroll.setWidgetResizable(True)
        scroll.setWidget(self._grid)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        left_l.addWidget(scroll, 1)
        root.addWidget(left, 1)

        # ══ RIGHT: efficiency + log form ══
        right = QWidget(); right.setFixedWidth(310)
        right_l = QVBoxLayout(right)
        right_l.setContentsMargins(8, 10, 12, 10)
        right_l.setSpacing(10)

        self._efficiency = EfficiencyPanel()
        right_l.addWidget(self._efficiency, 1)

        div = QFrame(); div.setFrameShape(QFrame.Shape.HLine)
        div.setObjectName("separator"); right_l.addWidget(div)

        self._log_form = LogForm(self._week_start)
        self._log_form.activity_added.connect(self._on_activity_added)
        self._log_form.activity_updated.connect(self._on_activity_updated)
        self._log_form.activity_deleted.connect(self._on_activity_deleted)
        right_l.addWidget(self._log_form)

        root.addWidget(right)

        # Auto-refresh timer
        self._auto_timer = QTimer(self)
        self._auto_timer.setInterval(60_000)
        self._auto_timer.timeout.connect(self._refresh)
        self._auto_timer.start()

    # ── Navigation ───────────────────────────────────

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
            f"{self._week_start.strftime('%b %d')} – {we.strftime('%b %d, %Y')}"
        )

        self._activities_by_date = {}
        for i in range(7):
            d = self._week_start + timedelta(days=i)
            self._activities_by_date[d] = self.store.get_for_date(d.isoformat())

        self._grid.load_week(self._week_start, self._activities_by_date)
        self._efficiency.update_data(self._week_start, self._activities_by_date)

    # ── Grid callbacks ───────────────────────────────

    def _on_block_clicked(self, activity: Activity):
        self._log_form.load_for_edit(activity)

    def _on_empty_clicked(self, d: date, hour: float):
        self._log_form.prefill(d, hour)

    # ── CRUD callbacks ───────────────────────────────

    def _on_activity_added(self, _activity: Activity):
        self._refresh()

    def _on_activity_updated(self, activity: Activity):
        self.store.update(activity)
        self._refresh()

    def _on_activity_deleted(self, activity_id: str):
        self.store.delete(activity_id)
        self._refresh()

    # ── Export ───────────────────────────────────────

    def _export(self):
        cfg = load_config()
        vault_path = cfg.get("obsidian_vault_path", "")
        if not vault_path or not Path(vault_path).is_dir():
            QMessageBox.warning(
                self, "No Vault",
                "Set an Obsidian vault path first (Notes → Set Vault)."
            )
            return

        vault = Path(vault_path)
        exported = 0
        for d, activities in self._activities_by_date.items():
            if not activities: continue
            year_f  = str(d.year)
            month_f = f"{d.month:02d} - {d.strftime('%B')}"
            day_f   = f"{d.day:02d} - {d.strftime('%A')}"
            base = vault / "Activity Tracker" / year_f / month_f / day_f
            base.mkdir(parents=True, exist_ok=True)

            total_mins = sum(a.duration_minutes for a in activities)
            h, m = divmod(total_mins, 60)
            lines = [
                f"# Activity Summary — {d.strftime('%A, %B %d, %Y')}",
                "", f"**Total tracked:** {h}h {m}m", "",
                "| Time | Activity | Duration | Notes |",
                "|------|----------|----------|-------|",
            ]
            for a in activities:
                notes = (a.notes or "").replace("\n"," ").replace("|","/")
                lines.append(f"| {a.start_time}–{a.end_time} | {a.activity} | {a.duration_minutes}m | {notes} |")
            (base / "_Daily Summary.md").write_text("\n".join(lines), encoding="utf-8")
            exported += len(activities)

        we = self._week_start + timedelta(days=6)
        QMessageBox.information(
            self, "Exported",
            f"Exported {exported} activities for week of "
            f"{self._week_start.strftime('%b %d')} – {we.strftime('%b %d')}."
        )