"""Filesystem watcher for Obsidian vault — detects local edits and triggers sync.

Uses a polling approach (no inotify dependency) to watch for .md file changes
in the configured vault directory. When changes are detected, emits a signal
so the sync engine can broadcast them to peers.
"""

import logging
import time
from pathlib import Path, PurePosixPath

from PyQt6.QtCore import QThread, pyqtSignal

from src.config import load_config
from src.sync.deletion_manifest import record_deletion, read_manifest

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
        """Build a dict of {posix_relative_path: mtime} for all .md files in vault.

        Always uses forward slashes so Windows/Linux snapshots are comparable.
        """
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
                # Normalize to forward slashes
                rel_posix = str(PurePosixPath(rel))
                try:
                    result[rel_posix] = md.stat().st_mtime
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
                    # Record any deletions before updating the snapshot
                    self._record_deletions(current)
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

    def _record_deletions(self, current: dict[str, float]):
        """When files disappear from the vault, record them in the deletion manifest.

        Uses the shared deletion_manifest module. Skips paths already recorded
        (e.g. by the UI doing an immediate delete/rename).
        """
        if not self._vault_path:
            return
        deleted = set(self._snapshot.keys()) - set(current.keys())
        if not deleted:
            return

        # Read manifest once to check what's already recorded
        existing_paths = {d["path"] for d in read_manifest(self._vault_path)}

        for path in deleted:
            if path not in existing_paths:
                record_deletion(path, self._vault_path)

    def stop(self):
        self._running = False
