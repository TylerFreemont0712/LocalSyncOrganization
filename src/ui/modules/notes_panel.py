"""Notes module UI — markdown editor with file tree and search."""

from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QListWidget, QListWidgetItem, QPlainTextEdit,
    QLineEdit, QPushButton, QLabel, QMessageBox, QInputDialog,
)

from src.data.notes_store import NotesStore


class NotesPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.store = NotesStore()
        self.current_note_path: str | None = None
        self._build_ui()
        self._refresh_list()

    def _build_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        # --- Left sidebar: search + note list ---
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(8, 8, 4, 8)

        title = QLabel("Notes")
        title.setObjectName("sectionTitle")
        sidebar_layout.addWidget(title)

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search notes...")
        self.search_box.textChanged.connect(self._on_search)
        sidebar_layout.addWidget(self.search_box)

        btn_row = QHBoxLayout()
        self.btn_new = QPushButton("+ New")
        self.btn_new.clicked.connect(self._new_note)
        self.btn_delete = QPushButton("Delete")
        self.btn_delete.setObjectName("destructive")
        self.btn_delete.clicked.connect(self._delete_note)
        btn_row.addWidget(self.btn_new)
        btn_row.addWidget(self.btn_delete)
        sidebar_layout.addLayout(btn_row)

        self.note_list = QListWidget()
        self.note_list.currentItemChanged.connect(self._on_note_selected)
        sidebar_layout.addWidget(self.note_list)

        # --- Right side: editor ---
        editor_widget = QWidget()
        editor_layout = QVBoxLayout(editor_widget)
        editor_layout.setContentsMargins(4, 8, 8, 8)

        self.note_title_label = QLabel("Select or create a note")
        self.note_title_label.setObjectName("sectionTitle")
        editor_layout.addWidget(self.note_title_label)

        self.editor = QPlainTextEdit()
        self.editor.setPlaceholderText("Start writing in Markdown...")
        self.editor.textChanged.connect(self._on_text_changed)
        editor_layout.addWidget(self.editor)

        self.tag_label = QLabel("")
        self.tag_label.setObjectName("subtitle")
        editor_layout.addWidget(self.tag_label)

        splitter.addWidget(sidebar)
        splitter.addWidget(editor_widget)
        splitter.setSizes([250, 550])

        layout.addWidget(splitter)

    def _refresh_list(self, notes=None):
        self.note_list.blockSignals(True)
        self.note_list.clear()
        notes = notes or self.store.list_notes()
        for note in notes:
            item = QListWidgetItem(str(note.path))
            item.setData(Qt.ItemDataRole.UserRole, str(note.path))
            self.note_list.addItem(item)
        self.note_list.blockSignals(False)

    def _on_search(self, query: str):
        if query.strip():
            results = self.store.search(query)
            self._refresh_list(results)
        else:
            self._refresh_list()

    def _on_note_selected(self, current: QListWidgetItem | None, _prev):
        self._save_current()
        if current is None:
            return
        rel_path = current.data(Qt.ItemDataRole.UserRole)
        note = self.store.get_note(rel_path)
        if note:
            self.current_note_path = rel_path
            self.note_title_label.setText(note.title)
            self.editor.blockSignals(True)
            self.editor.setPlainText(note.content)
            self.editor.blockSignals(False)
            tags_text = ", ".join(f"#{t}" for t in note.tags) if note.tags else "No tags"
            self.tag_label.setText(tags_text)

    def _on_text_changed(self):
        # Auto-save on edit
        self._save_current()

    def _save_current(self):
        if self.current_note_path is None:
            return
        note = self.store.get_note(self.current_note_path)
        if note:
            new_content = self.editor.toPlainText()
            if new_content != note.content:
                note.content = new_content
                note.tags = self.store._extract_tags(new_content)
                self.store.save_note(note)
                tags_text = ", ".join(f"#{t}" for t in note.tags) if note.tags else "No tags"
                self.tag_label.setText(tags_text)

    def _new_note(self):
        name, ok = QInputDialog.getText(self, "New Note", "Note name (without .md):")
        if ok and name.strip():
            safe_name = name.strip().replace("/", "-").replace("\\", "-")
            rel = Path(f"{safe_name}.md")
            from src.data.notes_store import Note
            note = Note(title=safe_name, content="", path=rel)
            self.store.save_note(note)
            self._refresh_list()
            # Select the new note
            for i in range(self.note_list.count()):
                item = self.note_list.item(i)
                if item and item.data(Qt.ItemDataRole.UserRole) == str(rel):
                    self.note_list.setCurrentItem(item)
                    break

    def _delete_note(self):
        if self.current_note_path is None:
            return
        reply = QMessageBox.question(
            self, "Delete Note",
            f"Delete '{self.current_note_path}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.store.delete_note(self.current_note_path)
            self.current_note_path = None
            self.editor.clear()
            self.note_title_label.setText("Select or create a note")
            self.tag_label.setText("")
            self._refresh_list()
