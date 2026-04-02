"""Reusable theme-aware navigation arrow button.

Draws its arrow via QPainter — no glyph/font lookup whatsoever.
Works identically on every OS, every font configuration, every theme.

Usage:
    btn = NavButton("left")               # 28×28 single arrow
    btn = NavButton("right", size=24)     # custom size
    btn = NavButton("left", double=True)  # double arrow  «  style
    btn.clicked.connect(my_slot)

    # When theme changes:
    btn.refresh(palette_dict)
"""

from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import (
    QPainter, QColor, QBrush, QPen, QPolygonF,
)
from PyQt6.QtWidgets import QPushButton


# Module-level defaults (Catppuccin Dark) — overridden immediately when the
# first theme is applied via refresh().
_DEFAULTS: dict[str, str] = {
    "surface":        "#313244",
    "hover":          "#3b3d54",
    "border":         "#45475a",
    "fg":             "#cdd6f4",
    "accent":         "#89b4fa",
    "accent_fg":      "#1e1e2e",
    "accent_pressed": "#74a4ea",
}


class NavButton(QPushButton):
    """Theme-aware navigation arrow button rendered with QPainter.

    Parameters
    ----------
    direction : str
        One of ``'left'``, ``'right'``, ``'up'``, ``'down'``.
    size : int
        Width and height in pixels (the button is always square).
    double : bool
        When True, draws two chevrons (‹‹ / ›› style) for year-jump buttons.
    tooltip : str
        Optional tooltip text.
    """

    def __init__(
        self,
        direction: str,
        size: int = 28,
        double: bool = False,
        tooltip: str = "",
        parent=None,
    ):
        super().__init__(parent)
        self._direction = direction
        self._double = double
        self._hovered = False
        self._pressed_state = False
        self._c: dict[str, str] = dict(_DEFAULTS)

        self.setFixedSize(size, size)
        self.setText("")           # pure painter — no text label
        self.setFlat(True)         # suppress default QPushButton chrome
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        if tooltip:
            self.setToolTip(tooltip)

    # ── Public API ───────────────────────────────────────────────────────────

    def refresh(self, palette: dict) -> None:
        """Apply new palette colors and schedule a repaint."""
        for key in _DEFAULTS:
            if key in palette:
                self._c[key] = palette[key]
        self.update()

    # ── Qt overrides ─────────────────────────────────────────────────────────

    def enterEvent(self, e) -> None:
        self._hovered = True
        self.update()

    def leaveEvent(self, e) -> None:
        self._hovered = False
        self.update()

    def mousePressEvent(self, e) -> None:
        self._pressed_state = True
        self.update()
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e) -> None:
        self._pressed_state = False
        self.update()
        super().mouseReleaseEvent(e)

    def paintEvent(self, _) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()

        # ── Background fill ──────────────────────────────────────────────────
        if self._pressed_state:
            bg = QColor(self._c["accent"])
            bg.setAlpha(210)
        elif self._hovered:
            bg = QColor(self._c["accent"])
            bg.setAlpha(38)
        else:
            bg = QColor(self._c["surface"])

        p.setBrush(QBrush(bg))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(1, 1, w - 2, h - 2, 4, 4)

        # ── Border ───────────────────────────────────────────────────────────
        border_col = QColor(
            self._c["accent"] if (self._hovered or self._pressed_state)
            else self._c["border"]
        )
        p.setPen(QPen(border_col, 1))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawRoundedRect(0, 0, w - 1, h - 1, 4, 4)

        # ── Arrow(s) ─────────────────────────────────────────────────────────
        arrow_col = QColor(
            self._c["accent_fg"] if self._pressed_state
            else (self._c["accent"] if self._hovered else self._c["fg"])
        )
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QBrush(arrow_col))

        if self._double:
            self._draw_double(p, w, h)
        else:
            self._draw_single(p, w / 2.0, h / 2.0, w, h)

        p.end()

    # ── Drawing helpers ───────────────────────────────────────────────────────

    def _arrow_pts(
        self, cx: float, cy: float, w: int, h: int
    ) -> list[QPointF]:
        """Return triangle vertices for a single chevron centred at (cx, cy)."""
        s = min(w, h) * 0.18          # half the arrow's cross-axis span
        r = min(w, h) * 0.14          # depth along the pointing axis
        d = self._direction
        if d == "left":
            return [QPointF(cx + r, cy - s), QPointF(cx + r, cy + s), QPointF(cx - r, cy)]
        if d == "right":
            return [QPointF(cx - r, cy - s), QPointF(cx - r, cy + s), QPointF(cx + r, cy)]
        if d == "up":
            return [QPointF(cx - s, cy + r), QPointF(cx + s, cy + r), QPointF(cx, cy - r)]
        # down
        return [QPointF(cx - s, cy - r), QPointF(cx + s, cy - r), QPointF(cx, cy + r)]

    def _draw_single(
        self, p: QPainter, cx: float, cy: float, w: int, h: int
    ) -> None:
        pts = self._arrow_pts(cx, cy, w, h)
        p.drawPolygon(QPolygonF(pts))

    def _draw_double(self, p: QPainter, w: int, h: int) -> None:
        """Draw two small chevrons offset along the pointing axis."""
        gap = min(w, h) * 0.22        # spacing between the two chevrons
        cx, cy = w / 2.0, h / 2.0
        d = self._direction
        if d in ("left", "right"):
            off = QPointF(gap / 2 if d == "right" else -gap / 2, 0)
        else:
            off = QPointF(0, gap / 2 if d == "down" else -gap / 2)

        for sign in (-1, 1):
            ocx = cx + off.x() * sign
            ocy = cy + off.y() * sign
            pts = self._arrow_pts(ocx, ocy, w, h)
            p.drawPolygon(QPolygonF(pts))