"""Network settings dialog — configure sync, view peers, manage connections, AI/LLM."""

import socket
import threading

from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QLineEdit, QSpinBox, QCheckBox,
    QFrame, QTableWidget, QTableWidgetItem, QHeaderView,
    QTextEdit, QTabWidget, QWidget, QMessageBox, QFileDialog,
    QFormLayout, QListWidget, QComboBox, QScrollArea,
)

from src.config import load_config, save_config
from src.utils.llm import (
    LLMClient, LLMResult, LLMSignals,
    CouncilSignals, CouncilResult,
    DEFAULT_MODEL, save_llm_config,
    COUNCIL_SYNTHESIS_MODES, DEFAULT_SYNTHESIS_MODE,
    load_council_config, save_council_config,
)


class NetworkDialog(QDialog):
    """Network and sync settings with live peer status, log viewer, and AI config."""

    # Emitted after AI settings are saved so MainWindow can reload the client
    llm_settings_saved = pyqtSignal()

    def __init__(self, sync_engine=None, parent=None):
        super().__init__(parent)
        self.sync_engine = sync_engine
        self.setWindowTitle("Network & Sync Settings")
        self.setMinimumSize(650, 560)
        self.cfg = load_config()
        # Keep test signals alive — must be on self, not a local variable
        self._test_signals: LLMSignals | None = None
        self._council_test_signals: CouncilSignals | None = None
        self._build_ui()
        self._load_values()

        if self.sync_engine:
            self.sync_engine.peers_updated.connect(self._update_peer_table)
            self.sync_engine.sync_log.connect(self._append_log)

        self._refresh_timer = QTimer(self)
        self._refresh_timer.timeout.connect(self._refresh_peers)
        self._refresh_timer.start(5000)
        self._refresh_peers()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        tabs = QTabWidget()

        # ── Tab 0: Network Settings ───────────────────
        settings_tab = QWidget()
        settings_layout = QVBoxLayout(settings_tab)
        settings_layout.setSpacing(12)

        info_label = QLabel("This Device")
        info_label.setObjectName("sectionTitle")
        settings_layout.addWidget(info_label)

        local_ip = self._get_local_ip()
        hostname = socket.gethostname()
        info_grid = QGridLayout()
        info_grid.addWidget(QLabel("Hostname:"), 0, 0)
        info_grid.addWidget(QLabel(f"<b>{hostname}</b>"), 0, 1)
        info_grid.addWidget(QLabel("IP Address:"), 1, 0)
        info_grid.addWidget(QLabel(f"<b>{local_ip}</b>"), 1, 1)
        settings_layout.addLayout(info_grid)

        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine)
        settings_layout.addWidget(sep)

        sync_label = QLabel("Sync Configuration")
        sync_label.setObjectName("sectionTitle")
        settings_layout.addWidget(sync_label)

        form = QGridLayout()
        form.setSpacing(8)

        form.addWidget(QLabel("Sync enabled:"), 0, 0)
        self.sync_enabled_check = QCheckBox()
        form.addWidget(self.sync_enabled_check, 0, 1)

        form.addWidget(QLabel("Subnet prefix:"), 1, 0)
        self.subnet_edit = QLineEdit()
        self.subnet_edit.setPlaceholderText("e.g. 192.168.0")
        self.subnet_edit.setMaximumWidth(200)
        form.addWidget(self.subnet_edit, 1, 1)

        form.addWidget(QLabel("Sync port:"), 2, 0)
        self.port_spin = QSpinBox()
        self.port_spin.setRange(1024, 65535)
        self.port_spin.setMaximumWidth(120)
        form.addWidget(self.port_spin, 2, 1)

        form.addWidget(QLabel("Interval (seconds):"), 3, 0)
        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(30, 3600)
        self.interval_spin.setSingleStep(30)
        self.interval_spin.setMaximumWidth(120)
        form.addWidget(self.interval_spin, 3, 1)

        form.addWidget(QLabel("Scan timeout (ms):"), 4, 0)
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(50, 2000)
        self.timeout_spin.setSingleStep(50)
        self.timeout_spin.setMaximumWidth(120)
        form.addWidget(self.timeout_spin, 4, 1)

        settings_layout.addLayout(form)
        settings_layout.addStretch()

        save_row = QHBoxLayout()
        save_row.addStretch()
        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self._save_settings)
        save_row.addWidget(save_btn)
        settings_layout.addLayout(save_row)

        tabs.addTab(settings_tab, "Settings")

        # ── Tab 1: Obsidian ───────────────────────────
        obs_tab = QWidget()
        obs_layout = QVBoxLayout(obs_tab)
        obs_layout.setSpacing(10)

        obs_title = QLabel("Obsidian Integration")
        obs_title.setObjectName("sectionTitle")
        obs_layout.addWidget(obs_title)

        obs_desc = QLabel(
            "Configure your Obsidian vault path and REST API settings.\n"
            "The vault path is used to sync markdown files between computers.\n"
            "The REST API connects to the Obsidian Local REST API plugin."
        )
        obs_desc.setObjectName("subtitle")
        obs_desc.setWordWrap(True)
        obs_layout.addWidget(obs_desc)

        obs_form = QGridLayout()
        obs_form.setSpacing(8)

        obs_form.addWidget(QLabel("Vault path:"), 0, 0)
        self.vault_path_edit = QLineEdit()
        self.vault_path_edit.setPlaceholderText("/path/to/your/obsidian/vault")
        self.vault_path_edit.setText(self.cfg.get("obsidian_vault_path", ""))
        obs_form.addWidget(self.vault_path_edit, 0, 1)
        browse_btn = QPushButton("Browse")
        browse_btn.setObjectName("secondary")
        browse_btn.clicked.connect(self._browse_vault)
        obs_form.addWidget(browse_btn, 0, 2)

        obs_form.addWidget(QLabel("Sync vault files:"), 1, 0)
        self.vault_sync_check = QCheckBox()
        self.vault_sync_check.setChecked(self.cfg.get("obsidian_sync_enabled", False))
        obs_form.addWidget(self.vault_sync_check, 1, 1)

        sep_obs = QFrame()
        sep_obs.setObjectName("separator")
        sep_obs.setFrameShape(QFrame.Shape.HLine)
        obs_form.addWidget(sep_obs, 2, 0, 1, 3)

        obs_form.addWidget(QLabel("REST API key:"), 3, 0)
        self.api_key_edit = QLineEdit()
        self.api_key_edit.setPlaceholderText("From Obsidian Local REST API plugin")
        self.api_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_edit.setText(self.cfg.get("obsidian_api_key", ""))
        obs_form.addWidget(self.api_key_edit, 3, 1, 1, 2)

        obs_form.addWidget(QLabel("REST API URL:"), 4, 0)
        self.api_url_edit = QLineEdit()
        self.api_url_edit.setText(self.cfg.get("obsidian_api_url", "http://127.0.0.1:27123"))
        obs_form.addWidget(self.api_url_edit, 4, 1, 1, 2)

        obs_layout.addLayout(obs_form)
        obs_layout.addStretch()

        obs_save_row = QHBoxLayout()
        obs_save_row.addStretch()
        obs_save_btn = QPushButton("Save Obsidian Settings")
        obs_save_btn.clicked.connect(self._save_obsidian_settings)
        obs_save_row.addWidget(obs_save_btn)
        obs_layout.addLayout(obs_save_row)

        tabs.addTab(obs_tab, "Obsidian")

        # ── Tab 2: AI / LLM ──────────────────────────
        ai_outer = QWidget()
        ai_scroll = QScrollArea()
        ai_scroll.setWidgetResizable(True)
        ai_scroll.setFrameShape(QFrame.Shape.NoFrame)
        ai_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        ai_tab = QWidget()
        ai_layout = QVBoxLayout(ai_tab)
        ai_layout.setSpacing(12)

        # ── Primary model ──────────────────────────────
        ai_title = QLabel("AI Assistant — OpenRouter")
        ai_title.setObjectName("sectionTitle")
        ai_layout.addWidget(ai_title)

        ai_desc = QLabel(
            "LocalSync uses OpenRouter to access free LLMs for features like the "
            "Work Panel Japanese write-up generator. "
            "Get a free API key at openrouter.ai/keys and paste any model ID from "
            "openrouter.ai/models below. Free-tier models end in :free."
        )
        ai_desc.setObjectName("subtitle")
        ai_desc.setWordWrap(True)
        ai_layout.addWidget(ai_desc)

        ai_form = QFormLayout()
        ai_form.setSpacing(10)

        self.llm_key_edit = QLineEdit()
        self.llm_key_edit.setPlaceholderText("sk-or-v1-…")
        self.llm_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.llm_key_edit.setText(self.cfg.get("openrouter_api_key", ""))
        ai_form.addRow("API Key:", self.llm_key_edit)

        self.llm_model_edit = QLineEdit()
        self.llm_model_edit.setPlaceholderText("e.g. qwen/qwen3-6b-plus:free")
        self.llm_model_edit.setText(
            self.cfg.get("openrouter_model", DEFAULT_MODEL))
        ai_form.addRow("Primary Model ID:", self.llm_model_edit)

        ai_layout.addLayout(ai_form)

        # Test row
        test_row = QHBoxLayout()
        self._ai_test_btn = QPushButton("Test Connection")
        self._ai_test_btn.setObjectName("secondary")
        self._ai_test_btn.clicked.connect(self._test_ai)
        test_row.addWidget(self._ai_test_btn)
        self._ai_test_lbl = QLabel("")
        self._ai_test_lbl.setWordWrap(True)
        test_row.addWidget(self._ai_test_lbl, 1)
        ai_layout.addLayout(test_row)

        # Current model status
        key_set = bool(self.cfg.get("openrouter_api_key", "").strip())
        model   = self.cfg.get("openrouter_model", DEFAULT_MODEL)
        status_lbl = QLabel(
            f"Status: {'API key configured' if key_set else 'No API key set'}  "
            f"|  Model: {model}"
        )
        status_lbl.setObjectName("subtitle")
        status_lbl.setWordWrap(True)
        ai_layout.addWidget(status_lbl)
        self._ai_status_lbl = status_lbl

        ai_layout.addSpacing(4)

        # ── Council section ────────────────────────────
        council_sep = QFrame()
        council_sep.setObjectName("separator")
        council_sep.setFrameShape(QFrame.Shape.HLine)
        ai_layout.addWidget(council_sep)

        council_title = QLabel("LLM Council")
        council_title.setObjectName("sectionTitle")
        ai_layout.addWidget(council_title)

        council_desc = QLabel(
            "Fan out a single prompt to 3–6 models in parallel, then synthesise "
            "their responses into one final answer. Uses the same API key as above. "
            "Configure via the Debug panel (Ctrl+0)."
        )
        council_desc.setObjectName("subtitle")
        council_desc.setWordWrap(True)
        ai_layout.addWidget(council_desc)

        # Enable toggle
        enable_row = QHBoxLayout()
        enable_row.addWidget(QLabel("Enable Council:"))
        self._council_enabled_check = QCheckBox()
        self._council_enabled_check.setChecked(self.cfg.get("council_enabled", False))
        self._council_enabled_check.toggled.connect(self._on_council_toggled)
        enable_row.addWidget(self._council_enabled_check)
        enable_row.addStretch()
        ai_layout.addLayout(enable_row)

        # Council body (hidden when disabled)
        self._council_body = QWidget()
        council_body_layout = QVBoxLayout(self._council_body)
        council_body_layout.setContentsMargins(0, 0, 0, 0)
        council_body_layout.setSpacing(8)

        # Synthesis model + mode
        synth_form = QFormLayout()
        synth_form.setSpacing(8)

        self._synth_model_edit = QLineEdit()
        self._synth_model_edit.setPlaceholderText(
            "Synthesis model (leave blank to use first council model)")
        self._synth_model_edit.setText(
            self.cfg.get("council_synthesis_model", ""))
        synth_form.addRow("Synthesis Model:", self._synth_model_edit)

        self._synth_mode_combo = QComboBox()
        self._synth_mode_combo.addItems(COUNCIL_SYNTHESIS_MODES)
        saved_mode = self.cfg.get("council_synthesis_mode", DEFAULT_SYNTHESIS_MODE)
        idx = self._synth_mode_combo.findText(saved_mode)
        if idx >= 0:
            self._synth_mode_combo.setCurrentIndex(idx)
        synth_form.addRow("Synthesis Mode:", self._synth_mode_combo)

        council_body_layout.addLayout(synth_form)

        # Model list
        models_lbl = QLabel("Council Models (3–6)")
        models_lbl.setObjectName("subtitle")
        council_body_layout.addWidget(models_lbl)

        self._council_model_list = QListWidget()
        self._council_model_list.setMaximumHeight(130)
        self._council_model_list.setToolTip(
            "Double-click a model to edit it")
        self._council_model_list.itemDoubleClicked.connect(self._edit_council_model)
        for m in self.cfg.get("council_models", []):
            self._council_model_list.addItem(m)
        council_body_layout.addWidget(self._council_model_list)

        # Add / Remove row
        list_btn_row = QHBoxLayout()
        add_model_btn = QPushButton("+ Add Model")
        add_model_btn.setObjectName("secondary")
        add_model_btn.clicked.connect(self._add_council_model)
        list_btn_row.addWidget(add_model_btn)

        remove_model_btn = QPushButton("Remove Selected")
        remove_model_btn.setObjectName("secondary")
        remove_model_btn.clicked.connect(self._remove_council_model)
        list_btn_row.addWidget(remove_model_btn)

        list_btn_row.addStretch()

        self._council_count_lbl = QLabel("")
        self._council_count_lbl.setObjectName("subtitle")
        list_btn_row.addWidget(self._council_count_lbl)
        council_body_layout.addLayout(list_btn_row)
        self._update_council_count()

        # Test council button
        council_test_row = QHBoxLayout()
        self._council_test_btn = QPushButton("Test Council")
        self._council_test_btn.setObjectName("secondary")
        self._council_test_btn.clicked.connect(self._test_council)
        council_test_row.addWidget(self._council_test_btn)
        self._council_test_lbl = QLabel("")
        self._council_test_lbl.setWordWrap(True)
        council_test_row.addWidget(self._council_test_lbl, 1)
        council_body_layout.addLayout(council_test_row)

        ai_layout.addWidget(self._council_body)
        self._council_body.setVisible(self._council_enabled_check.isChecked())

        ai_layout.addStretch()

        # Save button
        ai_save_row = QHBoxLayout()
        ai_save_row.addStretch()
        ai_save_btn = QPushButton("Save AI Settings")
        ai_save_btn.clicked.connect(self._save_ai_settings)
        ai_save_row.addWidget(ai_save_btn)
        ai_layout.addLayout(ai_save_row)

        ai_scroll.setWidget(ai_tab)

        ai_outer_layout = QVBoxLayout(ai_outer)
        ai_outer_layout.setContentsMargins(0, 0, 0, 0)
        ai_outer_layout.addWidget(ai_scroll)

        tabs.addTab(ai_outer, "AI")

        # ── Tab 3: Peers ──────────────────────────────
        peers_tab = QWidget()
        peers_layout = QVBoxLayout(peers_tab)

        peers_header = QHBoxLayout()
        peers_title = QLabel("Discovered Peers")
        peers_title.setObjectName("sectionTitle")
        peers_header.addWidget(peers_title)
        peers_header.addStretch()

        scan_btn = QPushButton("Scan Now")
        scan_btn.setToolTip("Force a subnet scan")
        scan_btn.clicked.connect(self._force_scan)
        peers_header.addWidget(scan_btn)

        sync_btn = QPushButton("Sync Now")
        sync_btn.setToolTip("Force an immediate sync with all peers")
        sync_btn.clicked.connect(self._force_sync)
        peers_header.addWidget(sync_btn)

        peers_layout.addLayout(peers_header)

        self.peer_table = QTableWidget()
        self.peer_table.setColumnCount(4)
        self.peer_table.setHorizontalHeaderLabels(["IP Address", "Hostname", "Status", "Failures"])
        self.peer_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.peer_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.peer_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        peers_layout.addWidget(self.peer_table)

        add_row = QHBoxLayout()
        add_row.addWidget(QLabel("Add peer:"))
        self.manual_ip_edit = QLineEdit()
        self.manual_ip_edit.setPlaceholderText("e.g. 192.168.0.28")
        self.manual_ip_edit.setMaximumWidth(200)
        self.manual_ip_edit.returnPressed.connect(self._add_manual_peer)
        add_row.addWidget(self.manual_ip_edit)

        add_btn = QPushButton("Add")
        add_btn.setObjectName("secondary")
        add_btn.clicked.connect(self._add_manual_peer)
        add_row.addWidget(add_btn)

        ping_btn = QPushButton("Ping")
        ping_btn.setObjectName("secondary")
        ping_btn.clicked.connect(self._ping_selected)
        add_row.addWidget(ping_btn)

        add_row.addStretch()
        peers_layout.addLayout(add_row)

        tabs.addTab(peers_tab, "Peers")

        # ── Tab 4: Log ────────────────────────────────
        log_tab = QWidget()
        log_layout = QVBoxLayout(log_tab)

        log_header = QHBoxLayout()
        log_title = QLabel("Sync Log")
        log_title.setObjectName("sectionTitle")
        log_header.addWidget(log_title)
        log_header.addStretch()
        clear_btn = QPushButton("Clear")
        clear_btn.setObjectName("secondary")
        clear_btn.clicked.connect(lambda: self.log_view.clear())
        log_header.addWidget(clear_btn)
        log_layout.addLayout(log_header)

        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setStyleSheet("font-family: monospace; font-size: 12px;")
        log_layout.addWidget(self.log_view)

        tabs.addTab(log_tab, "Log")

        layout.addWidget(tabs)

    # ── Load / save ──────────────────────────────────

    def _load_values(self):
        self.sync_enabled_check.setChecked(self.cfg.get("sync_enabled", True))
        self.subnet_edit.setText(self.cfg.get("subnet", "192.168.0"))
        self.port_spin.setValue(self.cfg.get("sync_port", 42069))
        self.interval_spin.setValue(self.cfg.get("sync_interval_seconds", 300))
        self.timeout_spin.setValue(self.cfg.get("scan_timeout_ms", 150))

    def _save_settings(self):
        self.cfg["sync_enabled"] = self.sync_enabled_check.isChecked()
        self.cfg["subnet"] = self.subnet_edit.text().strip()
        self.cfg["sync_port"] = self.port_spin.value()
        self.cfg["sync_interval_seconds"] = self.interval_spin.value()
        self.cfg["scan_timeout_ms"] = self.timeout_spin.value()
        save_config(self.cfg)
        if self.sync_engine:
            self.sync_engine.reload_config()
        QMessageBox.information(self, "Saved", "Network settings saved.")

    def _save_ai_settings(self):
        key   = self.llm_key_edit.text().strip()
        model = self.llm_model_edit.text().strip() or DEFAULT_MODEL
        save_llm_config(key, model)
        self._ai_status_lbl.setText(
            f"Status: {'API key configured' if key else 'No API key set'}"
            f"  |  Model: {model}"
        )

        # Save council settings
        models = [
            self._council_model_list.item(i).text().strip()
            for i in range(self._council_model_list.count())
        ]
        save_council_config(
            enabled         = self._council_enabled_check.isChecked(),
            models          = models,
            synthesis_model = self._synth_model_edit.text().strip(),
            synthesis_mode  = self._synth_mode_combo.currentText(),
        )

        self.llm_settings_saved.emit()
        QMessageBox.information(self, "Saved",
            "AI settings saved.\nThe LLM client has been updated.")

    # ── AI test ─────────────────────────────────────

    def _test_ai(self):
        key   = self.llm_key_edit.text().strip()
        model = self.llm_model_edit.text().strip() or DEFAULT_MODEL
        if not key:
            self._ai_test_lbl.setText("Enter an API key first.")
            return
        self._ai_test_btn.setEnabled(False)
        self._ai_test_lbl.setText("Testing…")

        # Must be stored on self — local var would be GC'd before thread fires
        self._test_signals = LLMSignals()

        def _on_ok(result: LLMResult):
            self._ai_test_lbl.setText(f"Connected — {result.timing_summary()}")
            self._ai_test_btn.setEnabled(True)

        def _on_err(err: str):
            self._ai_test_lbl.setText(f"Error: {err}")
            self._ai_test_btn.setEnabled(True)

        self._test_signals.result.connect(_on_ok)
        self._test_signals.error.connect(_on_err)

        LLMClient(api_key=key, model=model).complete_async(
            [{"role": "user", "content": "Say hello in one word."}],
            on_result=self._test_signals.result.emit,
            on_error=self._test_signals.error.emit,
            max_tokens=16,
        )

    # ── Council helpers ──────────────────────────────

    def _on_council_toggled(self, enabled: bool):
        self._council_body.setVisible(enabled)

    def _update_council_count(self):
        n = self._council_model_list.count()
        color = "green" if 3 <= n <= 6 else "red"
        self._council_count_lbl.setText(
            f"<span style='color:{color}'>{n} model{'s' if n != 1 else ''}</span>"
        )

    def _add_council_model(self):
        if self._council_model_list.count() >= 6:
            QMessageBox.warning(self, "Council Full",
                "A council can have at most 6 models.")
            return
        from PyQt6.QtWidgets import QInputDialog
        text, ok = QInputDialog.getText(
            self, "Add Council Model",
            "Model ID (e.g. mistralai/mistral-7b-instruct:free):"
        )
        if ok and text.strip():
            self._council_model_list.addItem(text.strip())
            self._update_council_count()

    def _remove_council_model(self):
        row = self._council_model_list.currentRow()
        if row >= 0:
            self._council_model_list.takeItem(row)
            self._update_council_count()

    def _edit_council_model(self, item):
        from PyQt6.QtWidgets import QInputDialog
        text, ok = QInputDialog.getText(
            self, "Edit Council Model", "Model ID:", text=item.text()
        )
        if ok and text.strip():
            item.setText(text.strip())

    def _test_council(self):
        key = self.llm_key_edit.text().strip()
        if not key:
            self._council_test_lbl.setText("Enter an API key first.")
            return
        models = [
            self._council_model_list.item(i).text().strip()
            for i in range(self._council_model_list.count())
        ]
        if len(models) < 1:
            self._council_test_lbl.setText("Add at least one model first.")
            return

        self._council_test_btn.setEnabled(False)
        self._council_test_lbl.setText(f"Testing {len(models)} model(s)…")

        from src.utils.llm import LLMCouncil
        council = LLMCouncil(
            api_key         = key,
            council_models  = models,
            synthesis_model = self._synth_model_edit.text().strip(),
            synthesis_mode  = self._synth_mode_combo.currentText(),
        )

        self._council_test_signals = CouncilSignals()

        def _on_ok(result: CouncilResult):
            ok_count  = result.member_count
            fail_count = len(result.failed_models)
            parts = [f"{ok_count} responded"]
            if fail_count:
                parts.append(f"{fail_count} failed")
            parts.append(result.final.timing_summary())
            self._council_test_lbl.setText("Council OK — " + " · ".join(parts))
            self._council_test_btn.setEnabled(True)

        def _on_err(err: str):
            self._council_test_lbl.setText(f"Error: {err}")
            self._council_test_btn.setEnabled(True)

        self._council_test_signals.result.connect(_on_ok)
        self._council_test_signals.error.connect(_on_err)

        council.complete_async(
            [{"role": "user", "content": "Say hello in one word."}],
            on_result=self._council_test_signals.result.emit,
            on_error=self._council_test_signals.error.emit,
            max_tokens=16,
        )

    # ── Peer management ──────────────────────────────

    def _refresh_peers(self):
        if self.sync_engine:
            peers = self.sync_engine.get_peer_list()
            self._update_peer_table(peers)

    def _update_peer_table(self, peers: list):
        self.peer_table.setRowCount(len(peers))
        for row, p in enumerate(peers):
            self.peer_table.setItem(row, 0, QTableWidgetItem(p["ip"]))
            self.peer_table.setItem(row, 1, QTableWidgetItem(p.get("hostname", "")))
            status = p.get("status", "unknown")
            status_item = QTableWidgetItem(status)
            if status == "online":
                status_item.setForeground(Qt.GlobalColor.green)
            elif status == "stale":
                status_item.setForeground(Qt.GlobalColor.darkYellow)
            else:
                status_item.setForeground(Qt.GlobalColor.red)
            self.peer_table.setItem(row, 2, status_item)
            self.peer_table.setItem(row, 3, QTableWidgetItem(str(p.get("fail_count", 0))))

    def _add_manual_peer(self):
        ip = self.manual_ip_edit.text().strip()
        if ip and self.sync_engine:
            self.sync_engine.add_manual_peer(ip)
            known = self.cfg.get("known_peers", [])
            if ip not in known:
                known.append(ip)
                self.cfg["known_peers"] = known
                save_config(self.cfg)
            self.manual_ip_edit.clear()
            self._refresh_peers()

    def _ping_selected(self):
        rows = self.peer_table.selectionModel().selectedRows()
        if rows and self.sync_engine:
            ip_item = self.peer_table.item(rows[0].row(), 0)
            if ip_item:
                ip = ip_item.text()
                self._append_log(f"Pinging {ip}...")
                def do_ping():
                    ok, info = self.sync_engine.ping_peer(ip)
                    self._append_log(
                        f"Ping {ip}: OK ({info})" if ok
                        else f"Ping {ip}: FAILED ({info})")
                threading.Thread(target=do_ping, daemon=True).start()
        elif not rows:
            ip = self.manual_ip_edit.text().strip()
            if ip and self.sync_engine:
                self._append_log(f"Pinging {ip}...")
                def do_ping():
                    ok, info = self.sync_engine.ping_peer(ip)
                    self._append_log(
                        f"Ping {ip}: OK ({info})" if ok
                        else f"Ping {ip}: FAILED ({info})")
                threading.Thread(target=do_ping, daemon=True).start()

    def _force_scan(self):
        if self.sync_engine:
            self._append_log("Forcing subnet scan...")
            self.sync_engine.force_scan()

    def _force_sync(self):
        if self.sync_engine:
            self._append_log("Forcing immediate sync...")
            self.sync_engine.force_sync()

    def _browse_vault(self):
        path = QFileDialog.getExistingDirectory(
            self, "Select Obsidian Vault", self.vault_path_edit.text())
        if path:
            self.vault_path_edit.setText(path)

    def _save_obsidian_settings(self):
        self.cfg["obsidian_vault_path"]   = self.vault_path_edit.text().strip()
        self.cfg["obsidian_sync_enabled"] = self.vault_sync_check.isChecked()
        self.cfg["obsidian_api_key"]      = self.api_key_edit.text().strip()
        self.cfg["obsidian_api_url"]      = (
            self.api_url_edit.text().strip() or "http://127.0.0.1:27123")
        save_config(self.cfg)
        QMessageBox.information(self, "Saved",
            "Obsidian settings saved.\nRestart the app for vault changes to take effect.")

    def _append_log(self, msg: str):
        self.log_view.append(msg)
        self.log_view.verticalScrollBar().setValue(
            self.log_view.verticalScrollBar().maximum())

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