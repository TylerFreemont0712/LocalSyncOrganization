"""Main application window with sidebar navigation."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QStackedWidget, QPushButton, QLabel, QFrame,
)

from src.config import APP_NAME, APP_VERSION, load_config, save_config
from src.ui.themes.styles import THEMES
from src.ui.modules.notes_panel import NotesPanel
from src.ui.modules.calendar_panel import CalendarPanel
from src.ui.modules.finance_panel import FinancePanel


class SidebarButton(QPushButton):
    """A sidebar navigation button."""

    def __init__(self, text: str, icon_char: str = ""):
        display = f"{icon_char}  {text}" if icon_char else text
        super().__init__(display)
        self.setCheckable(True)
        self.setFixedHeight(44)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding-left: 16px;
                border: none;
                border-radius: 8px;
                font-size: 14px;
            }
            QPushButton:checked {
                background-color: #4a9eff;
                color: #1e1e2e;
                font-weight: bold;
            }
            QPushButton:hover:!checked {
                background-color: rgba(255,255,255,0.05);
            }
        """)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.cfg = load_config()
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.setMinimumSize(1000, 650)
        self.resize(1200, 750)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- Sidebar ---
        sidebar = QWidget()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("background-color: rgba(0,0,0,0.15);")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(8, 12, 8, 12)
        sidebar_layout.setSpacing(4)

        app_label = QLabel(APP_NAME)
        app_label.setStyleSheet("font-size: 20px; font-weight: bold; padding: 8px;")
        sidebar_layout.addWidget(app_label)

        version_label = QLabel(f"v{APP_VERSION}")
        version_label.setObjectName("subtitle")
        version_label.setStyleSheet("padding-left: 8px; margin-bottom: 12px;")
        sidebar_layout.addWidget(version_label)

        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine)
        sidebar_layout.addWidget(sep)

        self.nav_buttons: list[SidebarButton] = []
        nav_items = [
            ("Notes", "\U0001f4dd"),
            ("Calendar", "\U0001f4c5"),
            ("Finance", "\U0001f4b0"),
        ]
        for name, icon in nav_items:
            btn = SidebarButton(name, icon)
            btn.clicked.connect(lambda checked, n=name: self._navigate(n))
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append(btn)

        sidebar_layout.addStretch()

        # Theme toggle
        self.theme_btn = QPushButton("Toggle Theme")
        self.theme_btn.setObjectName("secondary")
        self.theme_btn.clicked.connect(self._toggle_theme)
        sidebar_layout.addWidget(self.theme_btn)

        # Sync status
        self.sync_label = QLabel("Sync: idle")
        self.sync_label.setObjectName("subtitle")
        self.sync_label.setStyleSheet("padding: 4px 8px;")
        sidebar_layout.addWidget(self.sync_label)

        main_layout.addWidget(sidebar)

        # --- Content area ---
        self.stack = QStackedWidget()
        self.notes_panel = NotesPanel()
        self.calendar_panel = CalendarPanel()
        self.finance_panel = FinancePanel()

        self.stack.addWidget(self.notes_panel)     # index 0
        self.stack.addWidget(self.calendar_panel)   # index 1
        self.stack.addWidget(self.finance_panel)    # index 2

        main_layout.addWidget(self.stack, 1)

        # Apply theme
        theme_name = self.cfg.get("theme", "dark")
        self._apply_theme(theme_name)

        # Default to Notes
        self._navigate("Notes")

    def _navigate(self, name: str):
        idx_map = {"Notes": 0, "Calendar": 1, "Finance": 2}
        idx = idx_map.get(name, 0)
        self.stack.setCurrentIndex(idx)
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == idx)

    def _toggle_theme(self):
        current = self.cfg.get("theme", "dark")
        new_theme = "light" if current == "dark" else "dark"
        self.cfg["theme"] = new_theme
        save_config(self.cfg)
        self._apply_theme(new_theme)

    def _apply_theme(self, name: str):
        sheet = THEMES.get(name, THEMES["dark"])
        self.setStyleSheet(sheet)

    def set_sync_status(self, text: str):
        self.sync_label.setText(f"Sync: {text}")
