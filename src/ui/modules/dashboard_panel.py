"""Dashboard panel — overview of tasks, upcoming deadlines, and productivity stats.

New in this version:
  • SideIncomeGoalSection — prominent month-browsable side income goal tracker
    with a color-coded progress bar (red → green → blue glow at major goal).
  • Goal data stored in side_income_goals table via FinanceStore.set_goal()
  • "Coming Up (Next 7 Days)" section for soft event reminders
  • Store injection — all stores passed in from main_window
"""

import calendar as _calendar
from datetime import date, datetime, timedelta

from PyQt6.QtCore import Qt, QRectF, QTimer
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen, QFont, QRadialGradient
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QFrame, QScrollArea, QProgressBar,
    QPushButton, QDialog, QDialogButtonBox, QDoubleSpinBox,
    QFormLayout, QSizePolicy, QComboBox, QTextEdit,
)

from src.config import load_config
from src.data.todo_store import TodoStore, PRIORITY_LABELS
from src.data.calendar_store import CalendarStore
from src.data.finance_store import FinanceStore
from src.data.soft_events_store import SoftEventStore
from src.ui.widgets.nav_button import NavButton


def _priority_colors(palette: dict) -> dict:
    """Return priority-level colours drawn from the current theme palette."""
    return {
        0: palette.get("muted",  "#a6adc8"),
        1: palette.get("green",  "#a6e3a1"),
        2: palette.get("yellow", "#f9e2af"),
        3: palette.get("red",    "#f38ba8"),
    }

# Sentinel → palette key map for store-layer color strings
SENTINEL_COLORS = {"birthday": "red", "holiday": "yellow", "trip": "accent"}

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

        at_major = self._current >= self._major_goal
        at_min   = self._current >= self._min_goal

        cap = self._major_goal * 1.05
        fill_ratio = min(self._current / cap, 1.0)

        if at_major:
            fill_color = QColor(self._palette.get("accent", "#89b4fa"))
        elif at_min:
            fill_color = QColor(self._palette.get("green", "#a6e3a1"))
        else:
            ratio_to_min = self._current / self._min_goal
            r_start = QColor("#e55050")
            r_end   = QColor("#f9a040")
            r = int(r_start.red()   + (r_end.red()   - r_start.red())   * ratio_to_min)
            g = int(r_start.green() + (r_end.green() - r_start.green()) * ratio_to_min)
            b = int(r_start.blue()  + (r_end.blue()  - r_start.blue())  * ratio_to_min)
            fill_color = QColor(r, g, b)

        bg = QColor(self._palette.get("surface", "#313244"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(bg))
        painter.drawRoundedRect(0, bar_y, w, bar_h, radius, radius)

        if at_major and fill_ratio > 0:
            glow = QColor(fill_color)
            glow.setAlpha(60)
            painter.setBrush(QBrush(glow))
            painter.drawRoundedRect(-3, bar_y - 3, w + 6, bar_h + 6, radius + 3, radius + 3)

        fill_w = max(int(w * fill_ratio), 0)
        if fill_w > 0:
            painter.setBrush(QBrush(fill_color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(0, bar_y, fill_w, bar_h, radius, radius)

        min_x = int(w * (self._min_goal / cap))
        if 0 < min_x < w:
            marker_pen = QPen(QColor("#ffffff"), 2)
            painter.setPen(marker_pen)
            painter.drawLine(min_x, bar_y - 2, min_x, bar_y + bar_h + 2)

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

        self._apply_usd_mode()
        self._min_spin.setValue(min_goal)
        self._major_spin.setValue(major_goal)
        self._update_hints()

    def _apply_usd_mode(self):
        for sp in (self._min_spin, self._major_spin):
            sp.setDecimals(0); sp.setSingleStep(100); sp.setPrefix("$ ")

    def _apply_jpy_mode(self):
        for sp in (self._min_spin, self._major_spin):
            sp.setDecimals(0); sp.setSingleStep(10_000); sp.setPrefix("\u00a5 ")

    def _on_currency_changed(self, idx: int):
        min_v   = self._min_spin.value()
        major_v = self._major_spin.value()
        if idx == 0:
            self._apply_usd_mode()
            if min_v > 5000:
                self._min_spin.setValue(round(min_v   / self._rate))
                self._major_spin.setValue(round(major_v / self._rate))
        else:
            self._apply_jpy_mode()
            if min_v < 5000:
                self._min_spin.setValue(round(min_v   * self._rate))
                self._major_spin.setValue(round(major_v * self._rate))
        self._update_hints()

    def _update_hints(self):
        rate = self._rate
        if self._cur_combo.currentIndex() == 0:
            min_jpy   = int(self._min_spin.value()   * rate)
            major_jpy = int(self._major_spin.value() * rate)
            self._min_hint.setText(f"\u2248 \u00a5{min_jpy:,} JPY")
            self._major_hint.setText(f"\u2248 \u00a5{major_jpy:,} JPY")
        else:
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
        if self._cur_combo.currentIndex() == 1:
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
        self._rate  = 150.0

        self.setObjectName("goalSection")
        self._build_ui()
        self._load_rate()
        self._refresh()

    def set_palette(self, palette: dict):
        self._palette = palette
        self._bar.set_palette(palette)
        # Refresh painter-based nav buttons with new palette colors
        self._prev_btn.refresh(palette)
        self._next_btn.refresh(palette)
        self._refresh()

    def _load_rate(self):
        cfg = load_config()
        self._rate = float(cfg.get("usd_jpy_fallback_rate", 150.0))

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(14, 12, 14, 12)
        outer.setSpacing(8)

        hdr = QHBoxLayout()

        # ── Use NavButton for painter-drawn arrows (no font/padding issues) ──
        self._prev_btn = NavButton("left", size=26, tooltip="Previous month")
        self._prev_btn.clicked.connect(self._prev_month)
        hdr.addWidget(self._prev_btn)

        self._month_lbl = QLabel()
        self._month_lbl.setStyleSheet("font-size:14px;font-weight:bold;")
        self._month_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hdr.addWidget(self._month_lbl, 1)

        self._next_btn = NavButton("right", size=26, tooltip="Next month")
        self._next_btn.clicked.connect(self._next_month)
        hdr.addWidget(self._next_btn)

        hdr.addSpacing(10)

        self._edit_btn = QPushButton("Edit Goals")
        self._edit_btn.setObjectName("secondary")
        self._edit_btn.setFixedHeight(26)
        self._edit_btn.clicked.connect(self._edit_goals)
        hdr.addWidget(self._edit_btn)

        outer.addLayout(hdr)

        self._bar = GoalBar()
        outer.addWidget(self._bar)

        self._amount_lbl = QLabel()
        self._amount_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._amount_lbl.setStyleSheet("font-size:12px;")
        outer.addWidget(self._amount_lbl)

        self._sub_lbl = QLabel()
        self._sub_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._sub_lbl.setStyleSheet("font-size:10px;")
        outer.addWidget(self._sub_lbl)

        self._no_goal_lbl = QLabel(
            "No goals set for this month. Click \u2018Edit Goals\u2019 to get started."
        )
        self._no_goal_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._no_goal_lbl.setStyleSheet("font-size:11px;")
        self._no_goal_lbl.setWordWrap(True)
        outer.addWidget(self._no_goal_lbl)

    def _refresh(self):
        self._load_rate()
        self._month_lbl.setText(f"{_MONTH_NAMES[self._month]} {self._year} \u2014 Side Income Goal")

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

        pct_min = min(earned_usd / goal.min_goal * 100, 999) if goal.min_goal > 0 else 0
        pct_major = min(earned_usd / goal.major_goal * 100, 999) if goal.major_goal > 0 else 0

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
            status_color = self._palette.get("red", "#f38ba8")

        self._amount_lbl.setText(
            f"${earned_usd:,.2f}  \u00a5{earned_jpy:,}"
            f"   \u2014   {pct_min:.0f}% of min  \u00b7  {pct_major:.0f}% of major"
        )
        self._amount_lbl.setStyleSheet("font-size:12px;font-weight:bold;")

        self._sub_lbl.setText(
            f"Min: ${goal.min_goal:,.0f} (\u00a5{min_jpy:,})   "
            f"\u00b7   Major: ${goal.major_goal:,.0f} (\u00a5{major_jpy:,})"
            f"   \u00b7   {status}"
        )
        self._sub_lbl.setStyleSheet(f"font-size:10px;color:{status_color};")

    def _prev_month(self):
        if self._month == 1:
            self._month = 12; self._year -= 1
        else:
            self._month -= 1
        self._refresh()

    def _next_month(self):
        if self._month == 12:
            self._month = 1; self._year += 1
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
#  SoftEventLogDialog — per-day log editor for a soft event
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class SoftEventLogDialog(QDialog):
    """Edit the per-day log for a soft event occurrence."""

    def __init__(self, parent, soft_events_store: SoftEventStore,
                 template, log_date: date):
        super().__init__(parent)
        self._store = soft_events_store
        self._template = template
        self._log_date = log_date
        self._palette: dict = getattr(parent, '_palette', {})

        date_str = log_date.isoformat()
        self.setWindowTitle(f"{template.title} \u2014 {date_str}")
        self.setMinimumSize(420, 360)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(16, 14, 16, 14)

        # Template universal note (read-only)
        if template.note:
            note_lbl = QLabel(template.note)
            note_lbl.setWordWrap(True)
            muted = self._palette.get("muted", "#7f849c")
            note_lbl.setStyleSheet(f"color: {muted}; font-style: italic; font-size: 11px;")
            layout.addWidget(note_lbl)

            sep = QFrame()
            sep.setObjectName("separator")
            sep.setFrameShape(QFrame.Shape.HLine)
            layout.addWidget(sep)

        # Editable log text
        self._log_entry = self._store.get_or_create_log(template.id, date_str)
        self._editor = QTextEdit()
        self._editor.setPlainText(self._log_entry.log_text)
        layout.addWidget(self._editor, 1)

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("secondary")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self._save)
        btn_row.addWidget(save_btn)
        layout.addLayout(btn_row)

    def _save(self):
        self._log_entry.log_text = self._editor.toPlainText()
        self._store.update_log(self._log_entry)
        self.accept()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ComingUpRow — a single soft event in the Coming Up section
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class _ComingUpRow(QFrame):
    """A single soft event reminder row."""

    def __init__(self, template, occurrence_date: date,
                 relative_label: str, parent_panel, parent=None):
        super().__init__(parent)
        self._template = template
        self._date = occurrence_date
        self._panel = parent_panel
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 3, 6, 3)
        layout.setSpacing(6)

        dot = QLabel("\u25cf")
        dot.setStyleSheet(f"color: {template.color}; font-size: 12px;")
        dot.setFixedWidth(14)
        layout.addWidget(dot)

        title = QLabel(template.title)
        title.setStyleSheet("font-size: 12px; font-weight: bold;")
        layout.addWidget(title, 1)

        rel = QLabel(relative_label)
        rel.setObjectName("subtitle")
        rel.setStyleSheet("font-size: 10px;")
        rel.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(rel)

    def mousePressEvent(self, ev):
        dlg = SoftEventLogDialog(
            self._panel, self._panel.soft_events_store,
            self._template, self._date,
        )
        dlg.exec()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  DashboardPanel
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class DashboardPanel(QWidget):

    def __init__(self, todo_store=None, calendar_store=None,
                 finance_store=None, soft_events_store=None, parent=None):
        super().__init__(parent)
        self.todo_store     = todo_store     or TodoStore()
        self.calendar_store = calendar_store or CalendarStore()
        self.finance_store  = finance_store  or FinanceStore()
        self.soft_events_store = soft_events_store or SoftEventStore()
        self._palette: dict = {}
        self._build_ui()
        self._refresh()

        # Auto-refresh every 60 seconds
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

        # ── Side Income Goal Section ──
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
        upcoming_scroll.setMinimumHeight(160)   # guarantee ~4-5 rows always visible
        left.addWidget(upcoming_scroll, 1)

        # ── Coming Up (Next 7 Days) section ──
        coming_up_title = QLabel("Coming Up (Next 7 Days)")
        coming_up_title.setStyleSheet("font-weight: bold; font-size: 13px;")
        left.addWidget(coming_up_title)

        self._coming_up_container = QWidget()
        self._coming_up_layout = QVBoxLayout(self._coming_up_container)
        self._coming_up_layout.setContentsMargins(0, 0, 0, 0)
        self._coming_up_layout.setSpacing(2)

        coming_up_scroll = QScrollArea()
        coming_up_scroll.setWidgetResizable(True)
        coming_up_scroll.setWidget(self._coming_up_container)
        coming_up_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        coming_up_scroll.setFrameShape(QFrame.Shape.NoFrame)
        coming_up_scroll.setMaximumHeight(180)  # cap at ~5 rows; scrollable if more
        left.addWidget(coming_up_scroll)

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

        # Upcoming deadlines (extended: 30 days, 12 items)
        self._clear_layout(self._upcoming_layout)
        upcoming_items: list[tuple[int, QWidget]] = []

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

        # Major events — 30-day lookahead, 12 items
        # Collect IDs so regular get_events() below doesn't duplicate them.
        majors = self.calendar_store.get_next_major_events(today, limit=12)
        thirty_days = today + timedelta(days=30)
        major_event_ids: set[str] = set()

        for ev_date, ev_title, category, color, item_id, is_birthday in majors:
            if ev_date > thirty_days:
                continue
            delta = (ev_date - today).days
            if delta == 0:   days_text = "Today"
            elif delta == 1: days_text = "Tomorrow"
            else:            days_text = f"In {delta}d"
            # Resolve sentinel colors
            resolved = self._palette.get(SENTINEL_COLORS.get(color, "accent"), color)
            upcoming_items.append((delta, UpcomingItem(
                ev_title, category.title(), resolved, days_text
            )))
            # Track real event IDs (birthdays have no calendar_events row to skip)
            if not is_birthday:
                major_event_ids.add(item_id)

        # Regular events for the next 7 days — skip any already shown via majors
        next_week = today + timedelta(days=7)
        upcoming_events = self.calendar_store.get_events(
            today.isoformat(), next_week.isoformat() + "T23:59:59"
        )
        for ev in upcoming_events:
            # Skip events that were already added from get_next_major_events()
            if ev.id in major_event_ids:
                continue
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

        # ── Coming Up (Next 7 Days) — soft events ──
        self._clear_layout(self._coming_up_layout)
        try:
            soft_upcoming = self.soft_events_store.get_upcoming(today, days_ahead=7)
        except Exception:
            soft_upcoming = []

        if soft_upcoming:
            for occ_date, tpl in soft_upcoming:
                delta = (occ_date - today).days
                if delta == 0:
                    rel_text = "Today"
                elif delta == 1:
                    rel_text = "Tomorrow"
                elif delta <= 6:
                    rel_text = f"Next {occ_date.strftime('%A')}"
                else:
                    rel_text = f"In {delta} days"
                row = _ComingUpRow(tpl, occ_date, rel_text, self)
                self._coming_up_layout.addWidget(row)
        else:
            muted = self._palette.get("muted", "#7f849c")
            no_soft = QLabel("No reminders in the next 7 days.")
            no_soft.setStyleSheet(f"color: {muted}; font-size: 11px; padding: 4px 0;")
            self._coming_up_layout.addWidget(no_soft)

        self._coming_up_layout.addStretch()

        # Priority breakdown
        self._clear_layout(self._priority_layout)
        priority_counts = {0: 0, 1: 0, 2: 0, 3: 0}
        for task in pending_tasks:
            priority_counts[task.priority] = priority_counts.get(task.priority, 0) + 1

        max_count = max(priority_counts.values()) if any(priority_counts.values()) else 1
        pcolors = _priority_colors(self._palette)
        for pri in [3, 2, 1, 0]:
            count = priority_counts[pri]
            row = QHBoxLayout()
            label = QLabel(PRIORITY_LABELS[pri])
            label.setFixedWidth(55)
            label.setStyleSheet(f"font-size: 11px; color: {pcolors[pri]};")
            row.addWidget(label)

            bar = QFrame()
            width = max(int(count / max_count * 120), 2) if max_count > 0 else 2
            bar.setFixedSize(width, 14)
            bar.setStyleSheet(
                f"background-color: {pcolors[pri]}; border-radius: 2px;"
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