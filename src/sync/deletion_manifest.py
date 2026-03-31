"""Shared deletion manifest utilities for vault sync.

Both the VaultWatcher (polling) and the UI (immediate delete/rename) need to
record deletions in `.localsync_deletions.json`. This module centralizes that
logic so there's one source of truth.
"""

import json
import logging
import time
from pathlib import Path

from src.config import load_config

logger = logging.getLogger(__name__)

MANIFEST_FILENAME = ".localsync_deletions.json"
RETENTION_DAYS = 30


def get_vault_path() -> Path | None:
    """Return the configured vault path, or None."""
    cfg = load_config()
    vault = cfg.get("obsidian_vault_path", "")
    if vault and Path(vault).is_dir():
        return Path(vault)
    return None


def _manifest_path(vault: Path) -> Path:
    return vault / MANIFEST_FILENAME


def read_manifest(vault: Path) -> list[dict]:
    mp = _manifest_path(vault)
    if mp.exists():
        try:
            data = json.loads(mp.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except Exception:
            return []
    return []


def write_manifest(vault: Path, entries: list[dict]):
    mp = _manifest_path(vault)
    try:
        mp.write_text(json.dumps(entries, indent=2), encoding="utf-8")
    except OSError as e:
        logger.warning(f"Failed to write deletion manifest: {e}")


def record_deletion(rel_posix: str, vault: Path | None = None):
    """Immediately record a file deletion in the vault manifest.

    Safe to call from any thread. If vault is None, reads from config.
    Includes both deleted_at (legacy) and deleted_at_ts (float unix timestamp)
    so engine.py LWW comparisons work.
    """
    if vault is None:
        vault = get_vault_path()
    if vault is None:
        return

    entries = read_manifest(vault)
    existing_paths = {d["path"] for d in entries}
    now = time.time()

    if rel_posix not in existing_paths:
        entries.append({
            "path": rel_posix,
            "deleted_at": now,
            "deleted_at_ts": now,
        })
        logger.info(f"Recorded vault deletion: {rel_posix}")

    # Prune old entries
    cutoff = now - (RETENTION_DAYS * 86400)
    entries = [d for d in entries if d.get("deleted_at", 0) > cutoff]

    write_manifest(vault, entries)


def is_deleted(rel_posix: str, vault: Path | None = None) -> bool:
    """Check if a path is in the deletion manifest."""
    if vault is None:
        vault = get_vault_path()
    if vault is None:
        return False
    entries = read_manifest(vault)
    return any(d["path"] == rel_posix for d in entries)


def remove_deletion(rel_posix: str, vault: Path | None = None):
    """Remove a path from the deletion manifest (file re-created)."""
    if vault is None:
        vault = get_vault_path()
    if vault is None:
        return
    entries = read_manifest(vault)
    entries = [d for d in entries if d["path"] != rel_posix]
    write_manifest(vault, entries)