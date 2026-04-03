"""Theme stylesheets for PyQt6.

Themes included:
  Dark   — Catppuccin Mocha, Tokyo Night, Dracula, Monokai Pro, One Dark Pro, Rosé Pine
  Medium — Nord, Gruvbox Dark
  Light  — Catppuccin Latte, Solarized Light

Arrow rendering:
  All dropdown / spinner arrows use inline SVG data-URIs so they render
  correctly in Qt6. The CSS border-trick (width:0; height:0; border-left…)
  creates triangles in web browsers but has no effect in Qt's QSS engine —
  the borders appear on a zero-size box and produce nothing visible.
"""


# ─────────────────────────────────────────────────────────
#  SVG arrow helper
# ─────────────────────────────────────────────────────────

def _svg_arrow(direction: str, color: str) -> str:
    """Return a QSS url() value for an inline SVG triangle arrow.

    direction: 'down' | 'up'
    color    : hex string e.g. '#cdd6f4'
    """
    col = color.replace("#", "%23")
    # 10×6 triangle
    if direction == "down":
        pts = "0,0 10,0 5,6"    # ▼
    else:                        # "up"
        pts = "0,6 10,6 5,0"    # ▲
    svg = (
        "%3Csvg xmlns='http://www.w3.org/2000/svg' "
        "width='10' height='6'%3E"
        f"%3Cpolygon points='{pts}' fill='{col}'/%3E"
        "%3C/svg%3E"
    )
    return f'url("data:image/svg+xml,{svg}")'


# ─────────────────────────────────────────────────────────
#  Theme builder
# ─────────────────────────────────────────────────────────

def _rgba(hex_color: str, alpha: int) -> str:
    """Convert a hex color string to a QSS rgba() value.

    Qt's QSS uses 0-255 for the alpha channel (not 0.0-1.0 like web CSS).
    """
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r}, {g}, {b}, {alpha})"


def _build_theme(c: dict) -> str:
    """Generate a full QSS stylesheet from a color palette dict.

    If the palette contains a ``panel_alpha`` key (int, 0-255), all panel
    background surfaces are rendered with that opacity level so an animated
    background (e.g. Matrix rain) bleeds through.
    """
    # Pre-compute SVG arrow URLs for each needed state
    _adn    = _svg_arrow("down", c["fg"])           # dropdown arrow, normal
    _adn_h  = _svg_arrow("down", c["accent_fg"])    # dropdown arrow, on hover
    _adn_on = _svg_arrow("up",   c["fg"])           # dropdown arrow, open (flip)
    _aup    = _svg_arrow("up",   c["fg"])           # spinbox up arrow
    _aup_h  = _svg_arrow("up",   c["accent_fg"])
    _adn2   = _svg_arrow("down", c["fg"])           # spinbox down arrow (alias)
    _adn2_h = _svg_arrow("down", c["accent_fg"])

    # Semi-transparent surface colours for themes with panel_alpha
    pa = c.get("panel_alpha", 255)
    _bg      = _rgba(c["bg"],         pa)       if pa < 255 else c["bg"]
    _surf    = _rgba(c["surface"],    pa)       if pa < 255 else c["surface"]
    _hdr     = _rgba(c["header_bg"],  min(pa + 25, 255)) if pa < 255 else c["header_bg"]
    _alt     = _rgba(c["alt_row"],    pa)       if pa < 255 else c["alt_row"]
    _hover   = _rgba(c["hover"],      min(pa + 30, 255)) if pa < 255 else c["hover"]

    return f"""
/* ━━━━ Base ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
QMainWindow, QWidget {{
    background-color: {_bg};
    color: {c['fg']};
    font-family: "Segoe UI", "Segoe UI Emoji", "Segoe UI Symbol", "Meiryo UI", "Ubuntu", "Noto Sans", sans-serif;
    font-size: 12px;
}}

/* Transparent scroll-area viewport so inner widgets set their own bg */
QScrollArea > QWidget > QWidget {{
    background-color: transparent;
}}

/* ━━━━ Menu bar ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
QMenuBar {{
    background-color: {_hdr};
    color: {c['fg']};
    border-bottom: 1px solid {c['border']};
    padding: 2px 4px;
    font-size: 12px;
}}
QMenuBar::item {{
    background-color: transparent;
    padding: 4px 10px;
    border-radius: 4px;
}}
QMenuBar::item:selected {{
    background-color: {c['accent']};
    color: {c['accent_fg']};
}}
QMenuBar::item:pressed {{
    background-color: {c['accent_pressed']};
    color: {c['accent_fg']};
}}

QMenu {{
    background-color: {_surf};
    color: {c['fg']};
    border: 1px solid {c['border']};
    border-radius: 6px;
    padding: 4px;
}}
QMenu::item {{
    padding: 5px 24px 5px 12px;
    border-radius: 3px;
}}
QMenu::item:selected {{
    background-color: {c['accent']};
    color: {c['accent_fg']};
}}
QMenu::separator {{
    height: 1px;
    background-color: {c['border']};
    margin: 4px 8px;
}}

/* ━━━━ Tab widget ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
QTabWidget::pane {{
    border: 1px solid {c['border']};
    border-radius: 6px;
    background-color: {c['surface']};
    top: -1px;
}}
QTabWidget[documentMode="true"]::pane {{
    border: none;
    border-top: 1px solid {c['border']};
    background-color: transparent;
    border-radius: 0;
}}
QTabBar {{
    background-color: transparent;
}}
QTabBar::tab {{
    background-color: transparent;
    color: {c['muted']};
    padding: 7px 16px;
    border: none;
    border-bottom: 2px solid transparent;
    min-width: 60px;
    font-size: 12px;
}}
QTabBar::tab:selected {{
    color: {c['fg']};
    border-bottom: 2px solid {c['accent']};
    font-weight: bold;
}}
QTabBar::tab:hover:!selected {{
    color: {c['fg']};
    background-color: {c['hover']};
    border-radius: 4px 4px 0 0;
}}
QTabBar::tab:disabled {{
    color: {c['border']};
}}

/* ━━━━ Text inputs ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
QLineEdit, QTextEdit, QPlainTextEdit {{
    background-color: {_surf};
    color: {c['fg']};
    border: 1px solid {c['border']};
    border-radius: 4px;
    padding: 4px 6px;
    selection-background-color: {c['accent']};
    selection-color: {c['accent_fg']};
}}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
    border: 1px solid {c['accent']};
    outline: none;
}}
QLineEdit[readOnly="true"] {{
    background-color: {_bg};
    color: {c['muted']};
}}

/* ━━━━ Push buttons ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
QPushButton {{
    background-color: {c['accent']};
    color: {c['accent_fg']};
    border: none;
    border-radius: 5px;
    padding: 5px 14px;
    font-weight: bold;
    font-size: 12px;
}}
QPushButton:hover {{
    background-color: {c['accent_hover']};
}}
QPushButton:pressed {{
    background-color: {c['accent_pressed']};
}}
QPushButton:disabled {{
    background-color: {c['border']};
    color: {c['muted']};
}}
QPushButton:flat {{
    background-color: transparent;
    border: none;
    color: {c['fg']};
    font-weight: normal;
}}
QPushButton:flat:hover {{
    background-color: {c['hover']};
}}

/* Destructive (delete) */
QPushButton#destructive {{
    background-color: {c['red']};
    color: #ffffff;
}}
QPushButton#destructive:hover {{
    background-color: {c['red_hover']};
}}
QPushButton#destructive:pressed {{
    background-color: {c['red']};
}}

/* Secondary (muted/ghost) — high contrast */
QPushButton#secondary {{
    background-color: {c['surface']};
    color: {c['fg']};
    border: 1px solid {c['border']};
    font-weight: normal;
}}
QPushButton#secondary:hover {{
    background-color: {c['hover']};
    border-color: {c['accent']};
    color: {c['fg']};
}}
QPushButton#secondary:pressed {{
    background-color: {c['border']};
}}
QPushButton#secondary:disabled {{
    color: {c['muted']};
    border-color: {c['border']};
}}

/* ━━━━ Tool buttons (color swatches, weekday pickers) ━━━━ */
QToolButton {{
    background-color: {_surf};
    color: {c['fg']};
    border: 1px solid {c['border']};
    border-radius: 4px;
    padding: 3px 6px;
    font-size: 11px;
}}
QToolButton:hover {{
    background-color: {_hover};
    border-color: {c['accent']};
}}
QToolButton:checked {{
    background-color: {c['accent']};
    color: {c['accent_fg']};
    border-color: {c['accent']};
    font-weight: bold;
}}
QToolButton:pressed {{
    background-color: {c['accent_pressed']};
    color: {c['accent_fg']};
}}
QToolButton::menu-indicator {{
    image: none;
}}

/* ━━━━ Lists ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
QListWidget {{
    background-color: {_surf};
    border: 1px solid {c['border']};
    border-radius: 6px;
    padding: 4px;
    outline: none;
}}
QListWidget::item {{
    padding: 5px 4px;
    border-radius: 4px;
}}
QListWidget::item:selected {{
    background-color: {c['accent']};
    color: {c['accent_fg']};
}}
QListWidget::item:hover:!selected {{
    background-color: {_hover};
}}

/* ━━━━ Tables ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
QTableWidget {{
    background-color: {_surf};
    border: 1px solid {c['border']};
    border-radius: 6px;
    gridline-color: {c['border']};
    outline: none;
    alternate-background-color: {_alt};
}}
QTableWidget::item {{
    padding: 4px;
}}
QTableWidget::item:selected {{
    background-color: {c['accent']};
    color: {c['accent_fg']};
}}
QHeaderView::section {{
    background-color: {_hdr};
    color: {c['fg']};
    padding: 5px 6px;
    border: none;
    border-bottom: 2px solid {c['accent']};
    border-right: 1px solid {c['border']};
    font-weight: bold;
    font-size: 11px;
}}
QHeaderView::section:last {{
    border-right: none;
}}

/* ━━━━ Combo boxes ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
QComboBox {{
    background-color: {_surf};
    color: {c['fg']};
    border: 1px solid {c['border']};
    border-radius: 4px;
    padding: 4px 6px;
    padding-right: 28px;
    min-width: 70px;
    font-size: 12px;
}}
QComboBox:hover {{
    border-color: {c['accent']};
}}
QComboBox:focus {{
    border-color: {c['accent']};
}}
QComboBox::drop-down {{
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 26px;
    background-color: {c['border']};
    border-left: 1px solid {c['border']};
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
}}
QComboBox::drop-down:hover {{
    background-color: {c['accent']};
}}
QComboBox::down-arrow {{
    image: {_adn};
    width: 10px;
    height: 6px;
}}
QComboBox::down-arrow:on {{
    image: {_adn_on};
}}
QComboBox::drop-down:hover + QComboBox::down-arrow,
QComboBox::down-arrow:hover {{
    image: {_adn_h};
}}
QComboBox QAbstractItemView {{
    background-color: {c['surface']};
    color: {c['fg']};
    selection-background-color: {c['accent']};
    selection-color: {c['accent_fg']};
    border: 1px solid {c['border']};
    border-radius: 4px;
    padding: 2px;
    outline: none;
}}

/* ━━━━ Spin boxes, Date/Time edits ━━━━━━━━━━━━━━━ */
QDateEdit, QTimeEdit, QSpinBox, QDoubleSpinBox {{
    background-color: {_surf};
    color: {c['fg']};
    border: 1px solid {c['border']};
    border-radius: 4px;
    padding: 4px 6px;
    font-size: 12px;
}}
QDateEdit:hover, QTimeEdit:hover, QSpinBox:hover, QDoubleSpinBox:hover {{
    border-color: {c['accent']};
}}
QDateEdit:focus, QTimeEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
    border-color: {c['accent']};
}}

/* Calendar / time popup drop-down button */
QDateEdit::drop-down, QTimeEdit::drop-down {{
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 26px;
    background-color: {c['border']};
    border-left: 1px solid {c['border']};
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
}}
QDateEdit::drop-down:hover, QTimeEdit::drop-down:hover {{
    background-color: {c['accent']};
}}
QDateEdit::down-arrow, QTimeEdit::down-arrow {{
    image: {_adn};
    width: 10px;
    height: 6px;
}}
QDateEdit::down-arrow:hover, QTimeEdit::down-arrow:hover {{
    image: {_adn_h};
}}

/* Spinbox increment buttons */
QSpinBox::up-button, QDoubleSpinBox::up-button {{
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 20px;
    background-color: {c['border']};
    border-left: 1px solid {c['border']};
    border-bottom: 1px solid {c['border']};
    border-top-right-radius: 4px;
}}
QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover {{
    background-color: {c['accent']};
}}
QSpinBox::up-button:pressed, QDoubleSpinBox::up-button:pressed {{
    background-color: {c['accent_pressed']};
}}
QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {{
    image: {_aup};
    width: 8px;
    height: 5px;
}}
QSpinBox::up-arrow:hover, QDoubleSpinBox::up-arrow:hover {{
    image: {_aup_h};
}}
QSpinBox::down-button, QDoubleSpinBox::down-button {{
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    width: 20px;
    background-color: {c['border']};
    border-left: 1px solid {c['border']};
    border-bottom-right-radius: 4px;
}}
QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {{
    background-color: {c['accent']};
}}
QSpinBox::down-button:pressed, QDoubleSpinBox::down-button:pressed {{
    background-color: {c['accent_pressed']};
}}
QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {{
    image: {_adn2};
    width: 8px;
    height: 5px;
}}
QSpinBox::down-arrow:hover, QDoubleSpinBox::down-arrow:hover {{
    image: {_adn2_h};
}}

/* Calendar popup widget (the QCalendarWidget) */
QCalendarWidget QWidget {{
    background-color: {c['surface']};
    color: {c['fg']};
}}
QCalendarWidget QAbstractItemView:enabled {{
    background-color: {c['surface']};
    color: {c['fg']};
    selection-background-color: {c['accent']};
    selection-color: {c['accent_fg']};
}}
QCalendarWidget QAbstractItemView:disabled {{
    color: {c['muted']};
}}
QCalendarWidget QToolButton {{
    background-color: transparent;
    color: {c['fg']};
    border: none;
    font-weight: bold;
    font-size: 13px;
    padding: 4px 8px;
}}
QCalendarWidget QToolButton:hover {{
    background-color: {c['hover']};
    border-radius: 4px;
}}
QCalendarWidget #qt_calendar_navigationbar {{
    background-color: {c['header_bg']};
    border-bottom: 1px solid {c['border']};
    padding: 4px;
}}

/* ━━━━ Checkboxes ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
QCheckBox {{
    spacing: 8px;
    color: {c['fg']};
    font-size: 12px;
}}
QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 2px solid {c['border']};
    background-color: {c['surface']};
}}
QCheckBox::indicator:hover {{
    border-color: {c['accent']};
}}
QCheckBox::indicator:checked {{
    background-color: {c['accent']};
    border-color: {c['accent']};
}}
QCheckBox::indicator:checked:hover {{
    background-color: {c['accent_hover']};
}}

/* ━━━━ Progress bar ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
QProgressBar {{
    background-color: {c['surface']};
    border: 1px solid {c['border']};
    border-radius: 4px;
    text-align: center;
    color: {c['fg']};
    font-size: 11px;
    min-height: 10px;
}}
QProgressBar::chunk {{
    background-color: {c['accent']};
    border-radius: 4px;
}}

/* ━━━━ Labels ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
QLabel#sectionTitle {{
    font-size: 15px;
    font-weight: bold;
    color: {c['fg']};
}}
QLabel#subtitle {{
    font-size: 11px;
    color: {c['muted']};
}}
QLabel#statusOk {{
    color: {c['green']};
    font-size: 12px;
    font-weight: bold;
}}
QLabel#statusWarn {{
    color: {c['yellow']};
    font-size: 12px;
    font-weight: bold;
}}

/* ━━━━ Separators ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
QFrame#separator {{
    background-color: {c['border']};
    max-height: 1px;
    border: none;
}}

/* ━━━━ Splitter ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
QSplitter::handle {{
    background-color: {c['border']};
    width: 2px;
    margin: 4px 2px;
}}
QSplitter::handle:hover {{
    background-color: {c['accent']};
}}

/* ━━━━ Scroll bars ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
QScrollBar:vertical {{
    background-color: transparent;
    width: 8px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background-color: {c['border']};
    border-radius: 4px;
    min-height: 24px;
}}
QScrollBar::handle:vertical:hover {{
    background-color: {c['muted']};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    height: 0;
    background: transparent;
}}
QScrollBar:horizontal {{
    background-color: transparent;
    height: 8px;
    margin: 0;
}}
QScrollBar::handle:horizontal {{
    background-color: {c['border']};
    border-radius: 4px;
    min-width: 24px;
}}
QScrollBar::handle:horizontal:hover {{
    background-color: {c['muted']};
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal,
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
    width: 0;
    background: transparent;
}}

/* ━━━━ Tooltips ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
QToolTip {{
    background-color: {c['surface']};
    color: {c['fg']};
    border: 1px solid {c['border']};
    border-radius: 4px;
    padding: 5px 8px;
    font-size: 12px;
}}

/* ━━━━ Dialogs ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
QDialog {{
    background-color: {_bg};
}}
QMessageBox {{
    background-color: {_bg};
}}
QMessageBox QLabel {{
    color: {c['fg']};
    font-size: 13px;
}}

/* ━━━━ Status bar ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
QStatusBar {{
    background-color: {c['header_bg']};
    color: {c['muted']};
    border-top: 1px solid {c['border']};
    font-size: 11px;
    padding: 1px 6px;
}}
QStatusBar::item {{
    border: none;
}}

/* ━━━━ Group boxes ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
QGroupBox {{
    border: 1px solid {c['border']};
    border-radius: 6px;
    margin-top: 14px;
    padding-top: 8px;
    font-weight: bold;
    color: {c['fg']};
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 4px;
    color: {c['accent']};
    font-size: 12px;
}}
"""


# ─────────────────────────────────────────────────────────
#  Dark themes
# ─────────────────────────────────────────────────────────

# Catppuccin Mocha — deep purple-dark, blue accent
_CATPPUCCIN_DARK = {
    "bg": "#1e1e2e",        "surface": "#313244",   "border": "#45475a",
    "fg": "#cdd6f4",        "muted": "#7f849c",      "hover": "#3b3d54",
    "accent": "#89b4fa",    "accent_fg": "#1e1e2e",
    "accent_hover": "#a0c5ff", "accent_pressed": "#74a4ea",
    "red": "#f38ba8",       "red_hover": "#f5a0b8",
    "green": "#a6e3a1",     "yellow": "#f9e2af",
    "header_bg": "#181825", "alt_row": "#252538",
}

# Tokyo Night — navy-dark, electric blue accent
_TOKYO_NIGHT = {
    "bg": "#1a1b26",        "surface": "#24283b",   "border": "#414868",
    "fg": "#c0caf5",        "muted": "#565f89",      "hover": "#2d3348",
    "accent": "#7aa2f7",    "accent_fg": "#1a1b26",
    "accent_hover": "#93b4fb", "accent_pressed": "#6090e5",
    "red": "#f7768e",       "red_hover": "#f88fa0",
    "green": "#9ece6a",     "yellow": "#e0af68",
    "header_bg": "#16161e", "alt_row": "#1f2335",
}

# Dracula — classic dark purple
_DRACULA = {
    "bg": "#282a36",        "surface": "#343746",   "border": "#44475a",
    "fg": "#f8f8f2",        "muted": "#8090c0",      "hover": "#3d4059",
    "accent": "#bd93f9",    "accent_fg": "#282a36",
    "accent_hover": "#cda7ff", "accent_pressed": "#ad83e9",
    "red": "#ff5555",       "red_hover": "#ff7070",
    "green": "#50fa7b",     "yellow": "#f1fa8c",
    "header_bg": "#21222c", "alt_row": "#2f303e",
}

# Monokai Pro — warm dark, golden accent
_MONOKAI = {
    "bg": "#2d2a2e",        "surface": "#403e41",   "border": "#5b595c",
    "fg": "#fcfcfa",        "muted": "#a9a7a7",      "hover": "#4a4849",
    "accent": "#ffd866",    "accent_fg": "#2d2a2e",
    "accent_hover": "#ffe085", "accent_pressed": "#e0be50",
    "red": "#ff6188",       "red_hover": "#ff7a9c",
    "green": "#a9dc76",     "yellow": "#ffd866",
    "header_bg": "#221f22", "alt_row": "#353135",
}

# One Dark Pro — Atom-inspired neutral dark
_ONE_DARK = {
    "bg": "#282c34",        "surface": "#353b45",   "border": "#4b5263",
    "fg": "#abb2bf",        "muted": "#7a8294",      "hover": "#3e4452",
    "accent": "#61afef",    "accent_fg": "#282c34",
    "accent_hover": "#7bbef5", "accent_pressed": "#519fd5",
    "red": "#e06c75",       "red_hover": "#e88090",
    "green": "#98c379",     "yellow": "#e5c07b",
    "header_bg": "#21252b", "alt_row": "#2c313c",
}

# Rosé Pine — muted, nature-inspired dark
_ROSE_PINE = {
    "bg": "#191724",        "surface": "#26233a",   "border": "#403d52",
    "fg": "#e0def4",        "muted": "#908caa",      "hover": "#2d2b3e",
    "accent": "#c4a7e7",    "accent_fg": "#191724",
    "accent_hover": "#d4b9f0", "accent_pressed": "#b498d4",
    "red": "#eb6f92",       "red_hover": "#f08098",
    "green": "#9ccfd8",     "yellow": "#f6c177",
    "header_bg": "#12111f", "alt_row": "#201e2e",
}

# ─────────────────────────────────────────────────────────
#  Medium themes
# ─────────────────────────────────────────────────────────

# Nord — arctic teal palette
_NORD = {
    "bg": "#2e3440",        "surface": "#3b4252",   "border": "#4c566a",
    "fg": "#eceff4",        "muted": "#9199aa",      "hover": "#434c5e",
    "accent": "#88c0d0",    "accent_fg": "#2e3440",
    "accent_hover": "#9bcfde", "accent_pressed": "#79b0c0",
    "red": "#bf616a",       "red_hover": "#cc7079",
    "green": "#a3be8c",     "yellow": "#ebcb8b",
    "header_bg": "#272c36", "alt_row": "#333a47",
}

# Gruvbox Dark — warm earthy tones
_GRUVBOX = {
    "bg": "#282828",        "surface": "#3c3836",   "border": "#665c54",
    "fg": "#ebdbb2",        "muted": "#bdae93",      "hover": "#504945",
    "accent": "#fabd2f",    "accent_fg": "#282828",
    "accent_hover": "#ffd045", "accent_pressed": "#d9a520",
    "red": "#fb4934",       "red_hover": "#ff6147",
    "green": "#b8bb26",     "yellow": "#fabd2f",
    "header_bg": "#1d2021", "alt_row": "#32302f",
}

# ─────────────────────────────────────────────────────────
#  Light themes
# ─────────────────────────────────────────────────────────

# Catppuccin Latte — soft warm light
_CATPPUCCIN_LIGHT = {
    "bg": "#eff1f5",        "surface": "#ffffff",   "border": "#bcc0cc",
    "fg": "#4c4f69",        "muted": "#7c7f93",      "hover": "#dce0ea",
    "accent": "#1e66f5",    "accent_fg": "#ffffff",
    "accent_hover": "#4080f7", "accent_pressed": "#1650d0",
    "red": "#d20f39",       "red_hover": "#e0304f",
    "green": "#40a02b",     "yellow": "#df8e1d",
    "header_bg": "#e6e9ef", "alt_row": "#f4f5f8",
}

# Solarized Light — high-readability warm ivory
_SOLARIZED_LIGHT = {
    "bg": "#fdf6e3",        "surface": "#eee8d5",   "border": "#d3cbbb",
    "fg": "#657b83",        "muted": "#93a1a1",      "hover": "#e2dac8",
    "accent": "#268bd2",    "accent_fg": "#fdf6e3",
    "accent_hover": "#3aa0e8", "accent_pressed": "#1a6da0",
    "red": "#dc322f",       "red_hover": "#e04545",
    "green": "#859900",     "yellow": "#b58900",
    "header_bg": "#ece7d6", "alt_row": "#f5f0e2",
}


# ─────────────────────────────────────────────────────────
#  Hacker / Terminal themes
# ─────────────────────────────────────────────────────────

# Hacker — neon green on near-black; inspired by classic terminal aesthetics
_HACKER = {
    "bg": "#0d0d0d",        "surface": "#1a1a1a",   "border": "#2d2d2d",
    "fg": "#e0e0e0",        "muted": "#606060",      "hover": "#222222",
    "accent": "#39ff14",    "accent_fg": "#000000",
    "accent_hover": "#55ff30", "accent_pressed": "#2acc0a",
    "red": "#ff3355",       "red_hover": "#ff5577",
    "green": "#39ff14",     "yellow": "#ffdd00",
    "header_bg": "#080808", "alt_row": "#141414",
}

# Matrix — phosphor green on pure black; iconic digital-rain palette.
# Colours are tuned to match the film's organic phosphor-screen aesthetic —
# muted sage green for UI text rather than blinding neon, with just enough
# glow to feel authentically "in the Matrix."
# panel_alpha < 255 activates rgba() semi-transparent surfaces so the
# animated rain background glows through every panel and widget.
_MATRIX = {
    "bg": "#000000",        "surface": "#001500",   "border": "#003800",
    "fg": "#9fd896",        "muted": "#3e6e3a",      "hover": "#002100",
    "accent": "#35b055",    "accent_fg": "#000000",
    "accent_hover": "#45c865", "accent_pressed": "#268040",
    "red": "#cc2233",       "red_hover": "#e03344",
    "green": "#35b055",     "yellow": "#88dd00",
    "header_bg": "#000a00", "alt_row": "#000d00",
    "panel_alpha": 190,     # panels ~75% opaque — rain glows through
}


# ─────────────────────────────────────────────────────────
#  Build registry
# ─────────────────────────────────────────────────────────

_ALL_PALETTES = {
    # Dark
    "Catppuccin Dark":  _CATPPUCCIN_DARK,
    "Tokyo Night":      _TOKYO_NIGHT,
    "Dracula":          _DRACULA,
    "Monokai Pro":      _MONOKAI,
    "One Dark Pro":     _ONE_DARK,
    "Rose Pine":        _ROSE_PINE,
    # Medium
    "Nord":             _NORD,
    "Gruvbox Dark":     _GRUVBOX,
    # Terminal
    "Hacker":           _HACKER,
    "Matrix":           _MATRIX,
    # Light
    "Catppuccin Light": _CATPPUCCIN_LIGHT,
    "Solarized Light":  _SOLARIZED_LIGHT,
}

THEMES   = {name: _build_theme(pal) for name, pal in _ALL_PALETTES.items()}
PALETTES = dict(_ALL_PALETTES)


def get_theme_names() -> list[str]:
    return list(THEMES.keys())