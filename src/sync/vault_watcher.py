"""Filesystem watcher for Obsidian vault — detects local edits and triggers sync.

Uses a polling approach (no inotify dependency) to watch for .md file changes
in the configured vault directory. When changes are detected, emits a signal
so the sync engine can broadcast them to peers.

Sync-safety features:
  • 10-second poll interval — relaxed for a personal two-machine setup.
  • Deletion debounce — a file must be absent for 5 consecutive polls (~50 s)
    before its deletion is recorded.  This prevents Obsidian's atomic-save
    behaviour (delete + recreate within milliseconds) from being misread as a
    real deletion.
  • Content-hash guard — when a pending-deletion file disappears, its MD5 hash
    (or size as fallback) is stored.  If a new file appears with the same hash
    during the debounce window, the deletion is treated as a rename/move and
    is not recorded in the manifest.
  • Sync-write guard — when the engine writes a vault file it calls
    mark_sync_written(); the watcher skips that path for the next poll cycle
    so it does not re-trigger a sync for data that arrived from a peer.
  • Quiet-period gate — vault_changed is only emitted after two full polls with
    no new activity.  Rapid sequences (move = delete + create) are collapsed
    into a single signal.
  • Move detection — if a pending-deletion's content hash or file size matches
    a newly appeared file in the same poll cycle the operation is treated as a
    rename and the deletion manifest entry is suppressed.
"""

import hashlib
import logging
import threading
import time
from pathlib import Path, PurePosixPath

from PyQt6.QtCore import QThread, pyqtSignal

from src.config import load_config
from src.sync.deletion_manifest import record_deletion, read_manifest

logger = logging.getLogger(__name__)

# ── Tuning constants ────────────────────────────────────────────────────────
POLL_INTERVAL          = 10  # seconds between each vault scan
DELETION_CONFIRM_POLLS = 5   # polls a file must be absent before deletion confirmed (~50 s)
QUIET_POLLS_BEFORE_EMIT = 2  # polls of silence required before emitting vault_changed


# ── Sync-write guard (module-level so engine.py can call without a reference) ─
_sync_written: set[str] = set()
_sync_written_lock = threading.Lock()


def mark_sync_written(rel_posix: str) -> None:
    """Register a vault-relative path that the sync engine just wrote to disk.

    The watcher will ignore this path for the next poll cycle so that incoming
    peer data does not immediately re-trigger a sync.  Call from any thread.
    """
    with _sync_written_lock:
        _sync_written.add(rel_posix)


def _pop_sync_written() -> set[str]:
    """Drain and return the current sync-written set (called once per poll)."""
    with _sync_written_lock:
        result = set(_sync_written)
        _sync_written.clear()
        return result


def _md5_file(path: Path) -> str | None:
    """Compute MD5 hex digest of a file, or None if unreadable."""
    try:
        h = hashlib.md5()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
    except OSError:
        return None


# ── Watcher thread ──────────────────────────────────────────────────────────

class VaultWatcher(QThread):
    """Polls the Obsidian vault for file changes and signals when detected."""

    # Emitted when vault files have changed (added, modified, or deleted)
    vault_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._running = True

        # rel_posix -> (mtime, size)
        self._snapshot: dict[str, tuple[float, int]] = {}

        # rel_posix -> md5 hex digest, refreshed lazily when a file is new
        # or has changed.  Persists across polls so that move-detection can
        # still match a file's hash after it disappears.
        self._hash_cache: dict[str, str] = {}

        self._vault_path: Path | None = None

        # Deletion debounce: rel_posix -> number of polls the file has been absent
        self._pending_deletions: dict[str, int] = {}
        # Size of the file when it was last seen (for move detection fallback)
        self._pending_deletion_sizes: dict[str, int] = {}
        # MD5 hash of the file when it was last seen (for move detection)
        self._pending_deletion_hashes: dict[str, str] = {}

        # Quiet-period state
        self._changes_pending: bool = False  # we have unsent changes
        self._quiet_polls: int = 0           # polls since last new-change detection

        self._load_vault_path()

    # ── Config ───────────────────────────────────────────────────────────────

    def _load_vault_path(self) -> None:
        cfg = load_config()
        vault = cfg.get("obsidian_vault_path", "")
        if vault and Path(vault).is_dir():
            self._vault_path = Path(vault)
        else:
            self._vault_path = None

    def reload_config(self) -> None:
        """Reload vault path from config (called after settings change)."""
        self._load_vault_path()
        self._snapshot.clear()
        self._hash_cache.clear()
        self._pending_deletions.clear()
        self._pending_deletion_sizes.clear()
        self._pending_deletion_hashes.clear()
        self._changes_pending = False
        self._quiet_polls = 0
        if self._vault_path:
            self._snapshot = self._scan_vault()
            self._refresh_hash_cache(self._snapshot)

    # ── Vault scanning ───────────────────────────────────────────────────────

    def _scan_vault(self) -> dict[str, tuple[float, int]]:
        """Return {posix_relative_path: (mtime, size)} for all visible .md files."""
        if not self._vault_path or not self._vault_path.is_dir():
            return {}
        result: dict[str, tuple[float, int]] = {}
        try:
            for md in self._vault_path.rglob("*.md"):
                rel = md.relative_to(self._vault_path)
                # Skip hidden dirs (.obsidian, .trash, etc.)
                if any(p.startswith(".") for p in rel.parts):
                    continue
                rel_posix = str(PurePosixPath(rel))
                try:
                    st = md.stat()
                    result[rel_posix] = (st.st_mtime, st.st_size)
                except OSError:
                    pass
        except OSError as e:
            logger.warning(f"Vault scan error: {e}")
        return result

    def _refresh_hash_cache(
        self,
        current: dict[str, tuple[float, int]],
    ) -> None:
        """Keep ``self._hash_cache`` in sync with ``current``.

        Hashes are computed lazily — only for files that are new in this poll
        or whose mtime/size has changed since the last poll.  Files that
        disappear keep their hash in the cache so that move-detection can
        match them against newly appeared files in the *same* poll cycle.
        """
        if not self._vault_path:
            return
        for path, (mtime, size) in current.items():
            prev_meta = self._snapshot.get(path)
            if prev_meta is not None and prev_meta == (mtime, size):
                # Unchanged since last poll — re-use cached hash if we have one
                continue
            full = self._vault_path / Path(path)
            h    = _md5_file(full)
            if h is not None:
                self._hash_cache[path] = h
        # Drop hashes for files that have been gone long enough that we no
        # longer have a pending-deletion entry tracking them
        live_or_pending = set(current.keys()) | set(self._pending_deletions.keys())
        for stale in list(self._hash_cache.keys()):
            if stale not in live_or_pending:
                self._hash_cache.pop(stale, None)

    # ── Main thread loop ─────────────────────────────────────────────────────

    def run(self) -> None:
        logger.info("Vault watcher started")

        if self._vault_path:
            self._snapshot = self._scan_vault()
            logger.info(
                f"Watching vault: {self._vault_path}  "
                f"({len(self._snapshot)} files)"
            )
        else:
            logger.info("No vault configured, watcher idle")

        while self._running:
            if self._vault_path and self._vault_path.is_dir():
                self._poll()
            else:
                # Re-check config periodically in case vault is set later
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

    # ── Poll logic ───────────────────────────────────────────────────────────

    def _poll(self) -> None:
        """One full poll cycle: detect changes, debounce, maybe emit."""
        current  = self._scan_vault()
        skip_set = _pop_sync_written()   # paths the engine just wrote — ignore

        # Refresh the hash cache *first* — cheap for unchanged files, and
        # ensures we have a hash for every live path before we start
        # processing disappearances.
        self._refresh_hash_cache(current)

        new_activity_this_poll = False   # did we find anything new *this* poll?

        # ── 1. New / modified files ─────────────────────────────────────────
        # Track sizes and hashes of genuinely new files for move detection later.
        new_file_sizes: set[int] = set()
        new_file_hashes: set[str] = set()

        for path, (mtime, size) in current.items():
            if path in skip_set:
                # Written by the sync engine — don't react to our own writes
                continue

            prev = self._snapshot.get(path)
            if prev is None:
                # File is brand-new (or re-appeared after a move)
                new_file_sizes.add(size)
                h = self._hash_cache.get(path)
                if h:
                    new_file_hashes.add(h)
                new_activity_this_poll = True
                logger.debug(f"New file detected: {path}")
            elif mtime > prev[0]:
                # File was modified
                new_activity_this_poll = True
                logger.debug(f"Modified file: {path}")

        # ── 2. Deletion debounce ────────────────────────────────────────────
        gone_now = set(self._snapshot.keys()) - set(current.keys())

        # Files that came back this poll (Obsidian atomic save — ignore them)
        returned = set(self._pending_deletions.keys()) & set(current.keys())
        for path in returned:
            logger.debug(
                f"'{path}' reappeared after being absent — "
                "likely an atomic save, clearing pending deletion"
            )
            self._pending_deletions.pop(path, None)
            self._pending_deletion_sizes.pop(path, None)
            self._pending_deletion_hashes.pop(path, None)

        # Increment absence counter for files still gone
        for path in gone_now:
            # AIRTIGHT: skip_set check BEFORE incrementing counter
            if path in skip_set:
                # Engine deleted it as part of a remote deletion — ignore
                self._pending_deletions.pop(path, None)
                self._pending_deletion_sizes.pop(path, None)
                self._pending_deletion_hashes.pop(path, None)
                continue

            count = self._pending_deletions.get(path, 0) + 1
            self._pending_deletions[path] = count

            # Cache the file's last known size for the move-detection fallback
            if path not in self._pending_deletion_sizes and path in self._snapshot:
                self._pending_deletion_sizes[path] = self._snapshot[path][1]

            # Pull the *previously* computed hash from the cache.  The old code
            # tried to re-hash the file here, but at this point it is already
            # gone from disk so the hash always came back None.
            if path not in self._pending_deletion_hashes:
                cached = self._hash_cache.get(path)
                if cached:
                    self._pending_deletion_hashes[path] = cached

            logger.debug(f"'{path}' absent for {count} poll(s) (confirm at {DELETION_CONFIRM_POLLS})")

        # ── 3. Confirm deletions that have been gone long enough ────────────
        for path in list(self._pending_deletions.keys()):
            if path in current:
                continue  # came back — handled above
            if self._pending_deletions[path] < DELETION_CONFIRM_POLLS:
                continue  # not yet confirmed

            # ── Move detection (content hash + size fallback) ──────────────
            del_hash = self._pending_deletion_hashes.get(path)
            del_size = self._pending_deletion_sizes.get(path)

            is_move = False
            if del_hash and del_hash in new_file_hashes:
                is_move = True
            elif del_size is not None and del_size in new_file_sizes:
                is_move = True

            if is_move:
                logger.info(
                    f"Move detected: '{path}' disappeared but a new file with "
                    f"matching content appeared — skipping deletion record"
                )
            else:
                # Genuine deletion — record in manifest and flag as changed
                if self._vault_path:
                    existing_paths = {d["path"] for d in read_manifest(self._vault_path)}
                    if path not in existing_paths:
                        record_deletion(path, self._vault_path)
                        logger.info(f"Confirmed deletion recorded: {path}")
                new_activity_this_poll = True

            # Clean up tracking dicts
            self._pending_deletions.pop(path)
            self._pending_deletion_sizes.pop(path, None)
            self._pending_deletion_hashes.pop(path, None)

        # ── 4. Quiet-period gate ────────────────────────────────────────────
        if new_activity_this_poll:
            self._changes_pending = True
            self._quiet_polls = 0          # reset — we're still seeing changes
        elif self._changes_pending:
            self._quiet_polls += 1         # one more quiet poll
            if self._quiet_polls >= QUIET_POLLS_BEFORE_EMIT:
                logger.info(
                    "Vault stable — emitting vault_changed "
                    f"(quiet for {self._quiet_polls} poll(s))"
                )
                self._changes_pending = False
                self._quiet_polls = 0
                self.vault_changed.emit()

        # ── 5. Advance snapshot ─────────────────────────────────────────────
        self._snapshot = current

    # ── Lifecycle ────────────────────────────────────────────────────────────

    def stop(self) -> None:
        self._running = False