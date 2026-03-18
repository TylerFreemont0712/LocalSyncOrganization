"""Filesystem watcher for Obsidian vault — detects local edits and triggers sync.

Uses a polling approach (no inotify dependency) to watch for .md file changes
in the configured vault directory. When changes are detected, emits a signal
so the sync engine can broadcast them to peers.
"""

import logging
import time
from pathlib import Path

from PyQt6.QtCore import QThread, pyqtSignal

from src.config import load_config

logger = logging.getLogger(__name__)

# How often to poll the vault directory for changes (seconds)
POLL_INTERVAL = 3


class VaultWatcher(QThread):
    """Polls the Obsidian vault for file changes and signals when detected."""

    # Emitted when vault files have changed (added, modified, or deleted)
    vault_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._running = True
        self._snapshot: dict[str, float] = {}  # rel_path -> mtime
        self._vault_path: Path | None = None
        self._load_vault_path()

    def _load_vault_path(self):
        cfg = load_config()
        vault = cfg.get("obsidian_vault_path", "")
        if vault and Path(vault).is_dir():
            self._vault_path = Path(vault)
        else:
            self._vault_path = None

    def reload_config(self):
        """Reload vault path from config (called after settings change)."""
        self._load_vault_path()
        self._snapshot.clear()
        if self._vault_path:
            self._snapshot = self._scan_vault()

    def _scan_vault(self) -> dict[str, float]:
        """Build a dict of {relative_path: mtime} for all .md files in vault."""
        if not self._vault_path or not self._vault_path.is_dir():
            return {}
        result = {}
        try:
            for md in self._vault_path.rglob("*.md"):
                # Skip hidden dirs like .obsidian, .trash
                rel = md.relative_to(self._vault_path)
                parts = rel.parts
                if any(p.startswith(".") for p in parts):
                    continue
                try:
                    result[str(rel)] = md.stat().st_mtime
                except OSError:
                    pass
        except OSError as e:
            logger.warning(f"Vault scan error: {e}")
        return result

    def run(self):
        logger.info("Vault watcher started")

        # Take initial snapshot
        if self._vault_path:
            self._snapshot = self._scan_vault()
            logger.info(f"Watching vault: {self._vault_path} ({len(self._snapshot)} files)")
        else:
            logger.info("No vault configured, watcher idle")

        while self._running:
            if self._vault_path and self._vault_path.is_dir():
                current = self._scan_vault()
                if self._has_changes(current):
                    logger.info("Vault changes detected, triggering sync")
                    self._snapshot = current
                    self.vault_changed.emit()
                else:
                    self._snapshot = current
            else:
                # Re-check config periodically in case vault was set
                self._load_vault_path()
                if self._vault_path:
                    self._snapshot = self._scan_vault()
                    logger.info(f"Vault now configured: {self._vault_path}")

            # Interruptible sleep
            for _ in range(POLL_INTERVAL):
                if not self._running:
                    break
                time.sleep(1)

        logger.info("Vault watcher stopped")

    def _has_changes(self, current: dict[str, float]) -> bool:
        """Compare current scan against previous snapshot."""
        # New or modified files
        for path, mtime in current.items():
            prev_mtime = self._snapshot.get(path)
            if prev_mtime is None or mtime > prev_mtime:
                return True
        # Deleted files
        for path in self._snapshot:
            if path not in current:
                return True
        return False

    def stop(self):
        self._running = False
