"""Main application window with menu bar, sidebar, theme selector, and sync integration."""

from datetime import datetime

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QKeySequence, QShortcut, QAction
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QStackedWidget, QPushButton, QLabel, QFrame,
    QComboBox, QStatusBar, QMenuBar,
)

from src.config import APP_NAME, APP_VERSION, load_config, save_config
from src.ui.themes.styles import THEMES, PALETTES, get_theme_names
from src.ui.modules.notes_panel import NotesPanel
from src.ui.modules.calendar_panel import CalendarPanel
from src.ui.modules.finance_panel import FinancePanel
from src.ui.modules.todo_panel import TodoPanel
from src.ui.modules.dashboard_panel import DashboardPanel
from src.ui.modules.finance_charts import FinanceChartsPanel


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
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.setMinimumSize(1000, 650)
        self.resize(1200, 750)

        self._build_menu_bar()
        self._build_central()
        self._build_status_bar()

        # Apply theme and default to Notes
        current_theme = self.cfg.get("theme", "Catppuccin Dark")
        if current_theme in ("dark", "light"):
            current_theme = "Catppuccin Dark" if current_theme == "dark" else "Catppuccin Light"
        self._apply_theme(current_theme)
        self._navigate("Dashboard")

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

        # ── Content stack ────────────────────────────
        self.stack = QStackedWidget()
        self.dashboard_panel = DashboardPanel()
        self.notes_panel = NotesPanel()
        self.calendar_panel = CalendarPanel()
        self.finance_panel = FinancePanel()
        self.charts_panel = FinanceChartsPanel()
        self.todo_panel = TodoPanel()

        self.stack.addWidget(self.dashboard_panel)   # 0
        self.stack.addWidget(self.notes_panel)       # 1
        self.stack.addWidget(self.calendar_panel)    # 2
        self.stack.addWidget(self.finance_panel)     # 3
        self.stack.addWidget(self.charts_panel)      # 4
        self.stack.addWidget(self.todo_panel)        # 5

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

    # ── Navigation ─────────────────────────────────────

    def _navigate(self, name: str):
        idx_map = {
            "Dashboard": 0, "Notes": 1, "Calendar": 2,
            "Earnings": 3, "Charts": 4, "Tasks": 5,
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
        dlg.exec()

    def _show_about(self):
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.about(
            self, f"About {APP_NAME}",
            f"<b>{APP_NAME}</b> v{APP_VERSION}<br><br>"
            f"Personal productivity app with LAN mesh sync.<br>"
            f"Notes \u2022 Calendar \u2022 Earnings \u2022 Tasks<br><br>"
            f"Syncs automatically over your home network.",
        )
