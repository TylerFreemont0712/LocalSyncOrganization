"""File-based notes storage — Obsidian-compatible markdown files."""

import re
from dataclasses import dataclass, field
from pathlib import Path

from src.config import load_config


@dataclass
class Note:
    title: str
    content: str
    path: Path  # Relative path within notes dir
    tags: list[str] = field(default_factory=list)

    @property
    def filename(self) -> str:
        return self.path.name


class NotesStore:
    """Manages markdown notes on disk in an Obsidian-compatible folder layout."""

    def __init__(self, notes_dir: Path | None = None):
        cfg = load_config()
        self.root = notes_dir or Path(cfg["notes_dir"])
        self.root.mkdir(parents=True, exist_ok=True)

    def list_notes(self) -> list[Note]:
        """List all .md files under the notes directory."""
        notes = []
        for md_file in sorted(self.root.rglob("*.md")):
            notes.append(self._load_note(md_file))
        return notes

    def get_note(self, rel_path: str) -> Note | None:
        full = self.root / rel_path
        if full.exists():
            return self._load_note(full)
        return None

    def save_note(self, note: Note):
        full = self.root / note.path
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(note.content, encoding="utf-8")

    def delete_note(self, rel_path: str):
        full = self.root / rel_path
        if full.exists():
            full.unlink()

    def search(self, query: str) -> list[Note]:
        """Simple case-insensitive search across titles and content."""
        query_lower = query.lower()
        results = []
        for note in self.list_notes():
            if (query_lower in note.title.lower()
                    or query_lower in note.content.lower()
                    or any(query_lower in t.lower() for t in note.tags)):
                results.append(note)
        return results

    def _load_note(self, full_path: Path) -> Note:
        content = full_path.read_text(encoding="utf-8")
        tags = self._extract_tags(content)
        title = full_path.stem
        rel = full_path.relative_to(self.root)
        return Note(title=title, content=content, path=rel, tags=tags)

    @staticmethod
    def _extract_tags(content: str) -> list[str]:
        """Extract #tags from markdown content."""
        # Match #tag but not inside code blocks or headings
        return list(set(re.findall(r'(?<!\w)#([a-zA-Z0-9_/-]+)', content)))
