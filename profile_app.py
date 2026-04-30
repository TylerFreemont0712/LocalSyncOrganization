import cProfile
import pstats
import sys
import time

def main():
    p = cProfile.Profile()
    p.enable()
    
    # Run the app for a few seconds
    from src.data.database import init_db
    from src.config import load_config
    from src.ui.main_window import MainWindow
    from src.sync.engine import SyncEngine
    from src.sync.vault_watcher import VaultWatcher
    
    init_db()
    
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    cfg = load_config()
    sync_engine = SyncEngine()
    window.set_sync_engine(sync_engine)
    sync_engine.start()
    
    vault_watcher = VaultWatcher()
    vault_watcher.vault_changed.connect(sync_engine.trigger_vault_sync)
    vault_watcher.vault_changed.connect(window._on_sync_completed)
    vault_watcher.start()
    
    time.sleep(5)  # Let it run for 5 seconds
    
    p.disable()
    
    s = pstats.Stats(p)
    s.sort_stats('cumtime')
    s.print_stats(30)
    
    return app.exec()

if __name__ == "__main__":
    main()
