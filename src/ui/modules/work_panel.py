"""Work Panel — daily write-up generator with centralised AI client injection."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QFrame, QScrollArea, QCheckBox,
    QApplication, QPlainTextEdit, QSplitter, QMessageBox, QDialog,
)

from src.config import load_config
from src.data.activity_store import ActivityStore, Activity, ACTIVITY_COLORS, DEFAULT_COLOR
from src.utils.llm import LLMClient, LLMResult, LLMSignals, DEFAULT_MODEL, save_llm_config


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Helpers
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

_JP_WEEKDAYS = ["月", "火", "水", "木", "金", "土", "日"]


def _jp_date(d: date) -> str:
    wd = _JP_WEEKDAYS[d.weekday()]
    return f"{d.year}年{d.month}月{d.day}日（{wd}）"


def _jp_duration(minutes: int) -> str:
    if minutes <= 0:
        return ""
    h, m = divmod(minutes, 60)
    if h and m:
        return f"{h}時間{m}分"
    return f"{h}時間" if h else f"{m}分"


def _build_report(jp_date_str: str, selected: list[tuple[str, int]],
                  renraku: str, ashita: str, ai_content: str = "") -> str:
    lines = [f"【日付】{jp_date_str}", "【本日の作業内容】"]
    if ai_content.strip():
        lines += [ln for ln in ai_content.strip().splitlines()]
    else:
        for name, mins in selected:
            dur = _jp_duration(mins)
            lines.append(f"・{name}（{dur}）" if dur else f"・{name}")
    lines.append("【連絡事項】")
    lines += [ln for ln in renraku.strip().splitlines()]
    lines.append("【明日の予定】")
    lines += [ln for ln in ashita.strip().splitlines()]
    return "\n".join(lines)


def _build_llm_prompt(activities: list[tuple[str, int, str]]) -> list[dict]:
    items = []
    for name, mins, notes in activities:
        dur       = _jp_duration(mins) or "不明"
        note_text = notes.strip() if notes.strip() else "（メモなし）"
        items.append(f"・{name}（{dur}）: {note_text}")
    system = (
        "あなたはソフトウェアエンジニアの日報作成を支援するアシスタントです。"
        "ビジネス向けの丁寧で簡潔な日本語で記述してください。"
    )
    user = (
        "以下の作業内容（英語のメモ付き）を元に、日報の【本日の作業内容】セクションの"
        "箇条書きを作成してください。\n\n"
        "【ルール】\n"
        "- 各項目は「・」で始める\n"
        "- 作業時間を括弧内に記載（例：2時間、1時間30分）\n"
        "- 英語のメモは自然なビジネス日本語に意訳する\n"
        "- 1項目につき1〜2文で簡潔にまとめる\n"
        "- ヘッダー（【本日の作業内容】）は出力しない、箇条書きのみ出力する\n\n"
        "作業リスト:\n" + "\n".join(items)
    )
    return [{"role": "system", "content": system},
            {"role": "user",   "content": user}]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Activity check row
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class _ActivityCheckRow(QWidget):
    def __init__(self, activity: Activity, palette: dict, parent=None):
        super().__init__(parent)
        self.activity = activity
        self.setFixedHeight(32)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 2, 8, 2)
        layout.setSpacing(8)

        self.check = QCheckBox()
        self.check.setChecked(True)
        layout.addWidget(self.check)

        color_str = ACTIVITY_COLORS.get(activity.activity, DEFAULT_COLOR)
        dot = QLabel("●")
        dot.setStyleSheet(f"color:{color_str};font-size:10px;")
        dot.setFixedWidth(14)
        layout.addWidget(dot)

        name_lbl = QLabel(activity.activity)
        name_lbl.setStyleSheet("font-size:12px;font-weight:bold;")
        layout.addWidget(name_lbl, 1)

        muted = palette.get("muted", "#7f849c")
        time_lbl = QLabel(f"{activity.start_time}–{activity.end_time}")
        time_lbl.setStyleSheet(f"font-size:10px;color:{muted};")
        layout.addWidget(time_lbl)

        dur = activity.duration_minutes
        dur_lbl = QLabel(_jp_duration(dur) if dur > 0 else "—")
        dur_lbl.setStyleSheet(f"font-size:11px;color:{muted};min-width:64px;")
        dur_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(dur_lbl)

        if activity.notes and activity.notes.strip():
            note_dot = QLabel("[note]")
            note_dot.setStyleSheet(f"font-size:9px;color:{muted};")
            note_dot.setToolTip(activity.notes.strip())
            layout.addWidget(note_dot)

    def is_checked(self) -> bool:
        return self.check.isChecked()

    def row_data(self) -> tuple[str, int]:
        return (self.activity.activity, self.activity.duration_minutes)

    def row_data_with_notes(self) -> tuple[str, int, str]:
        return (self.activity.activity,
                self.activity.duration_minutes,
                self.activity.notes or "")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  WorkPanel
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class WorkPanel(QWidget):
    """Daily 日報 write-up panel with optional AI generation.

    The LLMClient is owned by MainWindow and injected here.
    When settings change in the NetworkDialog, MainWindow calls
    set_llm_client() to push the new client in.
    """

    llm_config_changed = pyqtSignal()   # emitted after local settings save

    def __init__(self, llm_client: "LLMClient | None" = None, parent=None):
        super().__init__(parent)
        self._palette:    dict                    = {}
        self._llm_client: LLMClient | None        = llm_client
        self.store                                = ActivityStore()
        self._rows:       list[_ActivityCheckRow] = []
        self._ai_content  = ""
        self._ai_busy     = False
        # Kept on self — prevents GC before daemon thread fires
        self._signals     = LLMSignals()
        self._signals.result.connect(self._on_ai_result)
        self._signals.error.connect(self._on_ai_error)

        self._build_ui()
        self._load_drafts()
        self._refresh()

        self._auto_timer = QTimer(self)
        self._auto_timer.setInterval(60_000)
        self._auto_timer.timeout.connect(self._refresh)
        self._auto_timer.start()

    # ── Public API ──────────────────────────────────

    def set_llm_client(self, client: "LLMClient | None") -> None:
        self._llm_client = client
        status = "connected" if client else "no API key configured"
        self._ai_status.setText(f"AI: {status}")
        QTimer.singleShot(3000, lambda: self._ai_status.setText(""))

    def set_palette(self, palette: dict) -> None:
        self._palette = palette
        self._refresh()

    # ── Build UI ────────────────────────────────────

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(14, 10, 14, 10)
        root.setSpacing(8)

        # ── Header ──────────────────────────────────
        hdr = QHBoxLayout()
        title = QLabel("Work Panel — 日報作成")
        title.setObjectName("sectionTitle")
        hdr.addWidget(title)
        hdr.addStretch()

        self._date_lbl = QLabel()
        self._date_lbl.setStyleSheet("font-size:12px;font-weight:bold;")
        hdr.addWidget(self._date_lbl)

        # Text-label buttons — no emoji, always renders
        settings_btn = QPushButton("AI Settings")
        settings_btn.setObjectName("secondary")
        settings_btn.setFixedHeight(28)
        settings_btn.setToolTip("Configure OpenRouter API key and model")
        settings_btn.clicked.connect(self._open_settings)
        hdr.addWidget(settings_btn)

        refresh_btn = QPushButton("Refresh")
        refresh_btn.setObjectName("secondary")
        refresh_btn.setFixedHeight(28)
        refresh_btn.setToolTip("Reload today's activities")
        refresh_btn.clicked.connect(self._refresh)
        hdr.addWidget(refresh_btn)

        root.addLayout(hdr)

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        sep.setObjectName("separator")
        root.addWidget(sep)

        # ── Main splitter ───────────────────────────
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)

        # LEFT pane
        left = QWidget()
        left_l = QVBoxLayout(left)
        left_l.setContentsMargins(0, 0, 8, 0)
        left_l.setSpacing(8)

        # Activity list header with All / None buttons
        act_hdr = QHBoxLayout()
        act_title = QLabel("Today's Activities")
        act_title.setStyleSheet("font-size:12px;font-weight:bold;")
        act_hdr.addWidget(act_title)
        act_hdr.addStretch()

        all_btn = QPushButton("Select All")
        all_btn.setObjectName("secondary")
        all_btn.setFixedHeight(26)
        all_btn.clicked.connect(lambda: self._set_all_checked(True))
        act_hdr.addWidget(all_btn)

        none_btn = QPushButton("Select None")
        none_btn.setObjectName("secondary")
        none_btn.setFixedHeight(26)
        none_btn.clicked.connect(lambda: self._set_all_checked(False))
        act_hdr.addWidget(none_btn)

        left_l.addLayout(act_hdr)

        # Scrollable checklist
        self._act_container = QWidget()
        self._act_layout = QVBoxLayout(self._act_container)
        self._act_layout.setContentsMargins(0, 0, 0, 0)
        self._act_layout.setSpacing(1)

        act_scroll = QScrollArea()
        act_scroll.setWidgetResizable(True)
        act_scroll.setWidget(self._act_container)
        act_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        act_scroll.setFrameShape(QFrame.Shape.NoFrame)
        act_scroll.setMinimumHeight(100)
        act_scroll.setMaximumHeight(240)
        left_l.addWidget(act_scroll)

        # AI generate row
        ai_row = QHBoxLayout()
        self._ai_btn = QPushButton("AI Generate Japanese Write-up")
        self._ai_btn.setFixedHeight(30)
        self._ai_btn.setToolTip(
            "Uses the configured LLM to write polished Japanese descriptions\n"
            "from your activity notes. Configure via AI Settings above.")
        self._ai_btn.clicked.connect(self._run_ai)
        ai_row.addWidget(self._ai_btn, 1)

        self._clear_ai_btn = QPushButton("Clear AI")
        self._clear_ai_btn.setObjectName("secondary")
        self._clear_ai_btn.setFixedHeight(30)
        self._clear_ai_btn.setToolTip("Revert to auto-generated bullets")
        self._clear_ai_btn.clicked.connect(self._clear_ai)
        self._clear_ai_btn.setVisible(False)
        ai_row.addWidget(self._clear_ai_btn)
        left_l.addLayout(ai_row)

        self._ai_status = QLabel("")
        self._ai_status.setStyleSheet("font-size:10px;")
        self._ai_status.setWordWrap(True)
        left_l.addWidget(self._ai_status)

        sep2 = QFrame(); sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setObjectName("separator")
        left_l.addWidget(sep2)

        ren_lbl = QLabel("【連絡事項】")
        ren_lbl.setStyleSheet("font-size:12px;font-weight:bold;")
        left_l.addWidget(ren_lbl)
        self._renraku_edit = QPlainTextEdit()
        self._renraku_edit.setPlaceholderText("Communications, blockers, notices…")
        self._renraku_edit.setFixedHeight(75)
        self._renraku_edit.textChanged.connect(self._update_preview)
        left_l.addWidget(self._renraku_edit)

        ash_lbl = QLabel("【明日の予定】")
        ash_lbl.setStyleSheet("font-size:12px;font-weight:bold;")
        left_l.addWidget(ash_lbl)
        self._ashita_edit = QPlainTextEdit()
        self._ashita_edit.setPlaceholderText(
            "e.g.\nバックアップ手順書の仕上げに集中する\nコードレビューの対応")
        self._ashita_edit.setMinimumHeight(90)
        self._ashita_edit.textChanged.connect(self._update_preview)
        left_l.addWidget(self._ashita_edit, 1)

        save_btn = QPushButton("Save Draft")
        save_btn.setObjectName("secondary")
        save_btn.setFixedHeight(28)
        save_btn.clicked.connect(self._save_drafts)
        left_l.addWidget(save_btn)

        splitter.addWidget(left)

        # RIGHT pane
        right = QWidget()
        right_l = QVBoxLayout(right)
        right_l.setContentsMargins(8, 0, 0, 0)
        right_l.setSpacing(6)

        prev_hdr = QHBoxLayout()
        prev_title = QLabel("Preview")
        prev_title.setStyleSheet("font-size:12px;font-weight:bold;")
        prev_hdr.addWidget(prev_title)
        prev_hdr.addStretch()

        copy_btn = QPushButton("Copy to Clipboard")
        copy_btn.setFixedHeight(28)
        copy_btn.clicked.connect(self._copy_to_clipboard)
        prev_hdr.addWidget(copy_btn)
        right_l.addLayout(prev_hdr)

        self._preview = QTextEdit()
        self._preview.setReadOnly(True)
        pf = QFont()
        pf.setFamilies(["Meiryo UI", "Yu Gothic UI", "Segoe UI", "sans-serif"])
        pf.setPixelSize(13)
        self._preview.setFont(pf)
        self._preview.setStyleSheet(
            "QTextEdit{border:1px solid palette(mid);border-radius:6px;padding:8px;}")
        right_l.addWidget(self._preview, 1)

        export_btn = QPushButton("Export to Vault")
        export_btn.setObjectName("secondary")
        export_btn.setFixedHeight(28)
        export_btn.clicked.connect(self._export_to_vault)
        right_l.addWidget(export_btn)

        splitter.addWidget(right)
        splitter.setSizes([440, 360])
        root.addWidget(splitter, 1)

        self._feedback_lbl = QLabel("")
        self._feedback_lbl.setStyleSheet("font-size:11px;")
        root.addWidget(self._feedback_lbl)

    # ── Data ────────────────────────────────────────

    def _refresh(self):
        today = date.today()
        self._date_lbl.setText(_jp_date(today))
        activities = self.store.get_for_date(today.isoformat())

        while self._act_layout.count():
            child = self._act_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self._rows = []

        if activities:
            for act in activities:
                row = _ActivityCheckRow(act, self._palette)
                row.check.stateChanged.connect(self._update_preview)
                self._rows.append(row)
                self._act_layout.addWidget(row)
        else:
            muted = self._palette.get("muted", "#7f849c")
            lbl = QLabel("No activities logged today yet.")
            lbl.setStyleSheet(f"font-size:11px;color:{muted};padding:6px 2px;")
            lbl.setWordWrap(True)
            self._act_layout.addWidget(lbl)

        self._act_layout.addStretch()
        self._update_preview()

    def _update_preview(self):
        selected = [r.row_data() for r in self._rows if r.is_checked()]
        self._preview.setPlainText(_build_report(
            _jp_date(date.today()),
            selected,
            self._renraku_edit.toPlainText(),
            self._ashita_edit.toPlainText(),
            self._ai_content,
        ))

    def _set_all_checked(self, checked: bool):
        for row in self._rows:
            row.check.setChecked(checked)

    # ── AI generation ───────────────────────────────

    def _run_ai(self):
        if self._ai_busy:
            return
        if self._llm_client is None:
            QMessageBox.information(
                self, "API Key Required",
                "No OpenRouter API key configured.\n\n"
                "Click 'AI Settings' to add your key and model ID,\n"
                "or use Network Settings (Ctrl+Shift+N) → AI tab."
            )
            return
        checked = [r for r in self._rows if r.is_checked()]
        if not checked:
            self._flash("No activities selected.", ms=2500)
            return

        self._ai_busy = True
        self._ai_btn.setEnabled(False)
        self._ai_status.setText("Generating Japanese write-up…")

        self._llm_client.complete_async(
            _build_llm_prompt([r.row_data_with_notes() for r in checked]),
            on_result=self._signals.result.emit,
            on_error=self._signals.error.emit,
            max_tokens=800,
            temperature=0.35,
        )

    def _on_ai_result(self, result: LLMResult):
        self._ai_busy = False
        self._ai_btn.setEnabled(True)
        self._ai_content = result.text.strip()
        self._clear_ai_btn.setVisible(True)
        self._ai_status.setText(f"Done — {result.timing_summary()}")
        self._update_preview()

    def _on_ai_error(self, err: str):
        self._ai_busy = False
        self._ai_btn.setEnabled(True)
        self._ai_status.setText(f"Error: {err}")

    def _clear_ai(self):
        self._ai_content = ""
        self._clear_ai_btn.setVisible(False)
        self._ai_status.setText("")
        self._update_preview()

    # ── Settings ────────────────────────────────────

    def _open_settings(self):
        """Open a minimal inline settings dialog for the AI key/model."""
        from PyQt6.QtWidgets import (
            QDialogButtonBox, QLineEdit, QFormLayout, QDialog
        )

        dlg = QDialog(self)
        dlg.setWindowTitle("AI Settings — OpenRouter")
        dlg.setMinimumWidth(460)
        dlg.setModal(True)

        layout = QVBoxLayout(dlg)
        layout.setSpacing(10)
        layout.setContentsMargins(14, 12, 14, 12)

        info = QLabel(
            "Get a free key at openrouter.ai/keys  |  "
            "Find model IDs at openrouter.ai/models  |  "
            "Free-tier models end in :free"
        )
        info.setWordWrap(True)
        info.setStyleSheet("font-size:11px;")
        layout.addWidget(info)

        form = QFormLayout(); form.setSpacing(8)
        cfg = load_config()

        key_edit = QLineEdit()
        key_edit.setPlaceholderText("sk-or-v1-…")
        key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        key_edit.setText(cfg.get("openrouter_api_key", ""))
        form.addRow("API Key:", key_edit)

        model_edit = QLineEdit()
        model_edit.setPlaceholderText("e.g. qwen/qwen3-6b-plus:free")
        model_edit.setText(cfg.get("openrouter_model", DEFAULT_MODEL))
        form.addRow("Model ID:", model_edit)
        layout.addLayout(form)

        # Test row
        test_row = QHBoxLayout()
        test_btn = QPushButton("Test Connection")
        test_btn.setObjectName("secondary")
        test_lbl = QLabel("")
        test_lbl.setWordWrap(True)
        test_row.addWidget(test_btn)
        test_row.addWidget(test_lbl, 1)
        layout.addLayout(test_row)

        # Keep signals alive on the dialog
        dlg._test_signals = LLMSignals()

        def _do_test():
            key   = key_edit.text().strip()
            model = model_edit.text().strip() or DEFAULT_MODEL
            if not key:
                test_lbl.setText("Enter an API key first.")
                return
            test_btn.setEnabled(False)
            test_lbl.setText("Testing…")
            def _ok(r: LLMResult):
                test_lbl.setText(f"Connected — {r.timing_summary()}")
                test_btn.setEnabled(True)
            def _err(e: str):
                test_lbl.setText(f"Error: {e}")
                test_btn.setEnabled(True)
            dlg._test_signals.result.connect(_ok)
            dlg._test_signals.error.connect(_err)
            LLMClient(api_key=key, model=model).complete_async(
                [{"role": "user", "content": "Say hello in one word."}],
                on_result=dlg._test_signals.result.emit,
                on_error=dlg._test_signals.error.emit,
                max_tokens=16,
            )

        test_btn.clicked.connect(_do_test)

        btn_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save |
            QDialogButtonBox.StandardButton.Cancel
        )
        btn_box.accepted.connect(dlg.accept)
        btn_box.rejected.connect(dlg.reject)
        layout.addWidget(btn_box)

        if dlg.exec() == QDialog.DialogCode.Accepted:
            save_llm_config(key_edit.text().strip(),
                            model_edit.text().strip() or DEFAULT_MODEL)
            self.llm_config_changed.emit()

    # ── Drafts ──────────────────────────────────────

    def _load_drafts(self):
        cfg     = load_config()
        drafts  = cfg.get("work_panel_drafts", {})
        day_key = date.today().isoformat()
        saved   = drafts.get(day_key, {})
        self._renraku_edit.setPlainText(saved.get("renraku", ""))
        self._ashita_edit.setPlainText(saved.get("ashita", ""))

    def _save_drafts(self):
        from src.config import load_config, save_config
        cfg     = load_config()
        drafts  = cfg.get("work_panel_drafts", {})
        day_key = date.today().isoformat()
        cutoff  = date.today().toordinal() - 14
        drafts  = {k: v for k, v in drafts.items()
                   if date.fromisoformat(k).toordinal() >= cutoff}
        drafts[day_key] = {
            "renraku": self._renraku_edit.toPlainText(),
            "ashita":  self._ashita_edit.toPlainText(),
        }
        cfg["work_panel_drafts"] = drafts
        save_config(cfg)
        self._flash("Draft saved.")

    # ── Clipboard / export ───────────────────────────

    def _copy_to_clipboard(self):
        text = self._preview.toPlainText()
        if text:
            QApplication.clipboard().setText(text)
            self._flash("Copied to clipboard.")

    def _export_to_vault(self):
        cfg        = load_config()
        vault_path = cfg.get("obsidian_vault_path", "")
        if not vault_path or not Path(vault_path).is_dir():
            QMessageBox.warning(self, "No Vault",
                "Set an Obsidian vault path first (Notes → Set Vault).")
            return
        today   = date.today()
        out_dir = (Path(vault_path) / "Daily Reports"
                   / str(today.year)
                   / f"{today.month:02d} - {today.strftime('%B')}")
        out_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{today.isoformat()} 日報.md"
        (out_dir / filename).write_text(
            self._preview.toPlainText(), encoding="utf-8")
        self._flash(
            f"Saved to Daily Reports/{today.year}/{today.month:02d}/…/{filename}",
            ms=4000)

    def _flash(self, msg: str, ms: int = 3000):
        self._feedback_lbl.setText(msg)
        QTimer.singleShot(ms, lambda: self._feedback_lbl.setText(""))