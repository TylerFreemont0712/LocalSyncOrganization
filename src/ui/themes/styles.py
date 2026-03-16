"""Theme stylesheets for PyQt6 — Catppuccin Dark, Catppuccin Light, Nord, Solarized, Gruvbox."""


def _build_theme(c: dict) -> str:
    """Generate a full QSS stylesheet from a color palette dict."""
    return f"""
/* ── Base ──────────────────────────────────────────── */
QMainWindow, QWidget {{
    background-color: {c['bg']};
    color: {c['fg']};
    font-family: "Segoe UI", "Ubuntu", "Noto Sans", sans-serif;
    font-size: 14px;
}}

/* ── Text inputs ──────────────────────────────────── */
QLineEdit, QTextEdit, QPlainTextEdit {{
    background-color: {c['surface']};
    color: {c['fg']};
    border: 1px solid {c['border']};
    border-radius: 6px;
    padding: 6px;
    selection-background-color: {c['accent']};
    selection-color: {c['accent_fg']};
}}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
    border: 1px solid {c['accent']};
}}
QLineEdit[readOnly="true"] {{
    background-color: {c['bg']};
}}

/* ── Buttons ──────────────────────────────────────── */
QPushButton {{
    background-color: {c['accent']};
    color: {c['accent_fg']};
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: bold;
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
QPushButton#destructive {{
    background-color: {c['red']};
    color: {c['accent_fg']};
}}
QPushButton#destructive:hover {{
    background-color: {c['red_hover']};
}}
QPushButton#secondary {{
    background-color: {c['surface']};
    color: {c['fg']};
    border: 1px solid {c['border']};
}}
QPushButton#secondary:hover {{
    background-color: {c['border']};
}}

/* ── Lists ────────────────────────────────────────── */
QListWidget {{
    background-color: {c['surface']};
    border: 1px solid {c['border']};
    border-radius: 6px;
    padding: 4px;
    outline: none;
}}
QListWidget::item {{
    padding: 8px;
    border-radius: 4px;
}}
QListWidget::item:selected {{
    background-color: {c['accent']};
    color: {c['accent_fg']};
}}
QListWidget::item:hover:!selected {{
    background-color: {c['hover']};
}}

/* ── Tables ───────────────────────────────────────── */
QTableWidget {{
    background-color: {c['surface']};
    border: 1px solid {c['border']};
    border-radius: 6px;
    gridline-color: {c['border']};
    outline: none;
}}
QTableWidget::item {{
    padding: 6px;
}}
QTableWidget::item:selected {{
    background-color: {c['accent']};
    color: {c['accent_fg']};
}}
QTableWidget::item:alternate {{
    background-color: {c['alt_row']};
}}
QHeaderView::section {{
    background-color: {c['header_bg']};
    color: {c['fg']};
    padding: 8px;
    border: none;
    border-bottom: 2px solid {c['accent']};
    font-weight: bold;
}}

/* ── Combo boxes ──────────────────────────────────── */
QComboBox {{
    background-color: {c['surface']};
    color: {c['fg']};
    border: 1px solid {c['border']};
    border-radius: 6px;
    padding: 6px 8px;
    min-width: 80px;
}}
QComboBox::drop-down {{
    border: none;
    width: 20px;
}}
QComboBox QAbstractItemView {{
    background-color: {c['surface']};
    color: {c['fg']};
    selection-background-color: {c['accent']};
    selection-color: {c['accent_fg']};
    border: 1px solid {c['border']};
    border-radius: 4px;
}}

/* ── Spin boxes / Date edits ──────────────────────── */
QDateEdit, QTimeEdit, QSpinBox, QDoubleSpinBox {{
    background-color: {c['surface']};
    color: {c['fg']};
    border: 1px solid {c['border']};
    border-radius: 6px;
    padding: 6px;
}}
QDateEdit::drop-down, QTimeEdit::drop-down {{
    border: none;
}}

/* ── Check boxes ──────────────────────────────────── */
QCheckBox {{
    spacing: 8px;
}}
QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 2px solid {c['border']};
    background-color: {c['surface']};
}}
QCheckBox::indicator:checked {{
    background-color: {c['accent']};
    border-color: {c['accent']};
}}

/* ── Labels ───────────────────────────────────────── */
QLabel#sectionTitle {{
    font-size: 18px;
    font-weight: bold;
    color: {c['fg']};
    padding-bottom: 2px;
}}
QLabel#subtitle {{
    font-size: 12px;
    color: {c['muted']};
}}
QLabel#statusOk {{
    color: {c['green']};
    font-size: 12px;
}}
QLabel#statusWarn {{
    color: {c['yellow']};
    font-size: 12px;
}}

/* ── Separators ───────────────────────────────────── */
QFrame#separator {{
    background-color: {c['border']};
    max-height: 1px;
}}

/* ── Splitter handles ─────────────────────────────── */
QSplitter::handle {{
    background-color: {c['border']};
    width: 2px;
    margin: 4px 2px;
}}
QSplitter::handle:hover {{
    background-color: {c['accent']};
}}

/* ── Scroll bars ──────────────────────────────────── */
QScrollBar:vertical {{
    background-color: transparent;
    width: 10px;
    border-radius: 5px;
    margin: 2px;
}}
QScrollBar::handle:vertical {{
    background-color: {c['border']};
    border-radius: 5px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{
    background-color: {c['muted']};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}
QScrollBar:horizontal {{
    background-color: transparent;
    height: 10px;
    border-radius: 5px;
    margin: 2px;
}}
QScrollBar::handle:horizontal {{
    background-color: {c['border']};
    border-radius: 5px;
    min-width: 30px;
}}
QScrollBar::handle:horizontal:hover {{
    background-color: {c['muted']};
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0px;
}}

/* ── Tooltips ─────────────────────────────────────── */
QToolTip {{
    background-color: {c['surface']};
    color: {c['fg']};
    border: 1px solid {c['border']};
    border-radius: 4px;
    padding: 4px 8px;
}}

/* ── Dialogs ──────────────────────────────────────── */
QDialog {{
    background-color: {c['bg']};
}}
QMessageBox {{
    background-color: {c['bg']};
}}

/* ── Status bar ───────────────────────────────────── */
QStatusBar {{
    background-color: {c['header_bg']};
    color: {c['muted']};
    border-top: 1px solid {c['border']};
    font-size: 12px;
    padding: 2px 8px;
}}
QStatusBar::item {{
    border: none;
}}
"""


# ── Catppuccin Mocha (Dark) ──────────────────────────
_CATPPUCCIN_DARK = {
    "bg": "#1e1e2e", "surface": "#313244", "border": "#45475a",
    "fg": "#cdd6f4", "muted": "#a6adc8", "hover": "#3b3d54",
    "accent": "#4a9eff", "accent_fg": "#1e1e2e",
    "accent_hover": "#6ab0ff", "accent_pressed": "#3a8eef",
    "red": "#f38ba8", "red_hover": "#f5a0b8",
    "green": "#a6e3a1", "yellow": "#f9e2af",
    "header_bg": "#181825", "alt_row": "#2a2a3c",
}

# ── Catppuccin Latte (Light) ─────────────────────────
_CATPPUCCIN_LIGHT = {
    "bg": "#eff1f5", "surface": "#ffffff", "border": "#ccd0da",
    "fg": "#4c4f69", "muted": "#8c8fa1", "hover": "#e6e9ef",
    "accent": "#1e66f5", "accent_fg": "#ffffff",
    "accent_hover": "#4080f7", "accent_pressed": "#1650d0",
    "red": "#d20f39", "red_hover": "#e0304f",
    "green": "#40a02b", "yellow": "#df8e1d",
    "header_bg": "#e6e9ef", "alt_row": "#f4f5f8",
}

# ── Nord ─────────────────────────────────────────────
_NORD = {
    "bg": "#2e3440", "surface": "#3b4252", "border": "#4c566a",
    "fg": "#eceff4", "muted": "#d8dee9", "hover": "#434c5e",
    "accent": "#88c0d0", "accent_fg": "#2e3440",
    "accent_hover": "#8fbcbb", "accent_pressed": "#81a1c1",
    "red": "#bf616a", "red_hover": "#d08770",
    "green": "#a3be8c", "yellow": "#ebcb8b",
    "header_bg": "#272c36", "alt_row": "#333a47",
}

# ── Solarized Dark ───────────────────────────────────
_SOLARIZED = {
    "bg": "#002b36", "surface": "#073642", "border": "#586e75",
    "fg": "#839496", "muted": "#657b83", "hover": "#0a4050",
    "accent": "#268bd2", "accent_fg": "#fdf6e3",
    "accent_hover": "#2aa198", "accent_pressed": "#1a6da0",
    "red": "#dc322f", "red_hover": "#e35550",
    "green": "#859900", "yellow": "#b58900",
    "header_bg": "#001f27", "alt_row": "#04303d",
}

# ── Gruvbox Dark ─────────────────────────────────────
_GRUVBOX = {
    "bg": "#282828", "surface": "#3c3836", "border": "#504945",
    "fg": "#ebdbb2", "muted": "#a89984", "hover": "#444240",
    "accent": "#d79921", "accent_fg": "#282828",
    "accent_hover": "#fabd2f", "accent_pressed": "#b57614",
    "red": "#cc241d", "red_hover": "#fb4934",
    "green": "#98971a", "yellow": "#d79921",
    "header_bg": "#1d2021", "alt_row": "#32302f",
}


# ── Build all themes ─────────────────────────────────
THEMES = {
    "Catppuccin Dark": _build_theme(_CATPPUCCIN_DARK),
    "Catppuccin Light": _build_theme(_CATPPUCCIN_LIGHT),
    "Nord": _build_theme(_NORD),
    "Solarized Dark": _build_theme(_SOLARIZED),
    "Gruvbox Dark": _build_theme(_GRUVBOX),
}

# Color palettes exposed for programmatic access (e.g. chart colors)
PALETTES = {
    "Catppuccin Dark": _CATPPUCCIN_DARK,
    "Catppuccin Light": _CATPPUCCIN_LIGHT,
    "Nord": _NORD,
    "Solarized Dark": _SOLARIZED,
    "Gruvbox Dark": _GRUVBOX,
}


def get_theme_names() -> list[str]:
    return list(THEMES.keys())
