"""Main application window with menu bar, sidebar, theme selector, and sync integration.

Changes in this version:
  • Store injection — all stores instantiated once and passed to panels
  • System tray icon — programmatic theme-aware icon, minimize to tray
  • Close-to-tray behaviour controlled by config key 'minimize_to_tray'
"""

from datetime import datetime

from PyQt6.QtCore import Qt, QTimer, QEvent
from PyQt6.QtGui import QKeySequence, QShortcut, QAction, QPainter, QColor, QPixmap
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QStackedWidget, QPushButton, QLabel, QFrame,
    QComboBox, QStatusBar, QMenuBar, QSystemTrayIcon,
    QMenu, QApplication,
)

from src.config import APP_NAME, APP_VERSION, load_config, save_config
from src.ui.themes.styles import THEMES, PALETTES, get_theme_names
from src.ui.modules.notes_panel import NotesPanel
from src.ui.modules.calendar_panel import CalendarPanel
from src.ui.modules.finance_panel import FinancePanel
from src.ui.modules.todo_panel import TodoPanel
from src.ui.modules.dashboard_panel import DashboardPanel
from src.ui.modules.finance_charts import FinanceChartsPanel
from src.ui.modules.activity_panel import ActivityPanel
from src.ui.modules.work_panel import WorkPanel
from src.ui.modules.debug_panel import DebugPanel 

from src.data.todo_store import TodoStore
from src.data.calendar_store import CalendarStore
from src.data.finance_store import FinanceStore
from src.data.activity_store import ActivityStore
from src.data.soft_events_store import SoftEventStore
from src.ui.widgets.matrix_rain import MatrixRainWidget


class SidebarButton(QPushButton):

    def __init__(self, text: str, icon_char: str = "", shortcut_hint: str = ""):
        display = f"{icon_char}  {text}"
        if shortcut_hint:
            display += f"   {shortcut_hint}"
        super().__init__(display)
        self.setCheckable(True)
        self.setFixedHeight(34)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def apply_colors(self, accent: str, accent_fg: str, hover: str):
        self.setStyleSheet(f"""
            QPushButton {{
                text-align: left;
                padding-left: 12px;
                border: none;
                border-radius: 6px;
                font-size: 12px;
            }}
            QPushButton:checked {{
                background-color: {accent};
                color: {accent_fg};
                font-weight: bold;
            }}
            QPushButton:hover:!checked {{
                background-color: {hover};
            }}
        """)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.cfg = load_config()
        self.sync_engine = None  # Set by main.py after construction

        # ── Instantiate all stores once ──
        self.todo_store = TodoStore()
        self.calendar_store = CalendarStore()
        self.finance_store = FinanceStore()
        self.activity_store = ActivityStore()
        self.soft_events_store = SoftEventStore()
        from src.utils.llm import load_llm_client
        self.llm_client = load_llm_client()

        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.setMinimumSize(1000, 650)
        self.resize(1200, 750)

        self._palette: dict = {}
        self._tray = None  # initialized properly in _setup_tray()

        self._build_menu_bar()
        self._build_central()
        self._build_status_bar()

        # ── Matrix rain overlay (hidden until Matrix theme is active) ──
        # Child of the central widget so it fills the content area only.
        # lower() keeps it behind the sidebar and stacked panels.
        self._matrix_rain = MatrixRainWidget(self._central)
        self._matrix_rain.hide()

        # Apply theme and default to Dashboard
        current_theme = self.cfg.get("theme", "Catppuccin Dark")
        if current_theme in ("dark", "light"):
            current_theme = "Catppuccin Dark" if current_theme == "dark" else "Catppuccin Light"
        self._apply_theme(current_theme)
        self._navigate("Dashboard")

        # ── System tray ──
        self._setup_tray()

    # ── Resize — keep rain synced to central widget ────

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        if hasattr(self, "_matrix_rain") and self._matrix_rain.is_running():
            self._matrix_rain.sync_size()

    # ── Menu bar ───────────────────────────────────────

    def _build_menu_bar(self):
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")

        file_menu.addAction(self._action("&Dashboard", "Ctrl+1", lambda: self._navigate("Dashboard")))
        file_menu.addAction(self._action("&Notes", "Ctrl+2", lambda: self._navigate("Notes")))
        file_menu.addAction(self._action("&Calendar", "Ctrl+3", lambda: self._navigate("Calendar")))
        file_menu.addAction(self._action("&Earnings", "Ctrl+4", lambda: self._navigate("Earnings")))
        file_menu.addAction(self._action("&Charts", "Ctrl+5", lambda: self._navigate("Charts")))
        file_menu.addAction(self._action("&Tasks", "Ctrl+6", lambda: self._navigate("Tasks")))
        file_menu.addAction(self._action("&Activity", "Ctrl+7", lambda: self._navigate("Activity")))
        file_menu.addAction(self._action("&Work",     "Ctrl+8", lambda: self._navigate("Work")))
        file_menu.addSeparator()
        file_menu.addAction(self._action("E&xit", "Ctrl+Q", self.close))

        # Sync menu
        sync_menu = menubar.addMenu("&Sync")
        sync_menu.addAction(self._action("Sync &Now", "Ctrl+Shift+S", self._force_sync))
        sync_menu.addAction(self._action("&Network Settings...", "Ctrl+Shift+N", self._open_network_dialog))

        # View menu
        view_menu = menubar.addMenu("&View")
        for theme_name in get_theme_names():
            view_menu.addAction(self._action(
                theme_name, "",
                lambda checked=False, t=theme_name: self._on_theme_changed(t),
            ))

        # Help menu
        help_menu = menubar.addMenu("&Help")
        help_menu.addAction(self._action("&About", "", self._show_about))

    def _action(self, text: str, shortcut: str, callback) -> QAction:
        act = QAction(text, self)
        if shortcut:
            act.setShortcut(QKeySequence(shortcut))
        act.triggered.connect(callback)
        return act

    # ── Central widget ─────────────────────────────────

    def _build_central(self):
        central = QWidget()
        self._central = central          # kept for rain sizing
        central.setAutoFillBackground(False)   # let rain show through gaps
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ── Sidebar ──────────────────────────────────
        self.sidebar = QWidget()
        self.sidebar.setFixedWidth(190)
        self.sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(8, 10, 8, 10)
        sidebar_layout.setSpacing(3)

        app_label = QLabel(APP_NAME)
        app_label.setObjectName("sectionTitle")
        sidebar_layout.addWidget(app_label)

        version_label = QLabel(f"v{APP_VERSION}")
        version_label.setObjectName("subtitle")
        sidebar_layout.addWidget(version_label)

        sidebar_layout.addSpacing(8)
        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine)
        sidebar_layout.addWidget(sep)
        sidebar_layout.addSpacing(8)

        # Nav buttons
        self.nav_buttons: list[SidebarButton] = []
        nav_items = [
            ("Dashboard", "\U0001f4ca", "Ctrl+1"),
            ("Notes", "\U0001f4dd", "Ctrl+2"),
            ("Calendar", "\U0001f4c5", "Ctrl+3"),
            ("Earnings", "\U0001f4b0", "Ctrl+4"),
            ("Charts", "\U0001f4c8", "Ctrl+5"),
            ("Tasks", "\u2611", "Ctrl+6"),
            ("Activity", "\u23f1", "Ctrl+7"),
            ("Work",     "\U0001f4bc", "Ctrl+8"),
            ("Debug",    "\U0001f52c", "Ctrl+0"),
        ]
        for name, icon, shortcut_text in nav_items:
            btn = SidebarButton(name, icon, shortcut_text)
            btn.clicked.connect(lambda checked, n=name: self._navigate(n))
            btn.setToolTip(f"Switch to {name} ({shortcut_text})")
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append(btn)

            sc = QShortcut(QKeySequence(shortcut_text), self)
            sc.activated.connect(lambda n=name: self._navigate(n))

        sidebar_layout.addStretch()

        # Theme selector
        theme_label = QLabel("Theme")
        theme_label.setObjectName("subtitle")
        sidebar_layout.addWidget(theme_label)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(get_theme_names())
        current_theme = self.cfg.get("theme", "Catppuccin Dark")
        if current_theme in ("dark", "light"):
            current_theme = "Catppuccin Dark" if current_theme == "dark" else "Catppuccin Light"
        idx = self.theme_combo.findText(current_theme)
        if idx >= 0:
            self.theme_combo.setCurrentIndex(idx)
        self.theme_combo.currentTextChanged.connect(self._on_theme_changed)
        sidebar_layout.addWidget(self.theme_combo)

        sidebar_layout.addSpacing(8)

        # Network button
        net_btn = QPushButton("Network...")
        net_btn.setObjectName("secondary")
        net_btn.setToolTip("Open network & sync settings")
        net_btn.clicked.connect(self._open_network_dialog)
        sidebar_layout.addWidget(net_btn)

        sidebar_layout.addSpacing(4)

        # Sync status
        self.sync_label = QLabel("Sync: starting...")
        self.sync_label.setObjectName("subtitle")
        sidebar_layout.addWidget(self.sync_label)

        self.peer_count_label = QLabel("Peers: 0")
        self.peer_count_label.setObjectName("subtitle")
        sidebar_layout.addWidget(self.peer_count_label)

        main_layout.addWidget(self.sidebar)

        # ── Content stack (panels receive injected stores) ──
        self.stack = QStackedWidget()
        self.dashboard_panel = DashboardPanel(
            todo_store=self.todo_store,
            calendar_store=self.calendar_store,
            finance_store=self.finance_store,
            soft_events_store=self.soft_events_store,
        )
        self.notes_panel = NotesPanel()
        self.calendar_panel = CalendarPanel(
            calendar_store=self.calendar_store,
            soft_events_store=self.soft_events_store,
        )
        self.finance_panel = FinancePanel()
        self.charts_panel = FinanceChartsPanel()
        self.todo_panel = TodoPanel(todo_store=self.todo_store)
        self.activity_panel = ActivityPanel()
        self.work_panel  = WorkPanel(llm_client=self.llm_client)
        self.debug_panel = DebugPanel()

        self.stack.addWidget(self.dashboard_panel)   # 0
        self.stack.addWidget(self.notes_panel)       # 1
        self.stack.addWidget(self.calendar_panel)    # 2
        self.stack.addWidget(self.finance_panel)     # 3
        self.stack.addWidget(self.charts_panel)      # 4
        self.stack.addWidget(self.todo_panel)        # 5
        self.stack.addWidget(self.activity_panel)    # 6
        self.stack.addWidget(self.work_panel)        # 7
        self.stack.addWidget(self.debug_panel)       # 8
        self.work_panel.llm_config_changed.connect(self._reload_llm_client)        
        main_layout.addWidget(self.stack, 1)

    # ── Status bar ─────────────────────────────────────

    def _build_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.clock_label = QLabel()
        self.status_bar.addPermanentWidget(self.clock_label)
        self._update_clock()

        clock_timer = QTimer(self)
        clock_timer.timeout.connect(self._update_clock)
        clock_timer.start(30_000)

    def _update_clock(self):
        now = datetime.now()
        self.clock_label.setText(now.strftime("%A, %b %d  %H:%M"))

    # ── System tray ────────────────────────────────────

    def _setup_tray(self):
        if not QSystemTrayIcon.isSystemTrayAvailable():
            self._tray = None
            return

        self._tray = QSystemTrayIcon(self)
        self._tray.setToolTip("LocalSync")
        self._update_tray_icon()

        # Context menu
        tray_menu = QMenu()
        show_action = tray_menu.addAction("Show")
        show_action.triggered.connect(self._tray_show)
        tray_menu.addSeparator()
        quit_action = tray_menu.addAction("Quit")
        quit_action.triggered.connect(QApplication.quit)
        self._tray.setContextMenu(tray_menu)

        # Double-click to show
        self._tray.activated.connect(self._on_tray_activated)

    def _update_tray_icon(self):
        """Generate a 32x32 theme-aware tray icon (solid circle)."""
        if not self._tray:
            return
        accent = self._palette.get("accent", "#89b4fa")
        bg = self._palette.get("bg", "#1e1e2e")

        pixmap = QPixmap(32, 32)
        pixmap.fill(QColor(bg))
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(accent))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(4, 4, 24, 24)
        painter.end()

        from PyQt6.QtGui import QIcon
        self._tray.setIcon(QIcon(pixmap))

    def _tray_show(self):
        self.show()
        self.raise_()
        self.activateWindow()

    def _on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self._tray_show()

    # ── Close / minimize to tray ───────────────────────

    def closeEvent(self, event):
        minimize_to_tray = self.cfg.get("minimize_to_tray", True)
        if minimize_to_tray and self._tray:
            event.ignore()
            self.hide()
            self._tray.show()
        else:
            super().closeEvent(event)

    def changeEvent(self, event):
        if (event.type() == QEvent.Type.WindowStateChange
                and self.isMinimized()
                and self.cfg.get("minimize_to_tray", True)
                and self._tray):
            self.hide()
            self._tray.show()
        super().changeEvent(event)

    # ── Navigation ─────────────────────────────────────

    def _navigate(self, name: str):
        idx_map = {
            "Dashboard": 0, "Notes": 1, "Calendar": 2,
            "Earnings": 3, "Charts": 4, "Tasks": 5, "Activity": 6,
            "Work": 7, "Debug": 8,
        }
        idx = idx_map.get(name, 0)
        self.stack.setCurrentIndex(idx)
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == idx)
        self.status_bar.showMessage(f"  {name}", 2000)

    # ── Theming ────────────────────────────────────────

    def _on_theme_changed(self, theme_name: str):
        self.cfg["theme"] = theme_name
        save_config(self.cfg)
        self._apply_theme(theme_name)
        # Keep combo in sync (in case called from menu)
        idx = self.theme_combo.findText(theme_name)
        if idx >= 0:
            self.theme_combo.blockSignals(True)
            self.theme_combo.setCurrentIndex(idx)
            self.theme_combo.blockSignals(False)

    def _apply_theme(self, name: str):
        sheet = THEMES.get(name, THEMES["Catppuccin Dark"])
        palette = PALETTES.get(name, PALETTES["Catppuccin Dark"])
        self._palette = palette
        self.setStyleSheet(sheet)
        self.sidebar.setStyleSheet(
            f"QWidget#sidebar {{ background-color: {palette['header_bg']}; }}"
        )
        for btn in self.nav_buttons:
            btn.apply_colors(palette["accent"], palette["accent_fg"], palette["hover"])
        if hasattr(self.finance_panel, 'set_palette'):
            self.finance_panel.set_palette(palette)
        if hasattr(self.calendar_panel, 'set_palette'):
            self.calendar_panel.set_palette(palette)
        if hasattr(self.todo_panel, 'set_palette'):
            self.todo_panel.set_palette(palette)
        if hasattr(self.dashboard_panel, 'set_palette'):
            self.dashboard_panel.set_palette(palette)
        if hasattr(self.charts_panel, 'set_palette'):
            self.charts_panel.set_palette(palette)
        if hasattr(self.activity_panel, 'set_palette'):
            self.activity_panel.set_palette(palette)
        if hasattr(self.activity_panel, 'set_palette'):
            self.activity_panel.set_palette(palette)
        if hasattr(self.notes_panel, 'set_palette'):
            self.notes_panel.set_palette(palette)
        if hasattr(self.debug_panel, 'set_palette'):
            self.debug_panel.set_palette(palette)

        # Update tray icon with new theme colors

        # Update tray icon with new theme colors
        self._update_tray_icon()

        # Start or stop the Matrix rain background
        if hasattr(self, "_matrix_rain"):
            if name == "Matrix":
                self._matrix_rain.sync_size()
                self._matrix_rain.start()   # start() calls lower() internally
            else:
                self._matrix_rain.stop()

    # ── Sync integration ───────────────────────────────

    def set_sync_engine(self, engine):
        """Called by main.py to wire up the sync engine."""
        self.sync_engine = engine
        engine.status_changed.connect(self.set_sync_status)
        engine.peers_updated.connect(self._on_peers_updated)
        engine.sync_completed.connect(self._on_sync_completed)

    def _on_sync_completed(self):
        """Refresh all panels after incoming data has been merged."""
        if hasattr(self.notes_panel, '_refresh_list'):
            self.notes_panel._refresh_list()
        if hasattr(self.calendar_panel, '_refresh'):
            self.calendar_panel._refresh()
        if hasattr(self.finance_panel, '_refresh'):
            self.finance_panel._refresh()
        if hasattr(self.todo_panel, '_refresh'):
            self.todo_panel._refresh()
        if hasattr(self.dashboard_panel, '_refresh'):
            self.dashboard_panel._refresh()
        if hasattr(self.charts_panel, '_refresh'):
            self.charts_panel._refresh()
        if hasattr(self.activity_panel, '_refresh'):
            self.activity_panel._refresh()
        if hasattr(self.work_panel, '_refresh'):
            self.work_panel._refresh()

    def set_sync_status(self, text: str):
        self.sync_label.setText(f"Sync: {text}")
        if "error" in text.lower():
            self.sync_label.setObjectName("statusWarn")
        else:
            self.sync_label.setObjectName("subtitle")
        self.sync_label.style().unpolish(self.sync_label)
        self.sync_label.style().polish(self.sync_label)

    def _on_peers_updated(self, peers: list):
        online = sum(1 for p in peers if p.get("status") == "online")
        total = len(peers)
        self.peer_count_label.setText(f"Peers: {online}/{total} online")

    def _force_sync(self):
        if self.sync_engine:
            self.sync_engine.force_sync()
            self.status_bar.showMessage("  Force sync triggered", 3000)

    def _open_network_dialog(self):
        from src.ui.widgets.network_dialog import NetworkDialog
        dlg = NetworkDialog(sync_engine=self.sync_engine, parent=self)
        dlg.llm_settings_saved.connect(self._reload_llm_client)
        dlg.exec()
        
    def _reload_llm_client(self):
        """Reload the LLM client from config and push it to all panels that use it."""
        from src.utils.llm import load_llm_client
        self.llm_client = load_llm_client()
        self.work_panel.set_llm_client(self.llm_client)

    def _show_about(self):
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.about(
            self, f"About {APP_NAME}",
            f"<b>{APP_NAME}</b> v{APP_VERSION}<br><br>"
            f"Personal productivity app with LAN mesh sync.<br>"
            f"Notes \u2022 Calendar \u2022 Earnings \u2022 Tasks<br><br>"
            f"Syncs automatically over your home network.",
        )