"""Finance charts — custom painted graphs for earnings data visualization.

Uses QPainter for zero-dependency chart rendering: line chart, bar chart, pie chart.
"""

import calendar
from datetime import date, timedelta
from math import cos, sin, pi

from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush, QFont, QPainterPath
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QFrame, QSizePolicy,
)

from src.data.finance_store import FinanceStore

CHART_COLORS = [
    "#4a9eff", "#a6e3a1", "#cba6f7", "#fab387", "#f9e2af",
    "#94e2d5", "#f38ba8", "#f5c2e7", "#89b4fa", "#74c7ec",
]


class LineChart(QWidget):
    """Monthly earnings line chart with area fill."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(200)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._data: list[tuple[str, float]] = []  # (month_label, amount)
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

        # Title
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

        # Grid lines + Y axis labels
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

        # Build points
        points = []
        step = chart_w / (n - 1)
        for i, (label, val) in enumerate(self._data):
            x = margin_left + i * step
            y = margin_top + chart_h - (val / max_val * chart_h)
            points.append(QPointF(x, y))

            # X axis label
            painter.setPen(label_pen)
            painter.drawText(
                QRectF(x - 20, h - margin_bottom + 6, 40, 16),
                Qt.AlignmentFlag.AlignCenter,
                label,
            )

        # Area fill
        area_path = QPainterPath()
        area_path.moveTo(points[0].x(), margin_top + chart_h)
        for pt in points:
            area_path.lineTo(pt)
        area_path.lineTo(points[-1].x(), margin_top + chart_h)
        area_path.closeSubpath()

        fill_color = QColor(self._color)
        fill_color.setAlpha(40)
        painter.fillPath(area_path, QBrush(fill_color))

        # Line
        line_pen = QPen(self._color, 2)
        painter.setPen(line_pen)
        for i in range(len(points) - 1):
            painter.drawLine(points[i], points[i + 1])

        # Dots
        painter.setBrush(QBrush(self._color))
        for pt in points:
            painter.drawEllipse(pt, 4, 4)

        painter.end()


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

        # Title
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

        # Grid
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

        # Bars
        for i, (label, val) in enumerate(self._data):
            x = margin_left + bar_gap + i * (bar_w + bar_gap)
            bar_h = (val / max_val) * chart_h
            y = margin_top + chart_h - bar_h

            color = QColor(self._colors[i % len(self._colors)])
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawRoundedRect(QRectF(x, y, bar_w, bar_h), 3, 3)

            # Label below
            painter.setPen(label_pen)
            # Truncate long labels
            display_label = label if len(label) <= 8 else label[:7] + ".."
            painter.drawText(
                QRectF(x - 4, margin_top + chart_h + 4, bar_w + 8, 30),
                Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
                display_label,
            )

            # Value on top
            painter.drawText(
                QRectF(x - 4, y - 16, bar_w + 8, 14),
                Qt.AlignmentFlag.AlignCenter,
                f"${val:,.0f}",
            )

        painter.end()


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

        # Title
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

        start_angle = 90 * 16  # Qt uses 1/16th degree units, start from top
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

            # Draw pie slice
            path = QPainterPath()
            path.moveTo(cx, cy)
            path.arcTo(rect, start_angle / 16, span / 16)
            path.lineTo(cx, cy)
            painter.drawPath(path)

            start_angle += span

        # Cut out center for donut
        painter.setBrush(QBrush(QColor("#1e1e2e")))
        painter.drawEllipse(inner_rect)

        # Center text
        painter.setPen(QPen(QColor("#cdd6f4")))
        font.setPixelSize(16)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(
            inner_rect, Qt.AlignmentFlag.AlignCenter, f"${total:,.0f}"
        )

        # Legend
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


class FinanceChartsPanel(QWidget):
    """Charts view for the finance data."""

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

        # Header
        header = QHBoxLayout()
        title = QLabel("Financial Charts")
        title.setObjectName("sectionTitle")
        header.addWidget(title)
        header.addStretch()

        header.addWidget(QLabel("Period:"))
        self.period_combo = QComboBox()
        self.period_combo.addItems(["Last 6 Months", "Last 12 Months", "This Year", "All Time"])
        self.period_combo.currentTextChanged.connect(self._refresh)
        header.addWidget(self.period_combo)

        layout.addLayout(header)

        # Top row: line chart
        self.line_chart = LineChart()
        self.line_chart.setMinimumHeight(220)
        layout.addWidget(self.line_chart, 2)

        # Bottom row: bar chart + pie chart
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
        else:  # All Time
            start = date(2020, 1, 1)
        return start.isoformat(), today.isoformat()

    def _refresh(self):
        green = self._palette.get("green", "#a6e3a1")
        accent = self._palette.get("accent", "#4a9eff")

        start, end = self._get_date_range()
        txns = self.store.get_transactions(start, end)

        # Monthly earnings line chart
        monthly: dict[str, float] = {}
        monthly_expense: dict[str, float] = {}
        for t in txns:
            month_key = t.date[:7]  # YYYY-MM
            if t.type == "income":
                monthly[month_key] = monthly.get(month_key, 0) + t.amount
            else:
                monthly_expense[month_key] = monthly_expense.get(month_key, 0) + t.amount

        # Ensure we have all months in range
        all_months = sorted(set(list(monthly.keys()) + list(monthly_expense.keys())))
        if not all_months:
            # Generate last 6 months even if no data
            today = date.today()
            for i in range(5, -1, -1):
                m = today - timedelta(days=30 * i)
                all_months.append(m.strftime("%Y-%m"))

        line_data = []
        for m in all_months:
            short_label = m[5:]  # MM from YYYY-MM
            try:
                month_num = int(short_label)
                short_label = calendar.month_abbr[month_num]
            except (ValueError, IndexError):
                pass
            line_data.append((short_label, monthly.get(m, 0)))

        self.line_chart._title = "Monthly Earnings"
        self.line_chart.set_data(line_data, green)

        # Category bar chart (income sources)
        summary = self.store.get_summary(start, end)
        by_cat = summary["by_category"]
        # Split into income and expense categories
        income_by_cat: dict[str, float] = {}
        for t in txns:
            if t.type == "income":
                income_by_cat[t.category] = income_by_cat.get(t.category, 0) + t.amount

        bar_data = sorted(income_by_cat.items(), key=lambda x: -x[1])[:8]
        self.bar_chart.set_data(
            [(cat, amt) for cat, amt in bar_data],
            title="Earnings by Source",
        )

        # Pie chart — all categories
        pie_data = sorted(by_cat.items(), key=lambda x: -x[1])[:8]
        self.pie_chart.set_data(pie_data, title="Spending Distribution")

        self.update()
