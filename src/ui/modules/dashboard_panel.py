"""Dashboard panel — overview of tasks, upcoming deadlines, and productivity stats.

New in this version:
  • SideIncomeGoalSection — prominent month-browsable side income goal tracker
    with a color-coded progress bar (red → green → blue glow at major goal).
  • Goal data stored in side_income_goals table via FinanceStore.set_goal()
"""

import calendar as _calendar
from datetime import date, datetime, timedelta

from PyQt6.QtCore import Qt, QRectF, QTimer
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen, QFont, QRadialGradient
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QFrame, QScrollArea, QProgressBar,
    QPushButton, QDialog, QDialogButtonBox, QDoubleSpinBox,
    QFormLayout, QSizePolicy, QComboBox,
)

from src.config import load_config
from src.data.todo_store import TodoStore, PRIORITY_LABELS
from src.data.calendar_store import CalendarStore
from src.data.finance_store import FinanceStore


PRIORITY_COLORS = {0: "#a6adc8", 1: "#a6e3a1", 2: "#f9e2af", 3: "#f38ba8"}

_MONTH_NAMES = [
    "", "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  StatCard
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class StatCard(QFrame):
    """A compact stat card with a big number and label."""

    def __init__(self, value: str, label: str, color: str = "#cdd6f4", parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            "StatCard { border: 1px solid palette(mid); border-radius: 6px; padding: 8px; }"
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

    def update_value(self, value: str, color: str | None = None):
        self._value_label.setText(value)
        if color:
            self._value_label.setStyleSheet(
                f"font-size: 24px; font-weight: bold; color: {color};"
            )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  UpcomingItem
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class UpcomingItem(QFrame):
    """A single upcoming deadline / event in the dashboard."""

    def __init__(self, title: str, subtitle: str, color: str,
                 days_label: str, parent=None):
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


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  GoalBar — custom painted bar with color states
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class GoalBar(QWidget):
    """Paints a progress bar that changes color based on goal thresholds.

    States:
      current < min_goal  → red/orange gradient fill
      current >= min_goal → green fill
      current >= major_goal → blue fill + subtle outer glow
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(28)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self._current = 0.0
        self._min_goal = 1.0
        self._major_goal = 2.0
        self._palette: dict = {}

    def set_values(self, current: float, min_goal: float, major_goal: float):
        self._current   = max(current, 0.0)
        self._min_goal  = max(min_goal, 0.01)
        self._major_goal = max(major_goal, min_goal + 0.01)
        self.update()

    def set_palette(self, palette: dict):
        self._palette = palette
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        bar_h = 20
        bar_y = (self.height() - bar_h) // 2
        radius = bar_h / 2

        # Determine fill state
        at_major = self._current >= self._major_goal
        at_min   = self._current >= self._min_goal

        # Fill ratio — capped at 100% of major goal for visual purposes
        cap = self._major_goal * 1.05
        fill_ratio = min(self._current / cap, 1.0)

        # Color
        if at_major:
            fill_color = QColor(self._palette.get("accent", "#89b4fa"))
        elif at_min:
            fill_color = QColor(self._palette.get("green", "#a6e3a1"))
        else:
            # Blend from dark red to orange based on progress toward min
            ratio_to_min = self._current / self._min_goal
            r_start = QColor("#e55050")
            r_end   = QColor("#f9a040")
            r = int(r_start.red()   + (r_end.red()   - r_start.red())   * ratio_to_min)
            g = int(r_start.green() + (r_end.green() - r_start.green()) * ratio_to_min)
            b = int(r_start.blue()  + (r_end.blue()  - r_start.blue())  * ratio_to_min)
            fill_color = QColor(r, g, b)

        # Background track
        bg = QColor(self._palette.get("surface", "#313244"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(bg))
        painter.drawRoundedRect(0, bar_y, w, bar_h, radius, radius)

        # Glow effect behind fill if at major goal
        if at_major and fill_ratio > 0:
            glow = QColor(fill_color)
            glow.setAlpha(60)
            painter.setBrush(QBrush(glow))
            painter.drawRoundedRect(-3, bar_y - 3, w + 6, bar_h + 6, radius + 3, radius + 3)

        # Fill
        fill_w = max(int(w * fill_ratio), 0)
        if fill_w > 0:
            painter.setBrush(QBrush(fill_color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(0, bar_y, fill_w, bar_h, radius, radius)

        # Min goal marker (white vertical line)
        min_x = int(w * (self._min_goal / cap))
        if 0 < min_x < w:
            marker_pen = QPen(QColor("#ffffff"), 2)
            painter.setPen(marker_pen)
            painter.drawLine(min_x, bar_y - 2, min_x, bar_y + bar_h + 2)

        # Major goal marker (gold vertical line)
        major_x = int(w * (self._major_goal / cap))
        if 0 < major_x < w:
            gold = QColor(self._palette.get("yellow", "#f9e2af"))
            painter.setPen(QPen(gold, 2))
            painter.drawLine(major_x, bar_y - 4, major_x, bar_y + bar_h + 4)

        painter.end()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  GoalEditDialog
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class GoalEditDialog(QDialog):
    """Set minimum and major monthly side income goals.

    Input can be entered in USD or JPY — get_goals() always returns USD.
    """

    def __init__(self, min_goal: float, major_goal: float,
                 year: int, month: int, rate: float, parent=None):
        super().__init__(parent)
        self._rate = max(rate, 1.0)
        self.setWindowTitle(f"Set Goals \u2014 {_MONTH_NAMES[month]} {year}")
        self.setMinimumWidth(380)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        layout.addWidget(QLabel(
            f"Set side income goals for {_MONTH_NAMES[month]} {year}.\n"
            "Only Side Job income counts toward these goals."
        ))

        # ── Currency selector ──
        cur_row = QHBoxLayout()
        cur_row.addWidget(QLabel("Enter goals in:"))
        self._cur_combo = QComboBox()
        self._cur_combo.addItems(["USD ($)", "JPY (\u00a5)"])
        self._cur_combo.currentIndexChanged.connect(self._on_currency_changed)
        cur_row.addWidget(self._cur_combo); cur_row.addStretch()
        layout.addLayout(cur_row)

        form = QFormLayout(); form.setSpacing(8)

        self._min_spin = QDoubleSpinBox()
        self._min_spin.setRange(0, 99_999_999)
        self._min_spin.valueChanged.connect(self._update_hints)
        form.addRow("Minimum Goal:", self._min_spin)
        self._min_hint = QLabel()
        self._min_hint.setStyleSheet("color: palette(mid); font-size: 10px;")
        form.addRow("", self._min_hint)

        self._major_spin = QDoubleSpinBox()
        self._major_spin.setRange(0, 99_999_999)
        self._major_spin.valueChanged.connect(self._update_hints)
        form.addRow("Major Goal:", self._major_spin)
        self._major_hint = QLabel()
        self._major_hint.setStyleSheet("color: palette(mid); font-size: 10px;")
        form.addRow("", self._major_hint)

        layout.addLayout(form)

        btn_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        btn_box.accepted.connect(self._validate_and_accept)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)

        # Initialise in USD mode with existing values
        self._apply_usd_mode()
        self._min_spin.setValue(min_goal)
        self._major_spin.setValue(major_goal)
        self._update_hints()

    # ── Currency mode helpers ─────────────────────────────────────────────────

    def _apply_usd_mode(self):
        for sp in (self._min_spin, self._major_spin):
            sp.setDecimals(0); sp.setSingleStep(100); sp.setPrefix("$ ")

    def _apply_jpy_mode(self):
        for sp in (self._min_spin, self._major_spin):
            sp.setDecimals(0); sp.setSingleStep(10_000); sp.setPrefix("\u00a5 ")

    def _on_currency_changed(self, idx: int):
        min_v   = self._min_spin.value()
        major_v = self._major_spin.value()
        if idx == 0:   # → USD
            self._apply_usd_mode()
            if min_v > 5000:  # looks like JPY, convert
                self._min_spin.setValue(round(min_v   / self._rate))
                self._major_spin.setValue(round(major_v / self._rate))
        else:           # → JPY
            self._apply_jpy_mode()
            if min_v < 5000:  # looks like USD, convert
                self._min_spin.setValue(round(min_v   * self._rate))
                self._major_spin.setValue(round(major_v * self._rate))
        self._update_hints()

    def _update_hints(self):
        rate = self._rate
        if self._cur_combo.currentIndex() == 0:   # USD mode
            min_jpy   = int(self._min_spin.value()   * rate)
            major_jpy = int(self._major_spin.value() * rate)
            self._min_hint.setText(f"\u2248 \u00a5{min_jpy:,} JPY")
            self._major_hint.setText(f"\u2248 \u00a5{major_jpy:,} JPY")
        else:                                       # JPY mode
            min_usd   = self._min_spin.value()   / rate if rate else 0
            major_usd = self._major_spin.value() / rate if rate else 0
            self._min_hint.setText(f"\u2248 ${min_usd:,.2f} USD")
            self._major_hint.setText(f"\u2248 ${major_usd:,.2f} USD")

    def _validate_and_accept(self):
        if self._major_spin.value() <= self._min_spin.value():
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Invalid Goals",
                "Major goal must be greater than minimum goal.")
            return
        self.accept()

    def get_goals(self) -> tuple[float, float]:
        """Always returns (min_usd, major_usd)."""
        if self._cur_combo.currentIndex() == 1:   # JPY → convert
            rate = self._rate
            return self._min_spin.value() / rate, self._major_spin.value() / rate
        return self._min_spin.value(), self._major_spin.value()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  SideIncomeGoalSection
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class SideIncomeGoalSection(QFrame):
    """Prominent side income goal tracker with month navigation and color-coded bar."""

    def __init__(self, finance_store: FinanceStore, parent=None):
        super().__init__(parent)
        self.store = finance_store
        self._palette: dict = {}
        self._year  = date.today().year
        self._month = date.today().month
        self._rate  = 150.0   # USD→JPY; updated from config

        self.setObjectName("goalSection")
        self._build_ui()
        self._load_rate()
        self._refresh()

    def set_palette(self, palette: dict):
        self._palette = palette
        self._bar.set_palette(palette)
        self._refresh()

    def _load_rate(self):
        cfg = load_config()
        self._rate = float(cfg.get("usd_jpy_fallback_rate", 150.0))

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(14, 12, 14, 12)
        outer.setSpacing(8)

        # ── Header row ──
        hdr = QHBoxLayout()

        # Month navigation
        self._prev_btn = QPushButton("\u2190")
        self._prev_btn.setObjectName("secondary")
        self._prev_btn.setFixedSize(26, 26)
        self._prev_btn.setStyleSheet("QPushButton{font-size:14px;font-weight:bold;}")
        self._prev_btn.clicked.connect(self._prev_month)
        hdr.addWidget(self._prev_btn)

        self._month_lbl = QLabel()
        self._month_lbl.setStyleSheet("font-size:14px;font-weight:bold;")
        self._month_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hdr.addWidget(self._month_lbl, 1)

        self._next_btn = QPushButton("\u2192")
        self._next_btn.setObjectName("secondary")
        self._next_btn.setFixedSize(26, 26)
        self._next_btn.setStyleSheet("QPushButton{font-size:14px;font-weight:bold;}")
        self._next_btn.clicked.connect(self._next_month)
        hdr.addWidget(self._next_btn)

        hdr.addSpacing(10)

        self._edit_btn = QPushButton("Edit Goals")
        self._edit_btn.setObjectName("secondary")
        self._edit_btn.setFixedHeight(26)
        self._edit_btn.clicked.connect(self._edit_goals)
        hdr.addWidget(self._edit_btn)

        outer.addLayout(hdr)

        # ── Progress bar ──
        self._bar = GoalBar()
        outer.addWidget(self._bar)

        # ── Amount labels row ──
        self._amount_lbl = QLabel()
        self._amount_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._amount_lbl.setStyleSheet("font-size:12px;")
        outer.addWidget(self._amount_lbl)

        self._sub_lbl = QLabel()
        self._sub_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._sub_lbl.setStyleSheet("font-size:10px;")
        outer.addWidget(self._sub_lbl)

        # ── No goal set label ──
        self._no_goal_lbl = QLabel(
            "No goals set for this month. Click \u2018Edit Goals\u2019 to get started."
        )
        self._no_goal_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._no_goal_lbl.setStyleSheet("font-size:11px;")
        self._no_goal_lbl.setWordWrap(True)
        outer.addWidget(self._no_goal_lbl)

    def _refresh(self):
        self._load_rate()
        self._month_lbl.setText(f"{_MONTH_NAMES[self._month]} {self._year} — Side Income Goal")

        goal = self.store.get_goal(self._year, self._month)
        earned_usd = self.store.get_side_income(self._year, self._month, self._rate)
        earned_jpy = int(earned_usd * self._rate)

        if goal is None:
            self._bar.setVisible(False)
            self._amount_lbl.setVisible(False)
            self._sub_lbl.setVisible(False)
            self._no_goal_lbl.setVisible(True)
            return

        self._bar.setVisible(True)
        self._amount_lbl.setVisible(True)
        self._sub_lbl.setVisible(True)
        self._no_goal_lbl.setVisible(False)

        self._bar.set_values(earned_usd, goal.min_goal, goal.major_goal)
        self._bar.set_palette(self._palette)

        min_jpy   = int(goal.min_goal   * self._rate)
        major_jpy = int(goal.major_goal * self._rate)

        # Percentage toward minimum (capped at 999% for display sanity)
        pct_min = min(earned_usd / goal.min_goal * 100, 999) if goal.min_goal > 0 else 0
        pct_major = min(earned_usd / goal.major_goal * 100, 999) if goal.major_goal > 0 else 0

        # Determine status label color
        if earned_usd >= goal.major_goal:
            status = "\u2605 Major Goal Reached!"
            status_color = self._palette.get("accent", "#89b4fa")
        elif earned_usd >= goal.min_goal:
            status = "\u2714 Minimum Goal Reached"
            status_color = self._palette.get("green", "#a6e3a1")
        else:
            remaining_usd = goal.min_goal - earned_usd
            remaining_jpy = int(remaining_usd * self._rate)
            status = f"${remaining_usd:,.0f} / \u00a5{remaining_jpy:,} until minimum"
            status_color = "#f38ba8"

        self._amount_lbl.setText(
            f"${earned_usd:,.2f}  \u00a5{earned_jpy:,}"
            f"   \u2014   {pct_min:.0f}% of min  ·  {pct_major:.0f}% of major"
        )
        self._amount_lbl.setStyleSheet(f"font-size:12px;font-weight:bold;")

        self._sub_lbl.setText(
            f"Min: ${goal.min_goal:,.0f} (\u00a5{min_jpy:,})   "
            f"\u00b7   Major: ${goal.major_goal:,.0f} (\u00a5{major_jpy:,})"
            f"   \u00b7   {status}"
        )
        self._sub_lbl.setStyleSheet(f"font-size:10px;color:{status_color};")

    def _prev_month(self):
        if self._month == 1:
            self._month = 12
            self._year -= 1
        else:
            self._month -= 1
        self._refresh()

    def _next_month(self):
        if self._month == 12:
            self._month = 1
            self._year += 1
        else:
            self._month += 1
        self._refresh()

    def _edit_goals(self):
        goal = self.store.get_goal(self._year, self._month)
        min_g   = goal.min_goal   if goal else 0.0
        major_g = goal.major_goal if goal else 0.0

        dlg = GoalEditDialog(
            min_g, major_g, self._year, self._month, self._rate, self
        )
        if dlg.exec() == QDialog.DialogCode.Accepted:
            min_goal, major_goal = dlg.get_goals()
            self.store.set_goal(self._year, self._month, min_goal, major_goal)
            self._refresh()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  DashboardPanel
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class DashboardPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.todo_store     = TodoStore()
        self.calendar_store = CalendarStore()
        self.finance_store  = FinanceStore()
        self._palette: dict = {}
        self._build_ui()
        self._refresh()

        # Auto-refresh every 60 seconds so stats stay current
        self._auto_timer = QTimer(self)
        self._auto_timer.setInterval(60_000)
        self._auto_timer.timeout.connect(self._refresh)
        self._auto_timer.start()

    def showEvent(self, event):
        """Refresh immediately whenever the Dashboard tab becomes visible."""
        super().showEvent(event)
        self._refresh()

    def set_palette(self, palette: dict):
        self._palette = palette
        self._goal_section.set_palette(palette)
        self._refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)

        # ── Header ──
        header = QHBoxLayout()
        title = QLabel("Dashboard")
        title.setObjectName("sectionTitle")
        header.addWidget(title)
        header.addStretch()
        self.date_label = QLabel("")
        self.date_label.setObjectName("subtitle")
        header.addWidget(self.date_label)
        layout.addLayout(header)

        # ── Side Income Goal Section (prominent, full-width) ──
        self._goal_section = SideIncomeGoalSection(self.finance_store)
        self._goal_section.setStyleSheet(
            "#goalSection {"
            "  border: 1px solid palette(mid);"
            "  border-radius: 8px;"
            "}"
        )
        layout.addWidget(self._goal_section)

        # ── Stat cards row ──
        self._cards_layout = QHBoxLayout()
        self._cards_layout.setSpacing(10)

        self.card_pending       = StatCard("0", "Pending Tasks")
        self.card_done_today    = StatCard("0", "Done Today")
        self.card_overdue       = StatCard("0", "Overdue", "#f38ba8")
        self.card_events_week   = StatCard("0", "Events This Week")
        self.card_earned_month  = StatCard("$0", "Earned This Month")

        for card in [
            self.card_pending, self.card_done_today, self.card_overdue,
            self.card_events_week, self.card_earned_month,
        ]:
            self._cards_layout.addWidget(card)

        layout.addLayout(self._cards_layout)

        # ── Task completion progress bar ──
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

        # ── Two-column area ──
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

        # Right: priority + category breakdown
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
        green  = self._palette.get("green",  "#a6e3a1")
        red    = self._palette.get("red",    "#f38ba8")
        accent = self._palette.get("accent", "#4a9eff")
        yellow = self._palette.get("yellow", "#f9e2af")

        today = date.today()
        self.date_label.setText(today.strftime("%A, %B %d, %Y"))

        # Refresh goal section
        self._goal_section._refresh()

        # Task stats
        counts = self.todo_store.get_counts()
        all_tasks     = self.todo_store.get_all(include_done=True)
        pending_tasks = [t for t in all_tasks if not t.done and not t.deleted]
        done_tasks    = [t for t in all_tasks if t.done and not t.deleted]

        overdue = [
            t for t in pending_tasks
            if t.due_date and t.due_date < today.isoformat()
        ]

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
        done  = counts["done"]
        if total > 0:
            pct = int(done / total * 100)
            self.progress_bar.setValue(pct)
            self.progress_pct_label.setText(f"{done}/{total}")
        else:
            self.progress_bar.setValue(0)
            self.progress_pct_label.setText("No tasks")

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

        # Upcoming deadlines
        self._clear_layout(self._upcoming_layout)
        upcoming_items = []

        for task in sorted(pending_tasks, key=lambda t: t.due_date or "9999"):
            if task.due_date:
                try:
                    due = date.fromisoformat(task.due_date)
                    delta = (due - today).days
                    if delta < 0:
                        days_text, color = f"{-delta}d overdue", red
                    elif delta == 0:
                        days_text, color = "Today", yellow
                    elif delta == 1:
                        days_text, color = "Tomorrow", yellow
                    elif delta <= 7:
                        days_text, color = f"In {delta}d", accent
                    else:
                        days_text, color = f"In {delta}d", green
                    cat = f"Task \u00b7 {task.category}" if task.category else "Task"
                    upcoming_items.append((delta, UpcomingItem(
                        task.title, cat, color, days_text
                    )))
                except ValueError:
                    pass

        next_week = today + timedelta(days=7)
        upcoming_events = self.calendar_store.get_events(
            today.isoformat(), next_week.isoformat() + "T23:59:59"
        )
        for ev in upcoming_events:
            try:
                ev_date = datetime.fromisoformat(ev.start_time).date()
                delta = (ev_date - today).days
                if delta == 0:   days_text = "Today"
                elif delta == 1: days_text = "Tomorrow"
                else:            days_text = f"In {delta}d"
                time_str = ""
                if not ev.all_day:
                    time_str = datetime.fromisoformat(ev.start_time).strftime("%H:%M")
                sub = f"Event \u00b7 {time_str}" if time_str else "Event \u00b7 All day"
                upcoming_items.append((delta, UpcomingItem(
                    ev.title, sub, ev.color, days_text
                )))
            except (ValueError, AttributeError):
                pass

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
            for i, (cat, count) in enumerate(
                sorted(cat_counts.items(), key=lambda x: -x[1])
            ):
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