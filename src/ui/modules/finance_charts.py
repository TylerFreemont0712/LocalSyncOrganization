"""Finance charts — custom painted graphs for earnings data visualization.

Uses QPainter for zero-dependency chart rendering: line chart, bar chart,
pie chart, and activity stacked bar chart.

Tabs:
  Finance  — monthly line chart, earnings by source bar, category pie
  Activity — stacked daily bar chart of time spent per quick category
"""

import calendar
from datetime import date, timedelta
from math import cos, sin, pi

from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush, QFont, QPainterPath
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QFrame, QSizePolicy, QTabWidget,
)

from src.data.finance_store import FinanceStore
from src.data.activity_store import ActivityStore, ACTIVITY_COLORS, DEFAULT_COLOR, QUICK_CATEGORIES
from src.config import load_config

CHART_COLORS = [
    "#4a9eff", "#a6e3a1", "#cba6f7", "#fab387", "#f9e2af",
    "#94e2d5", "#f38ba8", "#f5c2e7", "#89b4fa", "#74c7ec",
]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  LineChart
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class LineChart(QWidget):
    """Monthly earnings line chart with area fill."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(200)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._data: list[tuple[str, float]] = []
        self._title = "Monthly Earnings"
        self._color = QColor("#4a9eff")

    def set_data(self, data: list[tuple[str, float]], color: str = "#4a9eff"):
        self._data = data
        self._color = QColor(color)
        self.update()

    def paintEvent(self, event):
        if not self._data:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()
        margin_left = 60
        margin_right = 20
        margin_top = 30
        margin_bottom = 40
        chart_w = w - margin_left - margin_right
        chart_h = h - margin_top - margin_bottom

        if chart_w < 50 or chart_h < 50:
            painter.end()
            return

        painter.setPen(QPen(QColor("#cdd6f4")))
        font = QFont()
        font.setBold(True)
        font.setPixelSize(13)
        painter.setFont(font)
        painter.drawText(margin_left, 18, self._title)

        values = [d[1] for d in self._data]
        max_val = max(values) if values else 1
        if max_val == 0:
            max_val = 1

        n = len(self._data)
        if n < 2:
            painter.end()
            return

        font.setBold(False)
        font.setPixelSize(10)
        painter.setFont(font)
        grid_pen = QPen(QColor("#45475a"), 1, Qt.PenStyle.DotLine)
        label_pen = QPen(QColor("#a6adc8"))

        num_grid = 4
        for i in range(num_grid + 1):
            y = margin_top + chart_h - (i / num_grid * chart_h)
            val = max_val * i / num_grid
            painter.setPen(grid_pen)
            painter.drawLine(int(margin_left), int(y), int(w - margin_right), int(y))
            painter.setPen(label_pen)
            painter.drawText(
                QRectF(0, y - 8, margin_left - 6, 16),
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                f"${val:,.0f}",
            )

        points = []
        step = chart_w / (n - 1)
        for i, (label, val) in enumerate(self._data):
            x = margin_left + i * step
            y = margin_top + chart_h - (val / max_val * chart_h)
            points.append(QPointF(x, y))
            painter.setPen(label_pen)
            painter.drawText(
                QRectF(x - 20, h - margin_bottom + 6, 40, 16),
                Qt.AlignmentFlag.AlignCenter,
                label,
            )

        area_path = QPainterPath()
        area_path.moveTo(points[0].x(), margin_top + chart_h)
        for pt in points:
            area_path.lineTo(pt)
        area_path.lineTo(points[-1].x(), margin_top + chart_h)
        area_path.closeSubpath()

        fill_color = QColor(self._color)
        fill_color.setAlpha(40)
        painter.fillPath(area_path, QBrush(fill_color))

        line_pen = QPen(self._color, 2)
        painter.setPen(line_pen)
        for i in range(len(points) - 1):
            painter.drawLine(points[i], points[i + 1])

        painter.setBrush(QBrush(self._color))
        for pt in points:
            painter.drawEllipse(pt, 4, 4)

        painter.end()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  BarChart
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class BarChart(QWidget):
    """Vertical bar chart for category or monthly comparisons."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(200)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._data: list[tuple[str, float]] = []
        self._title = ""
        self._colors: list[str] = CHART_COLORS

    def set_data(self, data: list[tuple[str, float]], title: str = "",
                 colors: list[str] | None = None):
        self._data = data
        self._title = title
        if colors:
            self._colors = colors
        self.update()

    def paintEvent(self, event):
        if not self._data:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()
        margin_left = 60
        margin_right = 20
        margin_top = 30
        margin_bottom = 50
        chart_w = w - margin_left - margin_right
        chart_h = h - margin_top - margin_bottom

        if chart_w < 50 or chart_h < 50:
            painter.end()
            return

        painter.setPen(QPen(QColor("#cdd6f4")))
        font = QFont()
        font.setBold(True)
        font.setPixelSize(13)
        painter.setFont(font)
        if self._title:
            painter.drawText(margin_left, 18, self._title)

        values = [d[1] for d in self._data]
        max_val = max(values) if values else 1
        if max_val == 0:
            max_val = 1

        n = len(self._data)
        if n == 0:
            painter.end()
            return

        bar_gap = 6
        bar_w = max((chart_w - bar_gap * (n + 1)) / n, 8)

        font.setBold(False)
        font.setPixelSize(10)
        painter.setFont(font)
        grid_pen = QPen(QColor("#45475a"), 1, Qt.PenStyle.DotLine)
        label_pen = QPen(QColor("#a6adc8"))

        for i in range(5):
            y = margin_top + chart_h - (i / 4 * chart_h)
            val = max_val * i / 4
            painter.setPen(grid_pen)
            painter.drawLine(int(margin_left), int(y), int(w - margin_right), int(y))
            painter.setPen(label_pen)
            painter.drawText(
                QRectF(0, y - 8, margin_left - 6, 16),
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                f"${val:,.0f}",
            )

        for i, (label, val) in enumerate(self._data):
            x = margin_left + bar_gap + i * (bar_w + bar_gap)
            bar_h = (val / max_val) * chart_h
            y = margin_top + chart_h - bar_h
            color = QColor(self._colors[i % len(self._colors)])
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawRoundedRect(QRectF(x, y, bar_w, bar_h), 3, 3)
            painter.setPen(label_pen)
            display_label = label if len(label) <= 8 else label[:7] + ".."
            painter.drawText(
                QRectF(x - 4, margin_top + chart_h + 4, bar_w + 8, 30),
                Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
                display_label,
            )
            painter.drawText(
                QRectF(x - 4, y - 16, bar_w + 8, 14),
                Qt.AlignmentFlag.AlignCenter,
                f"${val:,.0f}",
            )

        painter.end()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  PieChart
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class PieChart(QWidget):
    """Donut/pie chart for category distribution."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(200, 200)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._data: list[tuple[str, float]] = []
        self._title = ""
        self._colors = CHART_COLORS

    def set_data(self, data: list[tuple[str, float]], title: str = ""):
        self._data = data
        self._title = title
        self.update()

    def paintEvent(self, event):
        if not self._data:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()
        margin = 20
        legend_width = 120
        chart_area = min(w - margin * 2 - legend_width, h - margin * 2 - 20)
        if chart_area < 60:
            painter.end()
            return

        painter.setPen(QPen(QColor("#cdd6f4")))
        font = QFont()
        font.setBold(True)
        font.setPixelSize(13)
        painter.setFont(font)
        if self._title:
            painter.drawText(margin, 18, self._title)

        radius = chart_area / 2
        cx = margin + radius
        cy = margin + 24 + radius
        inner_radius = radius * 0.55

        total = sum(v for _, v in self._data)
        if total == 0:
            painter.end()
            return

        start_angle = 90 * 16
        rect = QRectF(cx - radius, cy - radius, radius * 2, radius * 2)
        inner_rect = QRectF(cx - inner_radius, cy - inner_radius,
                            inner_radius * 2, inner_radius * 2)

        font.setBold(False)
        font.setPixelSize(10)
        painter.setFont(font)

        for i, (label, val) in enumerate(self._data):
            span = int(val / total * 360 * 16)
            color = QColor(self._colors[i % len(self._colors)])
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(color))
            path = QPainterPath()
            path.moveTo(cx, cy)
            path.arcTo(rect, start_angle / 16, span / 16)
            path.lineTo(cx, cy)
            painter.drawPath(path)
            start_angle += span

        painter.setBrush(QBrush(QColor("#1e1e2e")))
        painter.drawEllipse(inner_rect)

        painter.setPen(QPen(QColor("#cdd6f4")))
        font.setPixelSize(16)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(inner_rect, Qt.AlignmentFlag.AlignCenter, f"${total:,.0f}")

        font.setPixelSize(10)
        font.setBold(False)
        painter.setFont(font)
        legend_x = cx + radius + 16
        legend_y = cy - radius + 10

        for i, (label, val) in enumerate(self._data):
            color = QColor(self._colors[i % len(self._colors)])
            y = legend_y + i * 18
            if y > h - 10:
                break
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawRoundedRect(QRectF(legend_x, y, 10, 10), 2, 2)
            pct = val / total * 100 if total > 0 else 0
            painter.setPen(QPen(QColor("#a6adc8")))
            painter.drawText(
                QRectF(legend_x + 14, y - 2, legend_width - 14, 16),
                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                f"{label} ({pct:.0f}%)",
            )

        painter.end()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  StackedActivityChart — daily stacked bar (hours)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class StackedActivityChart(QWidget):
    """Stacked bar chart: one bar per day, segments per quick category."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(260)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # List of (day_label, {category: minutes})
        self._days: list[tuple[str, dict[str, float]]] = []
        self._categories: list[str] = []
        self._title = "Daily Activity Breakdown"
        self._palette: dict = {}

    def set_data(self, days: list[tuple[str, dict[str, float]]],
                 categories: list[str], title: str = "Daily Activity Breakdown"):
        self._days = days
        self._categories = categories
        self._title = title
        self.update()

    def set_palette(self, palette: dict):
        self._palette = palette
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()
        margin_left   = 52
        margin_right  = 16
        margin_top    = 30
        margin_bottom = 54   # room for day labels + legend
        chart_w = w - margin_left - margin_right
        chart_h = h - margin_top - margin_bottom

        fg_color = QColor(self._palette.get("fg", "#cdd6f4"))
        muted_c  = QColor(self._palette.get("muted", "#7f849c"))
        grid_c   = QColor(self._palette.get("border", "#45475a"))

        if chart_w < 60 or chart_h < 60:
            painter.end()
            return

        # Title
        font = QFont(); font.setBold(True); font.setPixelSize(13)
        painter.setFont(font)
        painter.setPen(QPen(fg_color))
        painter.drawText(margin_left, 18, self._title)

        if not self._days:
            font.setBold(False); font.setPixelSize(11); painter.setFont(font)
            painter.setPen(QPen(muted_c))
            painter.drawText(
                QRectF(margin_left, margin_top, chart_w, chart_h),
                Qt.AlignmentFlag.AlignCenter, "No activity data for this period"
            )
            painter.end()
            return

        # Max total minutes across all days
        max_mins = max(
            sum(cats.values()) for _, cats in self._days
        ) if self._days else 1
        if max_mins == 0:
            max_mins = 60  # default 1h axis

        # Round up to nearest hour for nicer grid
        max_hours = (int(max_mins // 60) + 1)
        max_mins_axis = max_hours * 60

        # Y grid lines (hours)
        font.setBold(False); font.setPixelSize(9); painter.setFont(font)
        grid_pen = QPen(grid_c, 1, Qt.PenStyle.DotLine)

        for hh in range(max_hours + 1):
            y = margin_top + chart_h - (hh / max_hours * chart_h)
            painter.setPen(grid_pen)
            painter.drawLine(int(margin_left), int(y), int(w - margin_right), int(y))
            painter.setPen(QPen(muted_c))
            painter.drawText(
                QRectF(0, y - 8, margin_left - 4, 16),
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                f"{hh}h",
            )

        # Bars
        n = len(self._days)
        bar_gap = 8
        bar_w = max((chart_w - bar_gap * (n + 1)) / n, 10)

        for i, (day_label, cat_mins) in enumerate(self._days):
            x = margin_left + bar_gap + i * (bar_w + bar_gap)
            y_cursor = margin_top + chart_h  # start from bottom

            for cat in self._categories:
                mins = cat_mins.get(cat, 0.0)
                if mins <= 0:
                    continue
                seg_h = (mins / max_mins_axis) * chart_h
                color = QColor(ACTIVITY_COLORS.get(cat, DEFAULT_COLOR))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(QBrush(color))
                painter.drawRoundedRect(
                    QRectF(x, y_cursor - seg_h, bar_w, seg_h), 2, 2
                )
                # Label inside segment if tall enough
                if seg_h >= 16:
                    lbl_font = QFont(); lbl_font.setPixelSize(9)
                    painter.setFont(lbl_font)
                    text_c = QColor("#11111b") if color.lightness() > 128 else QColor("#cdd6f4")
                    painter.setPen(QPen(text_c))
                    short = cat[:4]
                    painter.drawText(
                        QRectF(x + 2, y_cursor - seg_h + 2, bar_w - 4, seg_h - 4),
                        Qt.AlignmentFlag.AlignCenter, short
                    )
                y_cursor -= seg_h

            # Day label below
            font.setBold(False); font.setPixelSize(10); painter.setFont(font)
            painter.setPen(QPen(muted_c))
            painter.drawText(
                QRectF(x - 4, margin_top + chart_h + 4, bar_w + 8, 20),
                Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
                day_label,
            )

        # Legend row at very bottom
        legend_y = h - 18
        legend_x = margin_left
        font.setPixelSize(9); painter.setFont(font)
        for cat in self._categories:
            color = QColor(ACTIVITY_COLORS.get(cat, DEFAULT_COLOR))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawRoundedRect(QRectF(legend_x, legend_y, 9, 9), 2, 2)
            painter.setPen(QPen(muted_c))
            painter.drawText(
                QRectF(legend_x + 11, legend_y - 2, 65, 14),
                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                cat[:8],
            )
            legend_x += 78
            if legend_x > w - 60:
                break

        painter.end()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ActivityChartsPanel — the Activity tab content
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ActivityChartsPanel(QWidget):
    """Activity stacked bar chart view."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.store = ActivityStore()
        self._palette: dict = {}
        self._build_ui()
        self._refresh()

    def set_palette(self, palette: dict):
        self._palette = palette
        self._chart.set_palette(palette)
        self._refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(10)

        header = QHBoxLayout()
        title = QLabel("Activity Charts")
        title.setObjectName("sectionTitle")
        header.addWidget(title)
        header.addStretch()

        header.addWidget(QLabel("Period:"))
        self.period_combo = QComboBox()
        self.period_combo.addItems(["This Week", "Last Week", "Last 4 Weeks"])
        self.period_combo.currentTextChanged.connect(self._refresh)
        header.addWidget(self.period_combo)
        layout.addLayout(header)

        self._chart = StackedActivityChart()
        layout.addWidget(self._chart, 1)

        # Summary label
        self._summary_lbl = QLabel("")
        self._summary_lbl.setStyleSheet("font-size:11px;")
        self._summary_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._summary_lbl)

    def _refresh(self):
        today = date.today()
        period = self.period_combo.currentText()
        cfg = load_config()
        quick_cats = cfg.get("activity_quick_categories", list(QUICK_CATEGORIES))

        if period == "This Week":
            week_start = today - timedelta(days=today.weekday())
            days_range = [(week_start + timedelta(days=i)) for i in range(7)]
        elif period == "Last Week":
            week_start = today - timedelta(days=today.weekday() + 7)
            days_range = [(week_start + timedelta(days=i)) for i in range(7)]
        else:  # Last 4 Weeks
            start = today - timedelta(days=27)
            days_range = [(start + timedelta(days=i)) for i in range(28)]

        # Build data: one entry per day
        day_data: list[tuple[str, dict[str, float]]] = []
        total_by_cat: dict[str, float] = {c: 0.0 for c in quick_cats}

        for d in days_range:
            acts = self.store.get_for_date(d.isoformat())
            cat_mins: dict[str, float] = {c: 0.0 for c in quick_cats}
            for a in acts:
                if a.activity in cat_mins:
                    mins = max(a.duration_minutes, 0)
                    cat_mins[a.activity] += mins
                    total_by_cat[a.activity] += mins
            if period == "Last 4 Weeks":
                label = d.strftime("%m/%d")
            else:
                label = d.strftime("%a")
            day_data.append((label, cat_mins))

        self._chart.set_data(day_data, quick_cats)
        self._chart.set_palette(self._palette)

        # Summary text
        total_mins = sum(total_by_cat.values())
        h, m = divmod(int(total_mins), 60)
        parts = [f"{c}: {int(v)//60}h{int(v)%60:02d}m"
                 for c, v in total_by_cat.items() if v > 0]
        summary = f"Total: {h}h {m}m   |   " + "  ·  ".join(parts) if parts else "No data"
        self._summary_lbl.setText(summary)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  FinanceChartsPanel — tabbed container
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class FinanceChartsPanel(QWidget):
    """Tabbed charts panel: Finance tab + Activity tab."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._palette: dict = {}
        self._build_ui()

    def set_palette(self, palette: dict):
        self._palette = palette
        self._finance_tab.set_palette(palette)
        self._activity_tab.set_palette(palette)

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self._tabs = QTabWidget()
        self._tabs.setDocumentMode(True)

        # Finance tab (original content)
        self._finance_tab = _FinanceChartsContent()
        self._tabs.addTab(self._finance_tab, "Finance")

        # Activity tab (new)
        self._activity_tab = ActivityChartsPanel()
        self._tabs.addTab(self._activity_tab, "Activity")

        layout.addWidget(self._tabs)

    def refresh(self):
        self._finance_tab._refresh()
        self._activity_tab._refresh()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  _FinanceChartsContent — original finance charts
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class _FinanceChartsContent(QWidget):
    """Original finance charts: line chart, bar chart, pie chart."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.store = FinanceStore()
        self._palette: dict = {}
        self._build_ui()
        self._refresh()

    def set_palette(self, palette: dict):
        self._palette = palette
        self._refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(10)

        header = QHBoxLayout()
        title = QLabel("Financial Charts")
        title.setObjectName("sectionTitle")
        header.addWidget(title)
        header.addStretch()

        header.addWidget(QLabel("Period:"))
        self.period_combo = QComboBox()
        self.period_combo.addItems([
            "Last 6 Months", "Last 12 Months", "This Year", "All Time"
        ])
        self.period_combo.currentTextChanged.connect(self._refresh)
        header.addWidget(self.period_combo)
        layout.addLayout(header)

        self.line_chart = LineChart()
        self.line_chart.setMinimumHeight(220)
        layout.addWidget(self.line_chart, 2)

        bottom = QHBoxLayout()
        bottom.setSpacing(12)

        self.bar_chart = BarChart()
        self.bar_chart.setMinimumHeight(200)
        bottom.addWidget(self.bar_chart, 3)

        self.pie_chart = PieChart()
        self.pie_chart.setMinimumHeight(200)
        bottom.addWidget(self.pie_chart, 2)

        layout.addLayout(bottom, 2)

    def _get_date_range(self) -> tuple[str, str]:
        today = date.today()
        period = self.period_combo.currentText()
        if period == "Last 6 Months":
            start = today - timedelta(days=180)
        elif period == "Last 12 Months":
            start = today - timedelta(days=365)
        elif period == "This Year":
            start = today.replace(month=1, day=1)
        else:
            start = date(2020, 1, 1)
        return start.isoformat(), today.isoformat()

    def _refresh(self):
        green = self._palette.get("green", "#a6e3a1")

        start, end = self._get_date_range()
        txns = self.store.get_transactions(start, end)

        monthly: dict[str, float] = {}
        for t in txns:
            month_key = t.date[:7]
            if t.type == "income":
                monthly[month_key] = monthly.get(month_key, 0) + t.amount

        all_months = sorted(monthly.keys())
        if not all_months:
            today = date.today()
            for i in range(5, -1, -1):
                m = today - timedelta(days=30 * i)
                all_months.append(m.strftime("%Y-%m"))

        line_data = []
        for m in all_months:
            short_label = m[5:]
            try:
                month_num = int(short_label)
                short_label = calendar.month_abbr[month_num]
            except (ValueError, IndexError):
                pass
            line_data.append((short_label, monthly.get(m, 0)))

        self.line_chart._title = "Monthly Earnings"
        self.line_chart.set_data(line_data, green)

        summary = self.store.get_summary(start, end)
        by_cat = summary["by_category"]

        income_by_cat: dict[str, float] = {}
        for t in txns:
            if t.type == "income":
                income_by_cat[t.category] = income_by_cat.get(t.category, 0) + t.amount

        bar_data = sorted(income_by_cat.items(), key=lambda x: -x[1])[:8]
        self.bar_chart.set_data(
            [(cat, amt) for cat, amt in bar_data],
            title="Earnings by Source",
        )

        pie_data = sorted(by_cat.items(), key=lambda x: -x[1])[:8]
        self.pie_chart.set_data(pie_data, title="Spending Distribution")
        self.update()