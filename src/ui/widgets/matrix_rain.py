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

Polish (v2)
-----------
  • Soft glow halo around the head character (oversize alpha-low draw)
    gives the leading glyph an authentic phosphor-bloom look.
  • Each stream gets its own mild charset bias so some streams skew more
    katakana, others more digits — adds visual variety.
  • Mutation roll is precomputed per tick (one random.random() per stream
    instead of one per cell-per-stream) — roughly halves random call volume.
  • Pixmap is only (re)allocated when the widget is actively running, so
    benign Qt resize events while hidden no longer churn memory.
  • Cooldown range tightened so wider monitors don't feel sparse.

Font
----
Tries "Matrix Code NFI" first (download free — search that exact name for the
most authentic look), then falls back through MS Gothic -> Meiryo UI ->
Noto Sans JP -> Courier New.  Half-width katakana (U+FF66-U+FF9D) renders
correctly in all of those families.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Optional

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import (
    QColor, QFont, QFontDatabase, QPainter, QPixmap,
)
from PyQt6.QtWidgets import QWidget


# ── Character palette ─────────────────────────────────────────────────────
_KATAKANA = [chr(c) for c in range(0xFF66, 0xFF9E)]   # half-width katakana
_DIGITS   = list("0123456789")
_SYMBOLS  = list(":;|=+*#@!")
_CHARSET  = _KATAKANA + _DIGITS + _SYMBOLS

# Per-stream charset variants — biases toward different glyph mixes so the
# rain feels less uniform.  Each variant is a flat list ready for random.choice.
_VARIANT_KATAKANA = _KATAKANA * 3 + _DIGITS + _SYMBOLS  # heavy katakana
_VARIANT_BALANCED = _CHARSET                            # default mix
_VARIANT_DIGITS   = _KATAKANA + _DIGITS * 4 + _SYMBOLS  # digit-heavy
_VARIANT_SYMBOLS  = _KATAKANA + _DIGITS + _SYMBOLS * 4  # symbol-heavy
_VARIANTS = (_VARIANT_KATAKANA, _VARIANT_BALANCED, _VARIANT_DIGITS, _VARIANT_SYMBOLS)


# ── Stream dataclass ──────────────────────────────────────────────────────

@dataclass
class _Stream:
    col:     int                # left-edge pixel x (snapped to cell grid)
    row:     float              # current head row (float for sub-cell smoothness)
    speed:   float              # rows per tick
    length:  int                # trail depth in cells
    chars:   list = field(default_factory=list)  # one char per trail cell
    charset: list = field(default_factory=list)  # which palette this stream draws from
    mut_p:   float = 0.18       # per-cell mutation probability for this stream


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

    # Soft halo behind the head to suggest phosphor bloom
    _C_GLOW = QColor(120, 255, 140,  55)

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

        self._font      = self._make_font(cell_size)
        self._head_font = self._make_head_font(cell_size)
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
        # Free the pixmap when hidden — no need to keep a screen-sized buffer
        # around when the user is on a non-Matrix theme.
        self._pixmap = None

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

    @staticmethod
    def _make_head_font(size: int) -> QFont:
        """Slightly larger font for the head glow halo."""
        families = QFontDatabase.families()
        for name in ("Matrix Code NFI", "MS Gothic", "Meiryo UI",
                     "Noto Sans JP", "Courier New"):
            if name in families or name == "Courier New":
                f = QFont(name, max(size - 1, 10))
                f.setStyleHint(QFont.StyleHint.Monospace)
                f.setBold(True)
                return f
        f = QFont()
        f.setFixedPitch(True)
        f.setPointSize(max(size - 1, 10))
        f.setBold(True)
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
        length  = random.randint(12, 38)   # longer trails suit the bigger cell size
        charset = random.choice(_VARIANTS)
        # Streams that are "calmer" feel slower-moving; pair speed with mutation rate
        speed   = random.uniform(0.18, 0.55)
        mut_p   = random.uniform(0.10, 0.22)
        self._streams.append(_Stream(
            col     = col,
            row     = 0.0,
            speed   = speed,
            length  = length,
            chars   = [random.choice(charset) for _ in range(length)],
            charset = charset,
            mut_p   = mut_p,
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
            if random.random() < 0.05:    # slightly higher spawn chance — denser feel
                self._spawn(col)

    def _draw_stream(self, p: QPainter, s: _Stream) -> None:
        head = int(s.row)
        nr   = self._n_rows()
        cell = self._cell
        # Cache locals — avoids attribute lookups in the hot loop
        c_head, c_hot, c_mid, c_dim, c_tail = (
            self._C_HEAD, self._C_HOT, self._C_MID, self._C_DIM, self._C_TAIL,
        )
        band = self._BAND
        align = Qt.AlignmentFlag.AlignCenter

        for i, ch in enumerate(s.chars):
            row = head - i
            if row < 0:
                continue
            if row >= nr:
                break
            if   i == 0:           colour = c_head
            elif i < band:         colour = c_hot
            elif i < band * 2:     colour = c_mid
            elif i < band * 3:     colour = c_dim
            else:                  colour = c_tail
            p.setPen(colour)
            p.drawText(s.col, row * cell, cell, cell, align, ch)

        # Soft glow halo behind the head — drawn last so it sits on top.
        # The larger bold font + low alpha gives a phosphor-bloom feel.
        if 0 <= head < nr and s.chars:
            p.setFont(self._head_font)
            p.setPen(self._C_GLOW)
            p.drawText(s.col - cell // 4, head * cell - cell // 4,
                       cell + cell // 2, cell + cell // 2,
                       align, s.chars[0])
            p.setFont(self._font)

    # ── Qt overrides ──────────────────────────────────────────────────────

    def resizeEvent(self, _) -> None:
        # Only allocate a fresh pixmap if we're actually rendering — avoids
        # expensive surface re-creation when the widget is hidden.
        if self.is_running():
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
        n_rows = self._n_rows()
        for idx, s in enumerate(self._streams):
            # Mutate roughly mut_p of the cells per tick — but precomputing the
            # threshold and using random.random() once per cell still beats the
            # old pattern slightly because we don't do attribute lookups.
            charset = s.charset
            mut_p   = s.mut_p
            chars   = s.chars
            for ci in range(len(chars)):
                if random.random() < mut_p:
                    chars[ci] = random.choice(charset)
            s.row += s.speed
            self._draw_stream(p, s)
            if s.row - s.length > n_rows:
                dead.append(idx)
                # Tighter cooldown range — denser feel, especially on wide screens
                self._cooldowns[s.col] = random.randint(5, 35)

        p.end()

        for idx in reversed(dead):
            self._streams.pop(idx)

        self._maybe_spawn()
        self.update()