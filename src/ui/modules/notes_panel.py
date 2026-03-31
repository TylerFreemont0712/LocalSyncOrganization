"""Notes/Obsidian module UI — tree-based vault browser, markdown editor, REST API integration.

The sidebar uses a QTreeWidget with collapsible folders (triangle toggles)
that mimics Obsidian's file explorer layout.
"""

import json
import logging
import os
import subprocess
import sys
import threading
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path, PurePosixPath

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QTreeWidget, QTreeWidgetItem, QPlainTextEdit, QTextBrowser,
    QLineEdit, QPushButton, QLabel, QMessageBox, QInputDialog,
    QFrame, QFileDialog, QStackedWidget,
)

from src.config import load_config, save_config
from src.data.notes_store import NotesStore, Note
from src.sync.deletion_manifest import record_deletion as _record_vault_deletion

logger = logging.getLogger(__name__)


class ObsidianAPI:
    """Minimal client for the Obsidian Local REST API plugin."""

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def is_available(self) -> bool:
        try:
            req = urllib.request.Request(
                f"{self.base_url}/", headers=self._headers(), method="GET",
            )
            with urllib.request.urlopen(req, timeout=3) as resp:
                return resp.status == 200
        except Exception:
            return False

    def list_files(self, folder: str = "/") -> list[str]:
        try:
            req = urllib.request.Request(
                f"{self.base_url}/vault{folder}",
                headers=self._headers(), method="GET",
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode())
                return data.get("files", [])
        except Exception as e:
            logger.warning(f"Obsidian API list_files failed: {e}")
            return []

    def read_note(self, path: str) -> str:
        try:
            encoded_path = urllib.parse.quote(path, safe="/")
            headers = self._headers()
            headers["Accept"] = "text/markdown"
            req = urllib.request.Request(
                f"{self.base_url}/vault/{encoded_path}",
                headers=headers, method="GET",
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                return resp.read().decode("utf-8")
        except Exception as e:
            logger.warning(f"Obsidian API read failed: {e}")
            return ""

    def create_note(self, path: str, content: str) -> bool:
        try:
            encoded_path = urllib.parse.quote(path, safe="/")
            headers = self._headers()
            headers["Content-Type"] = "text/markdown"
            req = urllib.request.Request(
                f"{self.base_url}/vault/{encoded_path}",
                data=content.encode("utf-8"),
                headers=headers, method="PUT",
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                return resp.status in (200, 201, 204)
        except Exception as e:
            logger.warning(f"Obsidian API create failed: {e}")
            return False

    def append_note(self, path: str, content: str) -> bool:
        try:
            encoded_path = urllib.parse.quote(path, safe="/")
            headers = self._headers()
            headers["Content-Type"] = "text/markdown"
            req = urllib.request.Request(
                f"{self.base_url}/vault/{encoded_path}",
                data=content.encode("utf-8"),
                headers=headers, method="POST",
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                return resp.status in (200, 201, 204)
        except Exception as e:
            logger.warning(f"Obsidian API append failed: {e}")
            return False

    def open_in_obsidian(self, path: str):
        """Open a note in the Obsidian desktop app via URI scheme."""
        cfg = load_config()
        vault_path = cfg.get("obsidian_vault_path", "")
        vault_name = Path(vault_path).name if vault_path else ""
        # Strip .md extension
        if path.endswith(".md"):
            path = path[:-3]
        encoded_vault = urllib.parse.quote(vault_name, safe="")
        encoded_file = urllib.parse.quote(path, safe="/")
        uri = f"obsidian://open?vault={encoded_vault}&file={encoded_file}"
        try:
            if sys.platform == "win32":
                os.startfile(uri)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", uri])
            else:
                subprocess.Popen(["xdg-open", uri])
        except Exception as e:
            logger.warning(f"Failed to open Obsidian: {e}")


# ── Tree builder ───────────────────────────────────────

def _build_tree_structure(notes: list[Note]) -> dict:
    """Build a nested dict from note paths for the tree view.

    Returns: {"_files": [Note, ...], "subfolder": {"_files": [...], ...}}
    """
    tree: dict = {"_files": []}
    for note in sorted(notes, key=lambda n: str(n.path).lower()):
        parts = PurePosixPath(str(note.path)).parts
        if len(parts) == 1:
            # Root-level file
            tree["_files"].append(note)
        else:
            # Navigate into subfolders
            node = tree
            for folder in parts[:-1]:
                if folder not in node:
                    node[folder] = {"_files": []}
                node = node[folder]
            node["_files"].append(note)
    return tree


def _populate_tree_widget(parent_item, tree_dict: dict, expanded_paths: set):
    """Recursively populate QTreeWidgetItems from the nested dict."""
    # Add subfolders first (sorted)
    folders = sorted(k for k in tree_dict if k != "_files")
    for folder_name in folders:
        folder_item = QTreeWidgetItem(parent_item)
        folder_item.setText(0, f"\U0001f4c1 {folder_name}")
        folder_item.setData(0, Qt.ItemDataRole.UserRole, None)  # Not a file
        folder_item.setData(0, Qt.ItemDataRole.UserRole + 1, folder_name)
        font = folder_item.font(0)
        font.setBold(True)
        folder_item.setFont(0, font)
        folder_item.setFlags(
            folder_item.flags() | Qt.ItemFlag.ItemIsAutoTristate
        )
        # Recursively fill
        _populate_tree_widget(folder_item, tree_dict[folder_name], expanded_paths)
        # Expand if it was previously expanded
        if folder_name in expanded_paths:
            folder_item.setExpanded(True)

    # Add files
    for note in tree_dict.get("_files", []):
        file_item = QTreeWidgetItem(parent_item)
        file_item.setText(0, f"\U0001f4c4 {note.title}")
        file_item.setData(0, Qt.ItemDataRole.UserRole, str(note.path))
        file_item.setToolTip(
            0,
            f"Tags: {', '.join('#' + t for t in note.tags) if note.tags else 'none'}"
        )


class NotesPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.cfg = load_config()
        self._init_store()
        self.current_note_path: str | None = None
        self._expanded_folders: set[str] = set()
        self._save_timer = QTimer(self)
        self._save_timer.setSingleShot(True)
        self._save_timer.setInterval(500)
        self._save_timer.timeout.connect(self._save_current)
        self._palette: dict = {}
        self._preview_mode: bool = False
        self._obsidian_api: ObsidianAPI | None = None
        self._obsidian_status = "not configured"
        self._build_ui()
        self._refresh_list()
        self._init_obsidian_api()

    def _init_store(self):
        vault = self.cfg.get("obsidian_vault_path", "")
        if vault and Path(vault).exists():
            self.store = NotesStore(notes_dir=Path(vault))
            self._mode = "vault"
        else:
            self.store = NotesStore()
            self._mode = "builtin"

    def _init_obsidian_api(self):
        api_key = self.cfg.get("obsidian_api_key", "")
        api_url = self.cfg.get("obsidian_api_url", "http://127.0.0.1:27123")
        if api_key:
            self._obsidian_api = ObsidianAPI(api_url, api_key)
            def check():
                if self._obsidian_api and self._obsidian_api.is_available():
                    self._obsidian_status = "connected"
                else:
                    self._obsidian_status = "unreachable"
                self._update_status_label()
            threading.Thread(target=check, daemon=True).start()
        else:
            self._obsidian_status = "no API key"

    def _build_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        # ── Left sidebar: tree view ──────────────────
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(8, 8, 4, 8)
        sidebar_layout.setSpacing(4)

        # Header
        header = QHBoxLayout()
        title = QLabel("Notes")
        title.setObjectName("sectionTitle")
        header.addWidget(title)
        header.addStretch()
        self.vault_badge = QLabel("")
        self.vault_badge.setObjectName("subtitle")
        header.addWidget(self.vault_badge)
        sidebar_layout.addLayout(header)

        # Obsidian status row
        obs_row = QHBoxLayout()
        obs_row.setSpacing(4)
        self.obsidian_status_label = QLabel("")
        self.obsidian_status_label.setObjectName("subtitle")
        obs_row.addWidget(self.obsidian_status_label)
        obs_row.addStretch()

        set_vault_btn = QPushButton("Set Vault")
        set_vault_btn.setObjectName("secondary")
        set_vault_btn.setFixedHeight(20)
        set_vault_btn.setStyleSheet("font-size: 10px; padding: 1px 5px;")
        set_vault_btn.clicked.connect(self._set_vault_path)
        obs_row.addWidget(set_vault_btn)

        api_btn = QPushButton("API")
        api_btn.setObjectName("secondary")
        api_btn.setFixedHeight(20)
        api_btn.setStyleSheet("font-size: 10px; padding: 1px 5px;")
        api_btn.setToolTip("Configure Obsidian REST API")
        api_btn.clicked.connect(self._configure_api)
        obs_row.addWidget(api_btn)

        sidebar_layout.addLayout(obs_row)

        # Search
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search notes...")
        self.search_box.setClearButtonEnabled(True)
        self.search_box.textChanged.connect(self._on_search)
        sidebar_layout.addWidget(self.search_box)

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(3)
        self.btn_new = QPushButton("+ Note")
        self.btn_new.clicked.connect(self._new_note)
        self.btn_folder = QPushButton("+ Folder")
        self.btn_folder.setObjectName("secondary")
        self.btn_folder.clicked.connect(self._new_folder)
        btn_row.addWidget(self.btn_new)
        btn_row.addWidget(self.btn_folder)
        sidebar_layout.addLayout(btn_row)

        # Tree widget (replaces the old flat list)
        self.file_tree = QTreeWidget()
        self.file_tree.setHeaderHidden(True)
        self.file_tree.setIndentation(16)
        self.file_tree.setAnimated(True)
        self.file_tree.setExpandsOnDoubleClick(False)
        self.file_tree.setStyleSheet("""
            QTreeWidget {
                border: 1px solid palette(mid);
                border-radius: 4px;
                padding: 2px;
                outline: none;
            }
            QTreeWidget::item {
                padding: 2px 0;
            }
            QTreeWidget::branch:has-children:!has-siblings:closed,
            QTreeWidget::branch:closed:has-children:has-siblings {
                border-image: none;
                image: none;
            }
            QTreeWidget::branch:open:has-children:!has-siblings,
            QTreeWidget::branch:open:has-children:has-siblings {
                border-image: none;
                image: none;
            }
        """)
        self.file_tree.currentItemChanged.connect(self._on_tree_item_selected)
        self.file_tree.itemExpanded.connect(self._on_item_expanded)
        self.file_tree.itemCollapsed.connect(self._on_item_collapsed)
        sidebar_layout.addWidget(self.file_tree, 1)

        self.note_count_label = QLabel("0 notes")
        self.note_count_label.setObjectName("subtitle")
        sidebar_layout.addWidget(self.note_count_label)

        # ── Right side: editor ───────────────────────
        editor_widget = QWidget()
        editor_layout = QVBoxLayout(editor_widget)
        editor_layout.setContentsMargins(4, 8, 8, 8)
        editor_layout.setSpacing(4)

        title_row = QHBoxLayout()
        self.note_title_label = QLabel("Select or create a note")
        self.note_title_label.setObjectName("sectionTitle")
        title_row.addWidget(self.note_title_label, 1)

        self.btn_open_obsidian = QPushButton("Open in Obsidian")
        self.btn_open_obsidian.setObjectName("secondary")
        self.btn_open_obsidian.setToolTip("Open this note in the Obsidian app")
        self.btn_open_obsidian.clicked.connect(self._open_in_obsidian)
        self.btn_open_obsidian.setVisible(False)
        title_row.addWidget(self.btn_open_obsidian)

        self.btn_rename = QPushButton("Rename")
        self.btn_rename.setObjectName("secondary")
        self.btn_rename.clicked.connect(self._rename_note)
        self.btn_rename.setVisible(False)
        title_row.addWidget(self.btn_rename)

        self.btn_delete = QPushButton("Delete")
        self.btn_delete.setObjectName("destructive")
        self.btn_delete.clicked.connect(self._delete_note)
        self.btn_delete.setVisible(False)
        title_row.addWidget(self.btn_delete)

        self._preview_btn = QPushButton("\U0001f441 Preview")
        self._preview_btn.setObjectName("secondary")
        self._preview_btn.setFixedHeight(24)
        self._preview_btn.clicked.connect(self._toggle_preview)
        title_row.addWidget(self._preview_btn)

        editor_layout.addLayout(title_row)

        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine)
        editor_layout.addWidget(sep)
        
        self._preview = QTextBrowser()
        self._preview.setReadOnly(True)
        self._preview.setOpenExternalLinks(True)
        self._preview.setVisible(False)

        self.editor = QPlainTextEdit()
        self.editor.setPlaceholderText(
            "Start writing in Markdown...\n\nUse #tags anywhere in your text."
        )
        self.editor.setTabStopDistance(28.0)
        self.editor.textChanged.connect(self._on_text_changed)
        editor_layout.addWidget(self.editor, 1)
        editor_layout.addWidget(self._preview, 1)

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
        splitter.setSizes([240, 540])
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        layout.addWidget(splitter)
        self._update_status_label()

    # ── Tree building ──────────────────────────────────

    def _refresh_list(self, notes=None):
        """Rebuild the tree from the note store."""
        # Remember which folders were expanded
        self._save_expanded_state()

        self.file_tree.blockSignals(True)
        self.file_tree.clear()

        notes = notes or self.store.list_notes()
        tree = _build_tree_structure(notes)
        _populate_tree_widget(self.file_tree.invisibleRootItem(), tree, self._expanded_folders)

        # Expand root-level folders by default on first load
        if not self._expanded_folders:
            for i in range(self.file_tree.topLevelItemCount()):
                item = self.file_tree.topLevelItem(i)
                if item and item.data(0, Qt.ItemDataRole.UserRole) is None:
                    item.setExpanded(True)

        self.file_tree.blockSignals(False)
        self.note_count_label.setText(f"{len(notes)} note{'s' if len(notes) != 1 else ''}")

        # Re-select current note if still present
        if self.current_note_path:
            self._select_note_in_tree(self.current_note_path)

        # Reload the open note if its content changed on disk (external edit)
        self._reload_if_changed_on_disk()

    def _save_expanded_state(self):
        """Walk the tree and record which folder names are expanded."""
        self._expanded_folders.clear()
        self._walk_expanded(self.file_tree.invisibleRootItem())

    def _walk_expanded(self, parent):
        for i in range(parent.childCount()):
            child = parent.child(i)
            if child.data(0, Qt.ItemDataRole.UserRole) is None:  # folder
                folder_name = child.data(0, Qt.ItemDataRole.UserRole + 1)
                if child.isExpanded() and folder_name:
                    self._expanded_folders.add(folder_name)
                self._walk_expanded(child)

    def _on_item_expanded(self, item):
        folder_name = item.data(0, Qt.ItemDataRole.UserRole + 1)
        if folder_name:
            self._expanded_folders.add(folder_name)

    def _on_item_collapsed(self, item):
        folder_name = item.data(0, Qt.ItemDataRole.UserRole + 1)
        if folder_name:
            self._expanded_folders.discard(folder_name)

    def _select_note_in_tree(self, rel_path: str):
        """Find and select a note in the tree by its relative path."""
        self.file_tree.blockSignals(True)
        item = self._find_tree_item(self.file_tree.invisibleRootItem(), rel_path)
        if item:
            self.file_tree.setCurrentItem(item)
        self.file_tree.blockSignals(False)

    def _find_tree_item(self, parent, rel_path: str):
        for i in range(parent.childCount()):
            child = parent.child(i)
            if child.data(0, Qt.ItemDataRole.UserRole) == rel_path:
                return child
            # Recurse into folders
            if child.data(0, Qt.ItemDataRole.UserRole) is None:
                found = self._find_tree_item(child, rel_path)
                if found:
                    return found
        return None

    def _reload_if_changed_on_disk(self):
        """If the currently open note was modified externally, reload it."""
        if not self.current_note_path:
            return
        note = self.store.get_note(self.current_note_path)
        if not note:
            return
        current_text = self.editor.toPlainText()
        if note.content != current_text:
            self.editor.blockSignals(True)
            cursor_pos = self.editor.textCursor().position()
            self.editor.setPlainText(note.content)
            # Restore cursor position as close as possible
            cursor = self.editor.textCursor()
            cursor.setPosition(min(cursor_pos, len(note.content)))
            self.editor.setTextCursor(cursor)
            self.editor.blockSignals(False)
            self._update_footer(note)

    def set_palette(self, palette: dict):
        self._palette = palette
        # If currently in preview mode, re-render with new palette
        if self._preview_mode:
            self._render_preview()

    def _toggle_preview(self):
        self._preview_mode = not self._preview_mode
        if self._preview_mode:
            self.editor.setVisible(False)
            self._preview.setVisible(True)
            self._preview_btn.setText("\u270f Edit")
            self._render_preview()
        else:
            self._preview.setVisible(False)
            self.editor.setVisible(True)
            self._preview_btn.setText("\U0001f441 Preview")

    def _render_preview(self):
        try:
            import mistune
            md = mistune.create_markdown()
            html = md(self.editor.toPlainText())
        except ImportError:
            html = "<p><i>Install mistune for Markdown preview: pip install mistune</i></p>"
            html += "<pre>" + self.editor.toPlainText().replace("<", "&lt;") + "</pre>"

        bg = self._palette.get("bg", "#1e1e2e")
        fg = self._palette.get("fg", "#cdd6f4")
        surface = self._palette.get("surface", "#313244")
        accent = self._palette.get("accent", "#89b4fa")

        css = (
            f"<style>"
            f"body {{ background: {bg}; color: {fg}; font-family: sans-serif; padding: 12px; }}"
            f"code {{ background: {surface}; padding: 2px 4px; border-radius: 3px; }}"
            f"pre {{ background: {surface}; padding: 8px; border-radius: 4px; overflow-x: auto; }}"
            f"a {{ color: {accent}; }}"
            f"h1, h2, h3 {{ color: {fg}; }}"
            f"blockquote {{ border-left: 3px solid {accent}; padding-left: 8px; margin-left: 0; }}"
            f"</style>"
        )
        self._preview.setHtml(css + html)

    # ── Status labels ──────────────────────────────────

    def _update_status_label(self):
        if self._mode == "vault":
            vault_path = self.cfg.get("obsidian_vault_path", "")
            vault_name = Path(vault_path).name if vault_path else "?"
            self.vault_badge.setText(f"Vault: {vault_name}")
        else:
            self.vault_badge.setText("Built-in notes")
        self.obsidian_status_label.setText(f"API: {self._obsidian_status}")

    # ── Vault / API configuration ──────────────────────

    def _set_vault_path(self):
        current = self.cfg.get("obsidian_vault_path", "")
        path = QFileDialog.getExistingDirectory(
            self, "Select Obsidian Vault Folder", current,
        )
        if path:
            self.cfg["obsidian_vault_path"] = path
            self.cfg["obsidian_sync_enabled"] = True
            save_config(self.cfg)
            self._init_store()
            self._refresh_list()
            self._update_status_label()
            QMessageBox.information(
                self, "Vault Set",
                f"Obsidian vault set to:\n{path}\n\n"
                "Notes will now sync from this folder.",
            )

    def _configure_api(self):
        current_key = self.cfg.get("obsidian_api_key", "")
        current_url = self.cfg.get("obsidian_api_url", "http://127.0.0.1:27123")
        key, ok = QInputDialog.getText(
            self, "Obsidian REST API Key",
            "Enter the API key from the Obsidian Local REST API plugin:\n"
            "(Leave blank to disable API integration)",
            text=current_key,
        )
        if ok:
            url, ok2 = QInputDialog.getText(
                self, "Obsidian REST API URL",
                "API base URL (default: http://127.0.0.1:27123):",
                text=current_url,
            )
            if ok2:
                self.cfg["obsidian_api_key"] = key.strip()
                self.cfg["obsidian_api_url"] = url.strip() or "http://127.0.0.1:27123"
                save_config(self.cfg)
                self._init_obsidian_api()
                self._update_status_label()

    def _create_via_api(self):
        if not self._obsidian_api:
            QMessageBox.warning(self, "No API", "Obsidian REST API not configured.")
            return
        name, ok = QInputDialog.getText(self, "Create via API", "Note name (without .md):")
        if ok and name.strip():
            path = f"{name.strip()}.md"
            content = f"# {name.strip()}\n\n"
            if self._obsidian_api.create_note(path, content):
                self._refresh_list()
                QMessageBox.information(self, "Created", f"Note '{path}' created via API.")
            else:
                QMessageBox.warning(self, "Failed", "Could not create note via API.")

    def _open_in_obsidian(self):
        """Open the current note in Obsidian via obsidian:// URI scheme."""
        if not self.current_note_path:
            return
        vault_path = self.cfg.get("obsidian_vault_path", "")
        vault_name = Path(vault_path).name if vault_path else ""
        if not vault_name:
            QMessageBox.warning(self, "No Vault", "Set an Obsidian vault path first.")
            return
        # Strip .md extension — Obsidian URI expects path without it
        note_path = self.current_note_path
        if note_path.endswith(".md"):
            note_path = note_path[:-3]
        # URL-encode vault name and file path for special characters
        encoded_vault = urllib.parse.quote(vault_name, safe="")
        encoded_file = urllib.parse.quote(note_path, safe="/")
        uri = f"obsidian://open?vault={encoded_vault}&file={encoded_file}"
        try:
            if sys.platform == "win32":
                os.startfile(uri)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", uri])
            else:
                subprocess.Popen(["xdg-open", uri])
        except Exception as e:
            logger.warning(f"Failed to open Obsidian: {e}")
            QMessageBox.warning(self, "Error", f"Could not open Obsidian:\n{e}")

    # ── Search ─────────────────────────────────────────

    def _on_search(self, query: str):
        if query.strip():
            self._refresh_list(self.store.search(query))
        else:
            self._refresh_list()

    # ── Note selection ─────────────────────────────────

    def _on_tree_item_selected(self, current, _prev):
        self._save_current()
        if current is None:
            self._clear_editor()
            return
        rel_path = current.data(0, Qt.ItemDataRole.UserRole)
        if rel_path is None:
            # Folder clicked — toggle expand
            current.setExpanded(not current.isExpanded())
            return
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
            self.btn_open_obsidian.setVisible(self._mode == "vault")

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
        self.btn_open_obsidian.setVisible(False)
        # Reset preview mode if active
        if self._preview_mode:
            self._preview_mode = False
            self._preview.setVisible(False)
            self.editor.setVisible(True)
            self._preview_btn.setText("\U0001f441 Preview")

    # ── Editing ────────────────────────────────────────

    def _on_text_changed(self):
        self._save_timer.start()
        text = self.editor.toPlainText()
        words = len(text.split()) if text.strip() else 0
        self.word_count_label.setText(f"{words} words | {len(text)} chars")

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
            rel = PurePosixPath(f"{safe_name}.md")
            note = Note(title=safe_name, content="", path=rel)
            self.store.save_note(note)
            self._refresh_list()
            self._select_note_in_tree(str(rel))

    def _new_folder(self):
        name, ok = QInputDialog.getText(self, "New Folder", "Folder name:")
        if ok and name.strip():
            safe_name = name.strip().replace("/", "-").replace("\\", "-")
            folder_path = self.store.root / safe_name
            folder_path.mkdir(parents=True, exist_ok=True)
            note_name, ok2 = QInputDialog.getText(
                self, "First Note", f"Note name in '{safe_name}/' (without .md):",
            )
            if ok2 and note_name.strip():
                safe_note = note_name.strip().replace("/", "-").replace("\\", "-")
                rel = PurePosixPath(safe_name) / f"{safe_note}.md"
                note = Note(title=safe_note, content="", path=rel)
                self.store.save_note(note)
                self._expanded_folders.add(safe_name)
                self._refresh_list()
                self._select_note_in_tree(str(rel))
            else:
                self._refresh_list()

    def _rename_note(self):
        if self.current_note_path is None:
            return
        old_path = PurePosixPath(self.current_note_path)
        current_name = old_path.stem
        new_name, ok = QInputDialog.getText(
            self, "Rename Note", "New name (without .md):", text=current_name,
        )
        if ok and new_name.strip() and new_name.strip() != current_name:
            safe_name = new_name.strip().replace("/", "-").replace("\\", "-")
            new_rel = old_path.parent / f"{safe_name}.md"
            note = self.store.get_note(self.current_note_path)
            if note:
                content = note.content
                # Record old path deletion BEFORE unlinking so sync won't re-create it
                old_posix = str(PurePosixPath(self.current_note_path))
                if self._mode == "vault":
                    _record_vault_deletion(old_posix)
                self.store.delete_note(self.current_note_path)
                new_note = Note(title=safe_name, content=content, path=new_rel, tags=note.tags)
                self.store.save_note(new_note)
                self.current_note_path = str(new_rel)
                self.note_title_label.setText(safe_name)
                self._refresh_list()
                self._select_note_in_tree(str(new_rel))

    def _delete_note(self):
        if self.current_note_path is None:
            return
        reply = QMessageBox.question(
            self, "Delete Note",
            f"Permanently delete '{self.current_note_path}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            # Record deletion in manifest BEFORE unlinking so sync won't re-create
            del_posix = str(PurePosixPath(self.current_note_path))
            if self._mode == "vault":
                _record_vault_deletion(del_posix)
            self.store.delete_note(self.current_note_path)
            self._clear_editor()
            self._refresh_list()