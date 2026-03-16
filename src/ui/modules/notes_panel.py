"""Notes module UI — markdown editor with file tree, search, word count, and folder support."""

from pathlib import Path

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QListWidget, QListWidgetItem, QPlainTextEdit,
    QLineEdit, QPushButton, QLabel, QMessageBox, QInputDialog,
    QFrame,
)

from src.data.notes_store import NotesStore, Note


class NotesPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.store = NotesStore()
        self.current_note_path: str | None = None
        self._save_timer = QTimer(self)
        self._save_timer.setSingleShot(True)
        self._save_timer.setInterval(500)  # debounce saves by 500ms
        self._save_timer.timeout.connect(self._save_current)
        self._build_ui()
        self._refresh_list()

    def _build_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        # ── Left sidebar: search + note list ──────────
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(12, 12, 6, 12)
        sidebar_layout.setSpacing(8)

        title = QLabel("Notes")
        title.setObjectName("sectionTitle")
        sidebar_layout.addWidget(title)

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search notes...")
        self.search_box.setClearButtonEnabled(True)
        self.search_box.textChanged.connect(self._on_search)
        sidebar_layout.addWidget(self.search_box)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(6)
        self.btn_new = QPushButton("+ Note")
        self.btn_new.setToolTip("Create a new note")
        self.btn_new.clicked.connect(self._new_note)
        self.btn_folder = QPushButton("+ Folder")
        self.btn_folder.setObjectName("secondary")
        self.btn_folder.setToolTip("Create a new folder")
        self.btn_folder.clicked.connect(self._new_folder)
        btn_row.addWidget(self.btn_new)
        btn_row.addWidget(self.btn_folder)
        sidebar_layout.addLayout(btn_row)

        self.note_list = QListWidget()
        self.note_list.currentItemChanged.connect(self._on_note_selected)
        sidebar_layout.addWidget(self.note_list, 1)

        self.note_count_label = QLabel("0 notes")
        self.note_count_label.setObjectName("subtitle")
        sidebar_layout.addWidget(self.note_count_label)

        # ── Right side: editor ────────────────────────
        editor_widget = QWidget()
        editor_layout = QVBoxLayout(editor_widget)
        editor_layout.setContentsMargins(6, 12, 12, 12)
        editor_layout.setSpacing(6)

        # Title bar
        title_row = QHBoxLayout()
        self.note_title_label = QLabel("Select or create a note")
        self.note_title_label.setObjectName("sectionTitle")
        title_row.addWidget(self.note_title_label, 1)

        self.btn_rename = QPushButton("Rename")
        self.btn_rename.setObjectName("secondary")
        self.btn_rename.setToolTip("Rename this note")
        self.btn_rename.clicked.connect(self._rename_note)
        self.btn_rename.setVisible(False)
        title_row.addWidget(self.btn_rename)

        self.btn_delete = QPushButton("Delete")
        self.btn_delete.setObjectName("destructive")
        self.btn_delete.setToolTip("Delete this note permanently")
        self.btn_delete.clicked.connect(self._delete_note)
        self.btn_delete.setVisible(False)
        title_row.addWidget(self.btn_delete)

        editor_layout.addLayout(title_row)

        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine)
        editor_layout.addWidget(sep)

        self.editor = QPlainTextEdit()
        self.editor.setPlaceholderText("Start writing in Markdown...\n\nUse #tags anywhere in your text.")
        self.editor.setTabStopDistance(28.0)
        self.editor.textChanged.connect(self._on_text_changed)
        editor_layout.addWidget(self.editor, 1)

        # Footer: tags + word count
        footer = QHBoxLayout()
        self.tag_label = QLabel("")
        self.tag_label.setObjectName("subtitle")
        footer.addWidget(self.tag_label, 1)

        self.word_count_label = QLabel("")
        self.word_count_label.setObjectName("subtitle")
        self.word_count_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        footer.addWidget(self.word_count_label)
        editor_layout.addLayout(footer)

        splitter.addWidget(sidebar)
        splitter.addWidget(editor_widget)
        splitter.setSizes([260, 540])
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        layout.addWidget(splitter)

    # ── List management ────────────────────────────────

    def _refresh_list(self, notes=None):
        self.note_list.blockSignals(True)
        self.note_list.clear()
        notes = notes or self.store.list_notes()
        for note in notes:
            display = str(note.path)
            item = QListWidgetItem(display)
            item.setData(Qt.ItemDataRole.UserRole, str(note.path))
            item.setToolTip(f"Tags: {', '.join('#' + t for t in note.tags) if note.tags else 'none'}")
            self.note_list.addItem(item)
        self.note_list.blockSignals(False)
        self.note_count_label.setText(f"{len(notes)} note{'s' if len(notes) != 1 else ''}")

    def _on_search(self, query: str):
        if query.strip():
            results = self.store.search(query)
            self._refresh_list(results)
        else:
            self._refresh_list()

    # ── Note selection ─────────────────────────────────

    def _on_note_selected(self, current: QListWidgetItem | None, _prev):
        self._save_current()
        if current is None:
            self._clear_editor()
            return
        rel_path = current.data(Qt.ItemDataRole.UserRole)
        note = self.store.get_note(rel_path)
        if note:
            self.current_note_path = rel_path
            self.note_title_label.setText(note.title)
            self.editor.blockSignals(True)
            self.editor.setPlainText(note.content)
            self.editor.blockSignals(False)
            self._update_footer(note)
            self.btn_rename.setVisible(True)
            self.btn_delete.setVisible(True)

    def _clear_editor(self):
        self.current_note_path = None
        self.note_title_label.setText("Select or create a note")
        self.editor.blockSignals(True)
        self.editor.clear()
        self.editor.blockSignals(False)
        self.tag_label.setText("")
        self.word_count_label.setText("")
        self.btn_rename.setVisible(False)
        self.btn_delete.setVisible(False)

    # ── Editing ────────────────────────────────────────

    def _on_text_changed(self):
        self._save_timer.start()  # debounced auto-save
        text = self.editor.toPlainText()
        words = len(text.split()) if text.strip() else 0
        chars = len(text)
        self.word_count_label.setText(f"{words} words | {chars} chars")

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
                self._update_footer(note)

    def _update_footer(self, note: Note):
        tags_text = "  ".join(f"#{t}" for t in note.tags) if note.tags else "No tags"
        self.tag_label.setText(tags_text)
        text = note.content
        words = len(text.split()) if text.strip() else 0
        self.word_count_label.setText(f"{words} words | {len(text)} chars")

    # ── CRUD actions ───────────────────────────────────

    def _new_note(self):
        name, ok = QInputDialog.getText(self, "New Note", "Note name (without .md):")
        if ok and name.strip():
            safe_name = name.strip().replace("/", "-").replace("\\", "-")
            rel = Path(f"{safe_name}.md")
            note = Note(title=safe_name, content="", path=rel)
            self.store.save_note(note)
            self._refresh_list()
            self._select_note(str(rel))

    def _new_folder(self):
        name, ok = QInputDialog.getText(self, "New Folder", "Folder name:")
        if ok and name.strip():
            safe_name = name.strip().replace("/", "-").replace("\\", "-")
            folder_path = self.store.root / safe_name
            folder_path.mkdir(parents=True, exist_ok=True)
            # Create a starter note in the folder
            note_name, ok2 = QInputDialog.getText(
                self, "First Note", f"Note name in '{safe_name}/' (without .md):",
            )
            if ok2 and note_name.strip():
                safe_note = note_name.strip().replace("/", "-").replace("\\", "-")
                rel = Path(safe_name) / f"{safe_note}.md"
                note = Note(title=safe_note, content="", path=rel)
                self.store.save_note(note)
                self._refresh_list()
                self._select_note(str(rel))
            else:
                self._refresh_list()

    def _rename_note(self):
        if self.current_note_path is None:
            return
        old_path = Path(self.current_note_path)
        current_name = old_path.stem
        new_name, ok = QInputDialog.getText(
            self, "Rename Note", "New name (without .md):", text=current_name,
        )
        if ok and new_name.strip() and new_name.strip() != current_name:
            safe_name = new_name.strip().replace("/", "-").replace("\\", "-")
            new_rel = old_path.parent / f"{safe_name}.md"
            # Read content, delete old, save new
            note = self.store.get_note(self.current_note_path)
            if note:
                content = note.content
                self.store.delete_note(self.current_note_path)
                new_note = Note(title=safe_name, content=content, path=new_rel, tags=note.tags)
                self.store.save_note(new_note)
                self.current_note_path = str(new_rel)
                self.note_title_label.setText(safe_name)
                self._refresh_list()
                self._select_note(str(new_rel))

    def _delete_note(self):
        if self.current_note_path is None:
            return
        reply = QMessageBox.question(
            self, "Delete Note",
            f"Permanently delete '{self.current_note_path}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.store.delete_note(self.current_note_path)
            self._clear_editor()
            self._refresh_list()

    def _select_note(self, rel_path: str):
        for i in range(self.note_list.count()):
            item = self.note_list.item(i)
            if item and item.data(Qt.ItemDataRole.UserRole) == rel_path:
                self.note_list.setCurrentItem(item)
                break
