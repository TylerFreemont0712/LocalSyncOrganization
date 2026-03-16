#!/usr/bin/env python3
"""LocalSync — Personal productivity app entry point."""

import logging
import sys

from PyQt6.QtWidgets import QApplication

from src.data.database import init_db
from src.config import load_config
from src.ui.main_window import MainWindow
from src.sync.engine import SyncEngine


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
    if cfg.get("sync_enabled", True):
        sync_engine = SyncEngine()
        sync_engine.status_changed.connect(window.set_sync_status)
        sync_engine.start()

    exit_code = app.exec()

    # Clean shutdown
    if sync_engine:
        sync_engine.stop()
        sync_engine.wait(5000)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
