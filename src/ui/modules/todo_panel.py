"""Todo list module UI — modern task manager with priorities, categories, and due dates."""

from datetime import date

from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor, QBrush, QFont
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QDialog, QLineEdit, QComboBox,
    QDateEdit, QTextEdit, QCheckBox, QFrame, QMessageBox,
    QListWidget, QListWidgetItem, QScrollArea,
)

from src.data.todo_store import (
    TodoStore, TodoItem, PRIORITY_LABELS, DEFAULT_TODO_CATEGORIES,
)


PRIORITY_COLORS = {0: "#a6adc8", 1: "#a6e3a1", 2: "#f9e2af", 3: "#f38ba8"}
PRIORITY_ICONS = {0: "", 1: "!", 2: "!!", 3: "!!!"}


def _hex_to_rgb(hex_str: str) -> tuple[int, int, int]:
    """Convert a hex color string like '#f38ba8' to (r, g, b) ints."""
    h = hex_str.lstrip("#")
    if len(h) == 6:
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return (200, 100, 100)  # fallback


class TodoDialog(QDialog):
    """Dialog to add/edit a todo item."""

    def __init__(self, parent=None, item: TodoItem | None = None):
        super().__init__(parent)
        self.setWindowTitle("Edit Task" if item else "New Task")
        self.setMinimumWidth(360)
        self.item = item
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(12, 10, 12, 10)

        layout.addWidget(QLabel("Title"))
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("What needs to be done?")
        if self.item:
            self.title_edit.setText(self.item.title)
        layout.addWidget(self.title_edit)

        row = QHBoxLayout()
        row.setSpacing(8)

        col1 = QVBoxLayout()
        col1.addWidget(QLabel("Priority"))
        self.priority_combo = QComboBox()
        for val, label in PRIORITY_LABELS.items():
            self.priority_combo.addItem(label, val)
        if self.item:
            idx = self.priority_combo.findData(self.item.priority)
            if idx >= 0:
                self.priority_combo.setCurrentIndex(idx)
        col1.addWidget(self.priority_combo)
        row.addLayout(col1)

        col2 = QVBoxLayout()
        col2.addWidget(QLabel("Category"))
        self.cat_combo = QComboBox()
        self.cat_combo.setEditable(True)
        self.cat_combo.addItems(DEFAULT_TODO_CATEGORIES)
        if self.item and self.item.category:
            self.cat_combo.setCurrentText(self.item.category)
        col2.addWidget(self.cat_combo)
        row.addLayout(col2)

        col3 = QVBoxLayout()
        col3.addWidget(QLabel("Due date"))
        self.due_check = QCheckBox("Set")
        self.due_edit = QDateEdit()
        self.due_edit.setCalendarPopup(True)
        if self.item and self.item.due_date:
            self.due_check.setChecked(True)
            parts = self.item.due_date.split("-")
            self.due_edit.setDate(QDate(int(parts[0]), int(parts[1]), int(parts[2])))
        else:
            self.due_check.setChecked(False)
            today = date.today()
            self.due_edit.setDate(QDate(today.year, today.month, today.day))
        self.due_check.toggled.connect(lambda c: self.due_edit.setEnabled(c))
        self.due_edit.setEnabled(self.due_check.isChecked())
        due_row = QHBoxLayout()
        due_row.addWidget(self.due_check)
        due_row.addWidget(self.due_edit, 1)
        col3.addLayout(due_row)
        row.addLayout(col3)

        layout.addLayout(row)

        layout.addWidget(QLabel("Notes"))
        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(60)
        self.notes_edit.setPlaceholderText("Optional notes...")
        if self.item:
            self.notes_edit.setPlainText(self.item.notes)
        layout.addWidget(self.notes_edit)

        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(sep)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("secondary")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        btn_row.addWidget(save_btn)
        layout.addLayout(btn_row)

    def get_data(self) -> dict:
        due = ""
        if self.due_check.isChecked():
            qd = self.due_edit.date()
            due = f"{qd.year():04d}-{qd.month():02d}-{qd.day():02d}"
        return {
            "title": self.title_edit.text().strip() or "Untitled",
            "priority": self.priority_combo.currentData(),
            "due_date": due,
            "category": self.cat_combo.currentText(),
            "notes": self.notes_edit.toPlainText(),
        }


class TodoItemWidget(QFrame):
    """A single todo item rendered as a compact card."""

    def __init__(self, item: TodoItem, parent_panel, palette: dict | None = None):
        super().__init__()
        self.item = item
        self.panel = parent_panel
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        palette = palette or {}

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(6)

        # Checkbox
        self.check = QCheckBox()
        self.check.setChecked(item.done)
        self.check.toggled.connect(self._on_toggle)
        layout.addWidget(self.check)

        # Priority dot
        if item.priority > 0:
            dot = QLabel(PRIORITY_ICONS[item.priority])
            color = PRIORITY_COLORS[item.priority]
            dot.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 11px;")
            dot.setFixedWidth(20)
            layout.addWidget(dot)

        # Title + metadata
        info = QVBoxLayout()
        info.setSpacing(0)
        info.setContentsMargins(0, 0, 0, 0)

        title = QLabel(item.title)
        font_style = "font-size: 12px; font-weight: bold;"
        if item.done:
            font_style += " text-decoration: line-through; opacity: 0.6;"
        title.setStyleSheet(font_style)
        info.addWidget(title)

        # Metadata row
        meta_parts = []
        if item.category:
            meta_parts.append(item.category)
        if item.due_date and not item.done:
            # Don't repeat due date here — we have a dedicated label on the right
            pass
        elif item.due_date:
            meta_parts.append(f"Due: {item.due_date}")
        if meta_parts:
            meta = QLabel(" \u00b7 ".join(meta_parts))
            meta.setObjectName("subtitle")
            meta.setStyleSheet("font-size: 10px;")
            info.addWidget(meta)

        layout.addLayout(info, 1)

        # Due date label (right-aligned)
        if item.due_date:
            today = date.today()
            try:
                due = date.fromisoformat(item.due_date)
                delta = (due - today).days
                if delta < 0 and not item.done:
                    due_text = f"Overdue {-delta}d"
                    due_color = palette.get("red", "#f38ba8")
                elif delta == 0:
                    due_text = "Due Today"
                    due_color = palette.get("yellow", "#f9e2af")
                else:
                    due_text = f"Due {due.strftime('%b %d')}"
                    due_color = palette.get("muted", "#7f849c")

                due_lbl = QLabel(due_text)
                due_lbl.setStyleSheet(
                    f"font-size: 10px; font-weight: bold; color: {due_color}; "
                    f"padding: 1px 4px;"
                )
                due_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                layout.addWidget(due_lbl)
            except ValueError:
                pass

        # Edit button
        edit_btn = QPushButton("Edit")
        edit_btn.setObjectName("secondary")
        edit_btn.setFixedSize(40, 22)
        edit_btn.setStyleSheet("font-size: 10px; padding: 2px 6px;")
        edit_btn.clicked.connect(self._on_edit)
        layout.addWidget(edit_btn)

        # Priority color stripe on left
        border_color = PRIORITY_COLORS.get(item.priority, "transparent")
        style_parts = []
        if item.priority > 0:
            style_parts.append(f"border-left: 3px solid {border_color};")
            style_parts.append("border-radius: 4px;")

        # Overdue background tint (15% alpha of palette red)
        if item.due_date and not item.done:
            try:
                due = date.fromisoformat(item.due_date)
                if due < today:
                    red_hex = palette.get("red", "#f38ba8")
                    r, g, b = _hex_to_rgb(red_hex)
                    style_parts.append(f"background-color: rgba({r},{g},{b}, 38);")
            except ValueError:
                pass

        if style_parts:
            self.setStyleSheet(
                "TodoItemWidget { " + " ".join(style_parts) + " }"
            )

    def _on_toggle(self, checked):
        self.panel._toggle_item(self.item.id)

    def _on_edit(self):
        self.panel._edit_item(self.item)

    def mouseDoubleClickEvent(self, ev):
        self.panel._edit_item(self.item)


class TodoPanel(QWidget):

    def __init__(self, todo_store=None, parent=None):
        super().__init__(parent)
        self.store = todo_store or TodoStore()
        self._palette: dict = {}
        self._build_ui()
        self._refresh()

    def set_palette(self, palette: dict):
        self._palette = palette
        self._refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(6)

        # Header
        header = QHBoxLayout()
        title = QLabel("Tasks")
        title.setObjectName("sectionTitle")
        header.addWidget(title)

        self.count_label = QLabel("0 tasks")
        self.count_label.setObjectName("subtitle")
        header.addWidget(self.count_label)

        header.addStretch()

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All", "Pending", "Completed"])
        self.filter_combo.setFixedWidth(90)
        self.filter_combo.currentTextChanged.connect(self._refresh)
        header.addWidget(self.filter_combo)

        btn_add = QPushButton("+ Task")
        btn_add.clicked.connect(self._add_item)
        header.addWidget(btn_add)

        btn_clear = QPushButton("Clear Done")
        btn_clear.setObjectName("secondary")
        btn_clear.clicked.connect(self._clear_done)
        header.addWidget(btn_clear)

        layout.addLayout(header)

        # Quick add
        quick_row = QHBoxLayout()
        quick_row.setSpacing(4)
        self.quick_input = QLineEdit()
        self.quick_input.setPlaceholderText("Quick add task... (Enter to add)")
        self.quick_input.returnPressed.connect(self._quick_add)
        quick_row.addWidget(self.quick_input, 1)
        layout.addLayout(quick_row)

        # Task list
        self._list_container = QWidget()
        self._list_layout = QVBoxLayout(self._list_container)
        self._list_layout.setContentsMargins(0, 0, 0, 0)
        self._list_layout.setSpacing(2)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self._list_container)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        layout.addWidget(scroll, 1)

        # Footer stats
        footer = QHBoxLayout()
        self.stats_label = QLabel("")
        self.stats_label.setObjectName("subtitle")
        footer.addWidget(self.stats_label)
        footer.addStretch()
        layout.addLayout(footer)

    def _refresh(self):
        # Clear list
        while self._list_layout.count():
            child = self._list_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        filter_mode = self.filter_combo.currentText()
        items = self.store.get_all(include_done=(filter_mode != "Pending"))

        if filter_mode == "Completed":
            items = [i for i in items if i.done]

        # Sort: overdue incomplete first, then priority desc, then created_at asc
        today_iso = date.today().isoformat()

        def _sort_key(item: TodoItem):
            is_overdue_incomplete = (
                not item.done
                and bool(item.due_date)
                and item.due_date < today_iso
            )
            # 0 = overdue incomplete (top), 1 = done, 2 = not done but not overdue
            if item.done:
                group = 2
            elif is_overdue_incomplete:
                group = 0
            else:
                group = 1
            return (group, -item.priority, item.created_at or "")

        items.sort(key=_sort_key)

        for item in items:
            widget = TodoItemWidget(item, self, self._palette)
            self._list_layout.addWidget(widget)

        self._list_layout.addStretch()

        counts = self.store.get_counts()
        self.count_label.setText(f"{counts['total']} tasks")
        self.stats_label.setText(
            f"{counts['pending']} pending \u00b7 {counts['done']} completed"
        )

    def _quick_add(self):
        text = self.quick_input.text().strip()
        if text:
            self.store.add(title=text)
            self.quick_input.clear()
            self._refresh()

    def _add_item(self):
        dlg = TodoDialog(self)
        if dlg.exec():
            data = dlg.get_data()
            self.store.add(**data)
            self._refresh()

    def _edit_item(self, item: TodoItem):
        dlg = TodoDialog(self, item)
        if dlg.exec():
            data = dlg.get_data()
            item.title = data["title"]
            item.priority = data["priority"]
            item.due_date = data["due_date"]
            item.category = data["category"]
            item.notes = data["notes"]
            self.store.update(item)
            self._refresh()

    def _toggle_item(self, item_id: str):
        self.store.toggle_done(item_id)
        self._refresh()

    def _clear_done(self):
        items = self.store.get_all()
        done_items = [i for i in items if i.done]
        if not done_items:
            return
        reply = QMessageBox.question(
            self, "Clear Completed",
            f"Remove {len(done_items)} completed task(s)?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            for item in done_items:
                self.store.delete(item.id)
            self._refresh()