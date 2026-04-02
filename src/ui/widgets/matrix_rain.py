"""Matrix digital-rain background widget.

Renders the classic phosphor-green digital rain as the *background* of the
application's central widget area.  The panels (sidebar, stack) sit on top;
they use semi-transparent ``rgba()`` backgrounds in the Matrix stylesheet so
the rain glows through every surface.

Architecture
------------
``MatrixRainWidget`` is a plain ``QWidget`` child of the central widget.  It is
always positioned to fill its parent exactly, and ``lower()`` places it at the
very bottom of the z-order so every other panel sits in front of it.

``WA_TransparentForMouseEvents`` is set so no click, scroll, or key press is
intercepted — they all reach the panels in front.

``setAutoFillBackground(False)`` prevents Qt from painting a solid colour over
the rain surface before our own ``paintEvent`` runs.

Rendering
---------
A ``QPixmap`` is used as a phosphor screen.  Each 40 ms tick:

1. A semi-transparent black rectangle fades all existing glyphs toward black
   (phosphor decay / trailing glow effect).
2. Each active stream is advanced and its head + trail characters are drawn
   in successively dimmer greens.
3. New streams are randomly spawned in idle columns.

Font
----
Tries "Matrix Code NFI" first (download free — search that exact name for the
most authentic look), then falls back through MS Gothic -> Meiryo UI ->
Noto Sans JP -> Courier New.  Half-width katakana (U+FF66-U+FF9D) renders
correctly in all of those families.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Optional

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import (
    QColor, QFont, QFontDatabase, QFontMetrics, QPainter, QPixmap,
)
from PyQt6.QtWidgets import QWidget


# ── Character palette ─────────────────────────────────────────────────────
_KATAKANA = [chr(c) for c in range(0xFF66, 0xFF9E)]   # half-width katakana
_DIGITS   = list("0123456789")
_SYMBOLS  = list(":;|=+*#@!")
_CHARSET  = _KATAKANA + _DIGITS + _SYMBOLS


def _rand_char() -> str:
    return random.choice(_CHARSET)


# ── Stream dataclass ──────────────────────────────────────────────────────

@dataclass
class _Stream:
    col:    int        # left-edge pixel x (snapped to cell grid)
    row:    float      # current head row (float for sub-cell smoothness)
    speed:  float      # rows per tick
    length: int        # trail depth in cells
    chars:  list       # one char per trail cell, randomly mutated each tick


# ── Widget ────────────────────────────────────────────────────────────────

class MatrixRainWidget(QWidget):
    """Full-parent-fill background widget that paints Matrix digital rain.

    Drop this widget as a child of your central widget and call lower()
    after all other children are added.
    """

    # Phosphor colour palette — tuned for the movie aesthetic:
    # warm near-white tip, organic mid-green trail, not pure neon
    _C_HEAD = QColor(210, 255, 200, 255)   # warm near-white — leading char
    _C_HOT  = QColor(0,   192,  60, 255)   # bright phosphor — 1-2 behind head
    _C_MID  = QColor(0,   145,  38, 225)   # mid trail
    _C_DIM  = QColor(0,    88,  22, 170)   # lower trail
    _C_TAIL = QColor(0,    44,  10,  95)   # tail end, barely visible

    _BAND   = 3    # cells per colour band — wider bands look better at larger size
    _FADE   = 16   # black-wash alpha per tick — slightly lower = longer, lazier trails

    def __init__(self, parent: QWidget, cell_size: int = 22):
        super().__init__(parent)
        self._cell      = cell_size
        self._streams:   list[_Stream]     = []
        self._cooldowns: dict[int, int]    = {}
        self._pixmap:    Optional[QPixmap] = None

        self._timer = QTimer(self)
        self._timer.setInterval(40)   # 25 fps
        self._timer.timeout.connect(self._tick)

        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground,         True)
        self.setAutoFillBackground(False)

        self._font = self._make_font(cell_size)
        self.hide()

    # ── Public API ────────────────────────────────────────────────────────

    def start(self) -> None:
        """Fill parent, push to back of z-order, begin animating."""
        self._fit_to_parent()
        self._reset_pixmap()
        self._streams.clear()
        self._cooldowns.clear()
        self.show()
        self.lower()
        self._timer.start()

    def stop(self) -> None:
        self._timer.stop()
        self.hide()

    def is_running(self) -> bool:
        return self._timer.isActive()

    def sync_size(self) -> None:
        """Call from the parent widget's resizeEvent."""
        self._fit_to_parent()
        if self.is_running():
            self._reset_pixmap()
            self.lower()

    # ── Internal helpers ──────────────────────────────────────────────────

    def _fit_to_parent(self) -> None:
        if self.parent():
            pw = self.parent().width()
            ph = self.parent().height()
            self.setGeometry(0, 0, pw, ph)

    @staticmethod
    def _make_font(size: int) -> QFont:
        families = QFontDatabase.families()
        for name in ("Matrix Code NFI", "MS Gothic", "Meiryo UI",
                     "Noto Sans JP", "Courier New"):
            if name in families or name == "Courier New":
                f = QFont(name, max(size - 4, 8))
                f.setStyleHint(QFont.StyleHint.Monospace)
                return f
        f = QFont()
        f.setFixedPitch(True)
        f.setPointSize(max(size - 4, 8))
        return f

    def _reset_pixmap(self) -> None:
        w = max(self.width(),  1)
        h = max(self.height(), 1)
        self._pixmap = QPixmap(w, h)
        self._pixmap.fill(QColor(0, 0, 0, 255))

    def _col_xs(self) -> list:
        return list(range(0, max(self.width() - self._cell, 1), self._cell))

    def _n_rows(self) -> int:
        return max(self.height() // self._cell, 1)

    def _spawn(self, col: int) -> None:
        length = random.randint(12, 38)   # longer trails suit the bigger cell size
        self._streams.append(_Stream(
            col    = col,
            row    = 0.0,
            speed  = random.uniform(0.18, 0.55),   # slower — matches the film pacing
            length = length,
            chars  = [_rand_char() for _ in range(length)],
        ))

    def _maybe_spawn(self) -> None:
        active = {s.col for s in self._streams}
        for col in self._col_xs():
            if col in active:
                continue
            if col in self._cooldowns:
                self._cooldowns[col] -= 1
                if self._cooldowns[col] > 0:
                    continue
                del self._cooldowns[col]
            if random.random() < 0.04:
                self._spawn(col)

    def _draw_stream(self, p: QPainter, s: _Stream) -> None:
        head = int(s.row)
        nr   = self._n_rows()
        for i, ch in enumerate(s.chars):
            row = head - i
            if row < 0:
                continue
            if row >= nr:
                break
            if   i == 0:              colour = self._C_HEAD
            elif i < self._BAND:      colour = self._C_HOT
            elif i < self._BAND * 2:  colour = self._C_MID
            elif i < self._BAND * 3:  colour = self._C_DIM
            else:                     colour = self._C_TAIL
            p.setPen(colour)
            p.drawText(s.col, row * self._cell,
                       self._cell, self._cell,
                       Qt.AlignmentFlag.AlignCenter, ch)

    # ── Qt overrides ──────────────────────────────────────────────────────

    def resizeEvent(self, _) -> None:
        self._reset_pixmap()
        valid = set(self._col_xs())
        self._streams = [s for s in self._streams if s.col in valid]

    def paintEvent(self, _) -> None:
        if self._pixmap is None:
            return
        p = QPainter(self)
        p.drawPixmap(0, 0, self._pixmap)
        p.end()

    # ── Animation tick ────────────────────────────────────────────────────

    def _tick(self) -> None:
        if self._pixmap is None:
            return

        p = QPainter(self._pixmap)
        p.setFont(self._font)

        # Phosphor decay: semi-transparent black wash
        p.fillRect(0, 0, self._pixmap.width(), self._pixmap.height(),
                   QColor(0, 0, 0, self._FADE))

        # Advance and draw each stream
        dead: list = []
        for idx, s in enumerate(self._streams):
            for ci in range(len(s.chars)):
                if random.random() < 0.18:   # ~18% chance per cell per tick — active flickering
                    s.chars[ci] = _rand_char()
            s.row += s.speed
            self._draw_stream(p, s)
            if s.row - s.length > self._n_rows():
                dead.append(idx)
                self._cooldowns[s.col] = random.randint(8, 55)

        p.end()

        for idx in reversed(dead):
            self._streams.pop(idx)

        self._maybe_spawn()
        self.update()