#!/usr/bin/env python3
"""LocalSync — Personal productivity desktop app.

Entry point: initializes the database, starts the Qt application,
launches sync engine and vault watcher, and displays the main window.
"""

import logging
import sys

from PyQt6.QtWidgets import QApplication

from src.data.database import init_db
from src.config import load_config
from src.ui.main_window import MainWindow
from src.sync.engine import SyncEngine
from src.sync.vault_watcher import VaultWatcher


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    # Initialize database
    init_db()

    app = QApplication(sys.argv)
    app.setApplicationName("LocalSync")

    window = MainWindow()
    window.show()

    # Start background sync if enabled
    cfg = load_config()
    sync_engine = None
    vault_watcher = None
    if cfg.get("sync_enabled", True):
        sync_engine = SyncEngine()
        window.set_sync_engine(sync_engine)
        sync_engine.start()

        # Start vault watcher — detects Obsidian edits and pushes to peers
        vault_watcher = VaultWatcher()
        vault_watcher.vault_changed.connect(sync_engine.trigger_vault_sync)
        vault_watcher.vault_changed.connect(window._on_sync_completed)
        vault_watcher.start()

    exit_code = app.exec()

    # Clean shutdown
    if vault_watcher:
        vault_watcher.stop()
        vault_watcher.wait(3000)
    if sync_engine:
        sync_engine.stop()
        sync_engine.wait(5000)

    return exit_code


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        import traceback
        try:
            from PyQt6.QtWidgets import QApplication, QMessageBox
            app = QApplication.instance() or QApplication(sys.argv)
            QMessageBox.critical(None, "Fatal Error", traceback.format_exc())
        except Exception:
            print(traceback.format_exc())
        sys.exit(1)