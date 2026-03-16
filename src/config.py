"""App-wide configuration and paths."""

import json
import platform
from pathlib import Path


APP_NAME = "LocalSync"
APP_VERSION = "0.2.0"

# Cross-platform data directory
if platform.system() == "Windows":
    _base = Path.home() / "AppData" / "Local" / APP_NAME
else:
    _base = Path.home() / ".local" / "share" / APP_NAME

DATA_DIR = _base / "data"
NOTES_DIR = DATA_DIR / "notes"
DB_PATH = DATA_DIR / "localsync.db"
CONFIG_PATH = _base / "config.json"
SYNC_LOG_PATH = _base / "sync.log"

# Ensure directories exist
for d in [DATA_DIR, NOTES_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Default settings
DEFAULTS = {
    "theme": "Catppuccin Dark",
    # Sync
    "sync_enabled": True,
    "sync_interval_seconds": 300,  # 5 minutes
    "sync_port": 42069,
    "discovery_port": 42070,
    "subnet": "192.168.0",          # /24 subnet prefix to scan
    "known_peers": [],               # Manually pinned peer IPs
    "scan_range_start": 1,
    "scan_range_end": 254,
    "scan_threads": 20,              # Parallel ping threads
    "scan_timeout_ms": 150,          # Per-host TCP probe timeout
    # Data
    "notes_dir": str(NOTES_DIR),
}


def load_config() -> dict:
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            saved = json.load(f)
        return {**DEFAULTS, **saved}
    return dict(DEFAULTS)


def save_config(cfg: dict):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
