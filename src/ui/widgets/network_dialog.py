"""Network settings dialog — configure sync, view peers, manage connections, AI/LLM.

Tabs
────
  ⚙  Settings  : Sync subnet/port/interval/timeout, peer table, force scan/sync, log
  📓  Obsidian  : Vault path, sync toggle, REST API key/URL
  🤖  AI / LLM  : llama.cpp server host, connection test, multi-pass council toggle
"""

import socket
import threading

from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import (
    QAbstractItemView, QCheckBox, QDialog, QFileDialog, QFormLayout,
    QFrame, QGridLayout, QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QMessageBox, QPushButton, QScrollArea, QSpinBox, QTableWidget, QComboBox,
    QTableWidgetItem, QTabWidget, QTextEdit, QVBoxLayout, QWidget,
)

from src.config import load_config, save_config
from src.utils.llm import (
    LLAMA_DEFAULT_HOST,
    CouncilResult,
    CouncilSignals,
    LLMClient,
    LLMResult,
    LLMSignals,
    LightCouncil,
)


class NetworkDialog(QDialog):
    """Network and sync settings with live peer status, log viewer, and AI config."""

    # Emitted after AI settings are saved so MainWindow can reload the client
    llm_settings_saved = pyqtSignal()

    def __init__(self, parent=None, sync_engine=None):
        super().__init__(parent)
        self.cfg         = load_config()
        self.sync_engine = sync_engine
        self.setWindowTitle("Network & AI Settings")
        self.setMinimumSize(660, 580)
        self.resize(740, 640)
        self._build_ui()
        self._load_values()
        if self.sync_engine:
            self._refresh_peers()

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  UI construction
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        tabs = QTabWidget()
        root.addWidget(tabs, 1)

        tabs.addTab(self._build_settings_tab(), "⚙  Settings")
        tabs.addTab(self._build_obsidian_tab(), "📓  Obsidian")
        tabs.addTab(self._build_ai_tab(),       "🤖  AI / LLM")

        # Close button
        btn_row = QHBoxLayout()
        btn_row.setContentsMargins(12, 8, 12, 12)
        btn_row.addStretch()
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        btn_row.addWidget(close_btn)
        root.addLayout(btn_row)

    # ── Tab: Settings ─────────────────────────────────

    def _build_settings_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        sync_title = QLabel("Sync Settings")
        sync_title.setObjectName("sectionTitle")
        layout.addWidget(sync_title)

        local_ip = self._get_local_ip()
        ip_lbl = QLabel(f"Local IP: {local_ip}")
        ip_lbl.setObjectName("subtitle")
        layout.addWidget(ip_lbl)

        form = QGridLayout()
        form.setSpacing(8)
        form.setColumnStretch(1, 1)

        form.addWidget(QLabel("Subnet:"), 0, 0)
        self.subnet_edit = QLineEdit()
        self.subnet_edit.setPlaceholderText("192.168.0")
        self.subnet_edit.setMaximumWidth(200)
        form.addWidget(self.subnet_edit, 0, 1)

        form.addWidget(QLabel("Sync port:"), 1, 0)
        self.port_spin = QSpinBox()
        self.port_spin.setRange(1024, 65535)
        self.port_spin.setMaximumWidth(120)
        form.addWidget(self.port_spin, 1, 1)

        form.addWidget(QLabel("Interval (seconds):"), 2, 0)
        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(30, 3600)
        self.interval_spin.setSingleStep(30)
        self.interval_spin.setMaximumWidth(120)
        form.addWidget(self.interval_spin, 2, 1)

        form.addWidget(QLabel("Scan timeout (ms):"), 3, 0)
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(50, 2000)
        self.timeout_spin.setSingleStep(50)
        self.timeout_spin.setMaximumWidth(120)
        form.addWidget(self.timeout_spin, 3, 1)

        layout.addLayout(form)

        save_row = QHBoxLayout()
        save_row.addStretch()
        save_btn = QPushButton("Save Sync Settings")
        save_btn.clicked.connect(self._save_settings)
        save_row.addWidget(save_btn)
        layout.addLayout(save_row)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setObjectName("separator")
        layout.addWidget(sep)

        peers_title = QLabel("Peers")
        peers_title.setObjectName("sectionTitle")
        layout.addWidget(peers_title)

        peer_btns = QHBoxLayout()
        for label, slot in [
            ("Refresh",      self._refresh_peers),
            ("Add Peer…",    self._add_manual_peer),
            ("Ping Selected",self._ping_selected),
            ("Force Scan",   self._force_scan),
            ("Force Sync",   self._force_sync),
        ]:
            btn = QPushButton(label)
            btn.setObjectName("secondary")
            btn.clicked.connect(slot)
            peer_btns.addWidget(btn)
        peer_btns.addStretch()
        layout.addLayout(peer_btns)

        self._peer_table = QTableWidget(0, 4)
        self._peer_table.setHorizontalHeaderLabels(["IP", "Hostname", "Status", "Fails"])
        hh = self._peer_table.horizontalHeader()
        hh.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        hh.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        hh.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self._peer_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self._peer_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self._peer_table.setFixedHeight(120)
        layout.addWidget(self._peer_table)

        log_lbl = QLabel("Sync Log")
        log_lbl.setObjectName("subtitle")
        layout.addWidget(log_lbl)

        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setMaximumHeight(110)
        layout.addWidget(self.log_view)

        layout.addStretch()
        return tab

    # ── Tab: Obsidian ─────────────────────────────────

    def _build_obsidian_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        title = QLabel("Obsidian Integration")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        desc = QLabel(
            "Configure your Obsidian vault path and REST API settings.\n"
            "The vault path is used to sync markdown files between computers.\n"
            "The REST API connects to the Obsidian Local REST API plugin."
        )
        desc.setObjectName("subtitle")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        obs_form = QFormLayout()
        obs_form.setSpacing(8)

        vault_row = QHBoxLayout()
        self.vault_path_edit = QLineEdit()
        self.vault_path_edit.setPlaceholderText("/path/to/your/vault")
        vault_row.addWidget(self.vault_path_edit)
        browse_btn = QPushButton("Browse…")
        browse_btn.setObjectName("secondary")
        browse_btn.setFixedWidth(90)
        browse_btn.clicked.connect(self._browse_vault)
        vault_row.addWidget(browse_btn)
        obs_form.addRow("Vault Path:", vault_row)

        self.vault_sync_check = QCheckBox("Enable vault file sync")
        obs_form.addRow("", self.vault_sync_check)

        self.api_key_edit = QLineEdit()
        self.api_key_edit.setPlaceholderText("Obsidian REST API key (optional)")
        self.api_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        obs_form.addRow("REST API Key:", self.api_key_edit)

        self.api_url_edit = QLineEdit()
        self.api_url_edit.setPlaceholderText("http://127.0.0.1:27123")
        obs_form.addRow("REST API URL:", self.api_url_edit)

        layout.addLayout(obs_form)
        layout.addStretch()

        save_row = QHBoxLayout()
        save_row.addStretch()
        save_btn = QPushButton("Save Obsidian Settings")
        save_btn.clicked.connect(self._save_obsidian_settings)
        save_row.addWidget(save_btn)
        layout.addLayout(save_row)

        return tab

    # ── Tab: AI / LLM ────────────────────────────────

    def _build_ai_tab(self) -> QWidget:
        # Wrap in a scroll area so it survives small windows
        outer = QWidget()
        outer_layout = QVBoxLayout(outer)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        outer_layout.addWidget(scroll)

        inner = QWidget()
        layout = QVBoxLayout(inner)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(14)

        # ── Server connection ──────────────────────────
        title = QLabel("llama.cpp Server")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        desc = QLabel(
            "LocalSync connects to your llama.cpp server for all AI features. "
            "The model is selected server-side — no model name is needed here."
        )
        desc.setObjectName("subtitle")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        conn_form = QFormLayout()
        conn_form.setSpacing(10)
        self.llama_host_edit = QLineEdit()
        self.llama_host_edit.setPlaceholderText(LLAMA_DEFAULT_HOST)
        conn_form.addRow("Server Host:", self.llama_host_edit)
        layout.addLayout(conn_form)

        test_row = QHBoxLayout()
        self._ai_test_btn = QPushButton("Test Connection")
        self._ai_test_btn.setObjectName("secondary")
        self._ai_test_btn.clicked.connect(self._test_ai)
        test_row.addWidget(self._ai_test_btn)
        self._ai_test_lbl = QLabel("")
        self._ai_test_lbl.setWordWrap(True)
        test_row.addWidget(self._ai_test_lbl, 1)
        layout.addLayout(test_row)

        # ── Multi-pass council ─────────────────────────
        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(sep)

        council_title = QLabel("Multi-Pass Council")
        council_title.setObjectName("sectionTitle")
        layout.addWidget(council_title)

        council_desc = QLabel(
            "When enabled, AI responses are generated in three parallel passes at "
            "different temperature settings — Precise (0.2), Balanced (0.6), and "
            "Creative (1.0) — then synthesised into a single answer. "
            "Produces richer results but uses more tokens and takes longer."
        )
        council_desc.setObjectName("subtitle")
        council_desc.setWordWrap(True)
        layout.addWidget(council_desc)

        self._council_check = QCheckBox("Enable multi-pass council")
        layout.addWidget(self._council_check)

        # Mode selector — Deliberate (default) runs the synthesis pass after
        # the 3 parallel passes; Quick skips it and returns the longest
        # non-empty pass directly.  Roughly halves wall-clock time.
        from src.utils.llm import COUNCIL_SYNTHESIS_MODES
        mode_row = QHBoxLayout()
        mode_row.setContentsMargins(20, 0, 0, 0)
        mode_lbl = QLabel("Mode:")
        mode_row.addWidget(mode_lbl)
        self._council_mode_combo = QComboBox()
        for m in COUNCIL_SYNTHESIS_MODES:
            self._council_mode_combo.addItem(m)
        mode_row.addWidget(self._council_mode_combo)
        mode_hint = QLabel(
            "Deliberate = synthesis pass · Quick = longest non-empty pass wins (faster)"
        )
        mode_hint.setObjectName("subtitle")
        mode_hint.setWordWrap(True)
        mode_row.addWidget(mode_hint, 1)
        layout.addLayout(mode_row)

        council_test_row = QHBoxLayout()
        self._council_test_btn = QPushButton("Test Council")
        self._council_test_btn.setObjectName("secondary")
        self._council_test_btn.clicked.connect(self._test_council)
        council_test_row.addWidget(self._council_test_btn)
        self._council_test_lbl = QLabel("")
        self._council_test_lbl.setWordWrap(True)
        council_test_row.addWidget(self._council_test_lbl, 1)
        layout.addLayout(council_test_row)

        layout.addStretch()

        save_row = QHBoxLayout()
        save_row.addStretch()
        save_btn = QPushButton("Save AI Settings")
        save_btn.clicked.connect(self._save_ai_settings)
        save_row.addWidget(save_btn)
        layout.addLayout(save_row)

        scroll.setWidget(inner)
        return outer

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  Load / Save
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def _load_values(self):
        # Sync
        self.subnet_edit.setText(self.cfg.get("sync_subnet", "192.168.0"))
        self.port_spin.setValue(self.cfg.get("sync_port", 47678))
        self.interval_spin.setValue(self.cfg.get("sync_interval", 60))
        self.timeout_spin.setValue(self.cfg.get("scan_timeout_ms", 300))
        # Obsidian
        self.vault_path_edit.setText(self.cfg.get("obsidian_vault_path", ""))
        self.vault_sync_check.setChecked(self.cfg.get("obsidian_sync_enabled", False))
        self.api_key_edit.setText(self.cfg.get("obsidian_api_key", ""))
        self.api_url_edit.setText(
            self.cfg.get("obsidian_api_url", "http://127.0.0.1:27123"))
        # AI
        self.llama_host_edit.setText(
            self.cfg.get("llama_host", LLAMA_DEFAULT_HOST))
        self._council_check.setChecked(self.cfg.get("council_enabled", False))
        from src.utils.llm import COUNCIL_DEFAULT_MODE, COUNCIL_SYNTHESIS_MODES
        saved_mode = self.cfg.get("council_mode", COUNCIL_DEFAULT_MODE)
        if saved_mode not in COUNCIL_SYNTHESIS_MODES:
            saved_mode = COUNCIL_DEFAULT_MODE
        self._council_mode_combo.setCurrentText(saved_mode)

    def _save_settings(self):
        self.cfg["sync_subnet"]     = self.subnet_edit.text().strip() or "192.168.0"
        self.cfg["sync_port"]       = self.port_spin.value()
        self.cfg["sync_interval"]   = self.interval_spin.value()
        self.cfg["scan_timeout_ms"] = self.timeout_spin.value()
        save_config(self.cfg)
        if self.sync_engine:
            self.sync_engine.reload_config()
        QMessageBox.information(self, "Saved", "Sync settings saved.")

    def _save_ai_settings(self):
        self.cfg["llama_host"]      = self.llama_host_edit.text().strip() or LLAMA_DEFAULT_HOST
        self.cfg["council_enabled"] = self._council_check.isChecked()
        self.cfg["council_mode"]    = self._council_mode_combo.currentText()
        save_config(self.cfg)
        self.llm_settings_saved.emit()
        QMessageBox.information(self, "Saved", "AI settings saved.")

    def _save_obsidian_settings(self):
        self.cfg["obsidian_vault_path"]   = self.vault_path_edit.text().strip()
        self.cfg["obsidian_sync_enabled"] = self.vault_sync_check.isChecked()
        self.cfg["obsidian_api_key"]      = self.api_key_edit.text().strip()
        self.cfg["obsidian_api_url"]      = (
            self.api_url_edit.text().strip() or "http://127.0.0.1:27123")
        save_config(self.cfg)
        QMessageBox.information(
            self, "Saved",
            "Obsidian settings saved.\n"
            "Restart the app for vault path changes to take effect.")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  AI tests
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def _test_ai(self):
        host = self.llama_host_edit.text().strip() or LLAMA_DEFAULT_HOST
        self._ai_test_btn.setEnabled(False)
        self._ai_test_lbl.setText("Testing…")
        # Stored on self to prevent GC before thread fires
        self._ai_test_signals = LLMSignals()

        def _on_ok(result: LLMResult):
            self._ai_test_lbl.setText(f"✓ Connected — {result.elapsed_ms} ms")
            self._ai_test_btn.setEnabled(True)

        def _on_err(err: str):
            self._ai_test_lbl.setText(f"✗ {err}")
            self._ai_test_btn.setEnabled(True)

        self._ai_test_signals.result.connect(_on_ok)
        self._ai_test_signals.error.connect(_on_err)

        LLMClient(host=host).complete_async(
            [{"role": "user", "content": "Reply with only the word OK."}],
            max_tokens = 8,
            on_result  = self._ai_test_signals.result.emit,
            on_error   = self._ai_test_signals.error.emit,
        )

    def _test_council(self):
        host = self.llama_host_edit.text().strip() or LLAMA_DEFAULT_HOST
        self._council_test_btn.setEnabled(False)
        self._council_test_lbl.setText("Running 3 passes… (may take a moment)")
        # Stored on self to prevent GC before thread fires
        self._council_test_signals = CouncilSignals()

        def _on_ok(result: CouncilResult):
            self._council_test_lbl.setText(f"✓ Council OK — {result.summary()}")
            self._council_test_btn.setEnabled(True)

        def _on_err(err: str):
            self._council_test_lbl.setText(f"✗ {err}")
            self._council_test_btn.setEnabled(True)

        self._council_test_signals.result.connect(_on_ok)
        self._council_test_signals.error.connect(_on_err)

        LightCouncil(host=host).complete_async(
            [{"role": "user", "content": "In one sentence, what is 2 + 2?"}],
            max_tokens = 64,
            on_result  = self._council_test_signals.result.emit,
            on_error   = self._council_test_signals.error.emit,
        )

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  Peers
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def _refresh_peers(self):
        if not self.sync_engine:
            return
        peers = self.sync_engine.get_peer_list()
        self._update_peer_table(peers)

    def _update_peer_table(self, peers: list[dict]):
        self._peer_table.setRowCount(len(peers))
        for row, peer in enumerate(peers):
            self._peer_table.setItem(row, 0, QTableWidgetItem(peer.get("ip", "")))
            self._peer_table.setItem(row, 1, QTableWidgetItem(peer.get("hostname", "")))
            self._peer_table.setItem(row, 2, QTableWidgetItem(peer.get("status", "")))
            self._peer_table.setItem(row, 3, QTableWidgetItem(str(peer.get("fail_count", 0))))

    def _add_manual_peer(self):
        text, ok = _input_dialog(self, "Add Peer", "Enter peer IP address:")
        if ok and text.strip() and self.sync_engine:
            self.sync_engine.add_manual_peer(text.strip())
            self._append_log(f"Added manual peer: {text.strip()}")
            QTimer.singleShot(500, self._refresh_peers)

    def _ping_selected(self):
        rows = self._peer_table.selectedItems()
        if not rows:
            return
        row      = rows[0].row()
        ip_item  = self._peer_table.item(row, 0)
        if not ip_item or not self.sync_engine:
            return
        ip = ip_item.text()

        def do_ping():
            ok, info = self.sync_engine.ping_peer(ip)
            self._append_log(
                f"Ping {ip}: OK ({info})" if ok else f"Ping {ip}: FAILED ({info})")
        threading.Thread(target=do_ping, daemon=True).start()

    def _force_scan(self):
        if self.sync_engine:
            self._append_log("Forcing subnet scan…")
            self.sync_engine.force_scan()

    def _force_sync(self):
        if self.sync_engine:
            self._append_log("Forcing immediate sync…")
            self.sync_engine.force_sync()

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  Obsidian helpers
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def _browse_vault(self):
        path = QFileDialog.getExistingDirectory(
            self, "Select Obsidian Vault", self.vault_path_edit.text())
        if path:
            self.vault_path_edit.setText(path)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  Utilities
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def _append_log(self, msg: str):
        self.log_view.append(msg)
        sb = self.log_view.verticalScrollBar()
        sb.setValue(sb.maximum())

    @staticmethod
    def _get_local_ip() -> str:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("192.168.0.1", 1))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "unknown"


# ── Minimal input dialog helper ───────────────────────────────────────────────

def _input_dialog(parent, title: str, label: str, default: str = "") -> tuple[str, bool]:
    dlg = QDialog(parent)
    dlg.setWindowTitle(title)
    dlg.setMinimumWidth(360)
    layout = QVBoxLayout(dlg)
    layout.addWidget(QLabel(label))
    edit = QLineEdit(default)
    layout.addWidget(edit)
    btn_row = QHBoxLayout()
    ok_btn     = QPushButton("OK")
    cancel_btn = QPushButton("Cancel")
    cancel_btn.setObjectName("secondary")
    ok_btn.clicked.connect(dlg.accept)
    cancel_btn.clicked.connect(dlg.reject)
    btn_row.addStretch()
    btn_row.addWidget(cancel_btn)
    btn_row.addWidget(ok_btn)
    layout.addLayout(btn_row)
    accepted = dlg.exec() == QDialog.DialogCode.Accepted
    return edit.text(), accepted