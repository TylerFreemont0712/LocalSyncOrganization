# 📘 Repository Context Document

This document contains the full context of the repository, formatted for optimal LLM consumption.

## 📑 Document Structure
1. File Tree
2. Project Summary
3. Dependency Graph
4. Docstring Summary
5. Full File Contents

---

## 📁 File Tree
```
- main.pyw
  - __init__.py
  - config.py
    - __init__.py
    - activity_store.py
    - calendar_store.py
    - database.py
    - finance_store.py
    - holidays_jp.py
    - notes_store.py
    - todo_store.py
    - __init__.py
    - deletion_manifest.py
    - engine.py
    - vault_watcher.py
    - __init__.py
    - main_window.py
      - __init__.py
      - activity_panel.py
      - calendar_panel.py
      - dashboard_panel.py
      - finance_charts.py
      - finance_panel.py
      - notes_panel.py
      - todo_panel.py
      - __init__.py
      - styles.py
      - __init__.py
      - network_dialog.py
    - __init__.py
    - paths.py
    - timestamps.py
  - __init__.py
```

## 📊 Project Summary
- Total Python files: **33**
- Total lines of code: **7415**

## 🔗 Dependency Graph
### main.pyw
- logging
- sys
- PyQt6.QtWidgets
- src.data.database
- src.config
- src.ui.main_window
- src.sync.engine
- src.sync.vault_watcher

### src\__init__.py
- src.config

### src\config.py
- json
- platform
- pathlib

### src\data\__init__.py
- src.data.database
- src.data.notes_store
- src.data.calendar_store
- src.data.finance_store
- src.data.todo_store

### src\data\activity_store.py
- uuid
- dataclasses
- src.data.database
- src.utils.timestamps

### src\data\calendar_store.py
- uuid
- dataclasses
- datetime
- src.data.database
- src.utils.timestamps

### src\data\database.py
- sqlite3
- pathlib
- src.config

### src\data\finance_store.py
- uuid
- dataclasses
- src.data.database
- src.utils.timestamps

### src\data\holidays_jp.py
- datetime

### src\data\notes_store.py
- re
- dataclasses
- pathlib
- src.config

### src\data\todo_store.py
- uuid
- dataclasses
- src.data.database
- src.utils.timestamps

### src\sync\__init__.py
- src.sync.engine

### src\sync\deletion_manifest.py
- json
- logging
- time
- pathlib
- src.config

### src\sync\engine.py
- json
- logging
- socket
- struct
- threading
- time
- concurrent.futures
- pathlib
- PyQt6.QtCore
- src.config
- src.data.database
- src.utils.timestamps
- src.sync.deletion_manifest

### src\sync\vault_watcher.py
- logging
- time
- pathlib
- PyQt6.QtCore
- src.config
- src.sync.deletion_manifest

### src\ui\__init__.py
- src.ui.main_window

### src\ui\main_window.py
- datetime
- PyQt6.QtCore
- PyQt6.QtGui
- PyQt6.QtWidgets
- src.config
- src.ui.themes.styles
- src.ui.modules.notes_panel
- src.ui.modules.calendar_panel
- src.ui.modules.finance_panel
- src.ui.modules.todo_panel
- src.ui.modules.dashboard_panel
- src.ui.modules.finance_charts
- src.ui.modules.activity_panel
- src.ui.widgets.network_dialog
- PyQt6.QtWidgets

### src\ui\modules\__init__.py
- src.ui.modules.notes_panel
- src.ui.modules.calendar_panel
- src.ui.modules.finance_panel

### src\ui\modules\activity_panel.py
- datetime
- pathlib
- PyQt6.QtCore
- PyQt6.QtGui
- PyQt6.QtWidgets
- src.config
- src.data.activity_store

### src\ui\modules\calendar_panel.py
- datetime
- calendar
- PyQt6.QtCore
- PyQt6.QtWidgets
- src.data.calendar_store
- PyQt6.QtCore

### src\ui\modules\dashboard_panel.py
- datetime
- PyQt6.QtCore
- PyQt6.QtWidgets
- src.data.todo_store
- src.data.calendar_store
- src.data.finance_store

### src\ui\modules\finance_charts.py
- calendar
- datetime
- math
- PyQt6.QtCore
- PyQt6.QtGui
- PyQt6.QtWidgets
- src.data.finance_store

### src\ui\modules\finance_panel.py
- datetime
- PyQt6.QtCore
- PyQt6.QtGui
- PyQt6.QtWidgets
- src.data.finance_store

### src\ui\modules\notes_panel.py
- json
- logging
- threading
- collections
- pathlib
- PyQt6.QtCore
- PyQt6.QtGui
- PyQt6.QtWidgets
- src.config
- src.data.notes_store
- src.sync.deletion_manifest
- subprocess
- sys
- urllib.parse
- subprocess
- sys
- urllib.parse
- urllib.request
- urllib.request
- urllib.request
- urllib.parse
- urllib.request
- urllib.parse
- urllib.request
- urllib.parse
- os
- os

### src\ui\modules\todo_panel.py
- datetime
- PyQt6.QtCore
- PyQt6.QtGui
- PyQt6.QtWidgets
- src.data.todo_store

### src\ui\themes\__init__.py
- src.ui.themes.styles

### src\ui\widgets\__init__.py
- src.ui.widgets.network_dialog

### src\ui\widgets\network_dialog.py
- socket
- threading
- PyQt6.QtCore
- PyQt6.QtWidgets
- src.config
- PyQt6.QtWidgets

### src\utils\__init__.py
- src.utils.timestamps
- src.utils.paths

### src\utils\paths.py
- pathlib

### src\utils\timestamps.py
- datetime

## 📝 Docstring Summary
### main.pyw
**Module docstring:**
LocalSync — Personal productivity app entry point.

**Classes:**
- (None)

**Functions:**
- `main`: (No docstring)

### src\__init__.py
**Module docstring:**
LocalSync — Personal productivity desktop app.

**Classes:**
- (None)

**Functions:**
- (None)

### src\config.py
**Module docstring:**
App-wide configuration and paths.

**Classes:**
- (None)

**Functions:**
- `load_config`: (No docstring)
- `save_config`: (No docstring)

### src\data\__init__.py
**Module docstring:**
Data layer — storage backends for all modules.

**Classes:**
- (None)

**Functions:**
- (None)

### src\data\activity_store.py
**Module docstring:**
Activity tracking storage backed by SQLite.

**Classes:**
- `Activity`: (No docstring)
- `ActivityStore`: (No docstring)

**Functions:**
- `color`: (No docstring)
- `duration_minutes`: (No docstring)
- `add`: (No docstring)
- `update`: (No docstring)
- `delete`: (No docstring)
- `get_for_date`: (No docstring)
- `get_all`: (No docstring)
- `_upsert`: (No docstring)
- `_row_to_item`: (No docstring)

### src\data\calendar_store.py
**Module docstring:**
Calendar event storage backed by SQLite — supports recurring events and birthdays.

**Classes:**
- `Event`: (No docstring)
- `Birthday`: (No docstring)
- `CalendarStore`: (No docstring)

**Functions:**
- `parse_recurrence`: Parse a recurrence string into a dict.
- `build_recurrence`: Build a recurrence string from type and optional weekly days.
- `expand_recurring_to_range`: Expand a recurring event into concrete dates within [range_start, range_end].
- `add_event`: (No docstring)
- `update_event`: (No docstring)
- `delete_event`: (No docstring)
- `get_events`: Get non-deleted events, optionally filtered by date range.

For recurring events, this returns the *template* event if its
start_time falls before `end`. Use expand_recurring_to_range()
to generate concrete occurrences in a date range.
- `get_all_recurring_events`: Get all non-deleted recurring events regardless of date.
- `get_event`: (No docstring)
- `_upsert`: (No docstring)
- `_row_to_event`: (No docstring)
- `add_birthday`: (No docstring)
- `update_birthday`: (No docstring)
- `delete_birthday`: (No docstring)
- `get_birthdays`: (No docstring)
- `get_birthdays_for_month`: (No docstring)
- `_upsert_birthday`: (No docstring)
- `_row_to_birthday`: (No docstring)
- `get_next_major_events`: Return next `limit` upcoming major events as (event_date, title, category, color).

Sources:
1. Events with category in ('birthday', 'trip', 'holiday', 'major').
2. Birthdays table (next annual occurrence).
Results are sorted by date ascending.

### src\data\database.py
**Module docstring:**
SQLite database setup and connection for Calendar and Finance modules.

**Classes:**
- (None)

**Functions:**
- `get_connection`: (No docstring)
- `init_db`: Create tables if they don't exist, then run migrations.
- `_migrate`: Add columns that may be missing from older databases.

### src\data\finance_store.py
**Module docstring:**
Financial/earnings storage backed by SQLite.

Reframed for freelance work tracking: income categories focus on client/project
types, and the summary is oriented around "Amount Earned" rather than generic
income/expense tracking.

**Classes:**
- `Transaction`: (No docstring)
- `FinanceStore`: (No docstring)

**Functions:**
- `add_transaction`: (No docstring)
- `update_transaction`: (No docstring)
- `delete_transaction`: (No docstring)
- `get_transactions`: (No docstring)
- `get_summary`: Return earnings/expense totals and by-category breakdown.
- `get_all_time_earned`: Total income across all time.
- `_upsert`: (No docstring)
- `_row_to_txn`: (No docstring)

### src\data\holidays_jp.py
**Module docstring:**
Japanese national holidays calculator.

Covers all 16 national holidays defined by Japanese law, including
substitute holidays (振替休日) and special rules for vernal/autumnal equinox.

**Classes:**
- (None)

**Functions:**
- `_vernal_equinox_day`: Approximate day of vernal equinox (春分の日) for a given year.
- `_autumnal_equinox_day`: Approximate day of autumnal equinox (秋分の日) for a given year.
- `_monday_of_week`: Return the nth Monday of a given month (1-indexed).
- `get_japanese_holidays`: Return a dict mapping date -> holiday name for a given year.

All holiday names are provided in English with Japanese in parentheses.
- `is_japanese_holiday`: Return holiday name if the date is a Japanese national holiday, else None.

### src\data\notes_store.py
**Module docstring:**
File-based notes storage — Obsidian-compatible markdown files.

**Classes:**
- `Note`: (No docstring)
- `NotesStore`: Manages markdown notes on disk in an Obsidian-compatible folder layout.

**Functions:**
- `filename`: (No docstring)
- `__init__`: (No docstring)
- `list_notes`: List all .md files under the notes directory, skipping hidden dirs.
- `get_note`: (No docstring)
- `save_note`: (No docstring)
- `delete_note`: (No docstring)
- `search`: Simple case-insensitive search across titles and content.
- `_load_note`: (No docstring)
- `_extract_tags`: Extract #tags from markdown content.

### src\data\todo_store.py
**Module docstring:**
Todo/task storage backed by SQLite.

**Classes:**
- `TodoItem`: (No docstring)
- `TodoStore`: (No docstring)

**Functions:**
- `add`: (No docstring)
- `update`: (No docstring)
- `toggle_done`: (No docstring)
- `delete`: (No docstring)
- `get_all`: (No docstring)
- `get_counts`: (No docstring)
- `_upsert`: (No docstring)
- `_row_to_item`: (No docstring)

### src\sync\__init__.py
**Module docstring:**
LAN sync engine for peer-to-peer data synchronization.

**Classes:**
- (None)

**Functions:**
- (None)

### src\sync\deletion_manifest.py
**Module docstring:**
Shared deletion manifest utilities for vault sync.

Both the VaultWatcher (polling) and the UI (immediate delete/rename) need to
record deletions in `.localsync_deletions.json`. This module centralizes that
logic so there's one source of truth.

**Classes:**
- (None)

**Functions:**
- `get_vault_path`: Return the configured vault path, or None.
- `_manifest_path`: (No docstring)
- `read_manifest`: (No docstring)
- `write_manifest`: (No docstring)
- `record_deletion`: Immediately record a file deletion in the vault manifest.

Safe to call from any thread. If vault is None, reads from config.
- `is_deleted`: Check if a path is in the deletion manifest.
- `remove_deletion`: Remove a path from the deletion manifest (file re-created).

### src\sync\engine.py
**Module docstring:**
LAN mesh sync engine — subnet scanning, peer discovery, and data exchange.

How it works:
1. DISCOVERY: On each cycle, actively scans the local /24 subnet by attempting
   a fast TCP connect to the sync port on every host. Also listens for UDP
   broadcast announcements from other instances. This two-pronged approach
   means peers find each other automatically on the LAN.

2. SYNC: For each discovered peer, opens a TCP connection, exchanges full data
   sets (events, transactions, notes), and merges using last-write-wins on
   the updated_at timestamp. Soft-deleted records are propagated.

3. MESH: Every node is both client and server. There's no central coordinator.
   Any two nodes that can reach each other will converge.

Designed for your setup:
  Desktop (Windows) 192.168.0.4  <-->  Laptop (Linux) 192.168.0.28
  Both on the same 192.168.0.0/24 subnet.

**Classes:**
- `PeerInfo`: Tracks a discovered peer and its health.
- `SyncEngine`: Background mesh sync thread.

**Functions:**
- `__init__`: (No docstring)
- `is_stale`: (No docstring)
- `__repr__`: (No docstring)
- `__init__`: (No docstring)
- `run`: (No docstring)
- `stop`: (No docstring)
- `force_sync`: Trigger an immediate sync cycle (called from UI).
- `_force_sync_once`: (No docstring)
- `trigger_vault_sync`: Called by the vault watcher when local vault files changed.

Immediately syncs with all known peers so the changes propagate.
- `_vault_sync_once`: (No docstring)
- `add_manual_peer`: Add a peer IP manually (from the network settings dialog).
- `reload_config`: Reload config after settings change.
- `_scan_subnet`: Actively probe every host in the /24 subnet for our sync port.
- `_probe_host`: Try a fast TCP connect to see if a peer is listening on sync_port.
- `_broadcast_presence`: Announce ourselves on the LAN via UDP broadcast.
- `_discovery_listener`: Listen for UDP peer announcements.
- `_sync_server`: TCP server that accepts sync requests from peers.
- `_handle_incoming`: Handle an incoming sync connection from a peer.
- `_sync_with_peer`: Initiate a sync exchange with a specific peer.
- `ping_peer`: Ping a specific peer. Returns (reachable, hostname_or_error).
- `_gather_local_data`: (No docstring)
- `_get_vault_deletions`: Read the deletion manifest for vault files.
- `_record_vault_deletion`: Record a file deletion in the vault manifest.
- `_merge_remote_data`: Merge remote data. Returns count of changes applied.
- `_remove_vault_deletion`: Remove a path from the deletion manifest (file was re-created remotely).
- `_cleanup_empty_dirs`: Remove empty subdirectories (bottom-up) after file deletions.
- `_get_alive_peers`: (No docstring)
- `_prune_stale_peers`: (No docstring)
- `_emit_peer_list`: (No docstring)
- `get_peer_list`: Synchronous access to peer list for the settings dialog.
- `_send_json`: (No docstring)
- `_recv_json`: (No docstring)
- `_get_local_ips`: (No docstring)
- `_log`: (No docstring)

### src\sync\vault_watcher.py
**Module docstring:**
Filesystem watcher for Obsidian vault — detects local edits and triggers sync.

Uses a polling approach (no inotify dependency) to watch for .md file changes
in the configured vault directory. When changes are detected, emits a signal
so the sync engine can broadcast them to peers.

**Classes:**
- `VaultWatcher`: Polls the Obsidian vault for file changes and signals when detected.

**Functions:**
- `__init__`: (No docstring)
- `_load_vault_path`: (No docstring)
- `reload_config`: Reload vault path from config (called after settings change).
- `_scan_vault`: Build a dict of {posix_relative_path: mtime} for all .md files in vault.

Always uses forward slashes so Windows/Linux snapshots are comparable.
- `run`: (No docstring)
- `_has_changes`: Compare current scan against previous snapshot.
- `_record_deletions`: When files disappear from the vault, record them in the deletion manifest.

Uses the shared deletion_manifest module. Skips paths already recorded
(e.g. by the UI doing an immediate delete/rename).
- `stop`: (No docstring)

### src\ui\__init__.py
**Module docstring:**
UI layer — PyQt6 main window and module panels.

**Classes:**
- (None)

**Functions:**
- (None)

### src\ui\main_window.py
**Module docstring:**
Main application window with menu bar, sidebar, theme selector, and sync integration.

**Classes:**
- `SidebarButton`: (No docstring)
- `MainWindow`: (No docstring)

**Functions:**
- `__init__`: (No docstring)
- `apply_colors`: (No docstring)
- `__init__`: (No docstring)
- `_build_menu_bar`: (No docstring)
- `_action`: (No docstring)
- `_build_central`: (No docstring)
- `_build_status_bar`: (No docstring)
- `_update_clock`: (No docstring)
- `_navigate`: (No docstring)
- `_on_theme_changed`: (No docstring)
- `_apply_theme`: (No docstring)
- `set_sync_engine`: Called by main.py to wire up the sync engine.
- `_on_sync_completed`: Refresh all panels after incoming data has been merged.
- `set_sync_status`: (No docstring)
- `_on_peers_updated`: (No docstring)
- `_force_sync`: (No docstring)
- `_open_network_dialog`: (No docstring)
- `_show_about`: (No docstring)

### src\ui\modules\__init__.py
**Module docstring:**
Module panels for each app feature.

**Classes:**
- (None)

**Functions:**
- (None)

### src\ui\modules\activity_panel.py
**Module docstring:**
Activity Tracker panel — Gantt-style single-row day view with timer and manual input.

Tracks daily activities with start/end times. Primary input is via the live timer
(Start → Stop → Add), but manual time entry is always available.
Exports activities to the Obsidian vault.

**Classes:**
- `GanttBar`: Represents a single activity block on the Gantt chart.
- `GanttWidget`: Custom-painted Gantt chart showing a single day's activities.
- `ActivityPanel`: (No docstring)

**Functions:**
- `__init__`: (No docstring)
- `__init__`: (No docstring)
- `set_palette`: (No docstring)
- `set_bars`: (No docstring)
- `set_on_select`: (No docstring)
- `_time_to_x`: Convert HH:MM to x coordinate.
- `paintEvent`: (No docstring)
- `mousePressEvent`: (No docstring)
- `mouseMoveEvent`: (No docstring)
- `__init__`: (No docstring)
- `set_palette`: (No docstring)
- `_build_ui`: (No docstring)
- `_prev_day`: (No docstring)
- `_next_day`: (No docstring)
- `_go_today`: (No docstring)
- `_start_timer`: (No docstring)
- `_stop_timer`: (No docstring)
- `_update_timer_display`: (No docstring)
- `_refresh`: (No docstring)
- `_make_activity_row`: (No docstring)
- `_add_activity`: (No docstring)
- `_start_edit`: (No docstring)
- `_update_activity`: (No docstring)
- `_delete_activity`: (No docstring)
- `_cancel_edit`: (No docstring)
- `_on_bar_selected`: Called when user clicks a bar in the Gantt chart.
- `_export_to_vault`: (No docstring)
- `_clear_layout`: (No docstring)

### src\ui\modules\calendar_panel.py
**Module docstring:**
Calendar module UI — weekly main view + mini month navigator + colored dot indicators.

**Classes:**
- `EventDialog`: Dialog to add/edit an event.
- `MiniMonthCell`: A single day number in the mini calendar.
- `MiniMonth`: Compact month grid for date navigation.
- `WeekEventWidget`: A single event rendered in the weekly time grid.
- `DayColumn`: A single day column in the weekly view.
- `CalendarPanel`: (No docstring)

**Functions:**
- `__init__`: (No docstring)
- `_build_ui`: (No docstring)
- `_toggle_time`: (No docstring)
- `_on_delete`: (No docstring)
- `get_data`: (No docstring)
- `__init__`: (No docstring)
- `mousePressEvent`: (No docstring)
- `__init__`: (No docstring)
- `set_events`: (No docstring)
- `set_selected`: (No docstring)
- `_build`: (No docstring)
- `_render`: (No docstring)
- `_on_cell_click`: (No docstring)
- `_prev_month`: (No docstring)
- `_next_month`: (No docstring)
- `__init__`: (No docstring)
- `mouseDoubleClickEvent`: (No docstring)
- `__init__`: (No docstring)
- `mouseDoubleClickEvent`: (No docstring)
- `__init__`: (No docstring)
- `set_palette`: (No docstring)
- `_build_ui`: (No docstring)
- `_refresh`: (No docstring)
- `_get_week_start`: Monday of the selected week.
- `_render_week`: (No docstring)
- `_render_day_detail`: (No docstring)
- `_render_major_events`: (No docstring)
- `_update_mini_month_events`: Feed the mini month with event data so it can show colored dots.
- `_prev_week`: (No docstring)
- `_next_week`: (No docstring)
- `_go_today`: (No docstring)
- `_on_mini_date_selected`: (No docstring)
- `_add_event`: (No docstring)
- `_add_event_on_day_date`: (No docstring)
- `_edit_event`: (No docstring)

### src\ui\modules\dashboard_panel.py
**Module docstring:**
QA Dashboard panel — overview of tasks, upcoming deadlines, and productivity stats.

**Classes:**
- `StatCard`: A compact stat card with a big number and label.
- `UpcomingItem`: A single upcoming deadline / event in the dashboard.
- `DashboardPanel`: (No docstring)

**Functions:**
- `__init__`: (No docstring)
- `update_value`: (No docstring)
- `__init__`: (No docstring)
- `__init__`: (No docstring)
- `set_palette`: (No docstring)
- `_build_ui`: (No docstring)
- `_refresh`: (No docstring)
- `_clear_layout`: (No docstring)

### src\ui\modules\finance_charts.py
**Module docstring:**
Finance charts — custom painted graphs for earnings data visualization.

Uses QPainter for zero-dependency chart rendering: line chart, bar chart, pie chart.

**Classes:**
- `LineChart`: Monthly earnings line chart with area fill.
- `BarChart`: Vertical bar chart for category or monthly comparisons.
- `PieChart`: Donut/pie chart for category distribution.
- `FinanceChartsPanel`: Charts view for the finance data.

**Functions:**
- `__init__`: (No docstring)
- `set_data`: (No docstring)
- `paintEvent`: (No docstring)
- `__init__`: (No docstring)
- `set_data`: (No docstring)
- `paintEvent`: (No docstring)
- `__init__`: (No docstring)
- `set_data`: (No docstring)
- `paintEvent`: (No docstring)
- `__init__`: (No docstring)
- `set_palette`: (No docstring)
- `_build_ui`: (No docstring)
- `_get_date_range`: (No docstring)
- `_refresh`: (No docstring)

### src\ui\modules\finance_panel.py
**Module docstring:**
Earnings Tracker module UI — freelance income tracking with summaries.

**Classes:**
- `TransactionDialog`: Dialog to add/edit a transaction (earning or expense).
- `CategoryBar`: (No docstring)
- `FinancePanel`: (No docstring)

**Functions:**
- `__init__`: (No docstring)
- `_build_ui`: (No docstring)
- `_on_type_changed`: (No docstring)
- `get_data`: (No docstring)
- `__init__`: (No docstring)
- `__init__`: (No docstring)
- `set_palette`: (No docstring)
- `_build_ui`: (No docstring)
- `_get_filters`: (No docstring)
- `_refresh`: (No docstring)
- `_add_earning`: (No docstring)
- `_add_expense`: (No docstring)
- `_edit_transaction`: (No docstring)
- `_delete_transaction`: (No docstring)

### src\ui\modules\notes_panel.py
**Module docstring:**
Notes/Obsidian module UI — tree-based vault browser, markdown editor, REST API integration.

The sidebar uses a QTreeWidget with collapsible folders (triangle toggles)
that mimics Obsidian's file explorer layout.

**Classes:**
- `ObsidianAPI`: Minimal client for the Obsidian Local REST API plugin.
- `NotesPanel`: (No docstring)

**Functions:**
- `_build_tree_structure`: Build a nested dict from note paths for the tree view.

Returns: {"_files": [Note, ...], "subfolder": {"_files": [...], ...}}
- `_populate_tree_widget`: Recursively populate QTreeWidgetItems from the nested dict.
- `__init__`: (No docstring)
- `_headers`: (No docstring)
- `is_available`: (No docstring)
- `list_files`: (No docstring)
- `read_note`: (No docstring)
- `create_note`: (No docstring)
- `append_note`: (No docstring)
- `open_in_obsidian`: Open a note in the Obsidian desktop app via URI scheme.
- `__init__`: (No docstring)
- `_init_store`: (No docstring)
- `_init_obsidian_api`: (No docstring)
- `_build_ui`: (No docstring)
- `_refresh_list`: Rebuild the tree from the note store.
- `_save_expanded_state`: Walk the tree and record which folder names are expanded.
- `_walk_expanded`: (No docstring)
- `_on_item_expanded`: (No docstring)
- `_on_item_collapsed`: (No docstring)
- `_select_note_in_tree`: Find and select a note in the tree by its relative path.
- `_find_tree_item`: (No docstring)
- `_reload_if_changed_on_disk`: If the currently open note was modified externally, reload it.
- `_update_status_label`: (No docstring)
- `_set_vault_path`: (No docstring)
- `_configure_api`: (No docstring)
- `_create_via_api`: (No docstring)
- `_open_in_obsidian`: Open the current note in Obsidian via obsidian:// URI scheme.
- `_on_search`: (No docstring)
- `_on_tree_item_selected`: (No docstring)
- `_clear_editor`: (No docstring)
- `_on_text_changed`: (No docstring)
- `_save_current`: (No docstring)
- `_update_footer`: (No docstring)
- `_new_note`: (No docstring)
- `_new_folder`: (No docstring)
- `_rename_note`: (No docstring)
- `_delete_note`: (No docstring)
- `check`: (No docstring)

### src\ui\modules\todo_panel.py
**Module docstring:**
Todo list module UI — modern task manager with priorities, categories, and due dates.

**Classes:**
- `TodoDialog`: Dialog to add/edit a todo item.
- `TodoItemWidget`: A single todo item rendered as a compact card.
- `TodoPanel`: (No docstring)

**Functions:**
- `__init__`: (No docstring)
- `_build_ui`: (No docstring)
- `get_data`: (No docstring)
- `__init__`: (No docstring)
- `_on_toggle`: (No docstring)
- `_on_edit`: (No docstring)
- `mouseDoubleClickEvent`: (No docstring)
- `__init__`: (No docstring)
- `set_palette`: (No docstring)
- `_build_ui`: (No docstring)
- `_refresh`: (No docstring)
- `_quick_add`: (No docstring)
- `_add_item`: (No docstring)
- `_edit_item`: (No docstring)
- `_toggle_item`: (No docstring)
- `_clear_done`: (No docstring)

### src\ui\themes\__init__.py
**Module docstring:**
Theme definitions and management.

**Classes:**
- (None)

**Functions:**
- (None)

### src\ui\themes\styles.py
**Module docstring:**
Theme stylesheets for PyQt6 — Catppuccin Dark, Catppuccin Light, Nord, Solarized, Gruvbox.

**Classes:**
- (None)

**Functions:**
- `_build_theme`: Generate a full QSS stylesheet from a color palette dict.
- `get_theme_names`: (No docstring)

### src\ui\widgets\__init__.py
**Module docstring:**
Reusable UI widgets.

**Classes:**
- (None)

**Functions:**
- (None)

### src\ui\widgets\network_dialog.py
**Module docstring:**
Network settings dialog — configure sync, view peers, manage connections.

**Classes:**
- `NetworkDialog`: Network and sync settings with live peer status and log viewer.

**Functions:**
- `__init__`: (No docstring)
- `_build_ui`: (No docstring)
- `_load_values`: (No docstring)
- `_save_settings`: (No docstring)
- `_refresh_peers`: (No docstring)
- `_update_peer_table`: (No docstring)
- `_add_manual_peer`: (No docstring)
- `_ping_selected`: (No docstring)
- `_force_scan`: (No docstring)
- `_force_sync`: (No docstring)
- `_browse_vault`: (No docstring)
- `_save_obsidian_settings`: (No docstring)
- `_append_log`: (No docstring)
- `_get_local_ip`: (No docstring)
- `do_ping`: (No docstring)
- `do_ping`: (No docstring)

### src\utils\__init__.py
**Module docstring:**
Shared utilities.

**Classes:**
- (None)

**Functions:**
- (None)

### src\utils\paths.py
**Module docstring:**
Cross-platform path utilities.

**Classes:**
- (None)

**Functions:**
- `normalize_path`: Convert a path to forward-slash form for consistent storage.
- `ensure_parent`: Create parent directories if they don't exist.

### src\utils\timestamps.py
**Module docstring:**
Timestamp utilities for sync and data.

**Classes:**
- (None)

**Functions:**
- `now_utc`: ISO-8601 UTC timestamp string.
- `parse_ts`: Parse an ISO-8601 timestamp string.

### tests\__init__.py
**Module docstring:**
Tests for LocalSync.

**Classes:**
- (None)

**Functions:**
- (None)

## 📄 Full File Contents

### `main.pyw`

```python
#!/usr/bin/env python3
"""LocalSync — Personal productivity app entry point."""

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

    sys.exit(exit_code)


if __name__ == "__main__":
    main()

```

### `src\__init__.py`

```python
"""LocalSync — Personal productivity desktop app."""

from src.config import APP_NAME, APP_VERSION

__all__ = ["APP_NAME", "APP_VERSION"]

```

### `src\config.py`

```python
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
    "sync_interval_seconds": 30,  # 30 seconds for near-realtime sync
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
    # Obsidian
    "obsidian_vault_path": "",           # Path to the Obsidian vault folder
    "obsidian_api_key": "",              # Obsidian Local REST API plugin key
    "obsidian_api_url": "http://127.0.0.1:27123",  # REST API base URL
    "obsidian_sync_enabled": False,      # Whether to sync vault files
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

```

### `src\data\__init__.py`

```python
"""Data layer — storage backends for all modules."""

from src.data.database import get_connection, init_db
from src.data.notes_store import NotesStore, Note
from src.data.calendar_store import CalendarStore, Event
from src.data.finance_store import FinanceStore, Transaction, DEFAULT_CATEGORIES
from src.data.todo_store import TodoStore, TodoItem, PRIORITY_LABELS, DEFAULT_TODO_CATEGORIES

__all__ = [
    "get_connection", "init_db",
    "NotesStore", "Note",
    "CalendarStore", "Event",
    "FinanceStore", "Transaction", "DEFAULT_CATEGORIES",
    "TodoStore", "TodoItem", "PRIORITY_LABELS", "DEFAULT_TODO_CATEGORIES",
]

```

### `src\data\activity_store.py`

```python
"""Activity tracking storage backed by SQLite."""

import uuid
from dataclasses import dataclass

from src.data.database import get_connection
from src.utils.timestamps import now_utc


DEFAULT_ACTIVITIES = [
    "Deep Work", "Meetings", "Email / Comms", "Learning",
    "Exercise", "Break", "Errands", "Commute",
    "Coding", "Writing", "Reading", "Admin",
]

# Colors for activity bars (matched to common activities)
ACTIVITY_COLORS = {
    "Deep Work": "#89b4fa",
    "Meetings": "#f38ba8",
    "Email / Comms": "#fab387",
    "Learning": "#a6e3a1",
    "Exercise": "#94e2d5",
    "Break": "#9399b2",
    "Errands": "#f9e2af",
    "Commute": "#cba6f7",
    "Coding": "#74c7ec",
    "Writing": "#b4befe",
    "Reading": "#f2cdcd",
    "Admin": "#eba0ac",
}

DEFAULT_COLOR = "#89dceb"


@dataclass
class Activity:
    id: str
    date: str           # YYYY-MM-DD
    activity: str       # Name of the activity
    start_time: str     # HH:MM (24h)
    end_time: str       # HH:MM (24h)
    notes: str = ""
    created_at: str = ""
    updated_at: str = ""
    deleted: bool = False

    @property
    def color(self) -> str:
        return ACTIVITY_COLORS.get(self.activity, DEFAULT_COLOR)

    @property
    def duration_minutes(self) -> int:
        try:
            sh, sm = map(int, self.start_time.split(":"))
            eh, em = map(int, self.end_time.split(":"))
            return (eh * 60 + em) - (sh * 60 + sm)
        except (ValueError, AttributeError):
            return 0


class ActivityStore:

    def add(self, date: str, activity: str, start_time: str,
            end_time: str, notes: str = "") -> Activity:
        now = now_utc()
        item = Activity(
            id=str(uuid.uuid4()), date=date, activity=activity,
            start_time=start_time, end_time=end_time, notes=notes,
            created_at=now, updated_at=now,
        )
        self._upsert(item)
        return item

    def update(self, item: Activity) -> Activity:
        item.updated_at = now_utc()
        self._upsert(item)
        return item

    def delete(self, item_id: str):
        conn = get_connection()
        try:
            conn.execute(
                "UPDATE activities SET deleted=1, updated_at=? WHERE id=?",
                (now_utc(), item_id),
            )
            conn.commit()
        finally:
            conn.close()

    def get_for_date(self, date: str) -> list[Activity]:
        conn = get_connection()
        try:
            rows = conn.execute(
                "SELECT * FROM activities WHERE date=? AND deleted=0 "
                "ORDER BY start_time ASC",
                (date,),
            ).fetchall()
            return [self._row_to_item(r) for r in rows]
        finally:
            conn.close()

    def get_all(self) -> list[Activity]:
        conn = get_connection()
        try:
            rows = conn.execute(
                "SELECT * FROM activities WHERE deleted=0 ORDER BY date DESC, start_time ASC"
            ).fetchall()
            return [self._row_to_item(r) for r in rows]
        finally:
            conn.close()

    def _upsert(self, item: Activity):
        conn = get_connection()
        try:
            conn.execute(
                """INSERT INTO activities (id, date, activity, start_time, end_time,
                   notes, created_at, updated_at, deleted)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(id) DO UPDATE SET
                   date=excluded.date, activity=excluded.activity,
                   start_time=excluded.start_time, end_time=excluded.end_time,
                   notes=excluded.notes, updated_at=excluded.updated_at,
                   deleted=excluded.deleted""",
                (item.id, item.date, item.activity, item.start_time,
                 item.end_time, item.notes, item.created_at, item.updated_at,
                 int(item.deleted)),
            )
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def _row_to_item(row) -> Activity:
        return Activity(
            id=row["id"], date=row["date"], activity=row["activity"],
            start_time=row["start_time"], end_time=row["end_time"],
            notes=row["notes"] or "", created_at=row["created_at"],
            updated_at=row["updated_at"], deleted=bool(row["deleted"]),
        )

```

### `src\data\calendar_store.py`

```python
"""Calendar event storage backed by SQLite — supports recurring events and birthdays."""

import uuid
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta

from src.data.database import get_connection
from src.utils.timestamps import now_utc


# ── Recurrence types ──────────────────────────────────
# Stored as a string in the DB:
#   ""              → no recurrence
#   "daily"         → every day
#   "weekly:0,1,2"  → every Mon, Tue, Wed  (0=Mon … 6=Sun)
#   "monthly"       → same day each month
#   "yearly"        → same day each year

def parse_recurrence(rec: str) -> dict:
    """Parse a recurrence string into a dict."""
    if not rec:
        return {"type": "none"}
    if rec == "daily":
        return {"type": "daily"}
    if rec.startswith("weekly:"):
        days = [int(d) for d in rec.split(":")[1].split(",") if d.strip()]
        return {"type": "weekly", "days": days}
    if rec == "monthly":
        return {"type": "monthly"}
    if rec == "yearly":
        return {"type": "yearly"}
    return {"type": "none"}


def build_recurrence(rec_type: str, weekly_days: list[int] | None = None) -> str:
    """Build a recurrence string from type and optional weekly days."""
    if rec_type == "daily":
        return "daily"
    if rec_type == "weekly" and weekly_days:
        return "weekly:" + ",".join(str(d) for d in sorted(weekly_days))
    if rec_type == "monthly":
        return "monthly"
    if rec_type == "yearly":
        return "yearly"
    return ""


def expand_recurring_to_range(event: 'Event', range_start: date, range_end: date) -> list[date]:
    """Expand a recurring event into concrete dates within [range_start, range_end]."""
    rec = parse_recurrence(event.recurrence)
    if rec["type"] == "none":
        return []

    try:
        ev_start = datetime.fromisoformat(event.start_time).date()
    except Exception:
        return []

    dates: list[date] = []
    if rec["type"] == "daily":
        d = max(ev_start, range_start)
        while d <= range_end:
            dates.append(d)
            d += timedelta(days=1)
    elif rec["type"] == "weekly":
        target_days = set(rec.get("days", []))
        d = max(ev_start, range_start)
        while d <= range_end:
            if d.weekday() in target_days:
                dates.append(d)
            d += timedelta(days=1)
    elif rec["type"] == "monthly":
        target_day = ev_start.day
        m_start = max(ev_start.replace(day=1), range_start.replace(day=1))
        y, m = m_start.year, m_start.month
        while True:
            try:
                d = date(y, m, target_day)
            except ValueError:
                pass  # e.g. Feb 31
            else:
                if range_start <= d <= range_end and d >= ev_start:
                    dates.append(d)
            m += 1
            if m > 12:
                m = 1
                y += 1
            if date(y, m, 1) > range_end:
                break
    elif rec["type"] == "yearly":
        target_month, target_day = ev_start.month, ev_start.day
        for y in range(max(ev_start.year, range_start.year), range_end.year + 1):
            try:
                d = date(y, target_month, target_day)
            except ValueError:
                continue
            if range_start <= d <= range_end:
                dates.append(d)

    return dates


@dataclass
class Event:
    id: str
    title: str
    start_time: str  # ISO-8601
    end_time: str | None = None
    description: str = ""
    all_day: bool = False
    color: str = "#4a9eff"
    updated_at: str = ""
    deleted: bool = False
    recurrence: str = ""   # e.g. "weekly:0,1,2,3,4" for weekdays
    category: str = ""     # "work", "birthday", "holiday", or ""


@dataclass
class Birthday:
    id: str
    name: str
    month: int
    day: int
    year: int | None = None
    updated_at: str = ""
    deleted: bool = False


class CalendarStore:

    # ── Event CRUD ────────────────────────────────────

    def add_event(self, title: str, start_time: str, end_time: str | None = None,
                  description: str = "", all_day: bool = False, color: str = "#4a9eff",
                  recurrence: str = "", category: str = "") -> Event:
        ev = Event(
            id=str(uuid.uuid4()),
            title=title,
            start_time=start_time,
            end_time=end_time,
            description=description,
            all_day=all_day,
            color=color,
            updated_at=now_utc(),
            recurrence=recurrence,
            category=category,
        )
        self._upsert(ev)
        return ev

    def update_event(self, event: Event) -> Event:
        event.updated_at = now_utc()
        self._upsert(event)
        return event

    def delete_event(self, event_id: str):
        conn = get_connection()
        try:
            conn.execute(
                "UPDATE events SET deleted=1, updated_at=? WHERE id=?",
                (now_utc(), event_id),
            )
            conn.commit()
        finally:
            conn.close()

    def get_events(self, start: str | None = None, end: str | None = None) -> list[Event]:
        """Get non-deleted events, optionally filtered by date range.

        For recurring events, this returns the *template* event if its
        start_time falls before `end`. Use expand_recurring_to_range()
        to generate concrete occurrences in a date range.
        """
        conn = get_connection()
        try:
            query = "SELECT * FROM events WHERE deleted=0"
            params: list = []
            if start:
                query += " AND (start_time >= ? OR recurrence != '')"
                params.append(start)
            if end:
                query += " AND start_time <= ?"
                params.append(end)
            query += " ORDER BY start_time"
            rows = conn.execute(query, params).fetchall()
            return [self._row_to_event(r) for r in rows]
        finally:
            conn.close()

    def get_all_recurring_events(self) -> list[Event]:
        """Get all non-deleted recurring events regardless of date."""
        conn = get_connection()
        try:
            rows = conn.execute(
                "SELECT * FROM events WHERE deleted=0 AND recurrence != '' ORDER BY start_time"
            ).fetchall()
            return [self._row_to_event(r) for r in rows]
        finally:
            conn.close()

    def get_event(self, event_id: str) -> Event | None:
        conn = get_connection()
        try:
            row = conn.execute("SELECT * FROM events WHERE id=?", (event_id,)).fetchone()
            return self._row_to_event(row) if row else None
        finally:
            conn.close()

    def _upsert(self, ev: Event):
        conn = get_connection()
        try:
            conn.execute(
                """INSERT INTO events (id, title, description, start_time, end_time,
                   all_day, color, updated_at, deleted, recurrence, category)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(id) DO UPDATE SET
                   title=excluded.title, description=excluded.description,
                   start_time=excluded.start_time, end_time=excluded.end_time,
                   all_day=excluded.all_day, color=excluded.color,
                   updated_at=excluded.updated_at, deleted=excluded.deleted,
                   recurrence=excluded.recurrence, category=excluded.category""",
                (ev.id, ev.title, ev.description, ev.start_time, ev.end_time,
                 int(ev.all_day), ev.color, ev.updated_at, int(ev.deleted),
                 ev.recurrence, ev.category),
            )
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def _row_to_event(row) -> Event:
        return Event(
            id=row["id"], title=row["title"], description=row["description"],
            start_time=row["start_time"], end_time=row["end_time"],
            all_day=bool(row["all_day"]), color=row["color"],
            updated_at=row["updated_at"], deleted=bool(row["deleted"]),
            recurrence=row["recurrence"] if "recurrence" in row.keys() else "",
            category=row["category"] if "category" in row.keys() else "",
        )

    # ── Birthday CRUD ─────────────────────────────────

    def add_birthday(self, name: str, month: int, day: int,
                     year: int | None = None) -> Birthday:
        b = Birthday(
            id=str(uuid.uuid4()),
            name=name, month=month, day=day, year=year,
            updated_at=now_utc(),
        )
        self._upsert_birthday(b)
        return b

    def update_birthday(self, birthday: Birthday) -> Birthday:
        birthday.updated_at = now_utc()
        self._upsert_birthday(birthday)
        return birthday

    def delete_birthday(self, birthday_id: str):
        conn = get_connection()
        try:
            conn.execute(
                "UPDATE birthdays SET deleted=1, updated_at=? WHERE id=?",
                (now_utc(), birthday_id),
            )
            conn.commit()
        finally:
            conn.close()

    def get_birthdays(self) -> list[Birthday]:
        conn = get_connection()
        try:
            rows = conn.execute(
                "SELECT * FROM birthdays WHERE deleted=0 ORDER BY month, day"
            ).fetchall()
            return [self._row_to_birthday(r) for r in rows]
        finally:
            conn.close()

    def get_birthdays_for_month(self, month: int) -> list[Birthday]:
        conn = get_connection()
        try:
            rows = conn.execute(
                "SELECT * FROM birthdays WHERE deleted=0 AND month=? ORDER BY day",
                (month,),
            ).fetchall()
            return [self._row_to_birthday(r) for r in rows]
        finally:
            conn.close()

    def _upsert_birthday(self, b: Birthday):
        conn = get_connection()
        try:
            conn.execute(
                """INSERT INTO birthdays (id, name, month, day, year, updated_at, deleted)
                   VALUES (?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(id) DO UPDATE SET
                   name=excluded.name, month=excluded.month, day=excluded.day,
                   year=excluded.year, updated_at=excluded.updated_at,
                   deleted=excluded.deleted""",
                (b.id, b.name, b.month, b.day, b.year, b.updated_at, int(b.deleted)),
            )
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def _row_to_birthday(row) -> Birthday:
        return Birthday(
            id=row["id"], name=row["name"], month=row["month"],
            day=row["day"], year=row["year"],
            updated_at=row["updated_at"], deleted=bool(row["deleted"]),
        )

    # ── Major events ──────────────────────────────────

    def get_next_major_events(self, from_date: date, limit: int = 4) -> list[tuple]:
        """Return next `limit` upcoming major events as (event_date, title, category, color).

        Sources:
        1. Events with category in ('birthday', 'trip', 'holiday', 'major').
        2. Birthdays table (next annual occurrence).
        Results are sorted by date ascending.
        """
        results: list[tuple] = []

        # Regular events with a major category
        conn = get_connection()
        try:
            rows = conn.execute(
                """SELECT * FROM events WHERE deleted=0
                   AND category IN ('birthday','trip','holiday','major')
                   AND start_time >= ?
                   ORDER BY start_time""",
                (from_date.isoformat(),),
            ).fetchall()
        finally:
            conn.close()

        for row in rows:
            ev = self._row_to_event(row)
            try:
                ev_date = datetime.fromisoformat(ev.start_time).date()
            except Exception:
                continue
            results.append((ev_date, ev.title, ev.category, ev.color))

        # Birthday table — find next annual occurrence
        today = from_date
        for b in self.get_birthdays():
            try:
                candidate = date(today.year, b.month, b.day)
            except ValueError:
                continue
            if candidate < today:
                try:
                    candidate = date(today.year + 1, b.month, b.day)
                except ValueError:
                    continue
            results.append((candidate, b.name, "birthday", "#f38ba8"))

        results.sort(key=lambda x: x[0])
        return results[:limit]

```

### `src\data\database.py`

```python
"""SQLite database setup and connection for Calendar and Finance modules."""

import sqlite3
from pathlib import Path

from src.config import DB_PATH


def get_connection(db_path: Path | None = None) -> sqlite3.Connection:
    path = db_path or DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db(conn: sqlite3.Connection | None = None):
    """Create tables if they don't exist, then run migrations."""
    own_conn = conn is None
    if own_conn:
        conn = get_connection()
    try:
        conn.executescript(_SCHEMA)
        _migrate(conn)
        conn.commit()
    finally:
        if own_conn:
            conn.close()


def _migrate(conn: sqlite3.Connection):
    """Add columns that may be missing from older databases."""
    cols = {r["name"] for r in conn.execute("PRAGMA table_info(events)").fetchall()}
    if "recurrence" not in cols:
        conn.execute("ALTER TABLE events ADD COLUMN recurrence TEXT DEFAULT ''")
    if "category" not in cols:
        conn.execute("ALTER TABLE events ADD COLUMN category TEXT DEFAULT ''")


_SCHEMA = """
CREATE TABLE IF NOT EXISTS events (
    id          TEXT PRIMARY KEY,
    title       TEXT NOT NULL,
    description TEXT DEFAULT '',
    start_time  TEXT NOT NULL,
    end_time    TEXT,
    all_day     INTEGER DEFAULT 0,
    color       TEXT DEFAULT '#4a9eff',
    updated_at  TEXT NOT NULL,
    deleted     INTEGER DEFAULT 0,
    recurrence  TEXT DEFAULT '',
    category    TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS birthdays (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    month       INTEGER NOT NULL,
    day         INTEGER NOT NULL,
    year        INTEGER,
    updated_at  TEXT NOT NULL,
    deleted     INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS transactions (
    id          TEXT PRIMARY KEY,
    date        TEXT NOT NULL,
    amount      REAL NOT NULL,
    type        TEXT NOT NULL CHECK(type IN ('income', 'expense')),
    category    TEXT DEFAULT 'Uncategorized',
    description TEXT DEFAULT '',
    updated_at  TEXT NOT NULL,
    deleted     INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS todos (
    id          TEXT PRIMARY KEY,
    title       TEXT NOT NULL,
    done        INTEGER DEFAULT 0,
    priority    INTEGER DEFAULT 0,
    due_date    TEXT,
    category    TEXT DEFAULT '',
    notes       TEXT DEFAULT '',
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL,
    deleted     INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS activities (
    id          TEXT PRIMARY KEY,
    date        TEXT NOT NULL,
    activity    TEXT NOT NULL,
    start_time  TEXT NOT NULL,
    end_time    TEXT NOT NULL,
    notes       TEXT DEFAULT '',
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL,
    deleted     INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS sync_meta (
    key   TEXT PRIMARY KEY,
    value TEXT
);
"""

```

### `src\data\finance_store.py`

```python
"""Financial/earnings storage backed by SQLite.

Reframed for freelance work tracking: income categories focus on client/project
types, and the summary is oriented around "Amount Earned" rather than generic
income/expense tracking.
"""

import uuid
from dataclasses import dataclass

from src.data.database import get_connection
from src.utils.timestamps import now_utc


DEFAULT_CATEGORIES = [
    # Earnings sources
    "Freelance", "Contract", "Consulting", "Commission", "Royalties",
    "Side Project", "Referral Bonus",
    # Expense categories (still useful for net tracking)
    "Software/Tools", "Hardware", "Office", "Travel", "Education",
    "Taxes", "Fees", "Uncategorized",
]


@dataclass
class Transaction:
    id: str
    date: str  # YYYY-MM-DD
    amount: float
    type: str  # 'income' or 'expense'
    category: str = "Freelance"
    description: str = ""
    updated_at: str = ""
    deleted: bool = False


class FinanceStore:

    def add_transaction(self, date: str, amount: float, txn_type: str,
                        category: str = "Freelance", description: str = "") -> Transaction:
        txn = Transaction(
            id=str(uuid.uuid4()),
            date=date,
            amount=amount,
            type=txn_type,
            category=category,
            description=description,
            updated_at=now_utc(),
        )
        self._upsert(txn)
        return txn

    def update_transaction(self, txn: Transaction) -> Transaction:
        txn.updated_at = now_utc()
        self._upsert(txn)
        return txn

    def delete_transaction(self, txn_id: str):
        conn = get_connection()
        try:
            conn.execute(
                "UPDATE transactions SET deleted=1, updated_at=? WHERE id=?",
                (now_utc(), txn_id),
            )
            conn.commit()
        finally:
            conn.close()

    def get_transactions(self, start_date: str | None = None,
                         end_date: str | None = None,
                         txn_type: str | None = None) -> list[Transaction]:
        conn = get_connection()
        try:
            query = "SELECT * FROM transactions WHERE deleted=0"
            params: list = []
            if start_date:
                query += " AND date >= ?"
                params.append(start_date)
            if end_date:
                query += " AND date <= ?"
                params.append(end_date)
            if txn_type:
                query += " AND type = ?"
                params.append(txn_type)
            query += " ORDER BY date DESC"
            rows = conn.execute(query, params).fetchall()
            return [self._row_to_txn(r) for r in rows]
        finally:
            conn.close()

    def get_summary(self, start_date: str | None = None,
                    end_date: str | None = None) -> dict:
        """Return earnings/expense totals and by-category breakdown."""
        txns = self.get_transactions(start_date, end_date)
        earned = sum(t.amount for t in txns if t.type == "income")
        spent = sum(t.amount for t in txns if t.type == "expense")
        by_category: dict[str, float] = {}
        for t in txns:
            by_category[t.category] = by_category.get(t.category, 0) + t.amount
        return {
            "earned": earned,
            "spent": spent,
            "net": earned - spent,
            "by_category": by_category,
            "count": len(txns),
        }

    def get_all_time_earned(self) -> float:
        """Total income across all time."""
        conn = get_connection()
        try:
            row = conn.execute(
                "SELECT COALESCE(SUM(amount), 0) as total FROM transactions "
                "WHERE deleted=0 AND type='income'"
            ).fetchone()
            return row["total"]
        finally:
            conn.close()

    def _upsert(self, txn: Transaction):
        conn = get_connection()
        try:
            conn.execute(
                """INSERT INTO transactions (id, date, amount, type, category,
                   description, updated_at, deleted)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(id) DO UPDATE SET
                   date=excluded.date, amount=excluded.amount, type=excluded.type,
                   category=excluded.category, description=excluded.description,
                   updated_at=excluded.updated_at, deleted=excluded.deleted""",
                (txn.id, txn.date, txn.amount, txn.type, txn.category,
                 txn.description, txn.updated_at, int(txn.deleted)),
            )
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def _row_to_txn(row) -> Transaction:
        return Transaction(
            id=row["id"], date=row["date"], amount=row["amount"],
            type=row["type"], category=row["category"],
            description=row["description"], updated_at=row["updated_at"],
            deleted=bool(row["deleted"]),
        )

```

### `src\data\holidays_jp.py`

```python
"""Japanese national holidays calculator.

Covers all 16 national holidays defined by Japanese law, including
substitute holidays (振替休日) and special rules for vernal/autumnal equinox.
"""

from datetime import date, timedelta


def _vernal_equinox_day(year: int) -> int:
    """Approximate day of vernal equinox (春分の日) for a given year."""
    if year <= 1947:
        return 21
    if year <= 1979:
        return int(20.8357 + 0.242194 * (year - 1980) - int((year - 1983) / 4))
    if year <= 2099:
        return int(20.8431 + 0.242194 * (year - 1980) - int((year - 1980) / 4))
    return 21


def _autumnal_equinox_day(year: int) -> int:
    """Approximate day of autumnal equinox (秋分の日) for a given year."""
    if year <= 1947:
        return 23
    if year <= 1979:
        return int(23.2588 + 0.242194 * (year - 1980) - int((year - 1983) / 4))
    if year <= 2099:
        return int(23.2488 + 0.242194 * (year - 1980) - int((year - 1980) / 4))
    return 23


def _monday_of_week(year: int, month: int, nth: int) -> date:
    """Return the nth Monday of a given month (1-indexed)."""
    first = date(year, month, 1)
    # Days until first Monday
    offset = (7 - first.weekday()) % 7
    first_monday = first + timedelta(days=offset)
    return first_monday + timedelta(weeks=nth - 1)


def get_japanese_holidays(year: int) -> dict[date, str]:
    """Return a dict mapping date -> holiday name for a given year.

    All holiday names are provided in English with Japanese in parentheses.
    """
    holidays: dict[date, str] = {}

    # Fixed-date holidays
    holidays[date(year, 1, 1)] = "New Year's Day (元日)"
    holidays[date(year, 2, 11)] = "National Foundation Day (建国記念の日)"
    holidays[date(year, 2, 23)] = "Emperor's Birthday (天皇誕生日)"
    holidays[date(year, 4, 29)] = "Shōwa Day (昭和の日)"
    holidays[date(year, 5, 3)] = "Constitution Memorial Day (憲法記念日)"
    holidays[date(year, 5, 4)] = "Greenery Day (みどりの日)"
    holidays[date(year, 5, 5)] = "Children's Day (こどもの日)"
    holidays[date(year, 8, 11)] = "Mountain Day (山の日)"
    holidays[date(year, 11, 3)] = "Culture Day (文化の日)"
    holidays[date(year, 11, 23)] = "Labour Thanksgiving Day (勤労感謝の日)"

    # Happy Monday holidays (moved to specific Mondays)
    holidays[_monday_of_week(year, 1, 2)] = "Coming of Age Day (成人の日)"
    holidays[_monday_of_week(year, 7, 3)] = "Marine Day (海の日)"
    holidays[_monday_of_week(year, 9, 3)] = "Respect for the Aged Day (敬老の日)"
    holidays[_monday_of_week(year, 10, 2)] = "Sports Day (スポーツの日)"

    # Equinox days
    ve_day = _vernal_equinox_day(year)
    holidays[date(year, 3, ve_day)] = "Vernal Equinox Day (春分の日)"

    ae_day = _autumnal_equinox_day(year)
    holidays[date(year, 9, ae_day)] = "Autumnal Equinox Day (秋分の日)"

    # Substitute holidays (振替休日):
    # If a holiday falls on Sunday, the next non-holiday weekday is a holiday.
    substitute: dict[date, str] = {}
    for d, name in sorted(holidays.items()):
        if d.weekday() == 6:  # Sunday
            sub = d + timedelta(days=1)
            while sub in holidays or sub in substitute:
                sub += timedelta(days=1)
            substitute[sub] = f"Substitute Holiday ({name})"

    holidays.update(substitute)

    # Citizen's Holiday (国民の休日):
    # If a day is sandwiched between two holidays, it becomes a holiday.
    all_dates = sorted(holidays.keys())
    for i in range(len(all_dates) - 1):
        d1, d2 = all_dates[i], all_dates[i + 1]
        if (d2 - d1).days == 2:
            between = d1 + timedelta(days=1)
            if between not in holidays and between.weekday() != 6:
                holidays[between] = "Citizen's Holiday (国民の休日)"

    return holidays


def is_japanese_holiday(d: date) -> str | None:
    """Return holiday name if the date is a Japanese national holiday, else None."""
    holidays = get_japanese_holidays(d.year)
    return holidays.get(d)

```

### `src\data\notes_store.py`

```python
"""File-based notes storage — Obsidian-compatible markdown files."""

import re
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

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
        """List all .md files under the notes directory, skipping hidden dirs."""
        notes = []
        for md_file in sorted(self.root.rglob("*.md")):
            rel = md_file.relative_to(self.root)
            # Skip hidden directories like .obsidian, .trash, etc.
            if any(part.startswith(".") for part in rel.parts):
                continue
            notes.append(self._load_note(md_file))
        return notes

    def get_note(self, rel_path: str) -> Note | None:
        # Convert posix-style path to OS-native for file access
        full = self.root / Path(rel_path.replace("\\", "/"))
        if full.exists():
            return self._load_note(full)
        return None

    def save_note(self, note: Note):
        # Convert posix-style path to OS-native for file access
        full = self.root / Path(str(note.path).replace("\\", "/"))
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(note.content, encoding="utf-8")

    def delete_note(self, rel_path: str):
        full = self.root / Path(rel_path.replace("\\", "/"))
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
        # Always store relative path with forward slashes for cross-platform consistency
        rel = PurePosixPath(full_path.relative_to(self.root))
        return Note(title=title, content=content, path=rel, tags=tags)

    @staticmethod
    def _extract_tags(content: str) -> list[str]:
        """Extract #tags from markdown content."""
        # Match #tag but not inside code blocks or headings
        return list(set(re.findall(r'(?<!\w)#([a-zA-Z0-9_/-]+)', content)))

```

### `src\data\todo_store.py`

```python
"""Todo/task storage backed by SQLite."""

import uuid
from dataclasses import dataclass

from src.data.database import get_connection
from src.utils.timestamps import now_utc


PRIORITY_LABELS = {0: "None", 1: "Low", 2: "Medium", 3: "High"}
DEFAULT_TODO_CATEGORIES = [
    "Personal", "Work", "Freelance", "Errand", "Health",
    "Learning", "Project", "Urgent",
]


@dataclass
class TodoItem:
    id: str
    title: str
    done: bool = False
    priority: int = 0      # 0=none, 1=low, 2=med, 3=high
    due_date: str = ""     # YYYY-MM-DD or ""
    category: str = ""
    notes: str = ""
    created_at: str = ""
    updated_at: str = ""
    deleted: bool = False


class TodoStore:

    def add(self, title: str, priority: int = 0, due_date: str = "",
            category: str = "", notes: str = "") -> TodoItem:
        now = now_utc()
        item = TodoItem(
            id=str(uuid.uuid4()), title=title, priority=priority,
            due_date=due_date, category=category, notes=notes,
            created_at=now, updated_at=now,
        )
        self._upsert(item)
        return item

    def update(self, item: TodoItem) -> TodoItem:
        item.updated_at = now_utc()
        self._upsert(item)
        return item

    def toggle_done(self, item_id: str) -> bool:
        conn = get_connection()
        try:
            row = conn.execute("SELECT done FROM todos WHERE id=?", (item_id,)).fetchone()
            if row is None:
                return False
            new_val = 0 if row["done"] else 1
            conn.execute(
                "UPDATE todos SET done=?, updated_at=? WHERE id=?",
                (new_val, now_utc(), item_id),
            )
            conn.commit()
            return bool(new_val)
        finally:
            conn.close()

    def delete(self, item_id: str):
        conn = get_connection()
        try:
            conn.execute(
                "UPDATE todos SET deleted=1, updated_at=? WHERE id=?",
                (now_utc(), item_id),
            )
            conn.commit()
        finally:
            conn.close()

    def get_all(self, include_done: bool = True) -> list[TodoItem]:
        conn = get_connection()
        try:
            query = "SELECT * FROM todos WHERE deleted=0"
            if not include_done:
                query += " AND done=0"
            query += " ORDER BY done ASC, priority DESC, due_date ASC, created_at DESC"
            rows = conn.execute(query).fetchall()
            return [self._row_to_item(r) for r in rows]
        finally:
            conn.close()

    def get_counts(self) -> dict:
        conn = get_connection()
        try:
            total = conn.execute("SELECT COUNT(*) as c FROM todos WHERE deleted=0").fetchone()["c"]
            done = conn.execute("SELECT COUNT(*) as c FROM todos WHERE deleted=0 AND done=1").fetchone()["c"]
            return {"total": total, "done": done, "pending": total - done}
        finally:
            conn.close()

    def _upsert(self, item: TodoItem):
        conn = get_connection()
        try:
            conn.execute(
                """INSERT INTO todos (id, title, done, priority, due_date, category,
                   notes, created_at, updated_at, deleted)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(id) DO UPDATE SET
                   title=excluded.title, done=excluded.done, priority=excluded.priority,
                   due_date=excluded.due_date, category=excluded.category,
                   notes=excluded.notes, updated_at=excluded.updated_at,
                   deleted=excluded.deleted""",
                (item.id, item.title, int(item.done), item.priority,
                 item.due_date, item.category, item.notes,
                 item.created_at, item.updated_at, int(item.deleted)),
            )
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def _row_to_item(row) -> TodoItem:
        return TodoItem(
            id=row["id"], title=row["title"], done=bool(row["done"]),
            priority=row["priority"], due_date=row["due_date"] or "",
            category=row["category"] or "", notes=row["notes"] or "",
            created_at=row["created_at"], updated_at=row["updated_at"],
            deleted=bool(row["deleted"]),
        )

```

### `src\sync\__init__.py`

```python
"""LAN sync engine for peer-to-peer data synchronization."""

from src.sync.engine import SyncEngine

__all__ = ["SyncEngine"]

```

### `src\sync\deletion_manifest.py`

```python
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
    """
    if vault is None:
        vault = get_vault_path()
    if vault is None:
        return

    entries = read_manifest(vault)
    existing_paths = {d["path"] for d in entries}
    now = time.time()

    if rel_posix not in existing_paths:
        entries.append({"path": rel_posix, "deleted_at": now})
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

```

### `src\sync\engine.py`

```python
"""LAN mesh sync engine — subnet scanning, peer discovery, and data exchange.

How it works:
1. DISCOVERY: On each cycle, actively scans the local /24 subnet by attempting
   a fast TCP connect to the sync port on every host. Also listens for UDP
   broadcast announcements from other instances. This two-pronged approach
   means peers find each other automatically on the LAN.

2. SYNC: For each discovered peer, opens a TCP connection, exchanges full data
   sets (events, transactions, notes), and merges using last-write-wins on
   the updated_at timestamp. Soft-deleted records are propagated.

3. MESH: Every node is both client and server. There's no central coordinator.
   Any two nodes that can reach each other will converge.

Designed for your setup:
  Desktop (Windows) 192.168.0.4  <-->  Laptop (Linux) 192.168.0.28
  Both on the same 192.168.0.0/24 subnet.
"""

import json
import logging
import socket
import struct
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path, PurePosixPath

from PyQt6.QtCore import QThread, pyqtSignal

from src.config import load_config, NOTES_DIR
from src.data.database import get_connection
from src.utils.timestamps import now_utc
from src.sync.deletion_manifest import (
    read_manifest as _read_vault_manifest,
    record_deletion as _record_vault_del,
    remove_deletion as _remove_vault_del,
)

logger = logging.getLogger(__name__)

SYNC_MAGIC = b"LSYNC2"
PROTOCOL_VERSION = 2


class PeerInfo:
    """Tracks a discovered peer and its health."""

    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.last_seen: float = time.time()
        self.last_sync: float = 0
        self.fail_count: int = 0
        self.hostname: str = ""

    @property
    def is_stale(self) -> bool:
        return time.time() - self.last_seen > 600  # 10 min without contact

    def __repr__(self):
        return f"Peer({self.ip}:{self.port})"


class SyncEngine(QThread):
    """Background mesh sync thread."""

    # Signals for the UI
    status_changed = pyqtSignal(str)          # Human-readable status
    sync_completed = pyqtSignal()             # Fired after a successful sync cycle
    peer_discovered = pyqtSignal(str)         # IP of a newly found peer
    peer_lost = pyqtSignal(str)               # IP of a peer that went stale
    peers_updated = pyqtSignal(list)          # Full peer list [{"ip":..., "status":...}, ...]
    sync_log = pyqtSignal(str)                # Detailed log line for the network panel

    def __init__(self, parent=None):
        super().__init__(parent)
        self.cfg = load_config()
        self.sync_port: int = self.cfg.get("sync_port", 42069)
        self.discovery_port: int = self.cfg.get("discovery_port", 42070)
        self.interval: int = self.cfg.get("sync_interval_seconds", 300)
        self.subnet: str = self.cfg.get("subnet", "192.168.0")
        self.scan_start: int = self.cfg.get("scan_range_start", 1)
        self.scan_end: int = self.cfg.get("scan_range_end", 254)
        self.scan_threads: int = self.cfg.get("scan_threads", 20)
        self.scan_timeout: float = self.cfg.get("scan_timeout_ms", 150) / 1000.0

        self._running = True
        self._peers: dict[str, PeerInfo] = {}  # ip -> PeerInfo
        self._lock = threading.Lock()

        # Seed known peers from config
        for ip in self.cfg.get("known_peers", []):
            self._peers[ip] = PeerInfo(ip, self.sync_port)

    # ── Main loop ──────────────────────────────────────

    def run(self):
        # Start background listeners
        threading.Thread(target=self._discovery_listener, daemon=True).start()
        threading.Thread(target=self._sync_server, daemon=True).start()

        self._log("Sync engine started")
        self._log(f"Scanning subnet {self.subnet}.0/24 on port {self.sync_port}")
        self._log(f"Sync interval: {self.interval}s")

        while self._running:
            try:
                # Phase 1: Discover peers
                self.status_changed.emit("scanning...")
                self._broadcast_presence()
                self._scan_subnet()
                self._prune_stale_peers()
                self._emit_peer_list()

                # Phase 2: Sync with each peer
                alive_peers = self._get_alive_peers()
                if alive_peers:
                    self.status_changed.emit(f"syncing with {len(alive_peers)} peer(s)...")
                    synced = 0
                    for peer in alive_peers:
                        try:
                            self._sync_with_peer(peer)
                            peer.last_sync = time.time()
                            peer.fail_count = 0
                            synced += 1
                            self._log(f"Synced with {peer.ip}")
                        except Exception as e:
                            peer.fail_count += 1
                            self._log(f"Sync failed with {peer.ip}: {e}")
                            logger.warning(f"Sync with {peer.ip} failed: {e}")

                    self.status_changed.emit(
                        f"synced ({synced}/{len(alive_peers)} peers)"
                    )
                    self.sync_completed.emit()
                else:
                    self.status_changed.emit("no peers on network")
                    self._log("No peers found this cycle")

            except Exception as e:
                logger.error(f"Sync loop error: {e}")
                self.status_changed.emit(f"error: {e}")
                self._log(f"ERROR: {e}")

            # Interruptible sleep
            for _ in range(self.interval):
                if not self._running:
                    break
                time.sleep(1)

        self._log("Sync engine stopped")

    def stop(self):
        self._running = False

    def force_sync(self):
        """Trigger an immediate sync cycle (called from UI)."""
        # Just interrupt the sleep by setting a flag — next iteration runs immediately
        # We achieve this by starting a one-shot thread
        threading.Thread(target=self._force_sync_once, daemon=True).start()

    def _force_sync_once(self):
        self.status_changed.emit("force syncing...")
        self._broadcast_presence()
        self._scan_subnet()
        for peer in self._get_alive_peers():
            try:
                self._sync_with_peer(peer)
                peer.last_sync = time.time()
                peer.fail_count = 0
                self._log(f"Force-synced with {peer.ip}")
            except Exception as e:
                self._log(f"Force-sync failed with {peer.ip}: {e}")
        self._emit_peer_list()
        self.status_changed.emit("idle")
        self.sync_completed.emit()

    def trigger_vault_sync(self):
        """Called by the vault watcher when local vault files changed.

        Immediately syncs with all known peers so the changes propagate.
        """
        threading.Thread(target=self._vault_sync_once, daemon=True).start()

    def _vault_sync_once(self):
        self._log("Vault change detected — pushing to peers")
        self.status_changed.emit("vault changed, syncing...")
        peers = self._get_alive_peers()
        synced = 0
        for peer in peers:
            try:
                self._sync_with_peer(peer)
                peer.last_sync = time.time()
                peer.fail_count = 0
                synced += 1
                self._log(f"Vault sync pushed to {peer.ip}")
            except Exception as e:
                peer.fail_count += 1
                self._log(f"Vault sync to {peer.ip} failed: {e}")
        if synced:
            self.status_changed.emit(f"vault synced ({synced} peer{'s' if synced != 1 else ''})")
        else:
            self.status_changed.emit("vault changed (no peers)")
        self.sync_completed.emit()

    def add_manual_peer(self, ip: str):
        """Add a peer IP manually (from the network settings dialog)."""
        with self._lock:
            if ip not in self._peers:
                self._peers[ip] = PeerInfo(ip, self.sync_port)
                self._log(f"Manually added peer: {ip}")
                self.peer_discovered.emit(ip)
        self._emit_peer_list()

    def reload_config(self):
        """Reload config after settings change."""
        self.cfg = load_config()
        self.subnet = self.cfg.get("subnet", "192.168.0")
        self.interval = self.cfg.get("sync_interval_seconds", 300)
        self.sync_port = self.cfg.get("sync_port", 42069)
        self.scan_timeout = self.cfg.get("scan_timeout_ms", 150) / 1000.0
        self._log(f"Config reloaded — subnet={self.subnet}, interval={self.interval}s")

    # ── Subnet scanning ────────────────────────────────

    def _scan_subnet(self):
        """Actively probe every host in the /24 subnet for our sync port."""
        my_ips = self._get_local_ips()
        targets = [
            f"{self.subnet}.{i}"
            for i in range(self.scan_start, self.scan_end + 1)
            if f"{self.subnet}.{i}" not in my_ips
        ]

        found = []
        with ThreadPoolExecutor(max_workers=self.scan_threads) as pool:
            futures = {
                pool.submit(self._probe_host, ip): ip
                for ip in targets
            }
            for future in as_completed(futures):
                ip = futures[future]
                try:
                    if future.result():
                        found.append(ip)
                except Exception:
                    pass

        with self._lock:
            for ip in found:
                if ip not in self._peers:
                    self._peers[ip] = PeerInfo(ip, self.sync_port)
                    self._log(f"Discovered peer: {ip}")
                    self.peer_discovered.emit(ip)
                else:
                    self._peers[ip].last_seen = time.time()

    def _probe_host(self, ip: str) -> bool:
        """Try a fast TCP connect to see if a peer is listening on sync_port."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.scan_timeout)
            result = sock.connect_ex((ip, self.sync_port))
            sock.close()
            return result == 0
        except Exception:
            return False

    # ── UDP broadcast discovery (supplement to scanning) ──

    def _broadcast_presence(self):
        """Announce ourselves on the LAN via UDP broadcast."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.settimeout(1)
            hostname = socket.gethostname()[:32]
            payload = (
                SYNC_MAGIC
                + struct.pack("!HB", self.sync_port, PROTOCOL_VERSION)
                + hostname.encode("utf-8")
            )
            sock.sendto(payload, ("<broadcast>", self.discovery_port))
            sock.close()
        except Exception as e:
            logger.debug(f"Broadcast failed: {e}")

    def _discovery_listener(self):
        """Listen for UDP peer announcements."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(("", self.discovery_port))
            sock.settimeout(5)
        except Exception as e:
            logger.error(f"Discovery listener bind failed: {e}")
            self._log(f"Discovery listener failed: {e}")
            return

        my_ips = self._get_local_ips()
        while self._running:
            try:
                data, addr = sock.recvfrom(1024)
                if len(data) >= 9 and data[:6] == SYNC_MAGIC and addr[0] not in my_ips:
                    peer_port = struct.unpack("!H", data[6:8])[0]
                    _version = data[8]
                    hostname = data[9:].decode("utf-8", errors="replace")
                    ip = addr[0]
                    with self._lock:
                        if ip not in self._peers:
                            self._peers[ip] = PeerInfo(ip, peer_port)
                            self._log(f"Broadcast discovery: {ip} ({hostname})")
                            self.peer_discovered.emit(ip)
                        self._peers[ip].last_seen = time.time()
                        self._peers[ip].hostname = hostname
            except socket.timeout:
                continue
            except Exception as e:
                logger.debug(f"Discovery error: {e}")

    # ── Sync server (accept incoming connections) ──────

    def _sync_server(self):
        """TCP server that accepts sync requests from peers."""
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(("0.0.0.0", self.sync_port))
            server.listen(5)
            server.settimeout(5)
            self._log(f"Sync server listening on port {self.sync_port}")
        except Exception as e:
            logger.error(f"Sync server bind failed: {e}")
            self._log(f"FAILED to bind sync server on port {self.sync_port}: {e}")
            return

        while self._running:
            try:
                conn, addr = server.accept()
                threading.Thread(
                    target=self._handle_incoming, args=(conn, addr), daemon=True
                ).start()
            except socket.timeout:
                continue
            except Exception as e:
                logger.debug(f"Server accept error: {e}")

    def _handle_incoming(self, conn: socket.socket, addr: tuple):
        """Handle an incoming sync connection from a peer."""
        peer_ip = addr[0]
        try:
            msg = self._recv_json(conn)
            if not msg:
                return
            if msg.get("type") == "sync_request" and msg.get("version") == PROTOCOL_VERSION:
                # Register this peer if unknown
                with self._lock:
                    if peer_ip not in self._peers:
                        self._peers[peer_ip] = PeerInfo(peer_ip, self.sync_port)
                        self.peer_discovered.emit(peer_ip)
                    self._peers[peer_ip].last_seen = time.time()

                # Send our data back
                our_data = self._gather_local_data()
                self._send_json(conn, {
                    "type": "sync_response",
                    "version": PROTOCOL_VERSION,
                    "data": our_data,
                })
                # Merge their data into ours
                their_data = msg.get("data", {})
                changes = self._merge_remote_data(their_data)
                if changes:
                    self._log(f"Received {changes} change(s) from {peer_ip}")
                self.sync_completed.emit()
            elif msg.get("type") == "ping":
                self._send_json(conn, {"type": "pong", "hostname": socket.gethostname()})
        except Exception as e:
            logger.warning(f"Incoming sync error from {peer_ip}: {e}")
        finally:
            conn.close()

    # ── Sync client (outbound to a peer) ───────────────

    def _sync_with_peer(self, peer: PeerInfo):
        """Initiate a sync exchange with a specific peer."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(15)
        try:
            sock.connect((peer.ip, peer.port))
            our_data = self._gather_local_data()
            self._send_json(sock, {
                "type": "sync_request",
                "version": PROTOCOL_VERSION,
                "data": our_data,
            })
            response = self._recv_json(sock)
            if response and response.get("type") == "sync_response":
                changes = self._merge_remote_data(response.get("data", {}))
                if changes:
                    self._log(f"Merged {changes} change(s) from {peer.ip}")
        finally:
            sock.close()

    def ping_peer(self, ip: str) -> tuple[bool, str]:
        """Ping a specific peer. Returns (reachable, hostname_or_error)."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((ip, self.sync_port))
            self._send_json(sock, {"type": "ping"})
            resp = self._recv_json(sock)
            sock.close()
            if resp and resp.get("type") == "pong":
                return True, resp.get("hostname", ip)
            return True, ip
        except Exception as e:
            return False, str(e)

    # ── Data gathering & merging ───────────────────────

    def _gather_local_data(self) -> dict:
        conn = get_connection()
        try:
            events = [dict(r) for r in conn.execute("SELECT * FROM events").fetchall()]
            transactions = [dict(r) for r in conn.execute("SELECT * FROM transactions").fetchall()]
            todos = [dict(r) for r in conn.execute("SELECT * FROM todos").fetchall()]
            # Activities — may not exist in older DBs
            try:
                activities = [dict(r) for r in conn.execute("SELECT * FROM activities").fetchall()]
            except Exception:
                activities = []
            # Birthdays — may not exist in older DBs
            try:
                birthdays = [dict(r) for r in conn.execute("SELECT * FROM birthdays").fetchall()]
            except Exception:
                birthdays = []
        finally:
            conn.close()

        cfg = load_config()

        # Gather notes from configured notes dir (built-in notes)
        notes = []
        notes_dir = Path(cfg.get("notes_dir", str(NOTES_DIR)))
        if notes_dir.exists():
            for md in notes_dir.rglob("*.md"):
                rel = md.relative_to(notes_dir)
                if any(part.startswith(".") for part in rel.parts):
                    continue
                # Always use forward slashes for cross-platform compatibility
                rel_posix = str(PurePosixPath(rel))
                try:
                    mtime = md.stat().st_mtime
                    content = md.read_text(encoding="utf-8")
                    notes.append({"path": rel_posix, "mtime": mtime, "content": content})
                except OSError:
                    pass

        # Gather Obsidian vault files if configured
        vault_notes = []
        vault_existing_paths = set()  # track what exists for deletion manifest
        vault_path = cfg.get("obsidian_vault_path", "")
        if vault_path:
            vault_dir = Path(vault_path)
            if vault_dir.exists():
                for md in vault_dir.rglob("*.md"):
                    rel = md.relative_to(vault_dir)
                    # Skip hidden dirs (.obsidian, .trash, etc.)
                    if any(p.startswith(".") for p in rel.parts):
                        continue
                    # Always use forward slashes for cross-platform compatibility
                    rel_posix = str(PurePosixPath(rel))
                    vault_existing_paths.add(rel_posix)
                    try:
                        mtime = md.stat().st_mtime
                        content = md.read_text(encoding="utf-8")
                        vault_notes.append({"path": rel_posix, "mtime": mtime, "content": content})
                    except OSError:
                        pass

        # Build deletion manifest — files we know were deleted locally
        vault_deletions = self._get_vault_deletions(vault_path)

        return {
            "events": events, "transactions": transactions,
            "todos": todos, "activities": activities,
            "birthdays": birthdays,
            "notes": notes, "vault_notes": vault_notes,
            "vault_deletions": vault_deletions,
        }

    def _get_vault_deletions(self, vault_path: str) -> list[dict]:
        """Read the deletion manifest for vault files."""
        if not vault_path:
            return []
        return _read_vault_manifest(Path(vault_path))

    def _record_vault_deletion(self, vault_path: str, rel_posix: str):
        """Record a file deletion in the vault manifest."""
        if not vault_path:
            return
        _record_vault_del(rel_posix, Path(vault_path))

    def _merge_remote_data(self, remote: dict) -> int:
        """Merge remote data. Returns count of changes applied."""
        changes = 0
        conn = get_connection()
        try:
            for rev in remote.get("events", []):
                local = conn.execute(
                    "SELECT updated_at FROM events WHERE id=?", (rev["id"],)
                ).fetchone()
                if local is None or rev["updated_at"] > local["updated_at"]:
                    conn.execute(
                        """INSERT INTO events (id, title, description, start_time, end_time,
                           all_day, color, updated_at, deleted, recurrence, category)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                           ON CONFLICT(id) DO UPDATE SET
                           title=excluded.title, description=excluded.description,
                           start_time=excluded.start_time, end_time=excluded.end_time,
                           all_day=excluded.all_day, color=excluded.color,
                           updated_at=excluded.updated_at, deleted=excluded.deleted,
                           recurrence=excluded.recurrence, category=excluded.category""",
                        (rev["id"], rev["title"], rev["description"],
                         rev["start_time"], rev["end_time"], rev["all_day"],
                         rev["color"], rev["updated_at"], rev["deleted"],
                         rev.get("recurrence", ""), rev.get("category", "")),
                    )
                    changes += 1

            for rtx in remote.get("transactions", []):
                local = conn.execute(
                    "SELECT updated_at FROM transactions WHERE id=?", (rtx["id"],)
                ).fetchone()
                if local is None or rtx["updated_at"] > local["updated_at"]:
                    conn.execute(
                        """INSERT INTO transactions (id, date, amount, type, category,
                           description, updated_at, deleted)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                           ON CONFLICT(id) DO UPDATE SET
                           date=excluded.date, amount=excluded.amount, type=excluded.type,
                           category=excluded.category, description=excluded.description,
                           updated_at=excluded.updated_at, deleted=excluded.deleted""",
                        (rtx["id"], rtx["date"], rtx["amount"], rtx["type"],
                         rtx["category"], rtx["description"],
                         rtx["updated_at"], rtx["deleted"]),
                    )
                    changes += 1

            # Merge activities
            for ra in remote.get("activities", []):
                try:
                    local = conn.execute(
                        "SELECT updated_at FROM activities WHERE id=?", (ra["id"],)
                    ).fetchone()
                    if local is None or ra["updated_at"] > local["updated_at"]:
                        conn.execute(
                            """INSERT INTO activities (id, date, activity, start_time, end_time,
                               notes, created_at, updated_at, deleted)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                               ON CONFLICT(id) DO UPDATE SET
                               date=excluded.date, activity=excluded.activity,
                               start_time=excluded.start_time, end_time=excluded.end_time,
                               notes=excluded.notes, updated_at=excluded.updated_at,
                               deleted=excluded.deleted""",
                            (ra["id"], ra["date"], ra["activity"], ra["start_time"],
                             ra["end_time"], ra["notes"], ra["created_at"],
                             ra["updated_at"], ra["deleted"]),
                        )
                        changes += 1
                except Exception:
                    pass  # Gracefully handle if activities table doesn't exist on peer

            # Merge birthdays
            for rb in remote.get("birthdays", []):
                try:
                    local = conn.execute(
                        "SELECT updated_at FROM birthdays WHERE id=?", (rb["id"],)
                    ).fetchone()
                    if local is None or rb["updated_at"] > local["updated_at"]:
                        conn.execute(
                            """INSERT INTO birthdays (id, name, month, day, year,
                               updated_at, deleted)
                               VALUES (?, ?, ?, ?, ?, ?, ?)
                               ON CONFLICT(id) DO UPDATE SET
                               name=excluded.name, month=excluded.month,
                               day=excluded.day, year=excluded.year,
                               updated_at=excluded.updated_at,
                               deleted=excluded.deleted""",
                            (rb["id"], rb["name"], rb["month"], rb["day"],
                             rb.get("year"), rb["updated_at"], rb["deleted"]),
                        )
                        changes += 1
                except Exception:
                    pass  # Gracefully handle if birthdays table doesn't exist on peer

            # Merge todos
            for rt in remote.get("todos", []):
                local = conn.execute(
                    "SELECT updated_at FROM todos WHERE id=?", (rt["id"],)
                ).fetchone()
                if local is None or rt["updated_at"] > local["updated_at"]:
                    conn.execute(
                        """INSERT INTO todos (id, title, done, priority, due_date,
                           category, notes, created_at, updated_at, deleted)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                           ON CONFLICT(id) DO UPDATE SET
                           title=excluded.title, done=excluded.done,
                           priority=excluded.priority, due_date=excluded.due_date,
                           category=excluded.category, notes=excluded.notes,
                           updated_at=excluded.updated_at, deleted=excluded.deleted""",
                        (rt["id"], rt["title"], rt["done"], rt["priority"],
                         rt["due_date"], rt["category"], rt["notes"],
                         rt["created_at"], rt["updated_at"], rt["deleted"]),
                    )
                    changes += 1

            conn.commit()
        finally:
            conn.close()

        # Merge notes (built-in notes dir)
        cfg = load_config()
        notes_dir = Path(cfg.get("notes_dir", str(NOTES_DIR)))
        for rnote in remote.get("notes", []):
            # Normalize path — always convert to OS-native from posix
            rel_posix = rnote["path"].replace("\\", "/")
            local_path = notes_dir / Path(rel_posix)
            should_write = False
            if local_path.exists():
                if rnote["mtime"] > local_path.stat().st_mtime:
                    should_write = True
            else:
                should_write = True
            if should_write:
                local_path.parent.mkdir(parents=True, exist_ok=True)
                local_path.write_text(rnote["content"], encoding="utf-8")
                changes += 1

        # Merge Obsidian vault notes
        vault_path = cfg.get("obsidian_vault_path", "")
        if vault_path:
            vault_dir = Path(vault_path)

            # First, apply remote deletions — remove files the peer deleted
            for deletion in remote.get("vault_deletions", []):
                del_posix = deletion["path"].replace("\\", "/")
                del_time = deletion.get("deleted_at", 0)
                local_path = vault_dir / Path(del_posix)
                if local_path.exists():
                    # Only delete if the local file is older than the deletion
                    try:
                        local_mtime = local_path.stat().st_mtime
                        if del_time > local_mtime:
                            local_path.unlink()
                            changes += 1
                            self._log(f"Deleted vault file (remote deletion): {del_posix}")
                            # Also record locally so we don't re-create from other peers
                            self._record_vault_deletion(vault_path, del_posix)
                    except OSError as e:
                        logger.warning(f"Failed to delete {del_posix}: {e}")

            # Build set of remotely-deleted paths for this sync
            remote_deleted = {
                d["path"].replace("\\", "/")
                for d in remote.get("vault_deletions", [])
            }

            # Then, merge vault notes — create/update files
            for rnote in remote.get("vault_notes", []):
                rel_posix = rnote["path"].replace("\\", "/")
                # Skip if this file was deleted locally
                local_deletions = {
                    d["path"] for d in self._get_vault_deletions(vault_path)
                }
                if rel_posix in local_deletions:
                    # Check if remote mtime is newer than our deletion
                    local_del_time = 0
                    for d in self._get_vault_deletions(vault_path):
                        if d["path"] == rel_posix:
                            local_del_time = d.get("deleted_at", 0)
                            break
                    if rnote["mtime"] <= local_del_time:
                        continue  # Our deletion is newer, skip
                    # Remote edit is newer than our deletion — re-create
                    # Remove from deletion manifest
                    self._remove_vault_deletion(vault_path, rel_posix)

                local_path = vault_dir / Path(rel_posix)
                should_write = False
                if local_path.exists():
                    try:
                        if rnote["mtime"] > local_path.stat().st_mtime:
                            should_write = True
                    except OSError:
                        should_write = True
                else:
                    should_write = True
                if should_write:
                    local_path.parent.mkdir(parents=True, exist_ok=True)
                    local_path.write_text(rnote["content"], encoding="utf-8")
                    changes += 1

            # Clean up empty directories left after deletions
            if vault_dir.exists():
                self._cleanup_empty_dirs(vault_dir)

        return changes

    def _remove_vault_deletion(self, vault_path: str, rel_posix: str):
        """Remove a path from the deletion manifest (file was re-created remotely)."""
        if not vault_path:
            return
        _remove_vault_del(rel_posix, Path(vault_path))

    @staticmethod
    def _cleanup_empty_dirs(root: Path):
        """Remove empty subdirectories (bottom-up) after file deletions."""
        for dirpath in sorted(root.rglob("*"), reverse=True):
            if dirpath.is_dir() and dirpath != root:
                # Skip hidden dirs
                rel = dirpath.relative_to(root)
                if any(p.startswith(".") for p in rel.parts):
                    continue
                try:
                    if not any(dirpath.iterdir()):
                        dirpath.rmdir()
                except OSError:
                    pass

    # ── Peer management ────────────────────────────────

    def _get_alive_peers(self) -> list[PeerInfo]:
        with self._lock:
            return [p for p in self._peers.values() if not p.is_stale and p.fail_count < 5]

    def _prune_stale_peers(self):
        with self._lock:
            stale = [ip for ip, p in self._peers.items() if p.is_stale]
            for ip in stale:
                # Keep manually-added peers, just mark stale
                if ip in self.cfg.get("known_peers", []):
                    continue
                del self._peers[ip]
                self.peer_lost.emit(ip)
                self._log(f"Peer went stale: {ip}")

    def _emit_peer_list(self):
        with self._lock:
            peers = []
            for ip, p in self._peers.items():
                status = "stale" if p.is_stale else ("failing" if p.fail_count > 0 else "online")
                peers.append({
                    "ip": ip,
                    "hostname": p.hostname,
                    "status": status,
                    "last_seen": p.last_seen,
                    "last_sync": p.last_sync,
                    "fail_count": p.fail_count,
                })
            self.peers_updated.emit(peers)

    def get_peer_list(self) -> list[dict]:
        """Synchronous access to peer list for the settings dialog."""
        with self._lock:
            return [
                {"ip": ip, "hostname": p.hostname,
                 "status": "stale" if p.is_stale else "online",
                 "fail_count": p.fail_count}
                for ip, p in self._peers.items()
            ]

    # ── Network helpers ────────────────────────────────

    @staticmethod
    def _send_json(sock: socket.socket, obj: dict):
        data = json.dumps(obj).encode("utf-8")
        length = struct.pack("!I", len(data))
        sock.sendall(length + data)

    @staticmethod
    def _recv_json(sock: socket.socket) -> dict | None:
        raw_len = b""
        while len(raw_len) < 4:
            chunk = sock.recv(4 - len(raw_len))
            if not chunk:
                return None
            raw_len += chunk
        msg_len = struct.unpack("!I", raw_len)[0]
        if msg_len > 50_000_000:
            return None
        data = b""
        while len(data) < msg_len:
            chunk = sock.recv(min(65536, msg_len - len(data)))
            if not chunk:
                return None
            data += chunk
        return json.loads(data.decode("utf-8"))

    @staticmethod
    def _get_local_ips() -> set[str]:
        ips = {"127.0.0.1"}
        try:
            hostname = socket.gethostname()
            for info in socket.getaddrinfo(hostname, None, socket.AF_INET):
                ips.add(info[4][0])
        except Exception:
            pass
        # Also try connecting to an external address to find our LAN IP
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("192.168.0.1", 1))
            ips.add(s.getsockname()[0])
            s.close()
        except Exception:
            pass
        return ips

    def _log(self, msg: str):
        ts = time.strftime("%H:%M:%S")
        self.sync_log.emit(f"[{ts}] {msg}")
        logger.info(msg)

```

### `src\sync\vault_watcher.py`

```python
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

```

### `src\ui\__init__.py`

```python
"""UI layer — PyQt6 main window and module panels."""

from src.ui.main_window import MainWindow

__all__ = ["MainWindow"]

```

### `src\ui\main_window.py`

```python
"""Main application window with menu bar, sidebar, theme selector, and sync integration."""

from datetime import datetime

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QKeySequence, QShortcut, QAction
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QStackedWidget, QPushButton, QLabel, QFrame,
    QComboBox, QStatusBar, QMenuBar,
)

from src.config import APP_NAME, APP_VERSION, load_config, save_config
from src.ui.themes.styles import THEMES, PALETTES, get_theme_names
from src.ui.modules.notes_panel import NotesPanel
from src.ui.modules.calendar_panel import CalendarPanel
from src.ui.modules.finance_panel import FinancePanel
from src.ui.modules.todo_panel import TodoPanel
from src.ui.modules.dashboard_panel import DashboardPanel
from src.ui.modules.finance_charts import FinanceChartsPanel
from src.ui.modules.activity_panel import ActivityPanel


class SidebarButton(QPushButton):

    def __init__(self, text: str, icon_char: str = "", shortcut_hint: str = ""):
        display = f"{icon_char}  {text}"
        if shortcut_hint:
            display += f"   {shortcut_hint}"
        super().__init__(display)
        self.setCheckable(True)
        self.setFixedHeight(34)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def apply_colors(self, accent: str, accent_fg: str, hover: str):
        self.setStyleSheet(f"""
            QPushButton {{
                text-align: left;
                padding-left: 12px;
                border: none;
                border-radius: 6px;
                font-size: 12px;
            }}
            QPushButton:checked {{
                background-color: {accent};
                color: {accent_fg};
                font-weight: bold;
            }}
            QPushButton:hover:!checked {{
                background-color: {hover};
            }}
        """)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.cfg = load_config()
        self.sync_engine = None  # Set by main.py after construction
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.setMinimumSize(1000, 650)
        self.resize(1200, 750)

        self._build_menu_bar()
        self._build_central()
        self._build_status_bar()

        # Apply theme and default to Notes
        current_theme = self.cfg.get("theme", "Catppuccin Dark")
        if current_theme in ("dark", "light"):
            current_theme = "Catppuccin Dark" if current_theme == "dark" else "Catppuccin Light"
        self._apply_theme(current_theme)
        self._navigate("Dashboard")

    # ── Menu bar ───────────────────────────────────────

    def _build_menu_bar(self):
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")

        file_menu.addAction(self._action("&Dashboard", "Ctrl+1", lambda: self._navigate("Dashboard")))
        file_menu.addAction(self._action("&Notes", "Ctrl+2", lambda: self._navigate("Notes")))
        file_menu.addAction(self._action("&Calendar", "Ctrl+3", lambda: self._navigate("Calendar")))
        file_menu.addAction(self._action("&Earnings", "Ctrl+4", lambda: self._navigate("Earnings")))
        file_menu.addAction(self._action("&Charts", "Ctrl+5", lambda: self._navigate("Charts")))
        file_menu.addAction(self._action("&Tasks", "Ctrl+6", lambda: self._navigate("Tasks")))
        file_menu.addAction(self._action("&Activity", "Ctrl+7", lambda: self._navigate("Activity")))
        file_menu.addSeparator()
        file_menu.addAction(self._action("E&xit", "Ctrl+Q", self.close))

        # Sync menu
        sync_menu = menubar.addMenu("&Sync")
        sync_menu.addAction(self._action("Sync &Now", "Ctrl+Shift+S", self._force_sync))
        sync_menu.addAction(self._action("&Network Settings...", "Ctrl+Shift+N", self._open_network_dialog))

        # View menu
        view_menu = menubar.addMenu("&View")
        for theme_name in get_theme_names():
            view_menu.addAction(self._action(
                theme_name, "",
                lambda checked=False, t=theme_name: self._on_theme_changed(t),
            ))

        # Help menu
        help_menu = menubar.addMenu("&Help")
        help_menu.addAction(self._action("&About", "", self._show_about))

    def _action(self, text: str, shortcut: str, callback) -> QAction:
        act = QAction(text, self)
        if shortcut:
            act.setShortcut(QKeySequence(shortcut))
        act.triggered.connect(callback)
        return act

    # ── Central widget ─────────────────────────────────

    def _build_central(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ── Sidebar ──────────────────────────────────
        self.sidebar = QWidget()
        self.sidebar.setFixedWidth(190)
        self.sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(8, 10, 8, 10)
        sidebar_layout.setSpacing(3)

        app_label = QLabel(APP_NAME)
        app_label.setObjectName("sectionTitle")
        sidebar_layout.addWidget(app_label)

        version_label = QLabel(f"v{APP_VERSION}")
        version_label.setObjectName("subtitle")
        sidebar_layout.addWidget(version_label)

        sidebar_layout.addSpacing(8)
        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine)
        sidebar_layout.addWidget(sep)
        sidebar_layout.addSpacing(8)

        # Nav buttons
        self.nav_buttons: list[SidebarButton] = []
        nav_items = [
            ("Dashboard", "\U0001f4ca", "Ctrl+1"),
            ("Notes", "\U0001f4dd", "Ctrl+2"),
            ("Calendar", "\U0001f4c5", "Ctrl+3"),
            ("Earnings", "\U0001f4b0", "Ctrl+4"),
            ("Charts", "\U0001f4c8", "Ctrl+5"),
            ("Tasks", "\u2611", "Ctrl+6"),
            ("Activity", "\u23f1", "Ctrl+7"),
        ]
        for name, icon, shortcut_text in nav_items:
            btn = SidebarButton(name, icon, shortcut_text)
            btn.clicked.connect(lambda checked, n=name: self._navigate(n))
            btn.setToolTip(f"Switch to {name} ({shortcut_text})")
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append(btn)

            sc = QShortcut(QKeySequence(shortcut_text), self)
            sc.activated.connect(lambda n=name: self._navigate(n))

        sidebar_layout.addStretch()

        # Theme selector
        theme_label = QLabel("Theme")
        theme_label.setObjectName("subtitle")
        sidebar_layout.addWidget(theme_label)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(get_theme_names())
        current_theme = self.cfg.get("theme", "Catppuccin Dark")
        if current_theme in ("dark", "light"):
            current_theme = "Catppuccin Dark" if current_theme == "dark" else "Catppuccin Light"
        idx = self.theme_combo.findText(current_theme)
        if idx >= 0:
            self.theme_combo.setCurrentIndex(idx)
        self.theme_combo.currentTextChanged.connect(self._on_theme_changed)
        sidebar_layout.addWidget(self.theme_combo)

        sidebar_layout.addSpacing(8)

        # Network button
        net_btn = QPushButton("Network...")
        net_btn.setObjectName("secondary")
        net_btn.setToolTip("Open network & sync settings")
        net_btn.clicked.connect(self._open_network_dialog)
        sidebar_layout.addWidget(net_btn)

        sidebar_layout.addSpacing(4)

        # Sync status
        self.sync_label = QLabel("Sync: starting...")
        self.sync_label.setObjectName("subtitle")
        sidebar_layout.addWidget(self.sync_label)

        self.peer_count_label = QLabel("Peers: 0")
        self.peer_count_label.setObjectName("subtitle")
        sidebar_layout.addWidget(self.peer_count_label)

        main_layout.addWidget(self.sidebar)

        # ── Content stack ────────────────────────────
        self.stack = QStackedWidget()
        self.dashboard_panel = DashboardPanel()
        self.notes_panel = NotesPanel()
        self.calendar_panel = CalendarPanel()
        self.finance_panel = FinancePanel()
        self.charts_panel = FinanceChartsPanel()
        self.todo_panel = TodoPanel()
        self.activity_panel = ActivityPanel()

        self.stack.addWidget(self.dashboard_panel)   # 0
        self.stack.addWidget(self.notes_panel)       # 1
        self.stack.addWidget(self.calendar_panel)    # 2
        self.stack.addWidget(self.finance_panel)     # 3
        self.stack.addWidget(self.charts_panel)      # 4
        self.stack.addWidget(self.todo_panel)        # 5
        self.stack.addWidget(self.activity_panel)    # 6

        main_layout.addWidget(self.stack, 1)

    # ── Status bar ─────────────────────────────────────

    def _build_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.clock_label = QLabel()
        self.status_bar.addPermanentWidget(self.clock_label)
        self._update_clock()

        clock_timer = QTimer(self)
        clock_timer.timeout.connect(self._update_clock)
        clock_timer.start(30_000)

    def _update_clock(self):
        now = datetime.now()
        self.clock_label.setText(now.strftime("%A, %b %d  %H:%M"))

    # ── Navigation ─────────────────────────────────────

    def _navigate(self, name: str):
        idx_map = {
            "Dashboard": 0, "Notes": 1, "Calendar": 2,
            "Earnings": 3, "Charts": 4, "Tasks": 5, "Activity": 6,
        }
        idx = idx_map.get(name, 0)
        self.stack.setCurrentIndex(idx)
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == idx)
        self.status_bar.showMessage(f"  {name}", 2000)

    # ── Theming ────────────────────────────────────────

    def _on_theme_changed(self, theme_name: str):
        self.cfg["theme"] = theme_name
        save_config(self.cfg)
        self._apply_theme(theme_name)
        # Keep combo in sync (in case called from menu)
        idx = self.theme_combo.findText(theme_name)
        if idx >= 0:
            self.theme_combo.blockSignals(True)
            self.theme_combo.setCurrentIndex(idx)
            self.theme_combo.blockSignals(False)

    def _apply_theme(self, name: str):
        sheet = THEMES.get(name, THEMES["Catppuccin Dark"])
        palette = PALETTES.get(name, PALETTES["Catppuccin Dark"])
        self.setStyleSheet(sheet)
        self.sidebar.setStyleSheet(
            f"QWidget#sidebar {{ background-color: {palette['header_bg']}; }}"
        )
        for btn in self.nav_buttons:
            btn.apply_colors(palette["accent"], palette["accent_fg"], palette["hover"])
        if hasattr(self.finance_panel, 'set_palette'):
            self.finance_panel.set_palette(palette)
        if hasattr(self.calendar_panel, 'set_palette'):
            self.calendar_panel.set_palette(palette)
        if hasattr(self.todo_panel, 'set_palette'):
            self.todo_panel.set_palette(palette)
        if hasattr(self.dashboard_panel, 'set_palette'):
            self.dashboard_panel.set_palette(palette)
        if hasattr(self.charts_panel, 'set_palette'):
            self.charts_panel.set_palette(palette)
        if hasattr(self.activity_panel, 'set_palette'):
            self.activity_panel.set_palette(palette)

    # ── Sync integration ───────────────────────────────

    def set_sync_engine(self, engine):
        """Called by main.py to wire up the sync engine."""
        self.sync_engine = engine
        engine.status_changed.connect(self.set_sync_status)
        engine.peers_updated.connect(self._on_peers_updated)
        engine.sync_completed.connect(self._on_sync_completed)

    def _on_sync_completed(self):
        """Refresh all panels after incoming data has been merged."""
        if hasattr(self.notes_panel, '_refresh_list'):
            self.notes_panel._refresh_list()
        if hasattr(self.calendar_panel, '_refresh'):
            self.calendar_panel._refresh()
        if hasattr(self.finance_panel, '_refresh'):
            self.finance_panel._refresh()
        if hasattr(self.todo_panel, '_refresh'):
            self.todo_panel._refresh()
        if hasattr(self.dashboard_panel, '_refresh'):
            self.dashboard_panel._refresh()
        if hasattr(self.charts_panel, '_refresh'):
            self.charts_panel._refresh()
        if hasattr(self.activity_panel, '_refresh'):
            self.activity_panel._refresh()

    def set_sync_status(self, text: str):
        self.sync_label.setText(f"Sync: {text}")
        if "error" in text.lower():
            self.sync_label.setObjectName("statusWarn")
        else:
            self.sync_label.setObjectName("subtitle")
        self.sync_label.style().unpolish(self.sync_label)
        self.sync_label.style().polish(self.sync_label)

    def _on_peers_updated(self, peers: list):
        online = sum(1 for p in peers if p.get("status") == "online")
        total = len(peers)
        self.peer_count_label.setText(f"Peers: {online}/{total} online")

    def _force_sync(self):
        if self.sync_engine:
            self.sync_engine.force_sync()
            self.status_bar.showMessage("  Force sync triggered", 3000)

    def _open_network_dialog(self):
        from src.ui.widgets.network_dialog import NetworkDialog
        dlg = NetworkDialog(sync_engine=self.sync_engine, parent=self)
        dlg.exec()

    def _show_about(self):
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.about(
            self, f"About {APP_NAME}",
            f"<b>{APP_NAME}</b> v{APP_VERSION}<br><br>"
            f"Personal productivity app with LAN mesh sync.<br>"
            f"Notes \u2022 Calendar \u2022 Earnings \u2022 Tasks<br><br>"
            f"Syncs automatically over your home network.",
        )

```

### `src\ui\modules\__init__.py`

```python
"""Module panels for each app feature."""

from src.ui.modules.notes_panel import NotesPanel
from src.ui.modules.calendar_panel import CalendarPanel
from src.ui.modules.finance_panel import FinancePanel

__all__ = ["NotesPanel", "CalendarPanel", "FinancePanel"]

```

### `src\ui\modules\activity_panel.py`

```python
"""Activity Tracker panel — Gantt-style single-row day view with timer and manual input.

Tracks daily activities with start/end times. Primary input is via the live timer
(Start → Stop → Add), but manual time entry is always available.
Exports activities to the Obsidian vault.
"""

from datetime import date, datetime, timedelta
from pathlib import Path, PurePosixPath

from PyQt6.QtCore import Qt, QRectF, QPointF, QTimer, QTime
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QBrush, QMouseEvent
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QComboBox, QTimeEdit, QPlainTextEdit,
    QFrame, QScrollArea, QMessageBox, QSizePolicy,
)

from src.config import load_config
from src.data.activity_store import (
    ActivityStore, Activity, DEFAULT_ACTIVITIES, ACTIVITY_COLORS, DEFAULT_COLOR,
)


# Day view spans 0:00 to 30:00 (6 AM previous to noon next day conceptually,
# but we display 0-30 hours so users can log late-night activity)
DAY_START_HOUR = 0
DAY_END_HOUR = 30
HOUR_COUNT = DAY_END_HOUR - DAY_START_HOUR


class GanttBar:
    """Represents a single activity block on the Gantt chart."""

    def __init__(self, activity: Activity):
        self.activity = activity
        self.rect = QRectF()  # Set during painting


class GanttWidget(QWidget):
    """Custom-painted Gantt chart showing a single day's activities."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.bars: list[GanttBar] = []
        self.selected_bar: GanttBar | None = None
        self._palette: dict = {}
        self.setMinimumHeight(100)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(100)
        self.setMouseTracking(True)
        self._hover_bar: GanttBar | None = None
        self._on_select = None  # callback

    def set_palette(self, palette: dict):
        self._palette = palette
        self.update()

    def set_bars(self, activities: list[Activity]):
        self.bars = [GanttBar(a) for a in activities]
        self.selected_bar = None
        self.update()

    def set_on_select(self, callback):
        self._on_select = callback

    def _time_to_x(self, time_str: str, width: float, margin: float) -> float:
        """Convert HH:MM to x coordinate."""
        try:
            h, m = map(int, time_str.split(":"))
            total_minutes = h * 60 + m
            chart_width = width - 2 * margin
            return margin + (total_minutes / (HOUR_COUNT * 60)) * chart_width
        except (ValueError, AttributeError):
            return margin

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()
        margin_left = 40
        margin_right = 10
        margin_top = 18
        bar_height = 36
        chart_width = w - margin_left - margin_right

        bg = QColor(self._palette.get("bg", "#1e1e2e"))
        fg = QColor(self._palette.get("fg", "#cdd6f4"))
        grid_color = QColor(self._palette.get("border", "#45475a"))

        # Background
        painter.fillRect(0, 0, w, h, bg)

        # Hour grid lines and labels
        painter.setPen(QPen(grid_color, 1))
        label_font = QFont()
        label_font.setPixelSize(9)
        painter.setFont(label_font)

        for hour in range(DAY_START_HOUR, DAY_END_HOUR + 1):
            x = margin_left + (hour / HOUR_COUNT) * chart_width
            # Major lines every 6 hours, minor every hour
            if hour % 6 == 0:
                painter.setPen(QPen(grid_color, 1))
                painter.drawLine(QPointF(x, margin_top - 2), QPointF(x, margin_top + bar_height + 4))
                # Label
                display_h = hour % 24
                label = f"{display_h:02d}:00"
                painter.setPen(fg)
                painter.drawText(QRectF(x - 18, 0, 36, margin_top - 2),
                                 Qt.AlignmentFlag.AlignCenter, label)
            elif hour % 3 == 0:
                painter.setPen(QPen(grid_color, 1, Qt.PenStyle.DotLine))
                painter.drawLine(QPointF(x, margin_top), QPointF(x, margin_top + bar_height))

        # Track background
        track_rect = QRectF(margin_left, margin_top, chart_width, bar_height)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(grid_color.red(), grid_color.green(),
                                        grid_color.blue(), 80)))
        painter.drawRoundedRect(track_rect, 4, 4)

        # Activity bars
        for bar in self.bars:
            x1 = self._time_to_x(bar.activity.start_time, w, margin_left)
            x2 = self._time_to_x(bar.activity.end_time, w, margin_left)
            bar_w = max(x2 - x1, 2)
            bar.rect = QRectF(x1, margin_top + 2, bar_w, bar_height - 4)

            color = QColor(bar.activity.color)
            if bar == self.selected_bar:
                color = color.lighter(130)
            elif bar == self._hover_bar:
                color = color.lighter(115)

            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawRoundedRect(bar.rect, 3, 3)

            # Label inside bar if wide enough
            if bar_w > 40:
                painter.setPen(QColor("#11111b"))
                text_font = QFont()
                text_font.setPixelSize(10)
                text_font.setBold(True)
                painter.setFont(text_font)
                text_rect = bar.rect.adjusted(4, 0, -4, 0)
                painter.drawText(text_rect, Qt.AlignmentFlag.AlignVCenter |
                                 Qt.AlignmentFlag.AlignLeft,
                                 bar.activity.activity)

        # "Now" indicator if viewing today
        now = datetime.now()
        now_minutes = now.hour * 60 + now.minute
        if 0 <= now_minutes <= HOUR_COUNT * 60:
            now_x = margin_left + (now_minutes / (HOUR_COUNT * 60)) * chart_width
            painter.setPen(QPen(QColor("#f38ba8"), 2))
            painter.drawLine(QPointF(now_x, margin_top - 4),
                             QPointF(now_x, margin_top + bar_height + 4))

        # Bottom time summary
        total = sum(b.activity.duration_minutes for b in self.bars)
        hours = total // 60
        mins = total % 60
        painter.setPen(fg)
        summary_font = QFont()
        summary_font.setPixelSize(10)
        painter.setFont(summary_font)
        painter.drawText(QRectF(margin_left, margin_top + bar_height + 6,
                                chart_width, 20),
                         Qt.AlignmentFlag.AlignLeft,
                         f"Total tracked: {hours}h {mins}m")

        painter.end()

    def mousePressEvent(self, event: QMouseEvent):
        pos = event.position()
        clicked = None
        for bar in self.bars:
            if bar.rect.contains(pos):
                clicked = bar
                break
        self.selected_bar = clicked
        self.update()
        if self._on_select and clicked:
            self._on_select(clicked.activity)

    def mouseMoveEvent(self, event: QMouseEvent):
        pos = event.position()
        hover = None
        for bar in self.bars:
            if bar.rect.contains(pos):
                hover = bar
                break
        if hover != self._hover_bar:
            self._hover_bar = hover
            if hover:
                a = hover.activity
                self.setToolTip(
                    f"{a.activity}\n{a.start_time} – {a.end_time} "
                    f"({a.duration_minutes}m)\n{a.notes}" if a.notes
                    else f"{a.activity}\n{a.start_time} – {a.end_time} ({a.duration_minutes}m)"
                )
            else:
                self.setToolTip("")
            self.update()


class ActivityPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.store = ActivityStore()
        self._palette: dict = {}
        self._current_date = date.today()
        self._editing_activity: Activity | None = None
        self._active_timer: QTimer | None = None
        self._timer_start: datetime | None = None
        self._build_ui()
        self._refresh()

    def set_palette(self, palette: dict):
        self._palette = palette
        self.gantt.set_palette(palette)
        self._refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(10)

        # Header
        header = QHBoxLayout()
        title = QLabel("Activity Tracker")
        title.setObjectName("sectionTitle")
        header.addWidget(title)
        header.addStretch()

        btn_prev = QPushButton("\u25c0")
        btn_prev.setFixedSize(28, 28)
        btn_prev.clicked.connect(self._prev_day)
        header.addWidget(btn_prev)

        self.date_label = QLabel("")
        self.date_label.setStyleSheet("font-weight: bold; font-size: 13px;")
        header.addWidget(self.date_label)

        btn_next = QPushButton("\u25b6")
        btn_next.setFixedSize(28, 28)
        btn_next.clicked.connect(self._next_day)
        header.addWidget(btn_next)

        btn_today = QPushButton("Today")
        btn_today.setObjectName("secondary")
        btn_today.clicked.connect(self._go_today)
        header.addWidget(btn_today)

        layout.addLayout(header)

        # Gantt chart
        self.gantt = GanttWidget()
        self.gantt.set_on_select(self._on_bar_selected)
        layout.addWidget(self.gantt)

        # Input form — timer + quick entry
        form_frame = QFrame()
        form_frame.setStyleSheet(
            "QFrame { border: 1px solid palette(mid); border-radius: 6px; padding: 8px; }"
        )
        form_layout = QVBoxLayout(form_frame)
        form_layout.setContentsMargins(10, 8, 10, 8)
        form_layout.setSpacing(6)

        form_title = QLabel("Log Activity")
        form_title.setStyleSheet("font-weight: bold; font-size: 12px; border: none;")
        form_layout.addWidget(form_title)

        # Row 1: Activity + times
        row1 = QHBoxLayout()
        row1.setSpacing(8)

        self.activity_combo = QComboBox()
        self.activity_combo.setEditable(True)
        self.activity_combo.addItems(DEFAULT_ACTIVITIES)
        self.activity_combo.setMinimumWidth(140)
        self.activity_combo.setPlaceholderText("Activity...")
        row1.addWidget(QLabel("Activity:"))
        row1.addWidget(self.activity_combo, 1)

        row1.addWidget(QLabel("Start:"))
        self.start_edit = QTimeEdit()
        self.start_edit.setDisplayFormat("HH:mm")
        self.start_edit.setWrapping(True)
        now = datetime.now()
        self.start_edit.setTime(QTime(now.hour, 0))
        row1.addWidget(self.start_edit)

        row1.addWidget(QLabel("End:"))
        self.end_edit = QTimeEdit()
        self.end_edit.setDisplayFormat("HH:mm")
        self.end_edit.setWrapping(True)
        self.end_edit.setTime(QTime(min(now.hour + 1, 23), 0))
        row1.addWidget(self.end_edit)

        form_layout.addLayout(row1)

        # Row 2: Timer controls
        timer_row = QHBoxLayout()
        timer_row.setSpacing(8)

        self.timer_label = QLabel("\u23f1 00:00:00")
        self.timer_label.setStyleSheet(
            "font-size: 15px; font-weight: bold; font-family: monospace; border: none;"
        )
        self.timer_label.setMinimumWidth(110)
        timer_row.addWidget(self.timer_label)

        self.btn_start_timer = QPushButton("\u25b6 Start Timer")
        self.btn_start_timer.setStyleSheet(
            "background-color: #a6e3a1; color: #1e1e2e; font-weight: bold; border-radius: 4px;"
        )
        self.btn_start_timer.setFixedHeight(28)
        self.btn_start_timer.clicked.connect(self._start_timer)
        timer_row.addWidget(self.btn_start_timer)

        self.btn_stop_timer = QPushButton("\u25a0 Stop")
        self.btn_stop_timer.setStyleSheet(
            "background-color: #f38ba8; color: #1e1e2e; font-weight: bold; border-radius: 4px;"
        )
        self.btn_stop_timer.setFixedHeight(28)
        self.btn_stop_timer.setEnabled(False)
        self.btn_stop_timer.clicked.connect(self._stop_timer)
        timer_row.addWidget(self.btn_stop_timer)

        timer_row.addStretch()

        manual_hint = QLabel("or use manual Start/End times above")
        manual_hint.setObjectName("subtitle")
        manual_hint.setStyleSheet("font-size: 10px; font-style: italic; border: none;")
        timer_row.addWidget(manual_hint)

        form_layout.addLayout(timer_row)

        # Divider
        div = QFrame()
        div.setFrameShape(QFrame.Shape.HLine)
        div.setStyleSheet("border: none; border-top: 1px solid palette(mid);")
        form_layout.addWidget(div)

        # Row 3: Notes + buttons
        row3 = QHBoxLayout()
        row3.setSpacing(8)

        self.notes_edit = QPlainTextEdit()
        self.notes_edit.setPlaceholderText("Notes (optional)...")
        self.notes_edit.setMaximumHeight(50)
        self.notes_edit.setStyleSheet("border: 1px solid palette(mid); border-radius: 3px;")
        row3.addWidget(self.notes_edit, 1)

        btn_col = QVBoxLayout()
        btn_col.setSpacing(3)

        self.btn_add = QPushButton("Add")
        self.btn_add.setFixedWidth(70)
        self.btn_add.clicked.connect(self._add_activity)
        btn_col.addWidget(self.btn_add)

        self.btn_update = QPushButton("Update")
        self.btn_update.setObjectName("secondary")
        self.btn_update.setFixedWidth(70)
        self.btn_update.clicked.connect(self._update_activity)
        self.btn_update.setVisible(False)
        btn_col.addWidget(self.btn_update)

        self.btn_delete = QPushButton("Delete")
        self.btn_delete.setObjectName("destructive")
        self.btn_delete.setFixedWidth(70)
        self.btn_delete.clicked.connect(self._delete_activity)
        self.btn_delete.setVisible(False)
        btn_col.addWidget(self.btn_delete)

        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setObjectName("secondary")
        self.btn_cancel.setFixedWidth(70)
        self.btn_cancel.clicked.connect(self._cancel_edit)
        self.btn_cancel.setVisible(False)
        btn_col.addWidget(self.btn_cancel)

        row3.addLayout(btn_col)
        form_layout.addLayout(row3)

        layout.addWidget(form_frame)

        # Activity list for the day (scrollable)
        list_header = QHBoxLayout()
        list_title = QLabel("Today's Activities")
        list_title.setStyleSheet("font-weight: bold; font-size: 13px;")
        list_header.addWidget(list_title)
        list_header.addStretch()

        self.total_label = QLabel("")
        self.total_label.setObjectName("subtitle")
        list_header.addWidget(self.total_label)

        btn_export = QPushButton("Export to Vault")
        btn_export.setObjectName("secondary")
        btn_export.clicked.connect(self._export_to_vault)
        list_header.addWidget(btn_export)

        layout.addLayout(list_header)

        self._list_container = QWidget()
        self._list_layout = QVBoxLayout(self._list_container)
        self._list_layout.setContentsMargins(0, 0, 0, 0)
        self._list_layout.setSpacing(3)

        list_scroll = QScrollArea()
        list_scroll.setWidgetResizable(True)
        list_scroll.setWidget(self._list_container)
        list_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        layout.addWidget(list_scroll, 1)

    # ── Navigation ──────────────────────────────────────

    def _prev_day(self):
        self._stop_timer()
        self._current_date -= timedelta(days=1)
        self._refresh()

    def _next_day(self):
        self._stop_timer()
        self._current_date += timedelta(days=1)
        self._refresh()

    def _go_today(self):
        self._stop_timer()
        self._current_date = date.today()
        self._refresh()

    # ── Timer ───────────────────────────────────────────

    def _start_timer(self):
        now = datetime.now()
        self._timer_start = now
        self.start_edit.setTime(QTime(now.hour, now.minute))
        self.end_edit.setTime(QTime(now.hour, now.minute))

        self._active_timer = QTimer(self)
        self._active_timer.timeout.connect(self._update_timer_display)
        self._active_timer.start(1000)

        self.btn_start_timer.setEnabled(False)
        self.btn_stop_timer.setEnabled(True)
        self.timer_label.setStyleSheet(
            "font-size: 15px; font-weight: bold; font-family: monospace; "
            "color: #a6e3a1; border: none;"
        )

    def _stop_timer(self):
        if self._active_timer is not None:
            self._active_timer.stop()
            self._active_timer = None
        if self._timer_start is not None:
            now = datetime.now()
            self.end_edit.setTime(QTime(now.hour, now.minute))
        self._timer_start = None
        self.btn_start_timer.setEnabled(True)
        self.btn_stop_timer.setEnabled(False)
        self.timer_label.setStyleSheet(
            "font-size: 15px; font-weight: bold; font-family: monospace; border: none;"
        )

    def _update_timer_display(self):
        if self._timer_start is None:
            return
        elapsed = datetime.now() - self._timer_start
        total_secs = int(elapsed.total_seconds())
        h = total_secs // 3600
        m = (total_secs % 3600) // 60
        s = total_secs % 60
        self.timer_label.setText(f"\u23f1 {h:02d}:{m:02d}:{s:02d}")
        # Keep end_edit in sync with rolling now
        now = datetime.now()
        self.end_edit.setTime(QTime(now.hour, now.minute))

    # ── Refresh ─────────────────────────────────────────

    def _refresh(self):
        self.date_label.setText(self._current_date.strftime("%A, %B %d, %Y"))

        activities = self.store.get_for_date(self._current_date.isoformat())
        self.gantt.set_bars(activities)

        # Populate list
        self._clear_layout(self._list_layout)

        total_mins = 0
        for act in activities:
            total_mins += act.duration_minutes
            row = self._make_activity_row(act)
            self._list_layout.addWidget(row)

        if not activities:
            empty = QLabel("No activities logged for this day")
            empty.setObjectName("subtitle")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self._list_layout.addWidget(empty)

        self._list_layout.addStretch()

        hours = total_mins // 60
        mins = total_mins % 60
        self.total_label.setText(f"Total: {hours}h {mins}m")

        # Reset edit state
        self._cancel_edit()

    def _make_activity_row(self, act: Activity) -> QFrame:
        row = QFrame()
        row.setStyleSheet(
            "QFrame { border: 1px solid palette(mid); border-radius: 4px; padding: 4px; }"
        )
        layout = QHBoxLayout(row)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(8)

        # Color dot
        dot = QLabel("\u25cf")
        dot.setStyleSheet(f"color: {act.color}; font-size: 16px; border: none;")
        dot.setFixedWidth(18)
        layout.addWidget(dot)

        # Name
        name = QLabel(act.activity)
        name.setStyleSheet("font-weight: bold; font-size: 12px; border: none;")
        layout.addWidget(name)

        # Time range
        time_lbl = QLabel(f"{act.start_time} \u2013 {act.end_time}")
        time_lbl.setObjectName("subtitle")
        time_lbl.setStyleSheet("font-size: 11px; border: none;")
        layout.addWidget(time_lbl)

        # Duration
        dur = QLabel(f"{act.duration_minutes}m")
        dur.setObjectName("subtitle")
        dur.setStyleSheet("font-size: 11px; border: none;")
        dur.setFixedWidth(40)
        layout.addWidget(dur)

        # Notes preview
        if act.notes:
            notes_lbl = QLabel(act.notes[:50] + ("..." if len(act.notes) > 50 else ""))
            notes_lbl.setObjectName("subtitle")
            notes_lbl.setStyleSheet("font-size: 10px; font-style: italic; border: none;")
            layout.addWidget(notes_lbl, 1)
        else:
            layout.addStretch(1)

        # Edit button
        edit_btn = QPushButton("Edit")
        edit_btn.setObjectName("secondary")
        edit_btn.setFixedSize(40, 22)
        edit_btn.setStyleSheet("font-size: 10px; border: 1px solid palette(mid); border-radius: 3px;")
        edit_btn.clicked.connect(lambda _, a=act: self._start_edit(a))
        layout.addWidget(edit_btn)

        return row

    # ── CRUD ────────────────────────────────────────────

    def _add_activity(self):
        activity_name = self.activity_combo.currentText().strip()
        if not activity_name:
            return

        start = self.start_edit.time().toString("HH:mm")
        end = self.end_edit.time().toString("HH:mm")

        if start >= end:
            QMessageBox.warning(self, "Invalid Time", "End time must be after start time.")
            return

        # Stop timer if it was running when user clicks Add
        self._stop_timer()

        self.store.add(
            date=self._current_date.isoformat(),
            activity=activity_name,
            start_time=start,
            end_time=end,
            notes=self.notes_edit.toPlainText().strip(),
        )
        self._refresh()

    def _start_edit(self, act: Activity):
        self._editing_activity = act
        # Populate form
        idx = self.activity_combo.findText(act.activity)
        if idx >= 0:
            self.activity_combo.setCurrentIndex(idx)
        else:
            self.activity_combo.setCurrentText(act.activity)

        sh, sm = map(int, act.start_time.split(":"))
        eh, em = map(int, act.end_time.split(":"))
        self.start_edit.setTime(QTime(sh, sm))
        self.end_edit.setTime(QTime(eh, em))
        self.notes_edit.setPlainText(act.notes)

        self.btn_add.setVisible(False)
        self.btn_update.setVisible(True)
        self.btn_delete.setVisible(True)
        self.btn_cancel.setVisible(True)

    def _update_activity(self):
        if not self._editing_activity:
            return
        act = self._editing_activity
        act.activity = self.activity_combo.currentText().strip()
        act.start_time = self.start_edit.time().toString("HH:mm")
        act.end_time = self.end_edit.time().toString("HH:mm")
        act.notes = self.notes_edit.toPlainText().strip()

        if act.start_time >= act.end_time:
            QMessageBox.warning(self, "Invalid Time", "End time must be after start time.")
            return

        self.store.update(act)
        self._refresh()

    def _delete_activity(self):
        if not self._editing_activity:
            return
        reply = QMessageBox.question(
            self, "Delete Activity",
            f"Delete '{self._editing_activity.activity}' ({self._editing_activity.start_time}\u2013{self._editing_activity.end_time})?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.store.delete(self._editing_activity.id)
            self._refresh()

    def _cancel_edit(self):
        self._editing_activity = None
        self.btn_add.setVisible(True)
        self.btn_update.setVisible(False)
        self.btn_delete.setVisible(False)
        self.btn_cancel.setVisible(False)
        self.notes_edit.clear()

    def _on_bar_selected(self, activity: Activity):
        """Called when user clicks a bar in the Gantt chart."""
        self._start_edit(activity)

    # ── Obsidian export ─────────────────────────────────

    def _export_to_vault(self):
        cfg = load_config()
        vault_path = cfg.get("obsidian_vault_path", "")
        if not vault_path or not Path(vault_path).is_dir():
            QMessageBox.warning(
                self, "No Vault",
                "Set an Obsidian vault path first (Notes > Set Vault).",
            )
            return

        activities = self.store.get_for_date(self._current_date.isoformat())
        if not activities:
            QMessageBox.information(self, "Nothing to Export", "No activities logged for this day.")
            return

        vault = Path(vault_path)
        d = self._current_date
        # Structure: Activity Tracker / YYYY / MM - MonthName / DD - DayName / ActivityName.md
        year_folder = f"{d.year}"
        month_folder = f"{d.month:02d} - {d.strftime('%B')}"
        day_folder = f"{d.day:02d} - {d.strftime('%A')}"

        base = vault / "Activity Tracker" / year_folder / month_folder / day_folder
        base.mkdir(parents=True, exist_ok=True)

        # Write a summary file
        summary_path = base / "_Daily Summary.md"
        total_mins = sum(a.duration_minutes for a in activities)
        hours, mins = divmod(total_mins, 60)

        lines = [
            f"# Activity Summary \u2014 {d.strftime('%A, %B %d, %Y')}",
            "",
            f"**Total tracked:** {hours}h {mins}m",
            "",
            "| Time | Activity | Duration | Notes |",
            "|------|----------|----------|-------|",
        ]
        for a in activities:
            dur = f"{a.duration_minutes}m"
            notes = a.notes.replace("\n", " ").replace("|", "/") if a.notes else ""
            lines.append(f"| {a.start_time}\u2013{a.end_time} | {a.activity} | {dur} | {notes} |")

        lines.append("")
        summary_path.write_text("\n".join(lines), encoding="utf-8")

        # Write individual activity files
        for a in activities:
            safe_name = a.activity.replace("/", "-").replace("\\", "-")
            act_path = base / f"{safe_name}.md"
            content = [
                f"# {a.activity}",
                "",
                f"**Date:** {d.isoformat()}",
                f"**Time:** {a.start_time} \u2013 {a.end_time}",
                f"**Duration:** {a.duration_minutes} minutes",
                "",
            ]
            if a.notes:
                content.extend(["## Notes", "", a.notes, ""])
            act_path.write_text("\n".join(content), encoding="utf-8")

        QMessageBox.information(
            self, "Exported",
            f"Exported {len(activities)} activities to:\n{base}",
        )

    # ── Helpers ─────────────────────────────────────────

    @staticmethod
    def _clear_layout(layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

```

### `src\ui\modules\calendar_panel.py`

```python
"""Calendar module UI — weekly main view + mini month navigator + colored dot indicators."""

from datetime import date, datetime, timedelta
import calendar

from PyQt6.QtCore import Qt, QDate, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QDialog, QLineEdit, QTextEdit,
    QDateEdit, QTimeEdit, QCheckBox, QFrame, QComboBox,
    QMessageBox, QScrollArea, QSizePolicy,
)

from src.data.calendar_store import CalendarStore, Event


# ── Event colors ──────────────────────────────────────
EVENT_COLORS = {
    "Blue": "#4a9eff", "Green": "#a6e3a1", "Red": "#f38ba8",
    "Yellow": "#f9e2af", "Purple": "#cba6f7", "Orange": "#fab387",
    "Teal": "#94e2d5", "Pink": "#f5c2e7",
}

# ── Category emojis ───────────────────────────────────
CATEGORY_EMOJIS = {
    "birthday": "\U0001f382",   # 🎂
    "trip":     "\u2708\ufe0f", # ✈️
    "holiday":  "\U0001f389",   # 🎉
    "major":    "\u2b50",       # ⭐
    "work":     "\U0001f4bc",   # 💼
}

CATEGORY_OPTIONS = [
    ("", "None"),
    ("work", "Work \U0001f4bc"),
    ("birthday", "Birthday \U0001f382"),
    ("trip", "Trip \u2708\ufe0f"),
    ("holiday", "Holiday \U0001f389"),
    ("major", "Major Event \u2b50"),
]


class EventDialog(QDialog):
    """Dialog to add/edit an event."""

    def __init__(self, parent=None, event=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Event" if event else "New Event")
        self.setMinimumWidth(380)
        self.event = event
        self._delete_requested = False
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        layout.addWidget(QLabel("Title"))
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Event title...")
        if self.event:
            self.title_edit.setText(self.event.title)
        layout.addWidget(self.title_edit)

        layout.addWidget(QLabel("Description"))
        self.desc_edit = QTextEdit()
        self.desc_edit.setMaximumHeight(80)
        self.desc_edit.setPlaceholderText("Optional description...")
        if self.event:
            self.desc_edit.setPlainText(self.event.description)
        layout.addWidget(self.desc_edit)

        self.all_day_check = QCheckBox("All day event")
        if self.event:
            self.all_day_check.setChecked(self.event.all_day)
        self.all_day_check.toggled.connect(self._toggle_time)
        layout.addWidget(self.all_day_check)

        date_row = QHBoxLayout()
        date_row.addWidget(QLabel("Date"))
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        if self.event:
            dt = datetime.fromisoformat(self.event.start_time)
            self.date_edit.setDate(QDate(dt.year, dt.month, dt.day))
        else:
            today = date.today()
            self.date_edit.setDate(QDate(today.year, today.month, today.day))
        date_row.addWidget(self.date_edit, 1)
        layout.addLayout(date_row)

        from PyQt6.QtCore import QTime
        time_row = QHBoxLayout()
        time_row.addWidget(QLabel("Start"))
        self.start_time = QTimeEdit()
        self.start_time.setDisplayFormat("HH:mm")
        if self.event and not self.event.all_day:
            dt = datetime.fromisoformat(self.event.start_time)
            self.start_time.setTime(QTime(dt.hour, dt.minute))
        else:
            self.start_time.setTime(QTime(9, 0))
        time_row.addWidget(self.start_time, 1)
        time_row.addWidget(QLabel("End"))
        self.end_time = QTimeEdit()
        self.end_time.setDisplayFormat("HH:mm")
        if self.event and self.event.end_time:
            dt = datetime.fromisoformat(self.event.end_time)
            self.end_time.setTime(QTime(dt.hour, dt.minute))
        else:
            self.end_time.setTime(QTime(10, 0))
        time_row.addWidget(self.end_time, 1)
        layout.addLayout(time_row)
        self.time_widgets = [self.start_time, self.end_time]
        self._toggle_time(self.all_day_check.isChecked())

        # Color + Category side by side
        cc_row = QHBoxLayout()
        cc_row.setSpacing(12)

        color_col = QVBoxLayout()
        color_col.addWidget(QLabel("Color"))
        self.color_combo = QComboBox()
        for name, hex_val in EVENT_COLORS.items():
            self.color_combo.addItem(name, hex_val)
        if self.event:
            idx = self.color_combo.findData(self.event.color)
            if idx >= 0:
                self.color_combo.setCurrentIndex(idx)
        color_col.addWidget(self.color_combo)
        cc_row.addLayout(color_col, 1)

        cat_col = QVBoxLayout()
        cat_col.addWidget(QLabel("Category"))
        self.category_combo = QComboBox()
        for val, label in CATEGORY_OPTIONS:
            self.category_combo.addItem(label, val)
        if self.event:
            idx = self.category_combo.findData(self.event.category)
            if idx >= 0:
                self.category_combo.setCurrentIndex(idx)
        cat_col.addWidget(self.category_combo)
        cc_row.addLayout(cat_col, 1)

        layout.addLayout(cc_row)

        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(sep)

        btn_row = QHBoxLayout()
        if self.event:
            del_btn = QPushButton("Delete")
            del_btn.setObjectName("destructive")
            del_btn.clicked.connect(self._on_delete)
            btn_row.addWidget(del_btn)
        btn_row.addStretch()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("secondary")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        btn_row.addWidget(save_btn)
        layout.addLayout(btn_row)

    def _toggle_time(self, all_day: bool):
        for w in self.time_widgets:
            w.setEnabled(not all_day)

    def _on_delete(self):
        self._delete_requested = True
        self.reject()

    def get_data(self) -> dict:
        qd = self.date_edit.date()
        d = date(qd.year(), qd.month(), qd.day())
        if self.all_day_check.isChecked():
            start = datetime(d.year, d.month, d.day).isoformat()
            end = None
        else:
            st = self.start_time.time()
            et = self.end_time.time()
            start = datetime(d.year, d.month, d.day, st.hour(), st.minute()).isoformat()
            end = datetime(d.year, d.month, d.day, et.hour(), et.minute()).isoformat()
        return {
            "title": self.title_edit.text().strip() or "Untitled",
            "description": self.desc_edit.toPlainText(),
            "start_time": start, "end_time": end,
            "all_day": self.all_day_check.isChecked(),
            "color": self.color_combo.currentData(),
            "category": self.category_combo.currentData() or "",
        }


# ── Mini month calendar (for navigation) ──────────────

class MiniMonthCell(QLabel):
    """A single day number in the mini calendar."""
    clicked = pyqtSignal(int, int, int)  # year, month, day

    def __init__(self, year: int, month: int, day: int, is_today: bool,
                 is_selected: bool, has_events: bool, event_colors: list):
        super().__init__(str(day))
        self.year, self.month, self.day = year, month, day
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedSize(28, 28)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        style = "font-size: 11px; border-radius: 14px; "
        if is_today:
            style += "background-color: #4a9eff; color: #1e1e2e; font-weight: bold; "
        elif is_selected:
            style += "border: 1px solid #4a9eff; "

        self.setStyleSheet(style)

        if has_events and not is_today:
            self.setToolTip(f"{len(event_colors)} event(s)")
            self._dot_colors = event_colors[:3]
        else:
            self._dot_colors = []

    def mousePressEvent(self, ev):
        self.clicked.emit(self.year, self.month, self.day)


class MiniMonth(QWidget):
    """Compact month grid for date navigation."""
    date_selected = pyqtSignal(object)  # emits a date object

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(230)
        self._selected_date = date.today()
        self._view_year = date.today().year
        self._view_month = date.today().month
        self._events_by_date: dict[date, list] = {}
        self._build()

    def set_events(self, events_by_date: dict):
        self._events_by_date = events_by_date
        self._render()

    def set_selected(self, d: date):
        self._selected_date = d
        self._view_year = d.year
        self._view_month = d.month
        self._render()

    def _build(self):
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(8, 8, 8, 8)
        self._layout.setSpacing(4)

        # Header row
        header = QHBoxLayout()
        self._prev_btn = QPushButton("\u25c0")
        self._prev_btn.setObjectName("secondary")
        self._prev_btn.setFixedSize(24, 24)
        self._prev_btn.clicked.connect(self._prev_month)
        header.addWidget(self._prev_btn)

        self._title = QLabel()
        self._title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._title.setStyleSheet("font-weight: bold; font-size: 13px;")
        header.addWidget(self._title, 1)

        self._next_btn = QPushButton("\u25b6")
        self._next_btn.setObjectName("secondary")
        self._next_btn.setFixedSize(24, 24)
        self._next_btn.clicked.connect(self._next_month)
        header.addWidget(self._next_btn)

        self._layout.addLayout(header)

        # Day-of-week header
        dow_row = QHBoxLayout()
        dow_row.setSpacing(0)
        for d in ["M", "T", "W", "T", "F", "S", "S"]:
            lbl = QLabel(d)
            lbl.setFixedSize(28, 18)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setObjectName("subtitle")
            lbl.setStyleSheet("font-size: 10px; font-weight: bold;")
            dow_row.addWidget(lbl)
        self._layout.addLayout(dow_row)

        # Grid placeholder
        self._grid_widget = QWidget()
        self._grid = QGridLayout(self._grid_widget)
        self._grid.setSpacing(1)
        self._grid.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self._grid_widget)

        self._layout.addStretch()
        self._render()

    def _render(self):
        # Clear grid
        while self._grid.count():
            child = self._grid.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self._title.setText(f"{calendar.month_abbr[self._view_month]} {self._view_year}")

        today = date.today()
        cal = calendar.Calendar(firstweekday=0)
        weeks = cal.monthdayscalendar(self._view_year, self._view_month)

        for row, week in enumerate(weeks):
            for col, day in enumerate(week):
                if day == 0:
                    spacer = QLabel("")
                    spacer.setFixedSize(28, 28)
                    self._grid.addWidget(spacer, row, col)
                else:
                    d = date(self._view_year, self._view_month, day)
                    is_today = (d == today)
                    is_selected = (d == self._selected_date)
                    day_events = self._events_by_date.get(d, [])
                    event_colors = [ev.color for ev in day_events]

                    cell = MiniMonthCell(
                        self._view_year, self._view_month, day,
                        is_today, is_selected, bool(day_events), event_colors,
                    )
                    cell.clicked.connect(self._on_cell_click)
                    self._grid.addWidget(cell, row, col)

    def _on_cell_click(self, y, m, d):
        self._selected_date = date(y, m, d)
        self._render()
        self.date_selected.emit(self._selected_date)

    def _prev_month(self):
        if self._view_month == 1:
            self._view_month = 12
            self._view_year -= 1
        else:
            self._view_month -= 1
        self._render()

    def _next_month(self):
        if self._view_month == 12:
            self._view_month = 1
            self._view_year += 1
        else:
            self._view_month += 1
        self._render()


# ── Weekly view (main content) ─────────────────────────

class WeekEventWidget(QFrame):
    """A single event rendered in the weekly time grid."""

    def __init__(self, event: Event, parent_panel):
        super().__init__()
        self.event = event
        self.parent_panel = parent_panel
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 3, 6, 3)
        layout.setSpacing(6)

        # Color dot
        dot = QLabel("\u25cf")
        dot.setStyleSheet(f"color: {event.color}; font-size: 14px;")
        dot.setFixedWidth(16)
        layout.addWidget(dot)

        # Time + title
        info_layout = QVBoxLayout()
        info_layout.setSpacing(0)
        info_layout.setContentsMargins(0, 0, 0, 0)

        if not event.all_day:
            try:
                dt = datetime.fromisoformat(event.start_time)
                time_str = dt.strftime("%H:%M")
                if event.end_time:
                    et = datetime.fromisoformat(event.end_time)
                    time_str += f" - {et.strftime('%H:%M')}"
            except Exception:
                time_str = ""
            if time_str:
                time_label = QLabel(time_str)
                time_label.setObjectName("subtitle")
                time_label.setStyleSheet("font-size: 11px;")
                info_layout.addWidget(time_label)

        emoji = CATEGORY_EMOJIS.get(event.category, "")
        display_title = f"{emoji} {event.title}" if emoji else event.title
        title_label = QLabel(display_title)
        title_label.setStyleSheet("font-weight: bold; font-size: 13px;")
        title_label.setWordWrap(True)
        info_layout.addWidget(title_label)

        if event.description:
            desc = QLabel(event.description[:60])
            desc.setObjectName("subtitle")
            desc.setStyleSheet("font-size: 11px;")
            desc.setWordWrap(True)
            info_layout.addWidget(desc)

        layout.addLayout(info_layout, 1)

        self.setStyleSheet(
            f"WeekEventWidget {{ border-left: 3px solid {event.color}; "
            f"border-radius: 4px; padding: 2px; }}"
        )
        self.setToolTip(
            f"{display_title}\n{event.start_time}"
            + (f" - {event.end_time}" if event.end_time else "")
            + (f"\n{event.description}" if event.description else "")
        )

    def mouseDoubleClickEvent(self, ev):
        self.parent_panel._edit_event(self.event)


class DayColumn(QWidget):
    """A single day column in the weekly view."""

    def __init__(self, d: date, events: list, is_today: bool, parent_panel):
        super().__init__()
        self.d = d
        self.parent_panel = parent_panel
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)

        # Day header
        day_name = d.strftime("%a")
        day_num = str(d.day)
        header = QLabel(f"{day_name}\n{day_num}")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if is_today:
            header.setStyleSheet(
                "background-color: #4a9eff; color: #1e1e2e; "
                "border-radius: 8px; padding: 4px; font-weight: bold; font-size: 13px;"
            )
        else:
            header.setStyleSheet("font-size: 13px; padding: 4px;")
        layout.addWidget(header)

        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(sep)

        # Events sorted by time
        sorted_events = sorted(events, key=lambda e: e.start_time)

        # All-day events first
        for ev in sorted_events:
            if ev.all_day:
                w = WeekEventWidget(ev, parent_panel)
                layout.addWidget(w)

        # Timed events
        for ev in sorted_events:
            if not ev.all_day:
                w = WeekEventWidget(ev, parent_panel)
                layout.addWidget(w)

        layout.addStretch()

        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mouseDoubleClickEvent(self, ev):
        self.parent_panel._add_event_on_day_date(self.d)


# ── Main calendar panel ───────────────────────────────

class CalendarPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.store = CalendarStore()
        self._selected_date = date.today()
        self._palette = {}
        self._build_ui()
        self._refresh()

    def set_palette(self, palette: dict):
        self._palette = palette

    def _build_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ── Main area: weekly view + today's events ───
        main_area = QWidget()
        main_layout = QVBoxLayout(main_area)
        main_layout.setContentsMargins(16, 12, 8, 12)
        main_layout.setSpacing(0)

        # Week header
        week_header = QHBoxLayout()
        title = QLabel("Calendar")
        title.setObjectName("sectionTitle")
        week_header.addWidget(title)
        week_header.addStretch()

        self.btn_prev_week = QPushButton("\u25c0 Prev")
        self.btn_prev_week.setObjectName("secondary")
        self.btn_prev_week.clicked.connect(self._prev_week)
        week_header.addWidget(self.btn_prev_week)

        self.week_label = QLabel()
        self.week_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.week_label.setMinimumWidth(200)
        self.week_label.setStyleSheet("font-size: 15px; font-weight: bold;")
        week_header.addWidget(self.week_label)

        self.btn_next_week = QPushButton("Next \u25b6")
        self.btn_next_week.setObjectName("secondary")
        self.btn_next_week.clicked.connect(self._next_week)
        week_header.addWidget(self.btn_next_week)

        btn_today = QPushButton("Today")
        btn_today.setObjectName("secondary")
        btn_today.clicked.connect(self._go_today)
        week_header.addWidget(btn_today)

        btn_add = QPushButton("+ Event")
        btn_add.clicked.connect(self._add_event)
        week_header.addWidget(btn_add)

        main_layout.addLayout(week_header)
        main_layout.addSpacing(6)

        # Weekly grid (top half)
        self._week_container = QWidget()
        self._week_grid = QHBoxLayout(self._week_container)
        self._week_grid.setSpacing(2)
        self._week_grid.setContentsMargins(0, 0, 0, 0)

        week_scroll = QScrollArea()
        week_scroll.setWidgetResizable(True)
        week_scroll.setWidget(self._week_container)
        week_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        week_scroll.setMaximumHeight(280)
        main_layout.addWidget(week_scroll, 1)

        # Divider between weekly grid and today's events
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("border: none; border-top: 2px solid palette(mid); margin: 6px 0;")
        main_layout.addWidget(divider)

        # Today's Events (bottom half)
        today_header = QHBoxLayout()
        self.today_events_title = QLabel("Today's Events")
        self.today_events_title.setStyleSheet("font-weight: bold; font-size: 13px;")
        today_header.addWidget(self.today_events_title)
        today_header.addStretch()
        main_layout.addLayout(today_header)
        main_layout.addSpacing(4)

        self._today_event_list = QVBoxLayout()
        self._today_event_list.setSpacing(4)
        today_list_widget = QWidget()
        today_list_widget.setLayout(self._today_event_list)

        today_scroll = QScrollArea()
        today_scroll.setWidgetResizable(True)
        today_scroll.setWidget(today_list_widget)
        today_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        main_layout.addWidget(today_scroll, 1)

        layout.addWidget(main_area, 1)

        # ── Right sidebar: mini month + major events ──
        right_sidebar = QWidget()
        right_sidebar.setFixedWidth(250)
        right_layout = QVBoxLayout(right_sidebar)
        right_layout.setContentsMargins(8, 12, 12, 12)
        right_layout.setSpacing(8)

        self.mini_month = MiniMonth()
        self.mini_month.date_selected.connect(self._on_mini_date_selected)
        right_layout.addWidget(self.mini_month)

        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine)
        right_layout.addWidget(sep)

        # Next Major Events
        major_title = QLabel("Next Major Events")
        major_title.setStyleSheet("font-weight: bold; font-size: 13px;")
        right_layout.addWidget(major_title)

        self._major_events_list = QVBoxLayout()
        self._major_events_list.setSpacing(4)
        major_list_widget = QWidget()
        major_list_widget.setLayout(self._major_events_list)

        major_scroll = QScrollArea()
        major_scroll.setWidgetResizable(True)
        major_scroll.setWidget(major_list_widget)
        major_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        right_layout.addWidget(major_scroll, 1)

        layout.addWidget(right_sidebar)

    def _refresh(self):
        self._render_week()
        self._render_day_detail()
        self._render_major_events()
        self._update_mini_month_events()

    def _get_week_start(self) -> date:
        """Monday of the selected week."""
        d = self._selected_date
        return d - timedelta(days=d.weekday())

    def _render_week(self):
        # Clear
        while self._week_grid.count():
            child = self._week_grid.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        week_start = self._get_week_start()
        week_end = week_start + timedelta(days=6)
        self.week_label.setText(
            f"{week_start.strftime('%b %d')} - {week_end.strftime('%b %d, %Y')}"
        )

        events = self.store.get_events(
            week_start.isoformat(),
            week_end.isoformat() + "T23:59:59",
        )

        events_by_date: dict[date, list] = {}
        for ev in events:
            d = datetime.fromisoformat(ev.start_time).date()
            events_by_date.setdefault(d, []).append(ev)

        today = date.today()
        for i in range(7):
            d = week_start + timedelta(days=i)

            # Vertical divider between day columns
            if i > 0:
                col_div = QFrame()
                col_div.setFrameShape(QFrame.Shape.VLine)
                col_div.setStyleSheet("border: none; border-left: 1px solid palette(mid);")
                self._week_grid.addWidget(col_div)

            day_events = events_by_date.get(d, [])
            col = DayColumn(d, day_events, d == today, self)
            self._week_grid.addWidget(col, 1)

    def _render_day_detail(self):
        # Clear
        while self._today_event_list.count():
            child = self._today_event_list.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        d = self._selected_date
        self.today_events_title.setText(d.strftime("%A, %B %d"))

        events = self.store.get_events(
            d.isoformat(), d.isoformat() + "T23:59:59",
        )

        if not events:
            lbl = QLabel("No events")
            lbl.setObjectName("subtitle")
            self._today_event_list.addWidget(lbl)
        else:
            for ev in sorted(events, key=lambda e: e.start_time):
                row_widget = QFrame()
                row_widget.setStyleSheet(
                    "QFrame { border-left: 3px solid " + ev.color + "; "
                    "border-radius: 3px; padding: 2px 6px; }"
                )
                row_layout = QHBoxLayout(row_widget)
                row_layout.setContentsMargins(6, 3, 6, 3)
                row_layout.setSpacing(8)

                if not ev.all_day:
                    try:
                        t = datetime.fromisoformat(ev.start_time).strftime("%H:%M")
                    except Exception:
                        t = ""
                    time_lbl = QLabel(t)
                    time_lbl.setObjectName("subtitle")
                    time_lbl.setFixedWidth(42)
                    row_layout.addWidget(time_lbl)

                emoji = CATEGORY_EMOJIS.get(ev.category, "")
                display_title = f"{emoji} {ev.title}" if emoji else ev.title
                title_lbl = QLabel(display_title)
                title_lbl.setStyleSheet("font-size: 12px;")
                row_layout.addWidget(title_lbl, 1)

                row_widget.setCursor(Qt.CursorShape.PointingHandCursor)
                row_widget.mouseDoubleClickEvent = lambda _ev, event=ev: self._edit_event(event)
                self._today_event_list.addWidget(row_widget)

        self._today_event_list.addStretch()

    def _render_major_events(self):
        # Clear
        while self._major_events_list.count():
            child = self._major_events_list.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        major_events = self.store.get_next_major_events(date.today(), limit=4)

        if not major_events:
            lbl = QLabel("No upcoming major events")
            lbl.setObjectName("subtitle")
            lbl.setWordWrap(True)
            self._major_events_list.addWidget(lbl)
        else:
            for ev_date, title, category, color in major_events:
                row_widget = QFrame()
                row_widget.setStyleSheet(
                    "QFrame { border-left: 3px solid " + color + "; "
                    "border-radius: 3px; padding: 2px 4px; }"
                )
                row_layout = QHBoxLayout(row_widget)
                row_layout.setContentsMargins(6, 3, 4, 3)
                row_layout.setSpacing(6)

                emoji = CATEGORY_EMOJIS.get(category, "\u2022")
                emoji_lbl = QLabel(emoji)
                emoji_lbl.setFixedWidth(20)
                emoji_lbl.setStyleSheet("font-size: 14px;")
                row_layout.addWidget(emoji_lbl)

                date_lbl = QLabel(ev_date.strftime("%b %d"))
                date_lbl.setObjectName("subtitle")
                date_lbl.setFixedWidth(44)
                date_lbl.setStyleSheet("font-size: 11px;")
                row_layout.addWidget(date_lbl)

                title_lbl = QLabel(title)
                title_lbl.setStyleSheet("font-size: 12px;")
                title_lbl.setWordWrap(True)
                row_layout.addWidget(title_lbl, 1)

                self._major_events_list.addWidget(row_widget)

        self._major_events_list.addStretch()

    def _update_mini_month_events(self):
        """Feed the mini month with event data so it can show colored dots."""
        first = date(self.mini_month._view_year, self.mini_month._view_month, 1)
        if self.mini_month._view_month == 12:
            last = date(self.mini_month._view_year + 1, 1, 1) - timedelta(days=1)
        else:
            last = date(self.mini_month._view_year, self.mini_month._view_month + 1, 1) - timedelta(days=1)

        events = self.store.get_events(first.isoformat(), last.isoformat() + "T23:59:59")
        by_date: dict[date, list] = {}
        for ev in events:
            d = datetime.fromisoformat(ev.start_time).date()
            by_date.setdefault(d, []).append(ev)
        self.mini_month.set_events(by_date)

    # ── Navigation ─────────────────────────────────────

    def _prev_week(self):
        self._selected_date -= timedelta(weeks=1)
        self.mini_month.set_selected(self._selected_date)
        self._refresh()

    def _next_week(self):
        self._selected_date += timedelta(weeks=1)
        self.mini_month.set_selected(self._selected_date)
        self._refresh()

    def _go_today(self):
        self._selected_date = date.today()
        self.mini_month.set_selected(self._selected_date)
        self._refresh()

    def _on_mini_date_selected(self, d):
        self._selected_date = d
        self._refresh()

    # ── Event CRUD ─────────────────────────────────────

    def _add_event(self):
        dlg = EventDialog(self)
        dlg.date_edit.setDate(QDate(
            self._selected_date.year, self._selected_date.month, self._selected_date.day
        ))
        if dlg.exec():
            self.store.add_event(**dlg.get_data())
            self._refresh()

    def _add_event_on_day_date(self, d: date):
        dlg = EventDialog(self)
        dlg.date_edit.setDate(QDate(d.year, d.month, d.day))
        if dlg.exec():
            self.store.add_event(**dlg.get_data())
            self._refresh()

    def _edit_event(self, event: Event):
        dlg = EventDialog(self, event)
        result = dlg.exec()
        if dlg._delete_requested:
            reply = QMessageBox.question(
                self, "Delete Event", f"Delete '{event.title}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.store.delete_event(event.id)
                self._refresh()
        elif result:
            data = dlg.get_data()
            event.title = data["title"]
            event.description = data["description"]
            event.start_time = data["start_time"]
            event.end_time = data["end_time"]
            event.all_day = data["all_day"]
            event.color = data["color"]
            event.category = data["category"]
            self.store.update_event(event)
            self._refresh()

```

### `src\ui\modules\dashboard_panel.py`

```python
"""QA Dashboard panel — overview of tasks, upcoming deadlines, and productivity stats."""

from datetime import date, datetime, timedelta

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QFrame, QScrollArea, QProgressBar,
)

from src.data.todo_store import TodoStore, PRIORITY_LABELS
from src.data.calendar_store import CalendarStore
from src.data.finance_store import FinanceStore


PRIORITY_COLORS = {0: "#a6adc8", 1: "#a6e3a1", 2: "#f9e2af", 3: "#f38ba8"}


class StatCard(QFrame):
    """A compact stat card with a big number and label."""

    def __init__(self, value: str, label: str, color: str = "#cdd6f4", parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            f"StatCard {{ border: 1px solid palette(mid); border-radius: 6px; padding: 8px; }}"
        )
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(2)

        val = QLabel(value)
        val.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {color};")
        val.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(val)
        self._value_label = val

        lbl = QLabel(label)
        lbl.setObjectName("subtitle")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("font-size: 11px;")
        layout.addWidget(lbl)
        self._label = lbl

    def update_value(self, value: str, color: str | None = None):
        self._value_label.setText(value)
        if color:
            self._value_label.setStyleSheet(
                f"font-size: 24px; font-weight: bold; color: {color};"
            )


class UpcomingItem(QFrame):
    """A single upcoming deadline / event in the dashboard."""

    def __init__(self, title: str, subtitle: str, color: str, days_label: str, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(8)

        dot = QLabel("\u25cf")
        dot.setStyleSheet(f"color: {color}; font-size: 14px;")
        dot.setFixedWidth(16)
        layout.addWidget(dot)

        info = QVBoxLayout()
        info.setSpacing(0)
        t = QLabel(title)
        t.setStyleSheet("font-weight: bold; font-size: 12px;")
        info.addWidget(t)
        s = QLabel(subtitle)
        s.setObjectName("subtitle")
        s.setStyleSheet("font-size: 10px;")
        info.addWidget(s)
        layout.addLayout(info, 1)

        badge = QLabel(days_label)
        badge.setStyleSheet(
            f"color: {color}; font-size: 10px; font-weight: bold; "
            f"padding: 2px 6px; border: 1px solid {color}; border-radius: 3px;"
        )
        layout.addWidget(badge)


class DashboardPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.todo_store = TodoStore()
        self.calendar_store = CalendarStore()
        self.finance_store = FinanceStore()
        self._palette: dict = {}
        self._build_ui()
        self._refresh()

    def set_palette(self, palette: dict):
        self._palette = palette
        self._refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)

        # Header
        header = QHBoxLayout()
        title = QLabel("Dashboard")
        title.setObjectName("sectionTitle")
        header.addWidget(title)
        header.addStretch()
        self.date_label = QLabel("")
        self.date_label.setObjectName("subtitle")
        header.addWidget(self.date_label)
        layout.addLayout(header)

        # Stat cards row
        self._cards_layout = QHBoxLayout()
        self._cards_layout.setSpacing(10)

        self.card_pending = StatCard("0", "Pending Tasks")
        self.card_done_today = StatCard("0", "Done Today")
        self.card_overdue = StatCard("0", "Overdue", "#f38ba8")
        self.card_events_week = StatCard("0", "Events This Week")
        self.card_earned_month = StatCard("$0", "Earned This Month")

        for card in [self.card_pending, self.card_done_today, self.card_overdue,
                     self.card_events_week, self.card_earned_month]:
            self._cards_layout.addWidget(card)

        layout.addLayout(self._cards_layout)

        # Progress bar for task completion
        progress_row = QHBoxLayout()
        progress_row.setSpacing(8)
        progress_lbl = QLabel("Task Completion:")
        progress_lbl.setObjectName("subtitle")
        progress_row.addWidget(progress_lbl)
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(18)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p% complete")
        progress_row.addWidget(self.progress_bar, 1)
        self.progress_pct_label = QLabel("")
        self.progress_pct_label.setObjectName("subtitle")
        progress_row.addWidget(self.progress_pct_label)
        layout.addLayout(progress_row)

        # Two-column area: upcoming deadlines + priority breakdown
        columns = QHBoxLayout()
        columns.setSpacing(12)

        # Left: upcoming deadlines
        left = QVBoxLayout()
        upcoming_title = QLabel("Upcoming Deadlines & Events")
        upcoming_title.setStyleSheet("font-weight: bold; font-size: 13px;")
        left.addWidget(upcoming_title)

        self._upcoming_container = QWidget()
        self._upcoming_layout = QVBoxLayout(self._upcoming_container)
        self._upcoming_layout.setContentsMargins(0, 0, 0, 0)
        self._upcoming_layout.setSpacing(3)

        upcoming_scroll = QScrollArea()
        upcoming_scroll.setWidgetResizable(True)
        upcoming_scroll.setWidget(self._upcoming_container)
        upcoming_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        left.addWidget(upcoming_scroll, 1)
        columns.addLayout(left, 3)

        # Right: priority breakdown + category breakdown
        right = QVBoxLayout()

        priority_title = QLabel("Tasks by Priority")
        priority_title.setStyleSheet("font-weight: bold; font-size: 13px;")
        right.addWidget(priority_title)

        self._priority_container = QWidget()
        self._priority_layout = QVBoxLayout(self._priority_container)
        self._priority_layout.setContentsMargins(0, 0, 0, 0)
        self._priority_layout.setSpacing(4)
        right.addWidget(self._priority_container)

        right.addSpacing(12)

        cat_title = QLabel("Tasks by Category")
        cat_title.setStyleSheet("font-weight: bold; font-size: 13px;")
        right.addWidget(cat_title)

        self._category_container = QWidget()
        self._category_layout = QVBoxLayout(self._category_container)
        self._category_layout.setContentsMargins(0, 0, 0, 0)
        self._category_layout.setSpacing(4)
        right.addWidget(self._category_container)

        right.addStretch()
        columns.addLayout(right, 2)

        layout.addLayout(columns, 1)

    def _refresh(self):
        green = self._palette.get("green", "#a6e3a1")
        red = self._palette.get("red", "#f38ba8")
        accent = self._palette.get("accent", "#4a9eff")
        yellow = self._palette.get("yellow", "#f9e2af")

        today = date.today()
        self.date_label.setText(today.strftime("%A, %B %d, %Y"))

        # Task stats
        counts = self.todo_store.get_counts()
        all_tasks = self.todo_store.get_all(include_done=True)
        pending_tasks = [t for t in all_tasks if not t.done and not t.deleted]
        done_tasks = [t for t in all_tasks if t.done and not t.deleted]

        overdue = [
            t for t in pending_tasks
            if t.due_date and t.due_date < today.isoformat()
        ]

        # Done today
        today_str = today.isoformat()
        done_today = [
            t for t in done_tasks
            if t.updated_at and t.updated_at[:10] == today_str
        ]

        self.card_pending.update_value(str(counts["pending"]), accent)
        self.card_done_today.update_value(str(len(done_today)), green)
        self.card_overdue.update_value(str(len(overdue)), red if overdue else green)

        # Events this week
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        week_events = self.calendar_store.get_events(
            week_start.isoformat(), week_end.isoformat() + "T23:59:59"
        )
        self.card_events_week.update_value(str(len(week_events)), accent)

        # Earned this month
        month_start = today.replace(day=1).isoformat()
        month_earned = self.finance_store.get_summary(month_start, today.isoformat())
        self.card_earned_month.update_value(
            f"${month_earned['earned']:,.0f}", green
        )

        # Progress bar
        total = counts["total"]
        done = counts["done"]
        if total > 0:
            pct = int(done / total * 100)
            self.progress_bar.setValue(pct)
            self.progress_pct_label.setText(f"{done}/{total}")
        else:
            self.progress_bar.setValue(0)
            self.progress_pct_label.setText("No tasks")

        # Style the progress bar
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid palette(mid);
                border-radius: 4px;
                text-align: center;
                font-size: 11px;
            }}
            QProgressBar::chunk {{
                background-color: {accent};
                border-radius: 3px;
            }}
        """)

        # Upcoming deadlines (tasks with due dates + events in next 7 days)
        self._clear_layout(self._upcoming_layout)

        upcoming_items = []

        # Tasks with due dates (sorted by date)
        for task in sorted(pending_tasks, key=lambda t: t.due_date or "9999"):
            if task.due_date:
                try:
                    due = date.fromisoformat(task.due_date)
                    delta = (due - today).days
                    if delta < 0:
                        days_text = f"{-delta}d overdue"
                        color = red
                    elif delta == 0:
                        days_text = "Today"
                        color = yellow
                    elif delta == 1:
                        days_text = "Tomorrow"
                        color = yellow
                    elif delta <= 7:
                        days_text = f"In {delta}d"
                        color = accent
                    else:
                        days_text = f"In {delta}d"
                        color = green
                    cat = f"Task \u00b7 {task.category}" if task.category else "Task"
                    upcoming_items.append((delta, UpcomingItem(
                        task.title, cat, color, days_text
                    )))
                except ValueError:
                    pass

        # Events in next 7 days
        next_week = today + timedelta(days=7)
        upcoming_events = self.calendar_store.get_events(
            today.isoformat(), next_week.isoformat() + "T23:59:59"
        )
        for ev in upcoming_events:
            try:
                ev_date = datetime.fromisoformat(ev.start_time).date()
                delta = (ev_date - today).days
                if delta == 0:
                    days_text = "Today"
                elif delta == 1:
                    days_text = "Tomorrow"
                else:
                    days_text = f"In {delta}d"
                time_str = ""
                if not ev.all_day:
                    time_str = datetime.fromisoformat(ev.start_time).strftime("%H:%M")
                sub = f"Event \u00b7 {time_str}" if time_str else "Event \u00b7 All day"
                upcoming_items.append((delta, UpcomingItem(
                    ev.title, sub, ev.color, days_text
                )))
            except (ValueError, AttributeError):
                pass

        # Sort by urgency
        for _, widget in sorted(upcoming_items, key=lambda x: x[0]):
            self._upcoming_layout.addWidget(widget)

        if not upcoming_items:
            no_items = QLabel("No upcoming deadlines or events")
            no_items.setObjectName("subtitle")
            self._upcoming_layout.addWidget(no_items)

        self._upcoming_layout.addStretch()

        # Priority breakdown
        self._clear_layout(self._priority_layout)
        priority_counts = {0: 0, 1: 0, 2: 0, 3: 0}
        for task in pending_tasks:
            priority_counts[task.priority] = priority_counts.get(task.priority, 0) + 1

        max_count = max(priority_counts.values()) if any(priority_counts.values()) else 1
        for pri in [3, 2, 1, 0]:
            count = priority_counts[pri]
            row = QHBoxLayout()
            label = QLabel(PRIORITY_LABELS[pri])
            label.setFixedWidth(55)
            label.setStyleSheet(f"font-size: 11px; color: {PRIORITY_COLORS[pri]};")
            row.addWidget(label)

            bar = QFrame()
            width = max(int(count / max_count * 120), 2) if max_count > 0 else 2
            bar.setFixedSize(width, 14)
            bar.setStyleSheet(
                f"background-color: {PRIORITY_COLORS[pri]}; border-radius: 2px;"
            )
            row.addWidget(bar)

            cnt = QLabel(str(count))
            cnt.setObjectName("subtitle")
            cnt.setFixedWidth(25)
            row.addWidget(cnt)
            row.addStretch()

            container = QWidget()
            container.setLayout(row)
            self._priority_layout.addWidget(container)

        # Category breakdown
        self._clear_layout(self._category_layout)
        cat_counts: dict[str, int] = {}
        for task in pending_tasks:
            cat = task.category or "Uncategorized"
            cat_counts[cat] = cat_counts.get(cat, 0) + 1

        if cat_counts:
            max_cat = max(cat_counts.values())
            bar_colors = [accent, green, "#cba6f7", "#fab387", yellow, "#94e2d5"]
            for i, (cat, count) in enumerate(sorted(cat_counts.items(), key=lambda x: -x[1])):
                row = QHBoxLayout()
                label = QLabel(cat)
                label.setFixedWidth(80)
                label.setStyleSheet("font-size: 11px;")
                row.addWidget(label)

                bar = QFrame()
                width = max(int(count / max_cat * 100), 2) if max_cat > 0 else 2
                bar.setFixedSize(width, 14)
                color = bar_colors[i % len(bar_colors)]
                bar.setStyleSheet(f"background-color: {color}; border-radius: 2px;")
                row.addWidget(bar)

                cnt = QLabel(str(count))
                cnt.setObjectName("subtitle")
                cnt.setFixedWidth(25)
                row.addWidget(cnt)
                row.addStretch()

                container = QWidget()
                container.setLayout(row)
                self._category_layout.addWidget(container)
        else:
            no_cats = QLabel("No pending tasks")
            no_cats.setObjectName("subtitle")
            self._category_layout.addWidget(no_cats)

    @staticmethod
    def _clear_layout(layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

```

### `src\ui\modules\finance_charts.py`

```python
"""Finance charts — custom painted graphs for earnings data visualization.

Uses QPainter for zero-dependency chart rendering: line chart, bar chart, pie chart.
"""

import calendar
from datetime import date, timedelta
from math import cos, sin, pi

from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush, QFont, QPainterPath
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QFrame, QSizePolicy,
)

from src.data.finance_store import FinanceStore

CHART_COLORS = [
    "#4a9eff", "#a6e3a1", "#cba6f7", "#fab387", "#f9e2af",
    "#94e2d5", "#f38ba8", "#f5c2e7", "#89b4fa", "#74c7ec",
]


class LineChart(QWidget):
    """Monthly earnings line chart with area fill."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(200)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._data: list[tuple[str, float]] = []  # (month_label, amount)
        self._title = "Monthly Earnings"
        self._color = QColor("#4a9eff")

    def set_data(self, data: list[tuple[str, float]], color: str = "#4a9eff"):
        self._data = data
        self._color = QColor(color)
        self.update()

    def paintEvent(self, event):
        if not self._data:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()
        margin_left = 60
        margin_right = 20
        margin_top = 30
        margin_bottom = 40
        chart_w = w - margin_left - margin_right
        chart_h = h - margin_top - margin_bottom

        if chart_w < 50 or chart_h < 50:
            painter.end()
            return

        # Title
        painter.setPen(QPen(QColor("#cdd6f4")))
        font = QFont()
        font.setBold(True)
        font.setPixelSize(13)
        painter.setFont(font)
        painter.drawText(margin_left, 18, self._title)

        values = [d[1] for d in self._data]
        max_val = max(values) if values else 1
        if max_val == 0:
            max_val = 1

        n = len(self._data)
        if n < 2:
            painter.end()
            return

        # Grid lines + Y axis labels
        font.setBold(False)
        font.setPixelSize(10)
        painter.setFont(font)
        grid_pen = QPen(QColor("#45475a"), 1, Qt.PenStyle.DotLine)
        label_pen = QPen(QColor("#a6adc8"))

        num_grid = 4
        for i in range(num_grid + 1):
            y = margin_top + chart_h - (i / num_grid * chart_h)
            val = max_val * i / num_grid
            painter.setPen(grid_pen)
            painter.drawLine(int(margin_left), int(y), int(w - margin_right), int(y))
            painter.setPen(label_pen)
            painter.drawText(
                QRectF(0, y - 8, margin_left - 6, 16),
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                f"${val:,.0f}",
            )

        # Build points
        points = []
        step = chart_w / (n - 1)
        for i, (label, val) in enumerate(self._data):
            x = margin_left + i * step
            y = margin_top + chart_h - (val / max_val * chart_h)
            points.append(QPointF(x, y))

            # X axis label
            painter.setPen(label_pen)
            painter.drawText(
                QRectF(x - 20, h - margin_bottom + 6, 40, 16),
                Qt.AlignmentFlag.AlignCenter,
                label,
            )

        # Area fill
        area_path = QPainterPath()
        area_path.moveTo(points[0].x(), margin_top + chart_h)
        for pt in points:
            area_path.lineTo(pt)
        area_path.lineTo(points[-1].x(), margin_top + chart_h)
        area_path.closeSubpath()

        fill_color = QColor(self._color)
        fill_color.setAlpha(40)
        painter.fillPath(area_path, QBrush(fill_color))

        # Line
        line_pen = QPen(self._color, 2)
        painter.setPen(line_pen)
        for i in range(len(points) - 1):
            painter.drawLine(points[i], points[i + 1])

        # Dots
        painter.setBrush(QBrush(self._color))
        for pt in points:
            painter.drawEllipse(pt, 4, 4)

        painter.end()


class BarChart(QWidget):
    """Vertical bar chart for category or monthly comparisons."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(200)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._data: list[tuple[str, float]] = []
        self._title = ""
        self._colors: list[str] = CHART_COLORS

    def set_data(self, data: list[tuple[str, float]], title: str = "",
                 colors: list[str] | None = None):
        self._data = data
        self._title = title
        if colors:
            self._colors = colors
        self.update()

    def paintEvent(self, event):
        if not self._data:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()
        margin_left = 60
        margin_right = 20
        margin_top = 30
        margin_bottom = 50
        chart_w = w - margin_left - margin_right
        chart_h = h - margin_top - margin_bottom

        if chart_w < 50 or chart_h < 50:
            painter.end()
            return

        # Title
        painter.setPen(QPen(QColor("#cdd6f4")))
        font = QFont()
        font.setBold(True)
        font.setPixelSize(13)
        painter.setFont(font)
        if self._title:
            painter.drawText(margin_left, 18, self._title)

        values = [d[1] for d in self._data]
        max_val = max(values) if values else 1
        if max_val == 0:
            max_val = 1

        n = len(self._data)
        if n == 0:
            painter.end()
            return

        bar_gap = 6
        bar_w = max((chart_w - bar_gap * (n + 1)) / n, 8)

        # Grid
        font.setBold(False)
        font.setPixelSize(10)
        painter.setFont(font)
        grid_pen = QPen(QColor("#45475a"), 1, Qt.PenStyle.DotLine)
        label_pen = QPen(QColor("#a6adc8"))

        for i in range(5):
            y = margin_top + chart_h - (i / 4 * chart_h)
            val = max_val * i / 4
            painter.setPen(grid_pen)
            painter.drawLine(int(margin_left), int(y), int(w - margin_right), int(y))
            painter.setPen(label_pen)
            painter.drawText(
                QRectF(0, y - 8, margin_left - 6, 16),
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                f"${val:,.0f}",
            )

        # Bars
        for i, (label, val) in enumerate(self._data):
            x = margin_left + bar_gap + i * (bar_w + bar_gap)
            bar_h = (val / max_val) * chart_h
            y = margin_top + chart_h - bar_h

            color = QColor(self._colors[i % len(self._colors)])
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawRoundedRect(QRectF(x, y, bar_w, bar_h), 3, 3)

            # Label below
            painter.setPen(label_pen)
            # Truncate long labels
            display_label = label if len(label) <= 8 else label[:7] + ".."
            painter.drawText(
                QRectF(x - 4, margin_top + chart_h + 4, bar_w + 8, 30),
                Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
                display_label,
            )

            # Value on top
            painter.drawText(
                QRectF(x - 4, y - 16, bar_w + 8, 14),
                Qt.AlignmentFlag.AlignCenter,
                f"${val:,.0f}",
            )

        painter.end()


class PieChart(QWidget):
    """Donut/pie chart for category distribution."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(200, 200)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._data: list[tuple[str, float]] = []
        self._title = ""
        self._colors = CHART_COLORS

    def set_data(self, data: list[tuple[str, float]], title: str = ""):
        self._data = data
        self._title = title
        self.update()

    def paintEvent(self, event):
        if not self._data:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()
        margin = 20
        legend_width = 120
        chart_area = min(w - margin * 2 - legend_width, h - margin * 2 - 20)
        if chart_area < 60:
            painter.end()
            return

        # Title
        painter.setPen(QPen(QColor("#cdd6f4")))
        font = QFont()
        font.setBold(True)
        font.setPixelSize(13)
        painter.setFont(font)
        if self._title:
            painter.drawText(margin, 18, self._title)

        radius = chart_area / 2
        cx = margin + radius
        cy = margin + 24 + radius
        inner_radius = radius * 0.55

        total = sum(v for _, v in self._data)
        if total == 0:
            painter.end()
            return

        start_angle = 90 * 16  # Qt uses 1/16th degree units, start from top
        rect = QRectF(cx - radius, cy - radius, radius * 2, radius * 2)
        inner_rect = QRectF(cx - inner_radius, cy - inner_radius,
                            inner_radius * 2, inner_radius * 2)

        font.setBold(False)
        font.setPixelSize(10)
        painter.setFont(font)

        for i, (label, val) in enumerate(self._data):
            span = int(val / total * 360 * 16)
            color = QColor(self._colors[i % len(self._colors)])

            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(color))

            # Draw pie slice
            path = QPainterPath()
            path.moveTo(cx, cy)
            path.arcTo(rect, start_angle / 16, span / 16)
            path.lineTo(cx, cy)
            painter.drawPath(path)

            start_angle += span

        # Cut out center for donut
        painter.setBrush(QBrush(QColor("#1e1e2e")))
        painter.drawEllipse(inner_rect)

        # Center text
        painter.setPen(QPen(QColor("#cdd6f4")))
        font.setPixelSize(16)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(
            inner_rect, Qt.AlignmentFlag.AlignCenter, f"${total:,.0f}"
        )

        # Legend
        font.setPixelSize(10)
        font.setBold(False)
        painter.setFont(font)
        legend_x = cx + radius + 16
        legend_y = cy - radius + 10

        for i, (label, val) in enumerate(self._data):
            color = QColor(self._colors[i % len(self._colors)])
            y = legend_y + i * 18
            if y > h - 10:
                break

            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(color))
            painter.drawRoundedRect(QRectF(legend_x, y, 10, 10), 2, 2)

            pct = val / total * 100 if total > 0 else 0
            painter.setPen(QPen(QColor("#a6adc8")))
            painter.drawText(
                QRectF(legend_x + 14, y - 2, legend_width - 14, 16),
                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                f"{label} ({pct:.0f}%)",
            )

        painter.end()


class FinanceChartsPanel(QWidget):
    """Charts view for the finance data."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.store = FinanceStore()
        self._palette: dict = {}
        self._build_ui()
        self._refresh()

    def set_palette(self, palette: dict):
        self._palette = palette
        self._refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(10)

        # Header
        header = QHBoxLayout()
        title = QLabel("Financial Charts")
        title.setObjectName("sectionTitle")
        header.addWidget(title)
        header.addStretch()

        header.addWidget(QLabel("Period:"))
        self.period_combo = QComboBox()
        self.period_combo.addItems(["Last 6 Months", "Last 12 Months", "This Year", "All Time"])
        self.period_combo.currentTextChanged.connect(self._refresh)
        header.addWidget(self.period_combo)

        layout.addLayout(header)

        # Top row: line chart
        self.line_chart = LineChart()
        self.line_chart.setMinimumHeight(220)
        layout.addWidget(self.line_chart, 2)

        # Bottom row: bar chart + pie chart
        bottom = QHBoxLayout()
        bottom.setSpacing(12)

        self.bar_chart = BarChart()
        self.bar_chart.setMinimumHeight(200)
        bottom.addWidget(self.bar_chart, 3)

        self.pie_chart = PieChart()
        self.pie_chart.setMinimumHeight(200)
        bottom.addWidget(self.pie_chart, 2)

        layout.addLayout(bottom, 2)

    def _get_date_range(self) -> tuple[str, str]:
        today = date.today()
        period = self.period_combo.currentText()
        if period == "Last 6 Months":
            start = today - timedelta(days=180)
        elif period == "Last 12 Months":
            start = today - timedelta(days=365)
        elif period == "This Year":
            start = today.replace(month=1, day=1)
        else:  # All Time
            start = date(2020, 1, 1)
        return start.isoformat(), today.isoformat()

    def _refresh(self):
        green = self._palette.get("green", "#a6e3a1")
        accent = self._palette.get("accent", "#4a9eff")

        start, end = self._get_date_range()
        txns = self.store.get_transactions(start, end)

        # Monthly earnings line chart
        monthly: dict[str, float] = {}
        monthly_expense: dict[str, float] = {}
        for t in txns:
            month_key = t.date[:7]  # YYYY-MM
            if t.type == "income":
                monthly[month_key] = monthly.get(month_key, 0) + t.amount
            else:
                monthly_expense[month_key] = monthly_expense.get(month_key, 0) + t.amount

        # Ensure we have all months in range
        all_months = sorted(set(list(monthly.keys()) + list(monthly_expense.keys())))
        if not all_months:
            # Generate last 6 months even if no data
            today = date.today()
            for i in range(5, -1, -1):
                m = today - timedelta(days=30 * i)
                all_months.append(m.strftime("%Y-%m"))

        line_data = []
        for m in all_months:
            short_label = m[5:]  # MM from YYYY-MM
            try:
                month_num = int(short_label)
                short_label = calendar.month_abbr[month_num]
            except (ValueError, IndexError):
                pass
            line_data.append((short_label, monthly.get(m, 0)))

        self.line_chart._title = "Monthly Earnings"
        self.line_chart.set_data(line_data, green)

        # Category bar chart (income sources)
        summary = self.store.get_summary(start, end)
        by_cat = summary["by_category"]
        # Split into income and expense categories
        income_by_cat: dict[str, float] = {}
        for t in txns:
            if t.type == "income":
                income_by_cat[t.category] = income_by_cat.get(t.category, 0) + t.amount

        bar_data = sorted(income_by_cat.items(), key=lambda x: -x[1])[:8]
        self.bar_chart.set_data(
            [(cat, amt) for cat, amt in bar_data],
            title="Earnings by Source",
        )

        # Pie chart — all categories
        pie_data = sorted(by_cat.items(), key=lambda x: -x[1])[:8]
        self.pie_chart.set_data(pie_data, title="Spending Distribution")

        self.update()

```

### `src\ui\modules\finance_panel.py`

```python
"""Earnings Tracker module UI — freelance income tracking with summaries."""

from datetime import date

from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor, QBrush
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QLabel, QPushButton, QDialog, QLineEdit, QComboBox,
    QDateEdit, QDoubleSpinBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QFrame, QMessageBox,
)

from src.data.finance_store import FinanceStore, Transaction, DEFAULT_CATEGORIES


class TransactionDialog(QDialog):
    """Dialog to add/edit a transaction (earning or expense)."""

    def __init__(self, parent=None, txn=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Entry" if txn else "New Entry")
        self.setMinimumWidth(380)
        self.txn = txn
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        layout.addWidget(QLabel("Type"))
        self.type_combo = QComboBox()
        self.type_combo.addItems(["income", "expense"])
        if self.txn:
            self.type_combo.setCurrentText(self.txn.type)
        self.type_combo.currentTextChanged.connect(self._on_type_changed)
        layout.addWidget(self.type_combo)

        layout.addWidget(QLabel("Amount"))
        self.amount_spin = QDoubleSpinBox()
        self.amount_spin.setRange(0.01, 9999999.99)
        self.amount_spin.setDecimals(2)
        self.amount_spin.setPrefix("$ ")
        if self.txn:
            self.amount_spin.setValue(self.txn.amount)
        layout.addWidget(self.amount_spin)

        layout.addWidget(QLabel("Date"))
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        if self.txn:
            parts = self.txn.date.split("-")
            self.date_edit.setDate(QDate(int(parts[0]), int(parts[1]), int(parts[2])))
        else:
            today = date.today()
            self.date_edit.setDate(QDate(today.year, today.month, today.day))
        layout.addWidget(self.date_edit)

        self.cat_label = QLabel("Source")
        layout.addWidget(self.cat_label)
        self.cat_combo = QComboBox()
        self.cat_combo.addItems(DEFAULT_CATEGORIES)
        self.cat_combo.setEditable(True)
        if self.txn:
            self.cat_combo.setCurrentText(self.txn.category)
        layout.addWidget(self.cat_combo)

        layout.addWidget(QLabel("Description"))
        self.desc_edit = QLineEdit()
        self.desc_edit.setPlaceholderText("Client name, project, invoice #...")
        if self.txn:
            self.desc_edit.setText(self.txn.description)
        layout.addWidget(self.desc_edit)

        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(sep)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("secondary")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        btn_row.addWidget(save_btn)
        layout.addLayout(btn_row)

        self._on_type_changed(self.type_combo.currentText())

    def _on_type_changed(self, txn_type: str):
        self.cat_label.setText("Source" if txn_type == "income" else "Category")

    def get_data(self) -> dict:
        qd = self.date_edit.date()
        return {
            "date": f"{qd.year():04d}-{qd.month():02d}-{qd.day():02d}",
            "amount": self.amount_spin.value(),
            "txn_type": self.type_combo.currentText(),
            "category": self.cat_combo.currentText(),
            "description": self.desc_edit.text(),
        }


class CategoryBar(QWidget):

    def __init__(self, label: str, amount: float, max_amount: float,
                 bar_color: str = "#4a9eff", parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 2, 0, 2)
        layout.setSpacing(8)

        name_label = QLabel(label)
        name_label.setFixedWidth(110)
        layout.addWidget(name_label)

        bar_frame = QFrame()
        width_pct = (amount / max_amount * 100) if max_amount > 0 else 0
        bar_frame.setStyleSheet(
            f"background-color: {bar_color}; border-radius: 3px; min-height: 16px;"
        )
        bar_frame.setFixedWidth(max(int(width_pct * 1.5), 4))
        layout.addWidget(bar_frame)

        amt_label = QLabel(f"${amount:,.2f}")
        amt_label.setObjectName("subtitle")
        amt_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        amt_label.setFixedWidth(90)
        layout.addWidget(amt_label)

        layout.addStretch()


class FinancePanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.store = FinanceStore()
        self._palette: dict = {}
        self._build_ui()
        self._refresh()

    def set_palette(self, palette: dict):
        self._palette = palette
        self._refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)

        # ── Header with big earnings display ──────────
        header = QHBoxLayout()

        title_col = QVBoxLayout()
        title = QLabel("Earnings Tracker")
        title.setObjectName("sectionTitle")
        title_col.addWidget(title)
        subtitle = QLabel("Freelance income & expenses")
        subtitle.setObjectName("subtitle")
        title_col.addWidget(subtitle)
        header.addLayout(title_col)

        header.addStretch()

        # All-time earnings badge
        self.all_time_label = QLabel("$0.00")
        self.all_time_label.setStyleSheet(
            "font-size: 28px; font-weight: bold; padding: 4px 16px;"
        )
        self.all_time_label.setToolTip("Total amount earned (all time)")
        header.addWidget(self.all_time_label)

        all_time_caption = QLabel("earned all-time")
        all_time_caption.setObjectName("subtitle")
        header.addWidget(all_time_caption)

        header.addSpacing(20)

        btn_add_income = QPushButton("+ Earning")
        btn_add_income.setToolTip("Log a new earning")
        btn_add_income.clicked.connect(self._add_earning)
        header.addWidget(btn_add_income)

        btn_add_expense = QPushButton("+ Expense")
        btn_add_expense.setObjectName("secondary")
        btn_add_expense.setToolTip("Log a new expense")
        btn_add_expense.clicked.connect(self._add_expense)
        header.addWidget(btn_add_expense)

        btn_delete = QPushButton("Delete")
        btn_delete.setObjectName("destructive")
        btn_delete.clicked.connect(self._delete_transaction)
        header.addWidget(btn_delete)

        layout.addLayout(header)

        # ── Filters ───────────────────────────────────
        filter_row = QHBoxLayout()
        filter_row.setSpacing(8)
        filter_row.addWidget(QLabel("Show:"))

        self.filter_type = QComboBox()
        self.filter_type.addItems(["All", "income", "expense"])
        self.filter_type.currentTextChanged.connect(self._refresh)
        filter_row.addWidget(self.filter_type)

        filter_row.addSpacing(12)
        filter_row.addWidget(QLabel("From:"))
        self.filter_start = QDateEdit()
        self.filter_start.setCalendarPopup(True)
        today = date.today()
        self.filter_start.setDate(QDate(today.year, today.month, 1))
        self.filter_start.dateChanged.connect(self._refresh)
        filter_row.addWidget(self.filter_start)

        filter_row.addWidget(QLabel("To:"))
        self.filter_end = QDateEdit()
        self.filter_end.setCalendarPopup(True)
        self.filter_end.setDate(QDate(today.year, today.month, today.day))
        self.filter_end.dateChanged.connect(self._refresh)
        filter_row.addWidget(self.filter_end)

        filter_row.addStretch()
        layout.addLayout(filter_row)

        # ── Content: table + summary ──────────────────
        content = QSplitter(Qt.Orientation.Horizontal)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Date", "Type", "Source", "Amount", "Description"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.doubleClicked.connect(self._edit_transaction)
        content.addWidget(self.table)

        # Summary panel
        summary_widget = QWidget()
        self.summary_layout = QVBoxLayout(summary_widget)
        self.summary_layout.setContentsMargins(16, 12, 16, 12)
        self.summary_layout.setSpacing(8)

        period_title = QLabel("Period Summary")
        period_title.setObjectName("sectionTitle")
        self.summary_layout.addWidget(period_title)

        self.earned_label = QLabel("Earned: $0.00")
        self.earned_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.summary_layout.addWidget(self.earned_label)

        self.spent_label = QLabel("Spent: $0.00")
        self.spent_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.summary_layout.addWidget(self.spent_label)

        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine)
        self.summary_layout.addWidget(sep)

        self.net_label = QLabel("Net: $0.00")
        self.net_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.summary_layout.addWidget(self.net_label)

        self.txn_count_label = QLabel("0 transactions")
        self.txn_count_label.setObjectName("subtitle")
        self.summary_layout.addWidget(self.txn_count_label)

        sep2 = QFrame()
        sep2.setObjectName("separator")
        sep2.setFrameShape(QFrame.Shape.HLine)
        self.summary_layout.addWidget(sep2)

        cat_title = QLabel("By Source / Category")
        cat_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.summary_layout.addWidget(cat_title)

        self.cat_bars_container = QWidget()
        self.cat_bars_layout = QVBoxLayout(self.cat_bars_container)
        self.cat_bars_layout.setContentsMargins(0, 0, 0, 0)
        self.cat_bars_layout.setSpacing(2)
        self.summary_layout.addWidget(self.cat_bars_container)

        self.summary_layout.addStretch()
        content.addWidget(summary_widget)
        content.setSizes([520, 280])

        layout.addWidget(content, 1)

    def _get_filters(self) -> tuple:
        qs = self.filter_start.date()
        qe = self.filter_end.date()
        start = f"{qs.year():04d}-{qs.month():02d}-{qs.day():02d}"
        end = f"{qe.year():04d}-{qe.month():02d}-{qe.day():02d}"
        txn_type = self.filter_type.currentText()
        if txn_type == "All":
            txn_type = None
        return start, end, txn_type

    def _refresh(self):
        start, end, txn_type = self._get_filters()
        txns = self.store.get_transactions(start, end, txn_type)

        green = self._palette.get("green", "#a6e3a1")
        red = self._palette.get("red", "#f38ba8")
        accent = self._palette.get("accent", "#4a9eff")

        # All-time earned
        all_time = self.store.get_all_time_earned()
        self.all_time_label.setText(f"${all_time:,.2f}")
        self.all_time_label.setStyleSheet(
            f"color: {green}; font-size: 28px; font-weight: bold; padding: 4px 16px;"
        )

        # Table
        self.table.setRowCount(len(txns))
        self._txn_ids = []
        for row, txn in enumerate(txns):
            self._txn_ids.append(txn.id)
            self.table.setItem(row, 0, QTableWidgetItem(txn.date))

            type_text = "Earned" if txn.type == "income" else "Spent"
            type_item = QTableWidgetItem(type_text)
            color = QColor(green if txn.type == "income" else red)
            type_item.setForeground(QBrush(color))
            self.table.setItem(row, 1, type_item)

            self.table.setItem(row, 2, QTableWidgetItem(txn.category))

            prefix = "+" if txn.type == "income" else "-"
            amt_item = QTableWidgetItem(f"{prefix}${txn.amount:,.2f}")
            amt_item.setForeground(QBrush(color))
            amt_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row, 3, amt_item)

            self.table.setItem(row, 4, QTableWidgetItem(txn.description))

        # Summary
        summary = self.store.get_summary(start, end)
        self.earned_label.setText(f"Earned: ${summary['earned']:,.2f}")
        self.earned_label.setStyleSheet(f"color: {green}; font-size: 18px; font-weight: bold;")
        self.spent_label.setText(f"Spent: ${summary['spent']:,.2f}")
        self.spent_label.setStyleSheet(f"color: {red}; font-size: 16px; font-weight: bold;")

        net = summary['net']
        net_color = green if net >= 0 else red
        sign = "+" if net >= 0 else ""
        self.net_label.setText(f"Net: {sign}${net:,.2f}")
        self.net_label.setStyleSheet(f"color: {net_color}; font-size: 20px; font-weight: bold;")

        self.txn_count_label.setText(f"{summary['count']} transaction(s) in period")

        # Category bars
        while self.cat_bars_layout.count():
            child = self.cat_bars_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        by_cat = summary['by_category']
        if by_cat:
            max_amount = max(by_cat.values())
            bar_colors = [accent, green, "#cba6f7", "#fab387", "#f9e2af", "#94e2d5", red, "#f5c2e7"]
            for i, (cat, amount) in enumerate(sorted(by_cat.items(), key=lambda x: -x[1])):
                bar = CategoryBar(cat, amount, max_amount, bar_colors[i % len(bar_colors)])
                self.cat_bars_layout.addWidget(bar)
        else:
            no_data = QLabel("No transactions in this period")
            no_data.setObjectName("subtitle")
            self.cat_bars_layout.addWidget(no_data)

    def _add_earning(self):
        dlg = TransactionDialog(self)
        dlg.type_combo.setCurrentText("income")
        if dlg.exec():
            self.store.add_transaction(**dlg.get_data())
            self._refresh()

    def _add_expense(self):
        dlg = TransactionDialog(self)
        dlg.type_combo.setCurrentText("expense")
        if dlg.exec():
            self.store.add_transaction(**dlg.get_data())
            self._refresh()

    def _edit_transaction(self, index):
        row = index.row()
        if row < 0 or row >= len(self._txn_ids):
            return
        txn_id = self._txn_ids[row]
        txns = self.store.get_transactions()
        txn = next((t for t in txns if t.id == txn_id), None)
        if not txn:
            return
        dlg = TransactionDialog(self, txn)
        if dlg.exec():
            data = dlg.get_data()
            txn.date = data["date"]
            txn.amount = data["amount"]
            txn.type = data["txn_type"]
            txn.category = data["category"]
            txn.description = data["description"]
            self.store.update_transaction(txn)
            self._refresh()

    def _delete_transaction(self):
        rows = self.table.selectionModel().selectedRows()
        if not rows:
            return
        reply = QMessageBox.question(
            self, "Delete",
            f"Delete {len(rows)} entry/entries?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            for idx in rows:
                txn_id = self._txn_ids[idx.row()]
                self.store.delete_transaction(txn_id)
            self._refresh()

```

### `src\ui\modules\notes_panel.py`

```python
"""Notes/Obsidian module UI — tree-based vault browser, markdown editor, REST API integration.

The sidebar uses a QTreeWidget with collapsible folders (triangle toggles)
that mimics Obsidian's file explorer layout.
"""

import json
import logging
import threading
from collections import defaultdict
from pathlib import Path, PurePosixPath

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QTreeWidget, QTreeWidgetItem, QPlainTextEdit,
    QLineEdit, QPushButton, QLabel, QMessageBox, QInputDialog,
    QFrame, QFileDialog,
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
            import urllib.request
            req = urllib.request.Request(
                f"{self.base_url}/", headers=self._headers(), method="GET",
            )
            with urllib.request.urlopen(req, timeout=3) as resp:
                return resp.status == 200
        except Exception:
            return False

    def list_files(self, folder: str = "/") -> list[str]:
        try:
            import urllib.request
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
            import urllib.request, urllib.parse
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
            import urllib.request, urllib.parse
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
            import urllib.request, urllib.parse
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
        import subprocess
        import sys
        import urllib.parse
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
                import os
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

        editor_layout.addLayout(title_row)

        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine)
        editor_layout.addWidget(sep)

        self.editor = QPlainTextEdit()
        self.editor.setPlaceholderText(
            "Start writing in Markdown...\n\nUse #tags anywhere in your text."
        )
        self.editor.setTabStopDistance(28.0)
        self.editor.textChanged.connect(self._on_text_changed)
        editor_layout.addWidget(self.editor, 1)

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
        import subprocess
        import sys
        import urllib.parse
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
                import os
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

```

### `src\ui\modules\todo_panel.py`

```python
"""Todo list module UI — modern task manager with priorities, categories, and due dates."""

from datetime import date

from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor, QBrush, QFont
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QDialog, QLineEdit, QComboBox,
    QDateEdit, QTextEdit, QCheckBox, QFrame, QMessageBox,
    QListWidget, QListWidgetItem, QScrollArea,
)

from src.data.todo_store import (
    TodoStore, TodoItem, PRIORITY_LABELS, DEFAULT_TODO_CATEGORIES,
)


PRIORITY_COLORS = {0: "#a6adc8", 1: "#a6e3a1", 2: "#f9e2af", 3: "#f38ba8"}
PRIORITY_ICONS = {0: "", 1: "!", 2: "!!", 3: "!!!"}


class TodoDialog(QDialog):
    """Dialog to add/edit a todo item."""

    def __init__(self, parent=None, item: TodoItem | None = None):
        super().__init__(parent)
        self.setWindowTitle("Edit Task" if item else "New Task")
        self.setMinimumWidth(360)
        self.item = item
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(12, 10, 12, 10)

        layout.addWidget(QLabel("Title"))
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("What needs to be done?")
        if self.item:
            self.title_edit.setText(self.item.title)
        layout.addWidget(self.title_edit)

        row = QHBoxLayout()
        row.setSpacing(8)

        col1 = QVBoxLayout()
        col1.addWidget(QLabel("Priority"))
        self.priority_combo = QComboBox()
        for val, label in PRIORITY_LABELS.items():
            self.priority_combo.addItem(label, val)
        if self.item:
            idx = self.priority_combo.findData(self.item.priority)
            if idx >= 0:
                self.priority_combo.setCurrentIndex(idx)
        col1.addWidget(self.priority_combo)
        row.addLayout(col1)

        col2 = QVBoxLayout()
        col2.addWidget(QLabel("Category"))
        self.cat_combo = QComboBox()
        self.cat_combo.setEditable(True)
        self.cat_combo.addItems(DEFAULT_TODO_CATEGORIES)
        if self.item and self.item.category:
            self.cat_combo.setCurrentText(self.item.category)
        col2.addWidget(self.cat_combo)
        row.addLayout(col2)

        col3 = QVBoxLayout()
        col3.addWidget(QLabel("Due date"))
        self.due_check = QCheckBox("Set")
        self.due_edit = QDateEdit()
        self.due_edit.setCalendarPopup(True)
        if self.item and self.item.due_date:
            self.due_check.setChecked(True)
            parts = self.item.due_date.split("-")
            self.due_edit.setDate(QDate(int(parts[0]), int(parts[1]), int(parts[2])))
        else:
            self.due_check.setChecked(False)
            today = date.today()
            self.due_edit.setDate(QDate(today.year, today.month, today.day))
        self.due_check.toggled.connect(lambda c: self.due_edit.setEnabled(c))
        self.due_edit.setEnabled(self.due_check.isChecked())
        due_row = QHBoxLayout()
        due_row.addWidget(self.due_check)
        due_row.addWidget(self.due_edit, 1)
        col3.addLayout(due_row)
        row.addLayout(col3)

        layout.addLayout(row)

        layout.addWidget(QLabel("Notes"))
        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(60)
        self.notes_edit.setPlaceholderText("Optional notes...")
        if self.item:
            self.notes_edit.setPlainText(self.item.notes)
        layout.addWidget(self.notes_edit)

        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(sep)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("secondary")
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        btn_row.addWidget(save_btn)
        layout.addLayout(btn_row)

    def get_data(self) -> dict:
        due = ""
        if self.due_check.isChecked():
            qd = self.due_edit.date()
            due = f"{qd.year():04d}-{qd.month():02d}-{qd.day():02d}"
        return {
            "title": self.title_edit.text().strip() or "Untitled",
            "priority": self.priority_combo.currentData(),
            "due_date": due,
            "category": self.cat_combo.currentText(),
            "notes": self.notes_edit.toPlainText(),
        }


class TodoItemWidget(QFrame):
    """A single todo item rendered as a compact card."""

    def __init__(self, item: TodoItem, parent_panel):
        super().__init__()
        self.item = item
        self.panel = parent_panel
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(6)

        # Checkbox
        self.check = QCheckBox()
        self.check.setChecked(item.done)
        self.check.toggled.connect(self._on_toggle)
        layout.addWidget(self.check)

        # Priority dot
        if item.priority > 0:
            dot = QLabel(PRIORITY_ICONS[item.priority])
            color = PRIORITY_COLORS[item.priority]
            dot.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 11px;")
            dot.setFixedWidth(20)
            layout.addWidget(dot)

        # Title + metadata
        info = QVBoxLayout()
        info.setSpacing(0)
        info.setContentsMargins(0, 0, 0, 0)

        title = QLabel(item.title)
        font_style = "font-size: 12px; font-weight: bold;"
        if item.done:
            font_style += " text-decoration: line-through; opacity: 0.6;"
        title.setStyleSheet(font_style)
        info.addWidget(title)

        # Metadata row
        meta_parts = []
        if item.category:
            meta_parts.append(item.category)
        if item.due_date:
            meta_parts.append(f"Due: {item.due_date}")
        if meta_parts:
            meta = QLabel(" \u00b7 ".join(meta_parts))
            meta.setObjectName("subtitle")
            meta.setStyleSheet("font-size: 10px;")
            info.addWidget(meta)

        layout.addLayout(info, 1)

        # Edit button
        edit_btn = QPushButton("Edit")
        edit_btn.setObjectName("secondary")
        edit_btn.setFixedSize(40, 22)
        edit_btn.setStyleSheet("font-size: 10px; padding: 2px 6px;")
        edit_btn.clicked.connect(self._on_edit)
        layout.addWidget(edit_btn)

        # Priority color stripe on left
        border_color = PRIORITY_COLORS.get(item.priority, "transparent")
        if item.priority > 0:
            self.setStyleSheet(
                f"TodoItemWidget {{ border-left: 3px solid {border_color}; "
                f"border-radius: 4px; }}"
            )

    def _on_toggle(self, checked):
        self.panel._toggle_item(self.item.id)

    def _on_edit(self):
        self.panel._edit_item(self.item)

    def mouseDoubleClickEvent(self, ev):
        self.panel._edit_item(self.item)


class TodoPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.store = TodoStore()
        self._palette: dict = {}
        self._build_ui()
        self._refresh()

    def set_palette(self, palette: dict):
        self._palette = palette

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(6)

        # Header
        header = QHBoxLayout()
        title = QLabel("Tasks")
        title.setObjectName("sectionTitle")
        header.addWidget(title)

        self.count_label = QLabel("0 tasks")
        self.count_label.setObjectName("subtitle")
        header.addWidget(self.count_label)

        header.addStretch()

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All", "Pending", "Completed"])
        self.filter_combo.setFixedWidth(90)
        self.filter_combo.currentTextChanged.connect(self._refresh)
        header.addWidget(self.filter_combo)

        btn_add = QPushButton("+ Task")
        btn_add.clicked.connect(self._add_item)
        header.addWidget(btn_add)

        btn_clear = QPushButton("Clear Done")
        btn_clear.setObjectName("secondary")
        btn_clear.clicked.connect(self._clear_done)
        header.addWidget(btn_clear)

        layout.addLayout(header)

        # Quick add
        quick_row = QHBoxLayout()
        quick_row.setSpacing(4)
        self.quick_input = QLineEdit()
        self.quick_input.setPlaceholderText("Quick add task... (Enter to add)")
        self.quick_input.returnPressed.connect(self._quick_add)
        quick_row.addWidget(self.quick_input, 1)
        layout.addLayout(quick_row)

        # Task list
        self._list_container = QWidget()
        self._list_layout = QVBoxLayout(self._list_container)
        self._list_layout.setContentsMargins(0, 0, 0, 0)
        self._list_layout.setSpacing(2)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self._list_container)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        layout.addWidget(scroll, 1)

        # Footer stats
        footer = QHBoxLayout()
        self.stats_label = QLabel("")
        self.stats_label.setObjectName("subtitle")
        footer.addWidget(self.stats_label)
        footer.addStretch()
        layout.addLayout(footer)

    def _refresh(self):
        # Clear list
        while self._list_layout.count():
            child = self._list_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        filter_mode = self.filter_combo.currentText()
        items = self.store.get_all(include_done=(filter_mode != "Pending"))

        if filter_mode == "Completed":
            items = [i for i in items if i.done]

        for item in items:
            widget = TodoItemWidget(item, self)
            self._list_layout.addWidget(widget)

        self._list_layout.addStretch()

        counts = self.store.get_counts()
        self.count_label.setText(f"{counts['total']} tasks")
        self.stats_label.setText(
            f"{counts['pending']} pending \u00b7 {counts['done']} completed"
        )

    def _quick_add(self):
        text = self.quick_input.text().strip()
        if text:
            self.store.add(title=text)
            self.quick_input.clear()
            self._refresh()

    def _add_item(self):
        dlg = TodoDialog(self)
        if dlg.exec():
            data = dlg.get_data()
            self.store.add(**data)
            self._refresh()

    def _edit_item(self, item: TodoItem):
        dlg = TodoDialog(self, item)
        if dlg.exec():
            data = dlg.get_data()
            item.title = data["title"]
            item.priority = data["priority"]
            item.due_date = data["due_date"]
            item.category = data["category"]
            item.notes = data["notes"]
            self.store.update(item)
            self._refresh()

    def _toggle_item(self, item_id: str):
        self.store.toggle_done(item_id)
        self._refresh()

    def _clear_done(self):
        items = self.store.get_all()
        done_items = [i for i in items if i.done]
        if not done_items:
            return
        reply = QMessageBox.question(
            self, "Clear Completed",
            f"Remove {len(done_items)} completed task(s)?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            for item in done_items:
                self.store.delete(item.id)
            self._refresh()

```

### `src\ui\themes\__init__.py`

```python
"""Theme definitions and management."""

from src.ui.themes.styles import THEMES, get_theme_names

__all__ = ["THEMES", "get_theme_names"]

```

### `src\ui\themes\styles.py`

```python
"""Theme stylesheets for PyQt6 — Catppuccin Dark, Catppuccin Light, Nord, Solarized, Gruvbox."""


def _build_theme(c: dict) -> str:
    """Generate a full QSS stylesheet from a color palette dict."""
    return f"""
/* ── Base ──────────────────────────────────────────── */
QMainWindow, QWidget {{
    background-color: {c['bg']};
    color: {c['fg']};
    font-family: "Segoe UI", "Ubuntu", "Noto Sans", sans-serif;
    font-size: 12px;
}}

/* ── Text inputs ──────────────────────────────────── */
QLineEdit, QTextEdit, QPlainTextEdit {{
    background-color: {c['surface']};
    color: {c['fg']};
    border: 1px solid {c['border']};
    border-radius: 4px;
    padding: 4px;
    selection-background-color: {c['accent']};
    selection-color: {c['accent_fg']};
}}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
    border: 1px solid {c['accent']};
}}
QLineEdit[readOnly="true"] {{
    background-color: {c['bg']};
}}

/* ── Buttons ──────────────────────────────────────── */
QPushButton {{
    background-color: {c['accent']};
    color: {c['accent_fg']};
    border: none;
    border-radius: 4px;
    padding: 5px 12px;
    font-weight: bold;
}}
QPushButton:hover {{
    background-color: {c['accent_hover']};
}}
QPushButton:pressed {{
    background-color: {c['accent_pressed']};
}}
QPushButton:disabled {{
    background-color: {c['border']};
    color: {c['muted']};
}}
QPushButton#destructive {{
    background-color: {c['red']};
    color: {c['accent_fg']};
}}
QPushButton#destructive:hover {{
    background-color: {c['red_hover']};
}}
QPushButton#secondary {{
    background-color: {c['surface']};
    color: {c['fg']};
    border: 1px solid {c['border']};
}}
QPushButton#secondary:hover {{
    background-color: {c['border']};
}}

/* ── Lists ────────────────────────────────────────── */
QListWidget {{
    background-color: {c['surface']};
    border: 1px solid {c['border']};
    border-radius: 6px;
    padding: 4px;
    outline: none;
}}
QListWidget::item {{
    padding: 4px;
    border-radius: 3px;
}}
QListWidget::item:selected {{
    background-color: {c['accent']};
    color: {c['accent_fg']};
}}
QListWidget::item:hover:!selected {{
    background-color: {c['hover']};
}}

/* ── Tables ───────────────────────────────────────── */
QTableWidget {{
    background-color: {c['surface']};
    border: 1px solid {c['border']};
    border-radius: 6px;
    gridline-color: {c['border']};
    outline: none;
}}
QTableWidget::item {{
    padding: 3px;
}}
QTableWidget::item:selected {{
    background-color: {c['accent']};
    color: {c['accent_fg']};
}}
QTableWidget::item:alternate {{
    background-color: {c['alt_row']};
}}
QHeaderView::section {{
    background-color: {c['header_bg']};
    color: {c['fg']};
    padding: 4px;
    border: none;
    border-bottom: 2px solid {c['accent']};
    font-weight: bold;
}}

/* ── Combo boxes ──────────────────────────────────── */
QComboBox {{
    background-color: {c['surface']};
    color: {c['fg']};
    border: 1px solid {c['border']};
    border-radius: 4px;
    padding: 3px 6px;
    min-width: 70px;
}}
QComboBox::drop-down {{
    border: none;
    width: 20px;
}}
QComboBox QAbstractItemView {{
    background-color: {c['surface']};
    color: {c['fg']};
    selection-background-color: {c['accent']};
    selection-color: {c['accent_fg']};
    border: 1px solid {c['border']};
    border-radius: 4px;
}}

/* ── Spin boxes / Date edits ──────────────────────── */
QDateEdit, QTimeEdit, QSpinBox, QDoubleSpinBox {{
    background-color: {c['surface']};
    color: {c['fg']};
    border: 1px solid {c['border']};
    border-radius: 4px;
    padding: 3px;
}}
QDateEdit::drop-down, QTimeEdit::drop-down {{
    border: none;
}}

/* ── Check boxes ──────────────────────────────────── */
QCheckBox {{
    spacing: 8px;
}}
QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 2px solid {c['border']};
    background-color: {c['surface']};
}}
QCheckBox::indicator:checked {{
    background-color: {c['accent']};
    border-color: {c['accent']};
}}

/* ── Labels ───────────────────────────────────────── */
QLabel#sectionTitle {{
    font-size: 15px;
    font-weight: bold;
    color: {c['fg']};
    padding-bottom: 1px;
}}
QLabel#subtitle {{
    font-size: 11px;
    color: {c['muted']};
}}
QLabel#statusOk {{
    color: {c['green']};
    font-size: 12px;
}}
QLabel#statusWarn {{
    color: {c['yellow']};
    font-size: 12px;
}}

/* ── Separators ───────────────────────────────────── */
QFrame#separator {{
    background-color: {c['border']};
    max-height: 1px;
}}

/* ── Splitter handles ─────────────────────────────── */
QSplitter::handle {{
    background-color: {c['border']};
    width: 2px;
    margin: 4px 2px;
}}
QSplitter::handle:hover {{
    background-color: {c['accent']};
}}

/* ── Scroll bars ──────────────────────────────────── */
QScrollBar:vertical {{
    background-color: transparent;
    width: 10px;
    border-radius: 5px;
    margin: 2px;
}}
QScrollBar::handle:vertical {{
    background-color: {c['border']};
    border-radius: 5px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{
    background-color: {c['muted']};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}
QScrollBar:horizontal {{
    background-color: transparent;
    height: 10px;
    border-radius: 5px;
    margin: 2px;
}}
QScrollBar::handle:horizontal {{
    background-color: {c['border']};
    border-radius: 5px;
    min-width: 30px;
}}
QScrollBar::handle:horizontal:hover {{
    background-color: {c['muted']};
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0px;
}}

/* ── Tooltips ─────────────────────────────────────── */
QToolTip {{
    background-color: {c['surface']};
    color: {c['fg']};
    border: 1px solid {c['border']};
    border-radius: 4px;
    padding: 4px 8px;
}}

/* ── Dialogs ──────────────────────────────────────── */
QDialog {{
    background-color: {c['bg']};
}}
QMessageBox {{
    background-color: {c['bg']};
}}

/* ── Status bar ───────────────────────────────────── */
QStatusBar {{
    background-color: {c['header_bg']};
    color: {c['muted']};
    border-top: 1px solid {c['border']};
    font-size: 11px;
    padding: 1px 6px;
}}
QStatusBar::item {{
    border: none;
}}
"""


# ── Catppuccin Mocha (Dark) ──────────────────────────
_CATPPUCCIN_DARK = {
    "bg": "#1e1e2e", "surface": "#313244", "border": "#45475a",
    "fg": "#cdd6f4", "muted": "#a6adc8", "hover": "#3b3d54",
    "accent": "#4a9eff", "accent_fg": "#1e1e2e",
    "accent_hover": "#6ab0ff", "accent_pressed": "#3a8eef",
    "red": "#f38ba8", "red_hover": "#f5a0b8",
    "green": "#a6e3a1", "yellow": "#f9e2af",
    "header_bg": "#181825", "alt_row": "#2a2a3c",
}

# ── Catppuccin Latte (Light) ─────────────────────────
_CATPPUCCIN_LIGHT = {
    "bg": "#eff1f5", "surface": "#ffffff", "border": "#ccd0da",
    "fg": "#4c4f69", "muted": "#8c8fa1", "hover": "#e6e9ef",
    "accent": "#1e66f5", "accent_fg": "#ffffff",
    "accent_hover": "#4080f7", "accent_pressed": "#1650d0",
    "red": "#d20f39", "red_hover": "#e0304f",
    "green": "#40a02b", "yellow": "#df8e1d",
    "header_bg": "#e6e9ef", "alt_row": "#f4f5f8",
}

# ── Nord ─────────────────────────────────────────────
_NORD = {
    "bg": "#2e3440", "surface": "#3b4252", "border": "#4c566a",
    "fg": "#eceff4", "muted": "#d8dee9", "hover": "#434c5e",
    "accent": "#88c0d0", "accent_fg": "#2e3440",
    "accent_hover": "#8fbcbb", "accent_pressed": "#81a1c1",
    "red": "#bf616a", "red_hover": "#d08770",
    "green": "#a3be8c", "yellow": "#ebcb8b",
    "header_bg": "#272c36", "alt_row": "#333a47",
}

# ── Solarized Dark ───────────────────────────────────
_SOLARIZED = {
    "bg": "#002b36", "surface": "#073642", "border": "#586e75",
    "fg": "#839496", "muted": "#657b83", "hover": "#0a4050",
    "accent": "#268bd2", "accent_fg": "#fdf6e3",
    "accent_hover": "#2aa198", "accent_pressed": "#1a6da0",
    "red": "#dc322f", "red_hover": "#e35550",
    "green": "#859900", "yellow": "#b58900",
    "header_bg": "#001f27", "alt_row": "#04303d",
}

# ── Gruvbox Dark ─────────────────────────────────────
_GRUVBOX = {
    "bg": "#282828", "surface": "#3c3836", "border": "#504945",
    "fg": "#ebdbb2", "muted": "#a89984", "hover": "#444240",
    "accent": "#d79921", "accent_fg": "#282828",
    "accent_hover": "#fabd2f", "accent_pressed": "#b57614",
    "red": "#cc241d", "red_hover": "#fb4934",
    "green": "#98971a", "yellow": "#d79921",
    "header_bg": "#1d2021", "alt_row": "#32302f",
}


# ── Build all themes ─────────────────────────────────
THEMES = {
    "Catppuccin Dark": _build_theme(_CATPPUCCIN_DARK),
    "Catppuccin Light": _build_theme(_CATPPUCCIN_LIGHT),
    "Nord": _build_theme(_NORD),
    "Solarized Dark": _build_theme(_SOLARIZED),
    "Gruvbox Dark": _build_theme(_GRUVBOX),
}

# Color palettes exposed for programmatic access (e.g. chart colors)
PALETTES = {
    "Catppuccin Dark": _CATPPUCCIN_DARK,
    "Catppuccin Light": _CATPPUCCIN_LIGHT,
    "Nord": _NORD,
    "Solarized Dark": _SOLARIZED,
    "Gruvbox Dark": _GRUVBOX,
}


def get_theme_names() -> list[str]:
    return list(THEMES.keys())

```

### `src\ui\widgets\__init__.py`

```python
"""Reusable UI widgets."""

from src.ui.widgets.network_dialog import NetworkDialog

__all__ = ["NetworkDialog"]

```

### `src\ui\widgets\network_dialog.py`

```python
"""Network settings dialog — configure sync, view peers, manage connections."""

import socket
import threading

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QLineEdit, QSpinBox, QCheckBox,
    QFrame, QTableWidget, QTableWidgetItem, QHeaderView,
    QTextEdit, QTabWidget, QWidget, QMessageBox, QFileDialog,
)

from src.config import load_config, save_config


class NetworkDialog(QDialog):
    """Network and sync settings with live peer status and log viewer."""

    def __init__(self, sync_engine=None, parent=None):
        super().__init__(parent)
        self.sync_engine = sync_engine
        self.setWindowTitle("Network & Sync Settings")
        self.setMinimumSize(650, 520)
        self.cfg = load_config()
        self._build_ui()
        self._load_values()

        # Connect to sync engine signals
        if self.sync_engine:
            self.sync_engine.peers_updated.connect(self._update_peer_table)
            self.sync_engine.sync_log.connect(self._append_log)

        # Refresh peer table periodically
        self._refresh_timer = QTimer(self)
        self._refresh_timer.timeout.connect(self._refresh_peers)
        self._refresh_timer.start(5000)
        self._refresh_peers()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        tabs = QTabWidget()

        # ── Tab 1: Network Settings ───────────────────
        settings_tab = QWidget()
        settings_layout = QVBoxLayout(settings_tab)
        settings_layout.setSpacing(12)

        # Local info
        info_label = QLabel("This Device")
        info_label.setObjectName("sectionTitle")
        settings_layout.addWidget(info_label)

        local_ip = self._get_local_ip()
        hostname = socket.gethostname()
        info_grid = QGridLayout()
        info_grid.addWidget(QLabel("Hostname:"), 0, 0)
        info_grid.addWidget(QLabel(f"<b>{hostname}</b>"), 0, 1)
        info_grid.addWidget(QLabel("IP Address:"), 1, 0)
        info_grid.addWidget(QLabel(f"<b>{local_ip}</b>"), 1, 1)
        settings_layout.addLayout(info_grid)

        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine)
        settings_layout.addWidget(sep)

        # Sync config
        sync_label = QLabel("Sync Configuration")
        sync_label.setObjectName("sectionTitle")
        settings_layout.addWidget(sync_label)

        form = QGridLayout()
        form.setSpacing(8)

        form.addWidget(QLabel("Sync enabled:"), 0, 0)
        self.sync_enabled_check = QCheckBox()
        form.addWidget(self.sync_enabled_check, 0, 1)

        form.addWidget(QLabel("Subnet prefix:"), 1, 0)
        self.subnet_edit = QLineEdit()
        self.subnet_edit.setPlaceholderText("e.g. 192.168.0")
        self.subnet_edit.setMaximumWidth(200)
        form.addWidget(self.subnet_edit, 1, 1)

        form.addWidget(QLabel("Sync port:"), 2, 0)
        self.port_spin = QSpinBox()
        self.port_spin.setRange(1024, 65535)
        self.port_spin.setMaximumWidth(120)
        form.addWidget(self.port_spin, 2, 1)

        form.addWidget(QLabel("Interval (seconds):"), 3, 0)
        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(30, 3600)
        self.interval_spin.setSingleStep(30)
        self.interval_spin.setMaximumWidth(120)
        form.addWidget(self.interval_spin, 3, 1)

        form.addWidget(QLabel("Scan timeout (ms):"), 4, 0)
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(50, 2000)
        self.timeout_spin.setSingleStep(50)
        self.timeout_spin.setMaximumWidth(120)
        form.addWidget(self.timeout_spin, 4, 1)

        settings_layout.addLayout(form)
        settings_layout.addStretch()

        # Save button
        save_row = QHBoxLayout()
        save_row.addStretch()
        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self._save_settings)
        save_row.addWidget(save_btn)
        settings_layout.addLayout(save_row)

        tabs.addTab(settings_tab, "Settings")

        # ── Tab 1.5: Obsidian ─────────────────────────
        obs_tab = QWidget()
        obs_layout = QVBoxLayout(obs_tab)
        obs_layout.setSpacing(10)

        obs_title = QLabel("Obsidian Integration")
        obs_title.setObjectName("sectionTitle")
        obs_layout.addWidget(obs_title)

        obs_desc = QLabel(
            "Configure your Obsidian vault path and REST API settings.\n"
            "The vault path is used to sync markdown files between computers.\n"
            "The REST API connects to the Obsidian Local REST API plugin."
        )
        obs_desc.setObjectName("subtitle")
        obs_desc.setWordWrap(True)
        obs_layout.addWidget(obs_desc)

        obs_form = QGridLayout()
        obs_form.setSpacing(8)

        obs_form.addWidget(QLabel("Vault path:"), 0, 0)
        self.vault_path_edit = QLineEdit()
        self.vault_path_edit.setPlaceholderText("/path/to/your/obsidian/vault")
        self.vault_path_edit.setText(self.cfg.get("obsidian_vault_path", ""))
        obs_form.addWidget(self.vault_path_edit, 0, 1)
        browse_btn = QPushButton("Browse")
        browse_btn.setObjectName("secondary")
        browse_btn.clicked.connect(self._browse_vault)
        obs_form.addWidget(browse_btn, 0, 2)

        obs_form.addWidget(QLabel("Sync vault files:"), 1, 0)
        self.vault_sync_check = QCheckBox()
        self.vault_sync_check.setChecked(self.cfg.get("obsidian_sync_enabled", False))
        obs_form.addWidget(self.vault_sync_check, 1, 1)

        sep_obs = QFrame()
        sep_obs.setObjectName("separator")
        sep_obs.setFrameShape(QFrame.Shape.HLine)
        obs_form.addWidget(sep_obs, 2, 0, 1, 3)

        obs_form.addWidget(QLabel("REST API key:"), 3, 0)
        self.api_key_edit = QLineEdit()
        self.api_key_edit.setPlaceholderText("From Obsidian Local REST API plugin")
        self.api_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_edit.setText(self.cfg.get("obsidian_api_key", ""))
        obs_form.addWidget(self.api_key_edit, 3, 1, 1, 2)

        obs_form.addWidget(QLabel("REST API URL:"), 4, 0)
        self.api_url_edit = QLineEdit()
        self.api_url_edit.setText(self.cfg.get("obsidian_api_url", "http://127.0.0.1:27123"))
        obs_form.addWidget(self.api_url_edit, 4, 1, 1, 2)

        obs_layout.addLayout(obs_form)
        obs_layout.addStretch()

        obs_save_row = QHBoxLayout()
        obs_save_row.addStretch()
        obs_save_btn = QPushButton("Save Obsidian Settings")
        obs_save_btn.clicked.connect(self._save_obsidian_settings)
        obs_save_row.addWidget(obs_save_btn)
        obs_layout.addLayout(obs_save_row)

        tabs.addTab(obs_tab, "Obsidian")

        # ── Tab 2: Peers ──────────────────────────────
        peers_tab = QWidget()
        peers_layout = QVBoxLayout(peers_tab)

        peers_header = QHBoxLayout()
        peers_title = QLabel("Discovered Peers")
        peers_title.setObjectName("sectionTitle")
        peers_header.addWidget(peers_title)
        peers_header.addStretch()

        scan_btn = QPushButton("Scan Now")
        scan_btn.setToolTip("Force a subnet scan")
        scan_btn.clicked.connect(self._force_scan)
        peers_header.addWidget(scan_btn)

        sync_btn = QPushButton("Sync Now")
        sync_btn.setToolTip("Force an immediate sync with all peers")
        sync_btn.clicked.connect(self._force_sync)
        peers_header.addWidget(sync_btn)

        peers_layout.addLayout(peers_header)

        self.peer_table = QTableWidget()
        self.peer_table.setColumnCount(4)
        self.peer_table.setHorizontalHeaderLabels(["IP Address", "Hostname", "Status", "Failures"])
        self.peer_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.peer_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.peer_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        peers_layout.addWidget(self.peer_table)

        # Manual peer add
        add_row = QHBoxLayout()
        add_row.addWidget(QLabel("Add peer:"))
        self.manual_ip_edit = QLineEdit()
        self.manual_ip_edit.setPlaceholderText("e.g. 192.168.0.28")
        self.manual_ip_edit.setMaximumWidth(200)
        self.manual_ip_edit.returnPressed.connect(self._add_manual_peer)
        add_row.addWidget(self.manual_ip_edit)

        add_btn = QPushButton("Add")
        add_btn.setObjectName("secondary")
        add_btn.clicked.connect(self._add_manual_peer)
        add_row.addWidget(add_btn)

        ping_btn = QPushButton("Ping")
        ping_btn.setObjectName("secondary")
        ping_btn.clicked.connect(self._ping_selected)
        add_row.addWidget(ping_btn)

        add_row.addStretch()
        peers_layout.addLayout(add_row)

        tabs.addTab(peers_tab, "Peers")

        # ── Tab 3: Log ────────────────────────────────
        log_tab = QWidget()
        log_layout = QVBoxLayout(log_tab)

        log_header = QHBoxLayout()
        log_title = QLabel("Sync Log")
        log_title.setObjectName("sectionTitle")
        log_header.addWidget(log_title)
        log_header.addStretch()
        clear_btn = QPushButton("Clear")
        clear_btn.setObjectName("secondary")
        clear_btn.clicked.connect(lambda: self.log_view.clear())
        log_header.addWidget(clear_btn)
        log_layout.addLayout(log_header)

        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setStyleSheet("font-family: monospace; font-size: 12px;")
        log_layout.addWidget(self.log_view)

        tabs.addTab(log_tab, "Log")

        layout.addWidget(tabs)

    def _load_values(self):
        self.sync_enabled_check.setChecked(self.cfg.get("sync_enabled", True))
        self.subnet_edit.setText(self.cfg.get("subnet", "192.168.0"))
        self.port_spin.setValue(self.cfg.get("sync_port", 42069))
        self.interval_spin.setValue(self.cfg.get("sync_interval_seconds", 300))
        self.timeout_spin.setValue(self.cfg.get("scan_timeout_ms", 150))

    def _save_settings(self):
        self.cfg["sync_enabled"] = self.sync_enabled_check.isChecked()
        self.cfg["subnet"] = self.subnet_edit.text().strip()
        self.cfg["sync_port"] = self.port_spin.value()
        self.cfg["sync_interval_seconds"] = self.interval_spin.value()
        self.cfg["scan_timeout_ms"] = self.timeout_spin.value()
        save_config(self.cfg)
        if self.sync_engine:
            self.sync_engine.reload_config()
        QMessageBox.information(self, "Saved", "Network settings saved.")

    def _refresh_peers(self):
        if self.sync_engine:
            peers = self.sync_engine.get_peer_list()
            self._update_peer_table(peers)

    def _update_peer_table(self, peers: list):
        self.peer_table.setRowCount(len(peers))
        for row, p in enumerate(peers):
            self.peer_table.setItem(row, 0, QTableWidgetItem(p["ip"]))
            self.peer_table.setItem(row, 1, QTableWidgetItem(p.get("hostname", "")))
            status = p.get("status", "unknown")
            status_item = QTableWidgetItem(status)
            if status == "online":
                status_item.setForeground(Qt.GlobalColor.green)
            elif status == "stale":
                status_item.setForeground(Qt.GlobalColor.darkYellow)
            else:
                status_item.setForeground(Qt.GlobalColor.red)
            self.peer_table.setItem(row, 2, status_item)
            self.peer_table.setItem(row, 3, QTableWidgetItem(str(p.get("fail_count", 0))))

    def _add_manual_peer(self):
        ip = self.manual_ip_edit.text().strip()
        if ip and self.sync_engine:
            self.sync_engine.add_manual_peer(ip)
            # Also save to known_peers
            known = self.cfg.get("known_peers", [])
            if ip not in known:
                known.append(ip)
                self.cfg["known_peers"] = known
                save_config(self.cfg)
            self.manual_ip_edit.clear()
            self._refresh_peers()

    def _ping_selected(self):
        rows = self.peer_table.selectionModel().selectedRows()
        if rows and self.sync_engine:
            ip_item = self.peer_table.item(rows[0].row(), 0)
            if ip_item:
                ip = ip_item.text()
                self._append_log(f"Pinging {ip}...")

                def do_ping():
                    ok, info = self.sync_engine.ping_peer(ip)
                    if ok:
                        self._append_log(f"Ping {ip}: OK ({info})")
                    else:
                        self._append_log(f"Ping {ip}: FAILED ({info})")

                threading.Thread(target=do_ping, daemon=True).start()
        elif not rows:
            # Ping the manual IP field
            ip = self.manual_ip_edit.text().strip()
            if ip and self.sync_engine:
                self._append_log(f"Pinging {ip}...")

                def do_ping():
                    ok, info = self.sync_engine.ping_peer(ip)
                    if ok:
                        self._append_log(f"Ping {ip}: OK ({info})")
                    else:
                        self._append_log(f"Ping {ip}: FAILED ({info})")

                threading.Thread(target=do_ping, daemon=True).start()

    def _force_scan(self):
        if self.sync_engine:
            self._append_log("Forcing subnet scan...")
            self.sync_engine.force_sync()

    def _force_sync(self):
        if self.sync_engine:
            self._append_log("Forcing immediate sync...")
            self.sync_engine.force_sync()

    def _browse_vault(self):
        from PyQt6.QtWidgets import QFileDialog
        path = QFileDialog.getExistingDirectory(
            self, "Select Obsidian Vault",
            self.vault_path_edit.text(),
        )
        if path:
            self.vault_path_edit.setText(path)

    def _save_obsidian_settings(self):
        self.cfg["obsidian_vault_path"] = self.vault_path_edit.text().strip()
        self.cfg["obsidian_sync_enabled"] = self.vault_sync_check.isChecked()
        self.cfg["obsidian_api_key"] = self.api_key_edit.text().strip()
        self.cfg["obsidian_api_url"] = self.api_url_edit.text().strip() or "http://127.0.0.1:27123"
        save_config(self.cfg)
        QMessageBox.information(self, "Saved", "Obsidian settings saved.\nRestart the app for vault changes to take effect.")

    def _append_log(self, msg: str):
        self.log_view.append(msg)
        scrollbar = self.log_view.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    @staticmethod
    def _get_local_ip() -> str:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("192.168.0.1", 1))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "unknown"

```

### `src\utils\__init__.py`

```python
"""Shared utilities."""

from src.utils.timestamps import now_utc, parse_ts
from src.utils.paths import normalize_path, ensure_parent

__all__ = ["now_utc", "parse_ts", "normalize_path", "ensure_parent"]

```

### `src\utils\paths.py`

```python
"""Cross-platform path utilities."""

from pathlib import Path, PurePosixPath


def normalize_path(path: str | Path) -> str:
    """Convert a path to forward-slash form for consistent storage."""
    return PurePosixPath(Path(path)).as_posix()


def ensure_parent(path: Path):
    """Create parent directories if they don't exist."""
    path.parent.mkdir(parents=True, exist_ok=True)

```

### `src\utils\timestamps.py`

```python
"""Timestamp utilities for sync and data."""

from datetime import datetime, timezone


def now_utc() -> str:
    """ISO-8601 UTC timestamp string."""
    return datetime.now(timezone.utc).isoformat()


def parse_ts(ts: str) -> datetime:
    """Parse an ISO-8601 timestamp string."""
    return datetime.fromisoformat(ts)

```

### `tests\__init__.py`

```python
"""Tests for LocalSync."""

```
