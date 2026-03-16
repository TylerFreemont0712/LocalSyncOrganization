"""Light and dark theme stylesheets for PyQt6."""

DARK_THEME = """
QMainWindow, QWidget {
    background-color: #1e1e2e;
    color: #cdd6f4;
    font-family: "Segoe UI", "Ubuntu", sans-serif;
    font-size: 14px;
}
QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #313244;
    color: #cdd6f4;
    border: 1px solid #45475a;
    border-radius: 6px;
    padding: 6px;
    selection-background-color: #4a9eff;
}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border: 1px solid #4a9eff;
}
QPushButton {
    background-color: #4a9eff;
    color: #1e1e2e;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #6ab0ff;
}
QPushButton:pressed {
    background-color: #3a8eef;
}
QPushButton#destructive {
    background-color: #f38ba8;
}
QPushButton#destructive:hover {
    background-color: #f5a0b8;
}
QPushButton#secondary {
    background-color: #45475a;
    color: #cdd6f4;
}
QPushButton#secondary:hover {
    background-color: #585b70;
}
QListWidget {
    background-color: #313244;
    border: 1px solid #45475a;
    border-radius: 6px;
    padding: 4px;
}
QListWidget::item {
    padding: 8px;
    border-radius: 4px;
}
QListWidget::item:selected {
    background-color: #4a9eff;
    color: #1e1e2e;
}
QListWidget::item:hover {
    background-color: #45475a;
}
QTableWidget {
    background-color: #313244;
    border: 1px solid #45475a;
    border-radius: 6px;
    gridline-color: #45475a;
}
QTableWidget::item {
    padding: 6px;
}
QTableWidget::item:selected {
    background-color: #4a9eff;
    color: #1e1e2e;
}
QHeaderView::section {
    background-color: #45475a;
    color: #cdd6f4;
    padding: 8px;
    border: none;
    font-weight: bold;
}
QComboBox {
    background-color: #313244;
    color: #cdd6f4;
    border: 1px solid #45475a;
    border-radius: 6px;
    padding: 6px;
}
QComboBox::drop-down {
    border: none;
}
QComboBox QAbstractItemView {
    background-color: #313244;
    color: #cdd6f4;
    selection-background-color: #4a9eff;
}
QDateEdit, QSpinBox, QDoubleSpinBox {
    background-color: #313244;
    color: #cdd6f4;
    border: 1px solid #45475a;
    border-radius: 6px;
    padding: 6px;
}
QLabel#sectionTitle {
    font-size: 18px;
    font-weight: bold;
    color: #cdd6f4;
}
QLabel#subtitle {
    font-size: 12px;
    color: #a6adc8;
}
QFrame#separator {
    background-color: #45475a;
    max-height: 1px;
}
QScrollBar:vertical {
    background-color: #1e1e2e;
    width: 10px;
    border-radius: 5px;
}
QScrollBar::handle:vertical {
    background-color: #45475a;
    border-radius: 5px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background-color: #585b70;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
"""

LIGHT_THEME = """
QMainWindow, QWidget {
    background-color: #eff1f5;
    color: #4c4f69;
    font-family: "Segoe UI", "Ubuntu", sans-serif;
    font-size: 14px;
}
QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #ffffff;
    color: #4c4f69;
    border: 1px solid #ccd0da;
    border-radius: 6px;
    padding: 6px;
    selection-background-color: #1e66f5;
}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border: 1px solid #1e66f5;
}
QPushButton {
    background-color: #1e66f5;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #4080f7;
}
QPushButton:pressed {
    background-color: #1650d0;
}
QPushButton#destructive {
    background-color: #d20f39;
}
QPushButton#secondary {
    background-color: #ccd0da;
    color: #4c4f69;
}
QPushButton#secondary:hover {
    background-color: #bcc0cc;
}
QListWidget {
    background-color: #ffffff;
    border: 1px solid #ccd0da;
    border-radius: 6px;
    padding: 4px;
}
QListWidget::item {
    padding: 8px;
    border-radius: 4px;
}
QListWidget::item:selected {
    background-color: #1e66f5;
    color: #ffffff;
}
QListWidget::item:hover {
    background-color: #e6e9ef;
}
QTableWidget {
    background-color: #ffffff;
    border: 1px solid #ccd0da;
    border-radius: 6px;
    gridline-color: #ccd0da;
}
QTableWidget::item:selected {
    background-color: #1e66f5;
    color: #ffffff;
}
QHeaderView::section {
    background-color: #e6e9ef;
    color: #4c4f69;
    padding: 8px;
    border: none;
    font-weight: bold;
}
QComboBox {
    background-color: #ffffff;
    color: #4c4f69;
    border: 1px solid #ccd0da;
    border-radius: 6px;
    padding: 6px;
}
QComboBox QAbstractItemView {
    background-color: #ffffff;
    color: #4c4f69;
    selection-background-color: #1e66f5;
}
QDateEdit, QSpinBox, QDoubleSpinBox {
    background-color: #ffffff;
    color: #4c4f69;
    border: 1px solid #ccd0da;
    border-radius: 6px;
    padding: 6px;
}
QLabel#sectionTitle {
    font-size: 18px;
    font-weight: bold;
}
QLabel#subtitle {
    font-size: 12px;
    color: #8c8fa1;
}
QFrame#separator {
    background-color: #ccd0da;
    max-height: 1px;
}
QScrollBar:vertical {
    background-color: #eff1f5;
    width: 10px;
    border-radius: 5px;
}
QScrollBar::handle:vertical {
    background-color: #ccd0da;
    border-radius: 5px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background-color: #bcc0cc;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
"""

THEMES = {
    "dark": DARK_THEME,
    "light": LIGHT_THEME,
}
