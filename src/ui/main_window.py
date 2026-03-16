"""Main application window with sidebar navigation, theme selector, and status bar."""

from datetime import datetime

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QStackedWidget, QPushButton, QLabel, QFrame,
    QComboBox, QStatusBar,
)

from src.config import APP_NAME, APP_VERSION, load_config, save_config
from src.ui.themes.styles import THEMES, PALETTES, get_theme_names
from src.ui.modules.notes_panel import NotesPanel
from src.ui.modules.calendar_panel import CalendarPanel
from src.ui.modules.finance_panel import FinancePanel


class SidebarButton(QPushButton):
    """A sidebar navigation button with theme-aware active styling."""

    def __init__(self, text: str, icon_char: str = "", shortcut_hint: str = ""):
        display = f"{icon_char}  {text}"
        if shortcut_hint:
            display += f"   {shortcut_hint}"
        super().__init__(display)
        self.setCheckable(True)
        self.setFixedHeight(44)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def apply_colors(self, accent: str, accent_fg: str, hover: str):
        self.setStyleSheet(f"""
            QPushButton {{
                text-align: left;
                padding-left: 16px;
                border: none;
                border-radius: 8px;
                font-size: 14px;
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
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.setMinimumSize(1000, 650)
        self.resize(1200, 750)

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ── Sidebar ──────────────────────────────────
        self.sidebar = QWidget()
        self.sidebar.setFixedWidth(220)
        self.sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(10, 14, 10, 14)
        sidebar_layout.setSpacing(4)

        # App branding
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

        # Navigation buttons
        self.nav_buttons: list[SidebarButton] = []
        nav_items = [
            ("Notes", "\U0001f4dd", "Ctrl+1"),
            ("Calendar", "\U0001f4c5", "Ctrl+2"),
            ("Finance", "\U0001f4b0", "Ctrl+3"),
        ]
        for i, (name, icon, shortcut_text) in enumerate(nav_items):
            btn = SidebarButton(name, icon, shortcut_text)
            btn.clicked.connect(lambda checked, n=name: self._navigate(n))
            btn.setToolTip(f"Switch to {name} ({shortcut_text})")
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append(btn)

            # Keyboard shortcut
            sc = QShortcut(QKeySequence(shortcut_text), self)
            sc.activated.connect(lambda n=name: self._navigate(n))

        sidebar_layout.addStretch()

        # Theme selector
        sidebar_layout.addSpacing(4)
        theme_label = QLabel("Theme")
        theme_label.setObjectName("subtitle")
        sidebar_layout.addWidget(theme_label)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(get_theme_names())
        current_theme = self.cfg.get("theme", "Catppuccin Dark")
        # Migrate old config values
        if current_theme == "dark":
            current_theme = "Catppuccin Dark"
        elif current_theme == "light":
            current_theme = "Catppuccin Light"
        idx = self.theme_combo.findText(current_theme)
        if idx >= 0:
            self.theme_combo.setCurrentIndex(idx)
        self.theme_combo.currentTextChanged.connect(self._on_theme_changed)
        sidebar_layout.addWidget(self.theme_combo)

        sidebar_layout.addSpacing(8)

        # Sync status indicator
        self.sync_label = QLabel("Sync: idle")
        self.sync_label.setObjectName("subtitle")
        sidebar_layout.addWidget(self.sync_label)

        main_layout.addWidget(self.sidebar)

        # ── Content area ─────────────────────────────
        self.stack = QStackedWidget()
        self.notes_panel = NotesPanel()
        self.calendar_panel = CalendarPanel()
        self.finance_panel = FinancePanel()

        self.stack.addWidget(self.notes_panel)     # 0
        self.stack.addWidget(self.calendar_panel)   # 1
        self.stack.addWidget(self.finance_panel)    # 2

        main_layout.addWidget(self.stack, 1)

        # ── Status bar ───────────────────────────────
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.clock_label = QLabel()
        self.status_bar.addPermanentWidget(self.clock_label)
        self._update_clock()

        clock_timer = QTimer(self)
        clock_timer.timeout.connect(self._update_clock)
        clock_timer.start(30_000)  # update every 30s

        # Apply theme and navigate
        self._apply_theme(current_theme)
        self._navigate("Notes")

    # ── Navigation ─────────────────────────────────────

    def _navigate(self, name: str):
        idx_map = {"Notes": 0, "Calendar": 1, "Finance": 2}
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

    def _apply_theme(self, name: str):
        sheet = THEMES.get(name, THEMES["Catppuccin Dark"])
        palette = PALETTES.get(name, PALETTES["Catppuccin Dark"])

        self.setStyleSheet(sheet)

        # Update sidebar background
        self.sidebar.setStyleSheet(
            f"QWidget#sidebar {{ background-color: {palette['header_bg']}; }}"
        )

        # Update nav button colors
        for btn in self.nav_buttons:
            btn.apply_colors(palette["accent"], palette["accent_fg"], palette["hover"])

        # Notify panels that need palette info
        if hasattr(self.finance_panel, 'set_palette'):
            self.finance_panel.set_palette(palette)
        if hasattr(self.calendar_panel, 'set_palette'):
            self.calendar_panel.set_palette(palette)

    # ── Status bar ─────────────────────────────────────

    def _update_clock(self):
        now = datetime.now()
        self.clock_label.setText(now.strftime("%A, %b %d  %H:%M"))

    def set_sync_status(self, text: str):
        self.sync_label.setText(f"Sync: {text}")
        if "error" in text.lower():
            self.sync_label.setObjectName("statusWarn")
        else:
            self.sync_label.setObjectName("subtitle")
        # Force style refresh
        self.sync_label.style().unpolish(self.sync_label)
        self.sync_label.style().polish(self.sync_label)
