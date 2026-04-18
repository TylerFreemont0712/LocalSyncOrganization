"""Debug / Council Sandbox panel.

Always the final panel in the sidebar (Ctrl+0).  Provides:
  • A free-form prompt box to run any text through the LLM Council
  • Per-member response cards showing each model's individual answer + timing
  • A synthesised result box at the bottom with copy-to-clipboard
  • Graceful fallback to single-model mode when the council is not configured

This panel intentionally has no persistent state — it is a live debug
surface, not a data store.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QPlainTextEdit, QTextEdit, QScrollArea, QFrame, QSizePolicy,
    QApplication, QComboBox,
)

from src.utils.llm import (
    LLMResult, CouncilResult,
    LLMSignals, CouncilSignals,
    load_llm_client, load_council_config,
    COUNCIL_SYNTHESIS_MODES,
)

# ── Module-level palette (updated by set_palette) ─────────────────────────────
_PALETTE: dict = {}


def _p(key: str, fallback: str = "") -> str:
    return _PALETTE.get(key, fallback)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Member card widget
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class _MemberCard(QFrame):
    """Displays a single council member's response."""

    def __init__(self, index: int, result: LLMResult, parent=None):
        super().__init__(parent)
        self.setObjectName("MemberCard")
        self._apply_style()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(4)

        # Header row
        short_model = result.model.split("/")[-1].replace(":free", "").replace(":nitro", "")
        header = QHBoxLayout()
        model_lbl = QLabel(f"  Model {index + 1}  ·  {short_model}")
        model_lbl.setStyleSheet(
            f"font-size:11px;font-weight:bold;"
            f"color:{_p('accent','#89b4fa')};"
        )
        header.addWidget(model_lbl)
        header.addStretch()

        timing_lbl = QLabel(result.timing_summary())
        timing_lbl.setStyleSheet(
            f"font-size:10px;color:{_p('muted','#6c7086')};"
        )
        header.addWidget(timing_lbl)
        layout.addLayout(header)

        # Response text
        body = QTextEdit()
        body.setReadOnly(True)
        body.setPlainText(result.text.strip())
        body.setMinimumHeight(100)
        body.setMaximumHeight(200)
        body.setStyleSheet(
            f"QTextEdit{{border:1px solid {_p('border','#45475a')};"
            f"border-radius:4px;"
            f"background-color:{_p('bg','#1e1e2e')};"
            f"color:{_p('fg','#cdd6f4')};"
            f"font-size:12px;padding:4px;}}"
        )
        layout.addWidget(body)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

    def _apply_style(self):
        self.setStyleSheet(
            f"MemberCard{{border:1px solid {_p('border','#45475a')};"
            f"border-radius:6px;"
            f"background-color:{_p('surface','#313244')};}}"
        )


class _FailedCard(QFrame):
    """Displayed when a council member errored out."""

    def __init__(self, model: str, parent=None):
        super().__init__(parent)
        self.setObjectName("FailedCard")
        self.setStyleSheet(
            f"FailedCard{{border:1px solid {_p('red','#f38ba8')};"
            f"border-radius:6px;"
            f"background-color:{_p('surface','#313244')};}}"
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)

        short = model.split("/")[-1].replace(":free", "").replace(":nitro", "")
        lbl = QLabel(f"✗  {short}  —  failed to respond")
        lbl.setStyleSheet(
            f"font-size:11px;color:{_p('red','#f38ba8')};"
        )
        layout.addWidget(lbl)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Debug Panel
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class DebugPanel(QWidget):
    """LLM Council debug / sandbox panel — always the last nav item."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._busy           = False
        self._llm_signals:     LLMSignals    | None = None
        self._council_signals: CouncilSignals| None = None
        self._build_ui()

    # ── Palette ─────────────────────────────────────────────────────────────

    def set_palette(self, palette: dict):
        global _PALETTE
        _PALETTE = palette
        self._refresh_styles()

    def _refresh_styles(self):
        self._header_lbl.setStyleSheet(
            f"font-size:15px;font-weight:bold;color:{_p('fg')};"
        )
        self._status_lbl.setStyleSheet(
            f"font-size:11px;color:{_p('muted')};"
        )
        self._synth_lbl.setStyleSheet(
            f"font-size:12px;font-weight:bold;color:{_p('accent')};"
        )
        self._synth_box.setStyleSheet(
            f"QTextEdit{{border:2px solid {_p('accent','#89b4fa')};"
            f"border-radius:6px;"
            f"background-color:{_p('surface','#313244')};"
            f"color:{_p('fg','#cdd6f4')};"
            f"font-size:13px;padding:8px;}}"
        )

    # ── Build UI ─────────────────────────────────────────────────────────────

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(16, 12, 16, 12)
        root.setSpacing(10)

        # ── Top bar ──────────────────────────────────────────────────────────
        top_bar = QHBoxLayout()

        self._header_lbl = QLabel("🔬  Debug / Council Sandbox")
        self._header_lbl.setObjectName("sectionTitle")
        top_bar.addWidget(self._header_lbl)
        top_bar.addStretch()

        self._mode_combo = QComboBox()
        self._mode_combo.addItems(["Auto", "Council", "Single Model"])
        self._mode_combo.setToolTip(
            "Auto: use Council if configured, else single model\n"
            "Council: force council mode (requires council config)\n"
            "Single Model: always use the primary model"
        )
        self._mode_combo.setMaximumWidth(140)
        top_bar.addWidget(QLabel("Mode:"))
        top_bar.addWidget(self._mode_combo)

        root.addLayout(top_bar)

        # ── Prompt area ───────────────────────────────────────────────────────
        prompt_lbl = QLabel("Prompt")
        prompt_lbl.setObjectName("subtitle")
        root.addWidget(prompt_lbl)

        self._prompt_edit = QPlainTextEdit()
        self._prompt_edit.setPlaceholderText(
            "Type a prompt here and click Run to send it to the council…"
        )
        self._prompt_edit.setFixedHeight(90)
        root.addWidget(self._prompt_edit)

        # ── Run / Clear row ───────────────────────────────────────────────────
        btn_row = QHBoxLayout()

        self._run_btn = QPushButton("▶  Run")
        self._run_btn.setFixedHeight(32)
        self._run_btn.clicked.connect(self._run)
        btn_row.addWidget(self._run_btn)

        self._clear_btn = QPushButton("Clear")
        self._clear_btn.setObjectName("secondary")
        self._clear_btn.setFixedHeight(32)
        self._clear_btn.clicked.connect(self._clear)
        btn_row.addWidget(self._clear_btn)

        btn_row.addStretch()

        self._status_lbl = QLabel("Idle")
        self._status_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        btn_row.addWidget(self._status_lbl)

        root.addLayout(btn_row)

        # ── Separator ────────────────────────────────────────────────────────
        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine)
        root.addWidget(sep)

        # ── Member responses (scrollable) ─────────────────────────────────────
        members_lbl = QLabel("Member Responses")
        members_lbl.setObjectName("subtitle")
        root.addWidget(members_lbl)

        self._members_scroll = QScrollArea()
        self._members_scroll.setWidgetResizable(True)
        self._members_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self._members_scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self._members_scroll.setMinimumHeight(120)
        self._members_scroll.setMaximumHeight(320)

        self._members_container = QWidget()
        self._members_layout = QVBoxLayout(self._members_container)
        self._members_layout.setContentsMargins(0, 0, 0, 0)
        self._members_layout.setSpacing(8)
        self._members_layout.addStretch()

        self._members_scroll.setWidget(self._members_container)
        root.addWidget(self._members_scroll, 1)

        # ── Synthesised result ────────────────────────────────────────────────
        sep2 = QFrame()
        sep2.setObjectName("separator")
        sep2.setFrameShape(QFrame.Shape.HLine)
        root.addWidget(sep2)

        synth_hdr = QHBoxLayout()
        self._synth_lbl = QLabel("Synthesised Result")
        self._synth_lbl.setObjectName("subtitle")
        synth_hdr.addWidget(self._synth_lbl)
        synth_hdr.addStretch()

        self._copy_btn = QPushButton("Copy")
        self._copy_btn.setObjectName("secondary")
        self._copy_btn.setFixedHeight(26)
        self._copy_btn.setFixedWidth(60)
        self._copy_btn.setEnabled(False)
        self._copy_btn.clicked.connect(self._copy_result)
        synth_hdr.addWidget(self._copy_btn)
        root.addLayout(synth_hdr)

        self._synth_box = QTextEdit()
        self._synth_box.setReadOnly(True)
        self._synth_box.setPlaceholderText(
            "Synthesised answer will appear here after a council run…"
        )
        self._synth_box.setMinimumHeight(100)
        font = QFont()
        font.setPixelSize(13)
        self._synth_box.setFont(font)
        root.addWidget(self._synth_box, 1)

        self._refresh_styles()

    # ── Run logic ────────────────────────────────────────────────────────────

    def _run(self):
        if self._busy:
            return

        prompt = self._prompt_edit.toPlainText().strip()
        if not prompt:
            self._set_status("Enter a prompt first.")
            return

        messages = [{"role": "user", "content": prompt}]
        mode     = self._mode_combo.currentText()

        # Determine whether to use council or single model
        council = load_council_config() if mode != "Single Model" else None
        client  = None if council else load_llm_client()

        if mode == "Council" and council is None:
            self._set_status("Council not configured — check Network → AI tab.")
            return

        if council is None and client is None:
            self._set_status("No API key configured — check Network → AI tab.")
            return

        self._busy = True
        self._run_btn.setEnabled(False)
        self._clear_results()
        self._synth_box.clear()
        self._copy_btn.setEnabled(False)

        if council:
            # The mode dropdown is bound to COUNCIL_SYNTHESIS_MODES; only
            # pass it through if it's a real council mode (the dropdown also
            # contains the "Single Model" sentinel which is handled above).
            from src.utils.llm import COUNCIL_SYNTHESIS_MODES as _MODES
            chosen_mode = mode if mode in _MODES else council.default_mode
            self._set_status(
                f"Running council (3 passes · {chosen_mode})…"
            )
            self._council_signals = CouncilSignals()
            self._council_signals.result.connect(self._on_council_result)
            self._council_signals.error.connect(self._on_error)
            council.complete_async(
                messages,
                mode=chosen_mode,
                on_result=self._council_signals.result.emit,
                on_error=self._council_signals.error.emit,
                max_tokens=1200,
                temperature=0.45,
            )
        else:
            self._set_status("Running single model…")
            self._llm_signals = LLMSignals()
            self._llm_signals.result.connect(self._on_single_result)
            self._llm_signals.error.connect(self._on_error)
            client.complete_async(
                messages,
                on_result=self._llm_signals.result.emit,
                on_error=self._llm_signals.error.emit,
                max_tokens=1200,
                temperature=0.45,
            )

    # ── Result handlers ──────────────────────────────────────────────────────

    def _on_council_result(self, result: CouncilResult):
        self._busy = False
        self._run_btn.setEnabled(True)

        # Render member cards
        for i, member in enumerate(result.members):
            card = _MemberCard(i, member)
            self._members_layout.insertWidget(
                self._members_layout.count() - 1, card
            )

        for failed_model in result.failed:
            card = _FailedCard(failed_model)
            self._members_layout.insertWidget(
                self._members_layout.count() - 1, card
            )

        # Show synthesis (or quick-pick winner — both live on result.final)
        self._synth_box.setPlainText(result.final.text.strip())
        if result.mode == "Quick":
            self._synth_lbl.setText("Quick-Picked Result  ·  Multi-Pass")
        else:
            self._synth_lbl.setText("Synthesised Result  ·  Multi-Pass")
        self._copy_btn.setEnabled(True)
        self._set_status(result.summary())

    def _on_single_result(self, result: LLMResult):
        self._busy = False
        self._run_btn.setEnabled(True)

        # Show as a single member card
        card = _MemberCard(0, result)
        self._members_layout.insertWidget(
            self._members_layout.count() - 1, card
        )

        # In single-model mode the result IS the synthesis
        self._synth_box.setPlainText(result.text.strip())
        self._synth_lbl.setText("Result  ·  Single Model")
        self._copy_btn.setEnabled(True)
        self._set_status(result.timing_summary())

    def _on_error(self, err: str):
        self._busy = False
        self._run_btn.setEnabled(True)
        self._set_status(f"Error: {err}")

    # ── Helpers ──────────────────────────────────────────────────────────────

    def _clear_results(self):
        """Remove all member cards (keep the trailing stretch)."""
        while self._members_layout.count() > 1:
            item = self._members_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _clear(self):
        self._prompt_edit.clear()
        self._clear_results()
        self._synth_box.clear()
        self._synth_lbl.setText("Synthesised Result")
        self._copy_btn.setEnabled(False)
        self._set_status("Idle")

    def _copy_result(self):
        text = self._synth_box.toPlainText()
        if text:
            QApplication.clipboard().setText(text)
            self._set_status("Copied to clipboard.")
            QTimer.singleShot(2500, lambda: self._set_status("Idle"))

    def _set_status(self, msg: str):
        self._status_lbl.setText(msg)