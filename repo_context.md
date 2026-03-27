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
- Total lines of code: **9761**

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
- datetime

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
- __future__
- collections
- datetime
- pathlib
- PyQt6.QtCore
- PyQt6.QtGui
- PyQt6.QtWidgets
- src.config
- src.data.activity_store

### src\ui\modules\calendar_panel.py
- __future__
- calendar
- datetime
- PyQt6.QtCore
- PyQt6.QtGui
- PyQt6.QtWidgets
- src.data.calendar_store
- src.data.holidays_jp

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
- threading
- urllib.request
- urllib.error
- json
- datetime
- PyQt6.QtCore
- PyQt6.QtGui
- PyQt6.QtWidgets
- src.config
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
- `JobPreset`: (No docstring)
- `FinanceStore`: (No docstring)

**Functions:**
- `add_transaction`: (No docstring)
- `update_transaction`: (No docstring)
- `delete_transaction`: (No docstring)
- `get_transactions`: (No docstring)
- `get_summary`: Return earnings/expense totals and by-category breakdown.

All USD amounts; caller must convert JPY transactions using the
current exchange rate before passing in, or use get_summary_usd()
which accepts a rate parameter.
- `get_goal_income`: Return total additional income (non-job-pay) in USD for the period.

JPY transactions are converted to USD using usd_jpy_rate.
Only income transactions with is_job_pay=0 are counted.
- `get_all_time_earned`: Total income across all time (raw stored amounts, no currency conversion).
- `get_all_time_earned_usd`: Total income across all time, normalised to USD.
- `_upsert`: (No docstring)
- `_row_to_txn`: (No docstring)
- `get_presets`: (No docstring)
- `add_preset`: (No docstring)
- `update_preset`: (No docstring)
- `delete_preset`: (No docstring)
- `log_preset`: Log `count` completions of a preset job. Returns created transactions.
- `_upsert_preset`: (No docstring)
- `_row_to_preset`: (No docstring)

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
Activity Tracker panel — weekly 24-hour time-block view with efficiency totals.

Layout:
  Left (scrollable):  7-column × 24-hour painted block grid
  Right (fixed 310px): Efficiency panel + compact log form

Features:
  • Stacked colored blocks showing activities proportionally across 24 h
  • Cross-midnight activities drawn across the day boundary
  • "Now" horizontal line on today's column
  • Click a block to select / edit it in the log form
  • Double-click empty space to open add form for that day+time
  • Compact multi-row log form (activity, date, start, end, timer, add)
  • Notes are a pop-out dialog — not shown by default
  • Efficiency panel: weekly totals by activity category + per-day bar chart

**Classes:**
- `ActivityBlock`: Represents one painted rectangle on the weekly grid.
- `WeekBlockWidget`: Custom-painted weekly time-block grid.
- `NotesDialog`: (No docstring)
- `FillBar`: A horizontal bar that fills to a percentage of its parent width.
- `EfficiencyPanel`: Shows weekly activity totals and a per-day summary.
- `LogForm`: Compact activity log form docked at the bottom of the right panel.
- `ActivityPanel`: (No docstring)

**Functions:**
- `_parse_hhmm`: Convert 'HH:MM' to float hours (e.g. '09:30' → 9.5).
- `_hours_to_px`: (No docstring)
- `_px_to_hours`: (No docstring)
- `_fmt_hm`: (No docstring)
- `__init__`: (No docstring)
- `__init__`: (No docstring)
- `set_palette`: (No docstring)
- `load_week`: (No docstring)
- `select_activity`: (No docstring)
- `_col_x`: (No docstring)
- `_col_width`: (No docstring)
- `_block_at`: (No docstring)
- `_pos_to_col_hour`: (No docstring)
- `mousePressEvent`: (No docstring)
- `mouseDoubleClickEvent`: (No docstring)
- `mouseMoveEvent`: (No docstring)
- `paintEvent`: (No docstring)
- `__init__`: (No docstring)
- `get_notes`: (No docstring)
- `__init__`: (No docstring)
- `paintEvent`: (No docstring)
- `__init__`: (No docstring)
- `set_palette`: (No docstring)
- `_build_ui`: (No docstring)
- `update_data`: (No docstring)
- `_make_bar_row`: (No docstring)
- `_make_day_row`: (No docstring)
- `__init__`: (No docstring)
- `_build_ui`: (No docstring)
- `set_week_start`: (No docstring)
- `prefill`: Called when user double-clicks empty space on the grid.
- `load_for_edit`: Populate form fields with an existing activity for editing.
- `_rebuild_day_combo`: (No docstring)
- `_selected_date`: (No docstring)
- `_submit`: (No docstring)
- `_delete`: (No docstring)
- `_cancel_edit`: (No docstring)
- `_open_notes`: (No docstring)
- `_start_timer`: (No docstring)
- `_stop_timer`: (No docstring)
- `_tick`: (No docstring)
- `__init__`: (No docstring)
- `set_palette`: (No docstring)
- `_build_ui`: (No docstring)
- `_prev_week`: (No docstring)
- `_next_week`: (No docstring)
- `_go_today`: (No docstring)
- `_refresh`: (No docstring)
- `_on_block_clicked`: (No docstring)
- `_on_empty_clicked`: (No docstring)
- `_on_activity_added`: (No docstring)
- `_on_activity_updated`: (No docstring)
- `_on_activity_deleted`: (No docstring)
- `_export`: (No docstring)

### src\ui\modules\calendar_panel.py
**Module docstring:**
Calendar module UI — weekly view + mini-month navigator + major events.

All colors read from the active theme palette so the panel adapts when the
user switches themes.  No hardcoded hex values remain in inline stylesheets
or paintEvent code.

Layout (positions unchanged):
  Upper-left  → Weekly overview grid (7 day columns)
  Lower-left  → Selected-day detail list
  Upper-right → Mini month navigator (interactive dot indicators)
  Lower-right → Next major events panel

**Classes:**
- `ColorButton`: (No docstring)
- `EventDialog`: (No docstring)
- `BirthdayDialog`: (No docstring)
- `MiniMonthCell`: (No docstring)
- `MiniMonth`: (No docstring)
- `EventChip`: (No docstring)
- `DayColumn`: (No docstring)
- `MajorEventCard`: (No docstring)
- `DayEventRow`: (No docstring)
- `CalendarPanel`: (No docstring)
- `BirthdayManagerDialog`: (No docstring)

**Functions:**
- `_p`: Return current palette value for *key*.
- `_cat_emoji`: (No docstring)
- `_cat_color`: (No docstring)
- `_clear_layout`: (No docstring)
- `__init__`: (No docstring)
- `setChecked`: (No docstring)
- `_update_style`: (No docstring)
- `__init__`: (No docstring)
- `_build_ui`: (No docstring)
- `_on_color_picked`: (No docstring)
- `_on_category_changed`: (No docstring)
- `_toggle_time`: (No docstring)
- `_on_delete`: (No docstring)
- `_on_save`: (No docstring)
- `_selected_color`: (No docstring)
- `_selected_recurrence`: (No docstring)
- `get_data`: (No docstring)
- `__init__`: (No docstring)
- `_build_ui`: (No docstring)
- `_on_delete`: (No docstring)
- `_on_save`: (No docstring)
- `get_data`: (No docstring)
- `__init__`: (No docstring)
- `enterEvent`: (No docstring)
- `leaveEvent`: (No docstring)
- `mousePressEvent`: (No docstring)
- `paintEvent`: (No docstring)
- `__init__`: (No docstring)
- `set_events`: (No docstring)
- `set_holidays`: (No docstring)
- `set_selected`: (No docstring)
- `refresh_styles`: Re-apply palette colors to navigation buttons/labels.
- `_nav_style`: (No docstring)
- `_build`: (No docstring)
- `_render`: (No docstring)
- `_on_cell_click`: (No docstring)
- `_prev_month`: (No docstring)
- `_next_month`: (No docstring)
- `_prev_year`: (No docstring)
- `_next_year`: (No docstring)
- `_go_today_month`: (No docstring)
- `__init__`: (No docstring)
- `enterEvent`: (No docstring)
- `leaveEvent`: (No docstring)
- `mouseDoubleClickEvent`: (No docstring)
- `paintEvent`: (No docstring)
- `__init__`: (No docstring)
- `_build`: (No docstring)
- `enterEvent`: (No docstring)
- `leaveEvent`: (No docstring)
- `mouseDoubleClickEvent`: (No docstring)
- `paintEvent`: (No docstring)
- `__init__`: (No docstring)
- `mousePressEvent`: (No docstring)
- `__init__`: (No docstring)
- `mousePressEvent`: (No docstring)
- `mouseDoubleClickEvent`: (No docstring)
- `__init__`: (No docstring)
- `set_palette`: (No docstring)
- `_build_ui`: (No docstring)
- `_today_btn`: (No docstring)
- `_refresh`: (No docstring)
- `_get_week_start`: (No docstring)
- `_render_week`: (No docstring)
- `_render_day_detail`: (No docstring)
- `_render_major_events`: (No docstring)
- `_update_mini_month_events`: (No docstring)
- `_prev_week`: (No docstring)
- `_next_week`: (No docstring)
- `_go_today`: (No docstring)
- `_on_mini_date_selected`: (No docstring)
- `_jump_to_date`: (No docstring)
- `_add_event`: (No docstring)
- `_add_event_on_date`: (No docstring)
- `_edit_event`: (No docstring)
- `_open_major_event`: Dispatcher: open the editor for a MajorEventCard or birthday DayEventRow.
- `_manage_birthdays`: (No docstring)
- `__init__`: (No docstring)
- `_build_ui`: (No docstring)
- `_load`: (No docstring)
- `_filter`: (No docstring)
- `_make_row`: (No docstring)
- `_add_birthday`: (No docstring)
- `_edit_birthday`: (No docstring)
- `sk`: (No docstring)

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

Features:
- Quick-log preset jobs with one click (job pay, does not count toward goals)
- Manual earning / expense entry with USD or JPY currency selection
- Live USD→JPY exchange rate via open.er-api.com with offline fallback
- Dual-currency display throughout (USD + ¥JPY)
- Month's Goal section: Base Goal + Extra Goal progress bars
  (only additional income, not job pay, counts toward goals)
- Quick date-range buttons (This Month / Last Month / This Year / All Time)
- Period summary panel with category bars

**Classes:**
- `RateSignals`: (No docstring)
- `ExchangeRateManager`: Fetches USD→JPY rate in a background thread. Thread-safe.
- `GoalProgressBar`: Paints a two-tier progress bar: base goal and extra goal.
- `CategoryBar`: (No docstring)
- `PresetManagerDialog`: Add / edit / delete job presets.
- `GoalSettingsDialog`: Set base and extra monthly income goals (USD).
- `TransactionDialog`: Dialog to add/edit a transaction (earning or expense).
- `PresetButton`: A card-style button for one-click job logging.
- `FinancePanel`: (No docstring)

**Functions:**
- `__init__`: (No docstring)
- `rate`: (No docstring)
- `set_fallback`: (No docstring)
- `refresh`: (No docstring)
- `__init__`: (No docstring)
- `set_values`: (No docstring)
- `paintEvent`: (No docstring)
- `__init__`: (No docstring)
- `__init__`: (No docstring)
- `_build_ui`: (No docstring)
- `_refresh`: (No docstring)
- `_add_preset`: (No docstring)
- `_edit_selected`: (No docstring)
- `_delete_selected`: (No docstring)
- `__init__`: (No docstring)
- `_build_ui`: (No docstring)
- `_validate_and_accept`: (No docstring)
- `get_goals`: (No docstring)
- `__init__`: (No docstring)
- `_build_ui`: (No docstring)
- `_on_type_changed`: (No docstring)
- `_on_currency_changed`: (No docstring)
- `get_data`: (No docstring)
- `__init__`: (No docstring)
- `__init__`: (No docstring)
- `set_palette`: (No docstring)
- `_build_ui`: (No docstring)
- `_build_header`: (No docstring)
- `_build_quick_log_bar`: (No docstring)
- `_build_filter_row`: (No docstring)
- `_build_goal_section`: (No docstring)
- `_build_table`: (No docstring)
- `_build_summary_panel`: (No docstring)
- `_build_rate_bar`: (No docstring)
- `_set_date_range`: (No docstring)
- `_filter_this_month`: (No docstring)
- `_filter_last_month`: (No docstring)
- `_filter_this_year`: (No docstring)
- `_filter_all_time`: (No docstring)
- `_refresh_rate`: (No docstring)
- `_on_rate_updated`: (No docstring)
- `_on_rate_error`: (No docstring)
- `_rebuild_preset_buttons`: Clear and repopulate the Quick Log button row.
- `_log_preset`: (No docstring)
- `_open_preset_manager`: (No docstring)
- `_open_goal_settings`: (No docstring)
- `_update_goal_section`: (No docstring)
- `_get_filters`: (No docstring)
- `_refresh`: (No docstring)
- `_add_earning`: (No docstring)
- `_add_expense`: (No docstring)
- `_edit_transaction`: (No docstring)
- `_delete_transaction`: (No docstring)
- `_fetch`: (No docstring)

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
Theme stylesheets for PyQt6.

Themes included:
  Dark   — Catppuccin Mocha, Tokyo Night, Dracula, Monokai Pro, One Dark Pro, Rosé Pine
  Medium — Nord, Gruvbox Dark
  Light  — Catppuccin Latte, Solarized Light

Fixes over previous version:
  - Full QTabBar / QTabWidget styling (dialogs now have proper tabs)
  - QMenuBar / QMenu styling (menu bar no longer inherits OS chrome)
  - QToolButton styling (color swatches, weekday pickers, etc.)
  - QComboBox, QDateEdit, QTimeEdit, QSpinBox arrow-button subcontrols
    styled with visible backgrounds so arrows are legible on all themes
  - Secondary button contrast improved (explicit text color + stronger border)
  - QProgressBar added (used in dashboard)
  - QScrollArea viewport now transparent (no mismatched bg panels)
  - Solarized Light replaces Solarized Dark (fg was too muted for readability)

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
    note: str = ""
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
                     year: int | None = None, note: str = "") -> Birthday:
        b = Birthday(
            id=str(uuid.uuid4()),
            name=name, month=month, day=day, year=year,
            note=note, updated_at=now_utc(),
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
                """INSERT INTO birthdays (id, name, month, day, year, note, updated_at, deleted)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(id) DO UPDATE SET
                   name=excluded.name, month=excluded.month, day=excluded.day,
                   year=excluded.year, note=excluded.note,
                   updated_at=excluded.updated_at, deleted=excluded.deleted""",
                (b.id, b.name, b.month, b.day, b.year, b.note, b.updated_at, int(b.deleted)),
            )
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def _row_to_birthday(row) -> Birthday:
        return Birthday(
            id=row["id"], name=row["name"], month=row["month"],
            day=row["day"], year=row["year"],
            note=row["note"] if row["note"] else "",
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
            results.append((ev_date, ev.title, ev.category, ev.color, ev.id, False))

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
            results.append((candidate, b.name, "birthday", "#f38ba8", b.id, True))

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
    # --- events table ---
    cols = {r["name"] for r in conn.execute("PRAGMA table_info(events)").fetchall()}
    if "recurrence" not in cols:
        conn.execute("ALTER TABLE events ADD COLUMN recurrence TEXT DEFAULT ''")
    if "category" not in cols:
        conn.execute("ALTER TABLE events ADD COLUMN category TEXT DEFAULT ''")

    bcols = {r["name"] for r in conn.execute("PRAGMA table_info(birthdays)").fetchall()}
    if "note" not in bcols:
        conn.execute("ALTER TABLE birthdays ADD COLUMN note TEXT DEFAULT ''")
        
    # --- transactions table ---
    txn_cols = {r["name"] for r in conn.execute("PRAGMA table_info(transactions)").fetchall()}
    if "currency" not in txn_cols:
        conn.execute("ALTER TABLE transactions ADD COLUMN currency TEXT DEFAULT 'USD'")
    if "is_job_pay" not in txn_cols:
        conn.execute("ALTER TABLE transactions ADD COLUMN is_job_pay INTEGER DEFAULT 0")


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
    note        TEXT DEFAULT '',
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
    deleted     INTEGER DEFAULT 0,
    currency    TEXT DEFAULT 'USD',
    is_job_pay  INTEGER DEFAULT 0
);

 
CREATE TABLE IF NOT EXISTS job_presets (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    amount_usd  REAL NOT NULL,
    category    TEXT DEFAULT 'Contract',
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
from dataclasses import dataclass, field

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
    date: str           # YYYY-MM-DD
    amount: float       # Always stored in original currency
    type: str           # 'income' or 'expense'
    category: str = "Freelance"
    description: str = ""
    updated_at: str = ""
    deleted: bool = False
    currency: str = "USD"   # 'USD' or 'JPY'
    is_job_pay: bool = False


@dataclass
class JobPreset:
    id: str
    name: str
    amount_usd: float
    category: str = "Contract"
    updated_at: str = ""
    deleted: bool = False


class FinanceStore:

    # ── Transactions ──────────────────────────────────────────────────────────

    def add_transaction(self, date: str, amount: float, txn_type: str,
                        category: str = "Freelance", description: str = "",
                        currency: str = "USD", is_job_pay: bool = False) -> Transaction:
        txn = Transaction(
            id=str(uuid.uuid4()),
            date=date,
            amount=amount,
            type=txn_type,
            category=category,
            description=description,
            updated_at=now_utc(),
            currency=currency,
            is_job_pay=is_job_pay,
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
        """Return earnings/expense totals and by-category breakdown.

        All USD amounts; caller must convert JPY transactions using the
        current exchange rate before passing in, or use get_summary_usd()
        which accepts a rate parameter.
        """
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

    def get_goal_income(self, start_date: str, end_date: str,
                        usd_jpy_rate: float = 150.0) -> float:
        """Return total additional income (non-job-pay) in USD for the period.

        JPY transactions are converted to USD using usd_jpy_rate.
        Only income transactions with is_job_pay=0 are counted.
        """
        conn = get_connection()
        try:
            rows = conn.execute(
                "SELECT amount, currency FROM transactions "
                "WHERE deleted=0 AND type='income' AND is_job_pay=0 "
                "AND date >= ? AND date <= ?",
                (start_date, end_date),
            ).fetchall()
        finally:
            conn.close()

        total_usd = 0.0
        for r in rows:
            if r["currency"] == "JPY":
                total_usd += r["amount"] / usd_jpy_rate
            else:
                total_usd += r["amount"]
        return total_usd

    def get_all_time_earned(self) -> float:
        """Total income across all time (raw stored amounts, no currency conversion)."""
        conn = get_connection()
        try:
            row = conn.execute(
                "SELECT COALESCE(SUM(amount), 0) as total FROM transactions "
                "WHERE deleted=0 AND type='income'"
            ).fetchone()
            return row["total"]
        finally:
            conn.close()

    def get_all_time_earned_usd(self, usd_jpy_rate: float = 150.0) -> float:
        """Total income across all time, normalised to USD."""
        conn = get_connection()
        try:
            rows = conn.execute(
                "SELECT amount, currency FROM transactions "
                "WHERE deleted=0 AND type='income'"
            ).fetchall()
        finally:
            conn.close()

        total = 0.0
        for r in rows:
            if r["currency"] == "JPY":
                total += r["amount"] / usd_jpy_rate
            else:
                total += r["amount"]
        return total

    def _upsert(self, txn: Transaction):
        conn = get_connection()
        try:
            conn.execute(
                """INSERT INTO transactions
                   (id, date, amount, type, category, description,
                    updated_at, deleted, currency, is_job_pay)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(id) DO UPDATE SET
                   date=excluded.date, amount=excluded.amount, type=excluded.type,
                   category=excluded.category, description=excluded.description,
                   updated_at=excluded.updated_at, deleted=excluded.deleted,
                   currency=excluded.currency, is_job_pay=excluded.is_job_pay""",
                (txn.id, txn.date, txn.amount, txn.type, txn.category,
                 txn.description, txn.updated_at, int(txn.deleted),
                 txn.currency, int(txn.is_job_pay)),
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
            currency=row["currency"] if row["currency"] else "USD",
            is_job_pay=bool(row["is_job_pay"]),
        )

    # ── Job Presets ───────────────────────────────────────────────────────────

    def get_presets(self) -> list[JobPreset]:
        conn = get_connection()
        try:
            rows = conn.execute(
                "SELECT * FROM job_presets WHERE deleted=0 ORDER BY name"
            ).fetchall()
            return [self._row_to_preset(r) for r in rows]
        finally:
            conn.close()

    def add_preset(self, name: str, amount_usd: float,
                   category: str = "Contract") -> JobPreset:
        preset = JobPreset(
            id=str(uuid.uuid4()),
            name=name,
            amount_usd=amount_usd,
            category=category,
            updated_at=now_utc(),
        )
        self._upsert_preset(preset)
        return preset

    def update_preset(self, preset: JobPreset) -> JobPreset:
        preset.updated_at = now_utc()
        self._upsert_preset(preset)
        return preset

    def delete_preset(self, preset_id: str):
        conn = get_connection()
        try:
            conn.execute(
                "UPDATE job_presets SET deleted=1, updated_at=? WHERE id=?",
                (now_utc(), preset_id),
            )
            conn.commit()
        finally:
            conn.close()

    def log_preset(self, preset: JobPreset, count: int = 1,
                   on_date: str | None = None) -> list[Transaction]:
        """Log `count` completions of a preset job. Returns created transactions."""
        from datetime import date as _date
        day = on_date or _date.today().isoformat()
        txns = []
        for _ in range(count):
            txn = self.add_transaction(
                date=day,
                amount=preset.amount_usd,
                txn_type="income",
                category=preset.category,
                description=f"[Job] {preset.name}",
                currency="USD",
                is_job_pay=True,
            )
            txns.append(txn)
        return txns

    def _upsert_preset(self, preset: JobPreset):
        conn = get_connection()
        try:
            conn.execute(
                """INSERT INTO job_presets
                   (id, name, amount_usd, category, updated_at, deleted)
                   VALUES (?, ?, ?, ?, ?, ?)
                   ON CONFLICT(id) DO UPDATE SET
                   name=excluded.name, amount_usd=excluded.amount_usd,
                   category=excluded.category, updated_at=excluded.updated_at,
                   deleted=excluded.deleted""",
                (preset.id, preset.name, preset.amount_usd,
                 preset.category, preset.updated_at, int(preset.deleted)),
            )
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def _row_to_preset(row) -> JobPreset:
        return JobPreset(
            id=row["id"], name=row["name"], amount_usd=row["amount_usd"],
            category=row["category"], updated_at=row["updated_at"],
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
"""Activity Tracker panel — weekly 24-hour time-block view with efficiency totals.

Layout:
  Left (scrollable):  7-column × 24-hour painted block grid
  Right (fixed 310px): Efficiency panel + compact log form

Features:
  • Stacked colored blocks showing activities proportionally across 24 h
  • Cross-midnight activities drawn across the day boundary
  • "Now" horizontal line on today's column
  • Click a block to select / edit it in the log form
  • Double-click empty space to open add form for that day+time
  • Compact multi-row log form (activity, date, start, end, timer, add)
  • Notes are a pop-out dialog — not shown by default
  • Efficiency panel: weekly totals by activity category + per-day bar chart
"""

from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

from PyQt6.QtCore import Qt, QRectF, QPointF, QTimer, QTime, pyqtSignal
from PyQt6.QtGui import (
    QPainter, QColor, QFont, QFontMetrics, QPen, QBrush,
    QLinearGradient, QMouseEvent,
)
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QComboBox, QTimeEdit, QPlainTextEdit,
    QFrame, QScrollArea, QMessageBox, QSizePolicy,
    QDialog, QGridLayout,
)

from src.config import load_config
from src.data.activity_store import (
    ActivityStore, Activity,
    DEFAULT_ACTIVITIES, ACTIVITY_COLORS, DEFAULT_COLOR,
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Layout constants
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HOUR_H    = 52      # px per hour → 52 × 24 = 1248 px total height
HEADER_H  = 44      # day-name row height
TIME_W    = 52      # left column for hour labels
DAY_COUNT = 7       # Mon–Sun
TOTAL_H   = HEADER_H + 24 * HOUR_H   # 1292


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Helpers
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _parse_hhmm(s: str) -> float:
    """Convert 'HH:MM' to float hours (e.g. '09:30' → 9.5)."""
    try:
        h, m = map(int, s.split(":"))
        return h + m / 60.0
    except Exception:
        return 0.0

def _hours_to_px(hours: float) -> float:
    return HEADER_H + hours * HOUR_H

def _px_to_hours(py: float) -> float:
    return max(0.0, min(24.0, (py - HEADER_H) / HOUR_H))

def _fmt_hm(total_minutes: int) -> str:
    h, m = divmod(abs(total_minutes), 60)
    return f"{h}h {m}m" if m else f"{h}h"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ActivityBlock  — one drawn block on the grid
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ActivityBlock:
    """Represents one painted rectangle on the weekly grid."""
    def __init__(self, activity: Activity, col: int,
                 y_start: float, y_end: float, overflow: bool = False):
        self.activity  = activity
        self.col       = col
        self.y_start   = y_start   # pixel y of top
        self.y_end     = y_end     # pixel y of bottom
        self.overflow  = overflow  # True = this is the continuation from prev day
        self.rect      = QRectF()  # set during paint (includes column x offset)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  WeekBlockWidget  — fully-painted main calendar body
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class WeekBlockWidget(QWidget):
    """Custom-painted weekly time-block grid."""

    block_clicked  = pyqtSignal(object)    # Activity
    empty_clicked  = pyqtSignal(object, float)  # date, hour_float

    def __init__(self, parent=None):
        super().__init__(parent)
        self._palette: dict = {}
        self._blocks:  list[ActivityBlock] = []
        self._week_start: date = date.today() - timedelta(days=date.today().weekday())
        self._selected: ActivityBlock | None = None
        self._hovered:  ActivityBlock | None = None
        self.setFixedHeight(TOTAL_H)
        self.setMinimumWidth(400)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMouseTracking(True)

    # ── Public API ───────────────────────────────────

    def set_palette(self, palette: dict):
        self._palette = palette; self.update()

    def load_week(self, week_start: date, activities_by_date: dict[date, list[Activity]]):
        self._week_start = week_start
        self._blocks = []
        self._selected = None

        for col in range(DAY_COUNT):
            day = week_start + timedelta(days=col)
            acts = activities_by_date.get(day, [])

            # Also check previous day for any cross-midnight overflows
            prev_day = day - timedelta(days=1)
            for prev_act in activities_by_date.get(prev_day, []):
                sh = _parse_hhmm(prev_act.start_time)
                eh = _parse_hhmm(prev_act.end_time)
                if eh < sh:   # crosses midnight
                    y0 = _hours_to_px(0.0)
                    y1 = _hours_to_px(eh)
                    if y1 > y0:
                        self._blocks.append(ActivityBlock(
                            prev_act, col, y0, y1, overflow=True))

            for act in acts:
                sh = _parse_hhmm(act.start_time)
                eh = _parse_hhmm(act.end_time)
                if eh < sh:
                    # Crosses midnight: draw to bottom of this column
                    self._blocks.append(ActivityBlock(
                        act, col, _hours_to_px(sh), _hours_to_px(24.0)))
                else:
                    self._blocks.append(ActivityBlock(
                        act, col, _hours_to_px(sh), _hours_to_px(eh)))

        self.update()

    def select_activity(self, activity: Activity | None):
        if activity is None:
            self._selected = None
        else:
            for b in self._blocks:
                if b.activity.id == activity.id:
                    self._selected = b; break
        self.update()

    # ── Mouse ────────────────────────────────────────

    def _col_x(self, col: int) -> float:
        col_w = (self.width() - TIME_W) / DAY_COUNT
        return TIME_W + col * col_w

    def _col_width(self) -> float:
        return (self.width() - TIME_W) / DAY_COUNT

    def _block_at(self, pos: QPointF) -> ActivityBlock | None:
        for b in reversed(self._blocks):   # top = last drawn = front
            if b.rect.contains(pos):
                return b
        return None

    def _pos_to_col_hour(self, pos: QPointF):
        cw = self._col_width()
        col = int((pos.x() - TIME_W) / cw)
        col = max(0, min(DAY_COUNT - 1, col))
        hour = _px_to_hours(pos.y())
        return col, hour

    def mousePressEvent(self, ev: QMouseEvent):
        b = self._block_at(ev.position())
        if b:
            self._selected = b; self.update()
            self.block_clicked.emit(b.activity)
        else:
            self._selected = None; self.update()

    def mouseDoubleClickEvent(self, ev: QMouseEvent):
        b = self._block_at(ev.position())
        if not b:
            col, hour = self._pos_to_col_hour(ev.position())
            d = self._week_start + timedelta(days=col)
            self.empty_clicked.emit(d, hour)

    def mouseMoveEvent(self, ev: QMouseEvent):
        b = self._block_at(ev.position())
        if b != self._hovered:
            self._hovered = b
            if b:
                a = b.activity
                tip = f"{a.activity}\n{a.start_time} – {a.end_time}  ({a.duration_minutes}m)"
                if a.notes: tip += f"\n{a.notes}"
                self.setToolTip(tip)
            else:
                self.setToolTip("")
            self.update()

    # ── Paint ────────────────────────────────────────

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w = self.width()

        bg     = QColor(self._palette.get("bg",        "#1e1e2e"))
        surf   = QColor(self._palette.get("surface",   "#313244"))
        border = QColor(self._palette.get("border",    "#45475a"))
        fg     = QColor(self._palette.get("fg",        "#cdd6f4"))
        muted  = QColor(self._palette.get("muted",     "#7f849c"))
        accent = QColor(self._palette.get("accent",    "#89b4fa"))
        hdr_bg = QColor(self._palette.get("header_bg", "#181825"))

        col_w  = self._col_width()

        # ── Background ───────────────────────────────
        p.fillRect(0, 0, w, TOTAL_H, bg)
        p.fillRect(0, 0, w, HEADER_H, hdr_bg)

        # ── Hour grid lines ──────────────────────────
        hour_font = QFont(); hour_font.setPixelSize(9)
        p.setFont(hour_font)
        for h in range(25):
            y = _hours_to_px(h)
            is_major = (h % 6 == 0)
            c = QColor(border)
            if is_major: c.setAlpha(200)
            else:        c.setAlpha(80)
            p.setPen(QPen(c, 1 if is_major else 0.5))
            p.drawLine(QPointF(TIME_W, y), QPointF(w, y))

            if h < 24:
                lbl = f"{h:02d}:00"
                p.setPen(muted if h % 6 else fg)
                p.drawText(QRectF(0, y + 1, TIME_W - 4, HOUR_H - 2),
                           Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop, lbl)

        # ── Column dividers + day headers ─────────────
        today = date.today()
        day_font = QFont(); day_font.setPixelSize(11); day_font.setBold(True)
        num_font  = QFont(); num_font.setPixelSize(15); num_font.setBold(True)

        for col in range(DAY_COUNT):
            x = TIME_W + col * col_w
            d = self._week_start + timedelta(days=col)
            is_today = (d == today)
            is_weekend = (col >= 5)

            # Column background (weekend slightly tinted)
            if is_weekend:
                tint = QColor(surf)
                tint.setAlpha(30)
                p.fillRect(QRectF(x, HEADER_H, col_w, TOTAL_H - HEADER_H), QBrush(tint))

            # Column divider
            if col > 0:
                p.setPen(QPen(border, 1))
                p.drawLine(QPointF(x, 0), QPointF(x, TOTAL_H))

            # Day header
            if is_today:
                p.fillRect(QRectF(x, 0, col_w, HEADER_H), QBrush(accent))
                text_c = QColor(self._palette.get("accent_fg", "#1e1e2e"))
            else:
                text_c = fg

            p.setPen(text_c)
            p.setFont(day_font)
            p.drawText(QRectF(x, 4, col_w, 18),
                       Qt.AlignmentFlag.AlignCenter, d.strftime("%a").upper())
            p.setFont(num_font)
            p.drawText(QRectF(x, 20, col_w, 22),
                       Qt.AlignmentFlag.AlignCenter, str(d.day))

        # Time-label column border
        p.setPen(QPen(border, 1))
        p.drawLine(QPointF(TIME_W, 0), QPointF(TIME_W, TOTAL_H))

        # ── Activity blocks ──────────────────────────
        for b in self._blocks:
            x    = TIME_W + b.col * col_w
            bx   = x + 2
            bw   = col_w - 4
            by   = b.y_start
            bh   = b.y_end - b.y_start
            if bh < 1: continue
            b.rect = QRectF(bx, by, bw, bh)

            color = QColor(b.activity.color)
            is_sel = (b is self._selected)
            is_hov = (b is self._hovered)

            if b.overflow:
                color.setAlpha(160)
            if is_sel:   color = color.lighter(135)
            elif is_hov: color = color.lighter(115)

            p.setBrush(QBrush(color))
            p.setPen(QPen(color.lighter(160), 1) if is_sel else Qt.PenStyle.NoPen)
            p.drawRoundedRect(b.rect, 3, 3)

            # Label
            if bh >= 18:
                lbl_font = QFont()
                lbl_font.setPixelSize(10 if bh < 32 else 11)
                lbl_font.setBold(True)
                p.setFont(lbl_font)
                # Dark text on light block
                p.setPen(QColor("#11111b") if color.lightness() > 128
                         else QColor("#cdd6f4"))
                fm = QFontMetrics(lbl_font)
                text = b.activity.activity
                if b.overflow: text = "← " + text
                etext = fm.elidedText(text, Qt.TextElideMode.ElideRight, int(bw - 8))
                text_rect = b.rect.adjusted(4, 2, -4, -2)
                if bh >= 32:
                    p.drawText(text_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop, etext)
                    # Time hint on second line
                    lbl_font.setPixelSize(9); lbl_font.setBold(False); p.setFont(lbl_font)
                    time_lbl = f"{b.activity.start_time}–{b.activity.end_time}"
                    time_rect = QRectF(b.rect.x()+4, b.rect.y()+13, bw-8, 12)
                    p.drawText(time_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop, time_lbl)
                else:
                    p.drawText(text_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, etext)

        # ── "Now" indicator ──────────────────────────
        now = datetime.now()
        if self._week_start <= today <= self._week_start + timedelta(days=6):
            now_col = (today - self._week_start).days
            now_y   = _hours_to_px(now.hour + now.minute / 60)
            x0 = TIME_W + now_col * col_w
            x1 = x0 + col_w
            now_color = QColor(self._palette.get("red", "#f38ba8"))
            p.setPen(QPen(now_color, 2))
            p.drawLine(QPointF(x0, now_y), QPointF(x1, now_y))
            # Small circle at left edge
            p.setBrush(QBrush(now_color)); p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(QPointF(x0, now_y), 4, 4)

        p.end()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  NotesDialog
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class NotesDialog(QDialog):
    def __init__(self, parent=None, notes: str = ""):
        super().__init__(parent)
        self.setWindowTitle("Activity Notes")
        self.setMinimumSize(340, 200)
        self.setModal(True)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Notes (optional):"))
        self.edit = QPlainTextEdit()
        self.edit.setPlainText(notes)
        self.edit.setPlaceholderText("Add notes for this activity…")
        layout.addWidget(self.edit)
        btn_row = QHBoxLayout()
        cancel = QPushButton("Cancel"); cancel.setObjectName("secondary")
        cancel.clicked.connect(self.reject)
        ok = QPushButton("OK"); ok.setDefault(True); ok.clicked.connect(self.accept)
        btn_row.addStretch(); btn_row.addWidget(cancel); btn_row.addWidget(ok)
        layout.addLayout(btn_row)

    def get_notes(self) -> str:
        return self.edit.toPlainText().strip()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  FillBar — a proper auto-resizing percentage bar
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class FillBar(QWidget):
    """A horizontal bar that fills to a percentage of its parent width."""

    def __init__(self, ratio: float, fill_color: str, bg_color: str,
                 height: int = 6, parent=None):
        super().__init__(parent)
        self._ratio = max(0.0, min(1.0, ratio))
        self._fill_color = fill_color
        self._bg_color = bg_color
        self.setFixedHeight(height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def paintEvent(self, ev):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        r = h / 2

        # Background track
        p.setBrush(QBrush(QColor(self._bg_color)))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(0, 0, w, h, r, r)

        # Fill
        if self._ratio > 0:
            fill_w = max(h, int(w * self._ratio))  # at least pill-shaped
            p.setBrush(QBrush(QColor(self._fill_color)))
            p.drawRoundedRect(0, 0, fill_w, h, r, r)

        p.end()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  EfficiencyPanel  — right-side totals + mini bar chart
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class EfficiencyPanel(QWidget):
    """Shows weekly activity totals and a per-day summary."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._palette: dict = {}
        self._build_ui()

    def set_palette(self, palette: dict):
        self._palette = palette; self.update()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        hdr = QLabel("Week Efficiency")
        hdr.setStyleSheet("font-size:13px;font-weight:bold;")
        layout.addWidget(hdr)

        self._totals_lbl  = QLabel("—")
        self._totals_lbl.setStyleSheet("font-size:11px;")
        layout.addWidget(self._totals_lbl)

        self._today_lbl = QLabel("")
        self._today_lbl.setStyleSheet("font-size:10px;font-weight:bold;")
        layout.addWidget(self._today_lbl)

        div = QFrame(); div.setFrameShape(QFrame.Shape.HLine)
        div.setObjectName("separator"); layout.addWidget(div)

        self._bar_container = QWidget()
        self._bar_layout    = QVBoxLayout(self._bar_container)
        self._bar_layout.setContentsMargins(0, 0, 0, 0)
        self._bar_layout.setSpacing(4)
        layout.addWidget(self._bar_container)

        div2 = QFrame(); div2.setFrameShape(QFrame.Shape.HLine)
        div2.setObjectName("separator"); layout.addWidget(div2)

        daily_hdr = QLabel("Daily totals")
        daily_hdr.setStyleSheet("font-size:11px;font-weight:bold;")
        layout.addWidget(daily_hdr)

        self._daily_container = QWidget()
        self._daily_layout    = QVBoxLayout(self._daily_container)
        self._daily_layout.setContentsMargins(0, 0, 0, 0)
        self._daily_layout.setSpacing(3)
        layout.addWidget(self._daily_container)
        layout.addStretch()

    def update_data(self, week_start: date, activities_by_date: dict[date, list[Activity]]):
        # ── Category totals ──────────────────────────
        by_name: dict[str, int] = defaultdict(int)
        total_mins = 0
        for acts in activities_by_date.values():
            for a in acts:
                by_name[a.activity] += a.duration_minutes
                total_mins += a.duration_minutes

        # Proper average per day
        avg_mins_per_day = total_mins / 7
        avg_h = int(avg_mins_per_day) // 60
        avg_m = int(avg_mins_per_day) % 60
        avg_str = f"{avg_h}h {avg_m}m" if avg_m else f"{avg_h}h"

        self._totals_lbl.setText(
            f"Tracked: {_fmt_hm(total_mins)}  ·  ~{avg_str}/day"
        )

        # Today's total
        today = date.today()
        today_acts = activities_by_date.get(today, [])
        today_mins = sum(a.duration_minutes for a in today_acts)
        accent = self._palette.get("accent", "#89b4fa")
        green = self._palette.get("green", "#a6e3a1")
        if today_mins > 0:
            self._today_lbl.setText(f"Today: {_fmt_hm(today_mins)}")
            self._today_lbl.setStyleSheet(
                f"font-size:10px;font-weight:bold;color:{green};")
        else:
            self._today_lbl.setText("Today: —")
            self._today_lbl.setStyleSheet(
                f"font-size:10px;font-weight:bold;color:{self._palette.get('muted','#7f849c')};")

        # Clear bar rows
        while self._bar_layout.count():
            child = self._bar_layout.takeAt(0)
            if child.widget(): child.widget().deleteLater()

        max_mins = max(by_name.values(), default=1)
        for name, mins in sorted(by_name.items(), key=lambda x: -x[1])[:10]:
            color = ACTIVITY_COLORS.get(name, DEFAULT_COLOR)
            row = self._make_bar_row(name, mins, max_mins, color)
            self._bar_layout.addWidget(row)

        # ── Daily totals ─────────────────────────────
        while self._daily_layout.count():
            child = self._daily_layout.takeAt(0)
            if child.widget(): child.widget().deleteLater()

        day_labels = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        day_totals = []
        for i in range(7):
            d = week_start + timedelta(days=i)
            acts = activities_by_date.get(d, [])
            day_totals.append(sum(a.duration_minutes for a in acts))

        max_day = max(day_totals, default=1) or 1
        for i, (label, mins) in enumerate(zip(day_labels, day_totals)):
            d = week_start + timedelta(days=i)
            is_today = (d == today)
            row = self._make_day_row(label, mins, max_day, is_today)
            self._daily_layout.addWidget(row)

    def _make_bar_row(self, name: str, mins: int, max_mins: int, color: str) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w); layout.setContentsMargins(0,2,0,0); layout.setSpacing(1)

        top_row = QHBoxLayout(); top_row.setSpacing(4)
        name_lbl = QLabel(name)
        name_lbl.setStyleSheet("font-size:11px;")
        top_row.addWidget(name_lbl, 1)
        mins_lbl = QLabel(_fmt_hm(mins))
        mins_lbl.setStyleSheet("font-size:10px;font-weight:bold;")
        top_row.addWidget(mins_lbl)
        layout.addLayout(top_row)

        ratio = mins / max(max_mins, 1)
        bg_c = self._palette.get('border', '#45475a')
        bar = FillBar(ratio, color, bg_c, height=6)
        layout.addWidget(bar)

        return w

    def _make_day_row(self, label: str, mins: int, max_mins: int,
                      is_today: bool) -> QWidget:
        w = QWidget(); layout = QHBoxLayout(w)
        layout.setContentsMargins(0,1,0,1); layout.setSpacing(6)

        lbl = QLabel(label)
        lbl.setFixedWidth(28)
        lbl.setStyleSheet(
            f"font-size:10px;font-weight:bold;"
            f"color:{self._palette.get('accent','#89b4fa') if is_today else self._palette.get('muted','#7f849c')};")
        layout.addWidget(lbl)

        ratio = mins / max(max_mins, 1)
        accent_c = self._palette.get("accent","#89b4fa") if is_today else \
                   self._palette.get("green","#a6e3a1")
        bg_c = self._palette.get('border', '#45475a')
        bar = FillBar(ratio if mins > 0 else 0, accent_c, bg_c, height=8)
        layout.addWidget(bar, 1)

        time_lbl = QLabel(_fmt_hm(mins) if mins else "—")
        time_lbl.setFixedWidth(40)
        time_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        time_lbl.setStyleSheet("font-size:10px;")
        layout.addWidget(time_lbl)
        return w


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  LogForm  — redesigned multi-row activity entry
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class LogForm(QWidget):
    """Compact activity log form docked at the bottom of the right panel."""

    activity_added   = pyqtSignal(object)   # Activity
    activity_updated = pyqtSignal(object)   # Activity
    activity_deleted = pyqtSignal(str)      # id

    def __init__(self, week_start: date, parent=None):
        super().__init__(parent)
        self._week_start = week_start
        self._editing: Activity | None = None
        self._pending_notes: str = ""
        self._timer: QTimer | None = None
        self._timer_start: datetime | None = None
        self._build_ui()

    # ── Build ────────────────────────────────────────

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(6)

        # ── Header row ──
        hdr = QHBoxLayout()
        self._form_title = QLabel("Log Activity")
        self._form_title.setStyleSheet("font-size:12px;font-weight:bold;")
        hdr.addWidget(self._form_title); hdr.addStretch()

        self._cancel_btn = QPushButton("Cancel")
        self._cancel_btn.setObjectName("secondary")
        self._cancel_btn.setFixedHeight(24)
        self._cancel_btn.clicked.connect(self._cancel_edit)
        self._cancel_btn.setVisible(False)
        hdr.addWidget(self._cancel_btn)
        root.addLayout(hdr)

        # ── Row 1: Activity name (full width) ──
        self.activity_combo = QComboBox()
        self.activity_combo.setEditable(True)
        self.activity_combo.addItems(DEFAULT_ACTIVITIES)
        self.activity_combo.setPlaceholderText("Activity…")
        root.addWidget(self.activity_combo)

        # ── Row 2: Day selector (full width) ──
        self.day_combo = QComboBox()
        self._rebuild_day_combo()
        root.addWidget(self.day_combo)

        # ── Row 3: Start + End times ──
        time_row = QHBoxLayout(); time_row.setSpacing(6)

        start_lbl = QLabel("Start")
        start_lbl.setStyleSheet("font-size:10px;color:palette(mid);")
        start_lbl.setFixedWidth(30)
        time_row.addWidget(start_lbl)
        self.start_edit = QTimeEdit()
        self.start_edit.setDisplayFormat("HH:mm")
        now = datetime.now()
        self.start_edit.setTime(QTime(now.hour, 0))
        time_row.addWidget(self.start_edit, 1)

        time_row.addSpacing(4)

        end_lbl = QLabel("End")
        end_lbl.setStyleSheet("font-size:10px;color:palette(mid);")
        end_lbl.setFixedWidth(24)
        time_row.addWidget(end_lbl)
        self.end_edit = QTimeEdit()
        self.end_edit.setDisplayFormat("HH:mm")
        self.end_edit.setTime(QTime(min(now.hour + 1, 23), 0))
        time_row.addWidget(self.end_edit, 1)

        root.addLayout(time_row)

        # ── Row 4: Timer (dedicated row) ──
        timer_row = QHBoxLayout(); timer_row.setSpacing(6)

        timer_icon = QLabel("⏱")
        timer_icon.setStyleSheet("font-size:13px;")
        timer_icon.setFixedWidth(18)
        timer_row.addWidget(timer_icon)

        self._timer_label = QLabel("00:00")
        self._timer_label.setStyleSheet(
            "font-family:monospace;font-size:13px;font-weight:bold;")
        self._timer_label.setMinimumWidth(52)
        timer_row.addWidget(self._timer_label)

        timer_row.addStretch()

        self._start_btn = QPushButton("▶ Start")
        self._start_btn.setToolTip("Start timer")
        self._start_btn.setFixedHeight(26)
        self._start_btn.setStyleSheet(
            "background-color:#a6e3a1;color:#1e1e2e;font-weight:bold;"
            "border-radius:4px;padding:2px 10px;font-size:11px;")
        self._start_btn.clicked.connect(self._start_timer)
        timer_row.addWidget(self._start_btn)

        self._stop_btn = QPushButton("■ Stop")
        self._stop_btn.setToolTip("Stop timer")
        self._stop_btn.setFixedHeight(26)
        self._stop_btn.setStyleSheet(
            "background-color:#f38ba8;color:#1e1e2e;font-weight:bold;"
            "border-radius:4px;padding:2px 10px;font-size:11px;")
        self._stop_btn.setEnabled(False)
        self._stop_btn.clicked.connect(self._stop_timer)
        timer_row.addWidget(self._stop_btn)

        root.addLayout(timer_row)

        # ── Row 5: Notes + action buttons ──
        action_row = QHBoxLayout(); action_row.setSpacing(5)

        self._notes_btn = QPushButton("Notes…")
        self._notes_btn.setObjectName("secondary")
        self._notes_btn.setFixedHeight(26)
        self._notes_btn.clicked.connect(self._open_notes)
        action_row.addWidget(self._notes_btn)

        action_row.addStretch()

        self._delete_btn = QPushButton("Delete")
        self._delete_btn.setObjectName("destructive")
        self._delete_btn.setFixedHeight(26)
        self._delete_btn.clicked.connect(self._delete)
        self._delete_btn.setVisible(False)
        action_row.addWidget(self._delete_btn)

        self._action_btn = QPushButton("Add")
        self._action_btn.setFixedHeight(26)
        self._action_btn.clicked.connect(self._submit)
        action_row.addWidget(self._action_btn)

        root.addLayout(action_row)

    # ── Public ───────────────────────────────────────

    def set_week_start(self, week_start: date):
        self._week_start = week_start
        self._rebuild_day_combo()

    def prefill(self, d: date, hour: float):
        """Called when user double-clicks empty space on the grid."""
        self._cancel_edit()
        idx = (d - self._week_start).days
        if 0 <= idx < 7:
            self.day_combo.setCurrentIndex(idx)
        h = int(hour); m = int((hour - h) * 60)
        self.start_edit.setTime(QTime(h, m))
        self.end_edit.setTime(QTime(min(h + 1, 23), m))

    def load_for_edit(self, activity: Activity):
        """Populate form fields with an existing activity for editing."""
        self._editing = activity
        self._pending_notes = activity.notes or ""

        idx = self.activity_combo.findText(activity.activity)
        if idx >= 0: self.activity_combo.setCurrentIndex(idx)
        else:        self.activity_combo.setCurrentText(activity.activity)

        act_date = date.fromisoformat(activity.date)
        day_idx = (act_date - self._week_start).days
        if 0 <= day_idx < 7: self.day_combo.setCurrentIndex(day_idx)

        sh, sm = map(int, activity.start_time.split(":"))
        eh, em = map(int, activity.end_time.split(":"))
        self.start_edit.setTime(QTime(sh, sm))
        self.end_edit.setTime(QTime(eh, em))

        self._form_title.setText("Edit Activity")
        self._action_btn.setText("Update")
        self._cancel_btn.setVisible(True)
        self._delete_btn.setVisible(True)

    # ── Private ──────────────────────────────────────

    def _rebuild_day_combo(self):
        self.day_combo.clear()
        day_names = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        today = date.today()
        for i in range(7):
            d = self._week_start + timedelta(days=i)
            label = f"{day_names[i]} {d.day}"
            if d == today: label += " ★"
            self.day_combo.addItem(label, d)
        # Default to today if in range
        idx = (today - self._week_start).days
        if 0 <= idx < 7: self.day_combo.setCurrentIndex(idx)

    def _selected_date(self) -> date:
        d = self.day_combo.currentData()
        return d if isinstance(d, date) else self._week_start

    def _submit(self):
        name = self.activity_combo.currentText().strip()
        if not name: return

        self._stop_timer()
        start = self.start_edit.time().toString("HH:mm")
        end   = self.end_edit.time().toString("HH:mm")
        d     = self._selected_date()

        if self._editing:
            self._editing.activity   = name
            self._editing.date       = d.isoformat()
            self._editing.start_time = start
            self._editing.end_time   = end
            self._editing.notes      = self._pending_notes
            self.activity_updated.emit(self._editing)
            self._cancel_edit()
        else:
            store = ActivityStore()
            act = store.add(date=d.isoformat(), activity=name,
                            start_time=start, end_time=end,
                            notes=self._pending_notes)
            self._pending_notes = ""
            self.activity_added.emit(act)

    def _delete(self):
        if not self._editing: return
        reply = QMessageBox.question(
            self, "Delete Activity",
            f"Delete '{self._editing.activity}' ({self._editing.start_time}–{self._editing.end_time})?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.activity_deleted.emit(self._editing.id)
            self._cancel_edit()

    def _cancel_edit(self):
        self._editing = None
        self._pending_notes = ""
        self._form_title.setText("Log Activity")
        self._action_btn.setText("Add")
        self._cancel_btn.setVisible(False)
        self._delete_btn.setVisible(False)

    def _open_notes(self):
        dlg = NotesDialog(self, self._pending_notes)
        if dlg.exec():
            self._pending_notes = dlg.get_notes()

    def _start_timer(self):
        now = datetime.now()
        self._timer_start = now
        self.start_edit.setTime(QTime(now.hour, now.minute))
        self.end_edit.setTime(QTime(now.hour, now.minute))
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(1000)
        self._start_btn.setEnabled(False)
        self._stop_btn.setEnabled(True)
        self._timer_label.setStyleSheet(
            "font-family:monospace;font-size:13px;font-weight:bold;color:#a6e3a1;")

    def _stop_timer(self):
        if self._timer:
            self._timer.stop(); self._timer = None
        if self._timer_start:
            now = datetime.now()
            self.end_edit.setTime(QTime(now.hour, now.minute))
        self._timer_start = None
        self._start_btn.setEnabled(True)
        self._stop_btn.setEnabled(False)
        self._timer_label.setStyleSheet(
            "font-family:monospace;font-size:13px;font-weight:bold;")

    def _tick(self):
        if not self._timer_start: return
        secs = int((datetime.now() - self._timer_start).total_seconds())
        h, s = divmod(secs, 3600); m, s = divmod(s, 60)
        self._timer_label.setText(f"{h:02d}:{m:02d}" if h else f"{m:02d}:{s:02d}")
        now = datetime.now()
        self.end_edit.setTime(QTime(now.hour, now.minute))


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ActivityPanel  — main panel
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ActivityPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.store = ActivityStore()
        self._palette: dict = {}
        self._week_start = date.today() - timedelta(days=date.today().weekday())
        self._activities_by_date: dict[date, list[Activity]] = {}
        self._build_ui()
        self._refresh()

    # ── Palette ─────────────────────────────────────

    def set_palette(self, palette: dict):
        self._palette = palette
        self._grid.set_palette(palette)
        self._efficiency.set_palette(palette)

    # ── Build UI ────────────────────────────────────

    def _build_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ══ LEFT: scrollable week grid ══
        left = QWidget()
        left_l = QVBoxLayout(left)
        left_l.setContentsMargins(0, 10, 0, 10)
        left_l.setSpacing(8)

        # Top bar
        top_bar = QHBoxLayout(); top_bar.setContentsMargins(14, 0, 8, 0)
        title = QLabel("Activity Tracker"); title.setObjectName("sectionTitle")
        top_bar.addWidget(title); top_bar.addStretch()

        self._week_label = QLabel()
        self._week_label.setStyleSheet("font-size:12px;font-weight:bold;")
        top_bar.addWidget(self._week_label); top_bar.addSpacing(8)

        btn_prev = QPushButton("‹"); btn_prev.setObjectName("secondary")
        btn_prev.setFixedSize(28, 28); btn_prev.setToolTip("Previous week")
        btn_prev.clicked.connect(self._prev_week); top_bar.addWidget(btn_prev)

        btn_today = QPushButton("Today"); btn_today.setObjectName("secondary")
        btn_today.setFixedHeight(28); btn_today.clicked.connect(self._go_today)
        top_bar.addWidget(btn_today)

        btn_next = QPushButton("›"); btn_next.setObjectName("secondary")
        btn_next.setFixedSize(28, 28); btn_next.setToolTip("Next week")
        btn_next.clicked.connect(self._next_week); top_bar.addWidget(btn_next)

        top_bar.addSpacing(8)
        btn_export = QPushButton("Export…"); btn_export.setObjectName("secondary")
        btn_export.setFixedHeight(28); btn_export.clicked.connect(self._export)
        top_bar.addWidget(btn_export)

        left_l.addLayout(top_bar)

        # Grid inside scroll area
        self._grid = WeekBlockWidget()
        self._grid.block_clicked.connect(self._on_block_clicked)
        self._grid.empty_clicked.connect(self._on_empty_clicked)

        scroll = QScrollArea(); scroll.setWidgetResizable(True)
        scroll.setWidget(self._grid)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        left_l.addWidget(scroll, 1)
        root.addWidget(left, 1)

        # ══ RIGHT: efficiency + log form ══
        right = QWidget(); right.setFixedWidth(310)
        right_l = QVBoxLayout(right)
        right_l.setContentsMargins(8, 10, 12, 10)
        right_l.setSpacing(10)

        self._efficiency = EfficiencyPanel()
        right_l.addWidget(self._efficiency, 1)

        div = QFrame(); div.setFrameShape(QFrame.Shape.HLine)
        div.setObjectName("separator"); right_l.addWidget(div)

        self._log_form = LogForm(self._week_start)
        self._log_form.activity_added.connect(self._on_activity_added)
        self._log_form.activity_updated.connect(self._on_activity_updated)
        self._log_form.activity_deleted.connect(self._on_activity_deleted)
        right_l.addWidget(self._log_form)

        root.addWidget(right)

        # Auto-refresh timer
        self._auto_timer = QTimer(self)
        self._auto_timer.setInterval(60_000)
        self._auto_timer.timeout.connect(self._refresh)
        self._auto_timer.start()

    # ── Navigation ───────────────────────────────────

    def _prev_week(self):
        self._week_start -= timedelta(weeks=1)
        self._log_form.set_week_start(self._week_start)
        self._refresh()

    def _next_week(self):
        self._week_start += timedelta(weeks=1)
        self._log_form.set_week_start(self._week_start)
        self._refresh()

    def _go_today(self):
        today = date.today()
        self._week_start = today - timedelta(days=today.weekday())
        self._log_form.set_week_start(self._week_start)
        self._refresh()

    # ── Refresh ─────────────────────────────────────

    def _refresh(self):
        we = self._week_start + timedelta(days=6)
        self._week_label.setText(
            f"{self._week_start.strftime('%b %d')} – {we.strftime('%b %d, %Y')}"
        )

        self._activities_by_date = {}
        for i in range(7):
            d = self._week_start + timedelta(days=i)
            self._activities_by_date[d] = self.store.get_for_date(d.isoformat())

        self._grid.load_week(self._week_start, self._activities_by_date)
        self._efficiency.update_data(self._week_start, self._activities_by_date)

    # ── Grid callbacks ───────────────────────────────

    def _on_block_clicked(self, activity: Activity):
        self._log_form.load_for_edit(activity)

    def _on_empty_clicked(self, d: date, hour: float):
        self._log_form.prefill(d, hour)

    # ── CRUD callbacks ───────────────────────────────

    def _on_activity_added(self, _activity: Activity):
        self._refresh()

    def _on_activity_updated(self, activity: Activity):
        self.store.update(activity)
        self._refresh()

    def _on_activity_deleted(self, activity_id: str):
        self.store.delete(activity_id)
        self._refresh()

    # ── Export ───────────────────────────────────────

    def _export(self):
        cfg = load_config()
        vault_path = cfg.get("obsidian_vault_path", "")
        if not vault_path or not Path(vault_path).is_dir():
            QMessageBox.warning(
                self, "No Vault",
                "Set an Obsidian vault path first (Notes → Set Vault)."
            )
            return

        vault = Path(vault_path)
        exported = 0
        for d, activities in self._activities_by_date.items():
            if not activities: continue
            year_f  = str(d.year)
            month_f = f"{d.month:02d} - {d.strftime('%B')}"
            day_f   = f"{d.day:02d} - {d.strftime('%A')}"
            base = vault / "Activity Tracker" / year_f / month_f / day_f
            base.mkdir(parents=True, exist_ok=True)

            total_mins = sum(a.duration_minutes for a in activities)
            h, m = divmod(total_mins, 60)
            lines = [
                f"# Activity Summary — {d.strftime('%A, %B %d, %Y')}",
                "", f"**Total tracked:** {h}h {m}m", "",
                "| Time | Activity | Duration | Notes |",
                "|------|----------|----------|-------|",
            ]
            for a in activities:
                notes = (a.notes or "").replace("\n"," ").replace("|","/")
                lines.append(f"| {a.start_time}–{a.end_time} | {a.activity} | {a.duration_minutes}m | {notes} |")
            (base / "_Daily Summary.md").write_text("\n".join(lines), encoding="utf-8")
            exported += len(activities)

        we = self._week_start + timedelta(days=6)
        QMessageBox.information(
            self, "Exported",
            f"Exported {exported} activities for week of "
            f"{self._week_start.strftime('%b %d')} – {we.strftime('%b %d')}."
        )
```

### `src\ui\modules\calendar_panel.py`

```python
"""Calendar module UI — weekly view + mini-month navigator + major events.

All colors read from the active theme palette so the panel adapts when the
user switches themes.  No hardcoded hex values remain in inline stylesheets
or paintEvent code.

Layout (positions unchanged):
  Upper-left  → Weekly overview grid (7 day columns)
  Lower-left  → Selected-day detail list
  Upper-right → Mini month navigator (interactive dot indicators)
  Lower-right → Next major events panel
"""

from __future__ import annotations

import calendar
from datetime import date, datetime, timedelta

from PyQt6.QtCore import Qt, QDate, QTime, QTimer, pyqtSignal
from PyQt6.QtGui import QColor, QPainter, QPen, QBrush, QFont, QFontMetrics, QMouseEvent
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QDialog, QLineEdit, QTextEdit,
    QDateEdit, QTimeEdit, QCheckBox, QFrame, QComboBox,
    QMessageBox, QScrollArea, QSizePolicy, QTabWidget,
    QButtonGroup, QToolButton, QSpinBox,
)

from src.data.calendar_store import (
    CalendarStore, Event, Birthday,
    build_recurrence, expand_recurring_to_range,
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Module-level palette  (updated by CalendarPanel.set_palette)
#  Defaults = Catppuccin Dark so the panel renders correctly before
#  MainWindow calls set_palette() for the first time.
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

_PALETTE: dict = {
    "bg":        "#1e1e2e", "surface":   "#313244", "border": "#45475a",
    "fg":        "#cdd6f4", "muted":     "#7f849c",  "hover":  "#3b3d54",
    "accent":    "#89b4fa", "accent_fg": "#1e1e2e",
    "header_bg": "#181825", "alt_row":   "#252538",
    "red":       "#f38ba8", "green":     "#a6e3a1",  "yellow": "#f9e2af",
}


def _p(key: str, fallback: str = "#888888") -> str:
    """Return current palette value for *key*."""
    return _PALETTE.get(key, fallback)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Category / color constants
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EVENT_COLORS: dict[str, str] = {
    "Sky Blue": "#4a9eff", "Mint":     "#a6e3a1", "Rose":    "#f38ba8",
    "Peach":    "#fab387", "Gold":     "#f9e2af", "Lavender":"#cba6f7",
    "Teal":     "#94e2d5", "Pink":     "#f5c2e7", "Coral":   "#ff6b6b",
    "Sage":     "#74c7b8",
}

CATEGORY_META: dict[str, dict] = {
    "":         {"label": "General",     "emoji": "📅", "color": "#4a9eff"},
    "work":     {"label": "Work",        "emoji": "💼", "color": "#4a9eff"},
    "birthday": {"label": "Birthday",    "emoji": "🎂", "color": "#f38ba8"},
    "trip":     {"label": "Trip",        "emoji": "✈️",  "color": "#94e2d5"},
    "holiday":  {"label": "Holiday",     "emoji": "🎉", "color": "#f9e2af"},
    "major":    {"label": "Major Event", "emoji": "⭐", "color": "#cba6f7"},
    "health":   {"label": "Health",      "emoji": "🏥", "color": "#a6e3a1"},
    "social":   {"label": "Social",      "emoji": "🎭", "color": "#fab387"},
}

RECURRENCE_OPTIONS = [
    ("",        "Does not repeat"), ("daily",   "Every day"),
    ("weekly",  "Weekly (select days)"), ("monthly", "Monthly"),
    ("yearly",  "Yearly"),
]

WEEKDAY_LABELS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def _cat_emoji(cat: str) -> str:
    return CATEGORY_META.get(cat, CATEGORY_META[""]).get("emoji", "")

def _cat_color(cat: str) -> str:
    return CATEGORY_META.get(cat, CATEGORY_META[""]).get("color", "#4a9eff")

def _clear_layout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():   child.widget().deleteLater()
        elif child.layout(): _clear_layout(child.layout())


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ColorButton — theme-aware color swatch
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ColorButton(QToolButton):
    def __init__(self, hex_color: str, name: str, parent=None):
        super().__init__(parent)
        self.hex_color = hex_color
        self.setFixedSize(28, 28)
        self.setCheckable(True)
        self.setToolTip(name)
        self._update_style()

    def setChecked(self, checked: bool):
        super().setChecked(checked)
        self._update_style()

    def _update_style(self):
        border_color = _p("fg") if self.isChecked() else "transparent"
        border_width = "3px" if self.isChecked() else "2px"
        self.setStyleSheet(
            f"QToolButton {{ background-color: {self.hex_color}; "
            f"border: {border_width} solid {border_color}; border-radius: 6px; }}"
        )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  EventDialog
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class EventDialog(QDialog):
    def __init__(self, parent=None, event: Event | None = None,
                 prefill_date: date | None = None):
        super().__init__(parent)
        self.event = event
        self._delete_requested = False
        self.setWindowTitle("Edit Event" if event else "New Event")
        self.setMinimumWidth(460)
        self.setModal(True)
        self._build_ui(prefill_date)

    def _build_ui(self, prefill_date):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        init_color = self.event.color if self.event else _p("accent")
        self._header_strip = QFrame()
        self._header_strip.setFixedHeight(6)
        self._header_strip.setStyleSheet(
            f"background-color: {init_color}; border-radius: 3px 3px 0 0;")
        root.addWidget(self._header_strip)

        body = QWidget()
        body_l = QVBoxLayout(body)
        body_l.setContentsMargins(20, 16, 20, 16)
        body_l.setSpacing(12)
        root.addWidget(body)

        tabs = QTabWidget()
        tabs.setDocumentMode(True)
        body_l.addWidget(tabs)

        # ── Details tab ──
        det_tab = QWidget()
        det = QVBoxLayout(det_tab)
        det.setContentsMargins(4, 12, 4, 4)
        det.setSpacing(10)
        tabs.addTab(det_tab, "Details")

        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Event title…")
        self.title_edit.setStyleSheet("font-size: 15px; padding: 6px; font-weight: bold;")
        if self.event: self.title_edit.setText(self.event.title)
        det.addWidget(self.title_edit)

        self.desc_edit = QTextEdit()
        self.desc_edit.setMaximumHeight(68)
        self.desc_edit.setPlaceholderText("Optional description…")
        if self.event: self.desc_edit.setPlainText(self.event.description)
        det.addWidget(self.desc_edit)

        cat_row = QHBoxLayout()
        cat_row.addWidget(QLabel("Category"))
        self.category_combo = QComboBox()
        for key, meta in CATEGORY_META.items():
            self.category_combo.addItem(f"{meta['emoji']} {meta['label']}", key)
        if self.event:
            idx = self.category_combo.findData(self.event.category)
            if idx >= 0: self.category_combo.setCurrentIndex(idx)
        self.category_combo.currentIndexChanged.connect(self._on_category_changed)
        cat_row.addWidget(self.category_combo, 1)
        det.addLayout(cat_row)

        det.addWidget(QLabel("Color"))
        color_row = QHBoxLayout()
        color_row.setSpacing(6)
        self._color_group = QButtonGroup(self)
        self._color_group.setExclusive(True)
        self._color_btns: dict[str, ColorButton] = {}
        current_color = self.event.color if self.event else _p("accent")
        for name, hex_val in EVENT_COLORS.items():
            btn = ColorButton(hex_val, name)
            btn.setChecked(hex_val == current_color)
            btn.clicked.connect(lambda _, h=hex_val: self._on_color_picked(h))
            self._color_group.addButton(btn)
            self._color_btns[hex_val] = btn
            color_row.addWidget(btn)
        color_row.addStretch()
        det.addLayout(color_row)

        self.all_day_check = QCheckBox("All-day event")
        if self.event: self.all_day_check.setChecked(self.event.all_day)
        self.all_day_check.toggled.connect(self._toggle_time)
        det.addWidget(self.all_day_check)

        dt_row = QHBoxLayout()
        dt_row.setSpacing(8)
        dt_row.addWidget(QLabel("Date"))
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDisplayFormat("dd MMM yyyy")
        if self.event:
            d0 = datetime.fromisoformat(self.event.start_time)
            self.date_edit.setDate(QDate(d0.year, d0.month, d0.day))
        elif prefill_date:
            self.date_edit.setDate(QDate(prefill_date.year, prefill_date.month, prefill_date.day))
        else:
            t = date.today()
            self.date_edit.setDate(QDate(t.year, t.month, t.day))
        dt_row.addWidget(self.date_edit, 2)

        dt_row.addWidget(QLabel("Start"))
        self.start_time = QTimeEdit()
        self.start_time.setDisplayFormat("HH:mm")
        if self.event and not self.event.all_day:
            d0 = datetime.fromisoformat(self.event.start_time)
            self.start_time.setTime(QTime(d0.hour, d0.minute))
        else:
            self.start_time.setTime(QTime(9, 0))
        dt_row.addWidget(self.start_time, 1)

        dt_row.addWidget(QLabel("End"))
        self.end_time = QTimeEdit()
        self.end_time.setDisplayFormat("HH:mm")
        if self.event and self.event.end_time:
            d0 = datetime.fromisoformat(self.event.end_time)
            self.end_time.setTime(QTime(d0.hour, d0.minute))
        else:
            self.end_time.setTime(QTime(10, 0))
        dt_row.addWidget(self.end_time, 1)
        det.addLayout(dt_row)
        self._toggle_time(self.all_day_check.isChecked())

        # ── Repeat tab ──
        rec_tab = QWidget()
        rec = QVBoxLayout(rec_tab)
        rec.setContentsMargins(4, 12, 4, 4)
        rec.setSpacing(10)
        tabs.addTab(rec_tab, "Repeat")

        rec.addWidget(QLabel("Repeat pattern"))
        self.rec_combo = QComboBox()
        for val, label in RECURRENCE_OPTIONS:
            self.rec_combo.addItem(label, val)
        rec.addWidget(self.rec_combo)
        self.rec_combo.currentIndexChanged.connect(
            lambda _: self._weekday_frame.setVisible(
                self.rec_combo.currentData() == "weekly"))

        self._weekday_frame = QFrame()
        wdf = QHBoxLayout(self._weekday_frame)
        wdf.setContentsMargins(0, 4, 0, 0)
        wdf.setSpacing(4)
        self._weekday_btns: list[QToolButton] = []
        for label in WEEKDAY_LABELS:
            btn = QToolButton()
            btn.setText(label)
            btn.setCheckable(True)
            btn.setFixedSize(42, 30)
            self._weekday_btns.append(btn)
            wdf.addWidget(btn)
        wdf.addStretch()
        rec.addWidget(self._weekday_frame)
        self._weekday_frame.setVisible(False)
        rec.addStretch()

        if self.event and self.event.recurrence:
            r = self.event.recurrence
            if r == "daily":      self.rec_combo.setCurrentIndex(1)
            elif r.startswith("weekly:"):
                self.rec_combo.setCurrentIndex(2)
                for d in [int(x) for x in r.split(":")[1].split(",") if x.strip()]:
                    if 0 <= d < len(self._weekday_btns):
                        self._weekday_btns[d].setChecked(True)
            elif r == "monthly":  self.rec_combo.setCurrentIndex(3)
            elif r == "yearly":   self.rec_combo.setCurrentIndex(4)

        # ── Buttons ──
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setObjectName("separator")
        body_l.addWidget(sep)

        btn_row = QHBoxLayout()
        if self.event:
            del_btn = QPushButton("🗑  Delete")
            del_btn.setObjectName("destructive")
            del_btn.clicked.connect(self._on_delete)
            btn_row.addWidget(del_btn)
        btn_row.addStretch()
        cancel = QPushButton("Cancel")
        cancel.setObjectName("secondary")
        cancel.clicked.connect(self.reject)
        btn_row.addWidget(cancel)
        save = QPushButton("Save Event")
        save.setDefault(True)
        save.clicked.connect(self._on_save)
        btn_row.addWidget(save)
        body_l.addLayout(btn_row)

    def _on_color_picked(self, hex_val: str):
        self._header_strip.setStyleSheet(
            f"background-color: {hex_val}; border-radius: 3px 3px 0 0;")
        for hv, btn in self._color_btns.items():
            btn._update_style()

    def _on_category_changed(self, _):
        auto = _cat_color(self.category_combo.currentData())
        btn = self._color_btns.get(auto)
        if btn:
            for b in self._color_btns.values(): b.setChecked(False)
            btn.setChecked(True)
            self._on_color_picked(auto)

    def _toggle_time(self, all_day: bool):
        self.start_time.setEnabled(not all_day)
        self.end_time.setEnabled(not all_day)

    def _on_delete(self):
        self._delete_requested = True; self.reject()

    def _on_save(self):
        if not self.title_edit.text().strip():
            self.title_edit.setFocus()
            self.title_edit.setPlaceholderText("⚠ Title is required")
            return
        self.accept()

    def _selected_color(self) -> str:
        for hex_val, btn in self._color_btns.items():
            if btn.isChecked(): return hex_val
        return _p("accent")

    def _selected_recurrence(self) -> str:
        val = self.rec_combo.currentData()
        if val == "weekly":
            days = [i for i, b in enumerate(self._weekday_btns) if b.isChecked()]
            return build_recurrence("weekly", days) if days else ""
        return build_recurrence(val) if val else ""

    def get_data(self) -> dict:
        qd = self.date_edit.date()
        d = date(qd.year(), qd.month(), qd.day())
        all_day = self.all_day_check.isChecked()
        if all_day:
            start = datetime(d.year, d.month, d.day).isoformat()
            end = None
        else:
            st = self.start_time.time(); et = self.end_time.time()
            start = datetime(d.year, d.month, d.day, st.hour(), st.minute()).isoformat()
            end   = datetime(d.year, d.month, d.day, et.hour(), et.minute()).isoformat()
        return {
            "title":       self.title_edit.text().strip() or "Untitled",
            "description": self.desc_edit.toPlainText(),
            "start_time":  start, "end_time": end,
            "all_day":     all_day, "color": self._selected_color(),
            "category":    self.category_combo.currentData() or "",
            "recurrence":  self._selected_recurrence(),
        }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  BirthdayDialog
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class BirthdayDialog(QDialog):
    def __init__(self, parent=None, birthday: Birthday | None = None):
        super().__init__(parent)
        self.birthday = birthday
        self._delete_requested = False
        self.setWindowTitle("Edit Birthday" if birthday else "Add Birthday")
        self.setMinimumWidth(360); self.setModal(True)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 16)
        layout.setSpacing(12)

        hdr = QLabel("🎂  Birthday")
        hdr.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(hdr)

        layout.addWidget(QLabel("Name"))
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Person's name…")
        if self.birthday: self.name_edit.setText(self.birthday.name)
        layout.addWidget(self.name_edit)

        mdy = QHBoxLayout()
        for label, attr, lo, hi in [("Month", "month", 1, 12), ("Day", "day", 1, 31)]:
            col = QVBoxLayout()
            col.addWidget(QLabel(label))
            spin = QSpinBox(); spin.setRange(lo, hi)
            if self.birthday: spin.setValue(getattr(self.birthday, attr))
            col.addWidget(spin); mdy.addLayout(col)
            setattr(self, f"{attr}_spin", spin)
        yr_col = QVBoxLayout()
        yr_col.addWidget(QLabel("Year (optional)"))
        self.year_spin = QSpinBox()
        self.year_spin.setRange(0, 9999)
        self.year_spin.setSpecialValueText("—")
        self.year_spin.setValue(self.birthday.year if (self.birthday and self.birthday.year) else 0)
        yr_col.addWidget(self.year_spin); mdy.addLayout(yr_col)
        layout.addLayout(mdy)

        layout.addWidget(QLabel("Note"))
        self.note_edit = QTextEdit()
        self.note_edit.setPlaceholderText("Optional note about this person…")
        self.note_edit.setMinimumHeight(80)
        self.note_edit.setMaximumHeight(140)
        if self.birthday and self.birthday.note:
            self.note_edit.setPlainText(self.birthday.note)
        layout.addWidget(self.note_edit)

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine); sep.setObjectName("separator")
        layout.addWidget(sep)

        btn_row = QHBoxLayout()
        if self.birthday:
            del_btn = QPushButton("Delete"); del_btn.setObjectName("destructive")
            del_btn.clicked.connect(self._on_delete); btn_row.addWidget(del_btn)
        btn_row.addStretch()
        cancel = QPushButton("Cancel"); cancel.setObjectName("secondary")
        cancel.clicked.connect(self.reject); btn_row.addWidget(cancel)
        save = QPushButton("Save"); save.setDefault(True)
        save.clicked.connect(self._on_save); btn_row.addWidget(save)
        layout.addLayout(btn_row)

    def _on_delete(self): self._delete_requested = True; self.reject()

    def _on_save(self):
        if not self.name_edit.text().strip(): self.name_edit.setFocus(); return
        self.accept()

    def get_data(self) -> dict:
        y = self.year_spin.value()
        return {
            "name":  self.name_edit.text().strip(),
            "month": self.month_spin.value(),
            "day":   self.day_spin.value(),
            "year":  y if y > 0 else None,
            "note":  self.note_edit.toPlainText().strip(),
        }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  MiniMonthCell  — fully painted using current palette
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class MiniMonthCell(QWidget):
    clicked = pyqtSignal(int, int, int)
    CELL = 32

    def __init__(self, year, month, day, is_today, is_selected,
                 event_colors: list[str], is_holiday: bool = False, parent=None):
        super().__init__(parent)
        self.year, self.month, self.day = year, month, day
        self.is_today = is_today; self.is_selected = is_selected
        self.event_colors = event_colors[:4]; self.is_holiday = is_holiday
        self._hovered = False
        self.setFixedSize(self.CELL, self.CELL)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        if event_colors or is_holiday:
            parts = (["Holiday"] if is_holiday else []) + ([f"{len(event_colors)} event(s)"] if event_colors else [])
            self.setToolTip(", ".join(parts))

    def enterEvent(self, ev): self._hovered = True;  self.update()
    def leaveEvent(self, ev): self._hovered = False; self.update()
    def mousePressEvent(self, ev): self.clicked.emit(self.year, self.month, self.day)

    def paintEvent(self, ev):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        cx, cy = w / 2, (h - 6) / 2

        accent  = QColor(_p("accent"))
        fg      = QColor(_p("fg"))
        hover_c = QColor(_p("hover"))
        red     = QColor(_p("red"))

        if self.is_today:
            p.setBrush(QBrush(accent)); p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(int(cx-13), int(cy-13), 26, 26)
        elif self.is_selected:
            c = QColor(accent); c.setAlpha(45)
            p.setBrush(QBrush(c)); p.setPen(QPen(accent, 1.5))
            p.drawEllipse(int(cx-13), int(cy-13), 26, 26)
        elif self._hovered:
            p.setBrush(QBrush(hover_c)); p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(int(cx-13), int(cy-13), 26, 26)

        font = QFont(); font.setPixelSize(12)
        if self.is_today or self.is_selected: font.setBold(True)
        p.setFont(font)
        if self.is_today:     p.setPen(QColor(_p("accent_fg")))
        elif self.is_holiday: p.setPen(red)
        else:                 p.setPen(fg)
        p.drawText(0, 0, w, int(h-7), Qt.AlignmentFlag.AlignCenter, str(self.day))

        if self.event_colors:
            dr=3; n=len(self.event_colors); sp=dr*2+2
            sx = cx - (n*sp-2)/2; dy = h-5
            for i, color in enumerate(self.event_colors):
                p.setBrush(QBrush(QColor(color))); p.setPen(Qt.PenStyle.NoPen)
                p.drawEllipse(int(sx+i*sp-dr), int(dy-dr), dr*2, dr*2)
        p.end()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  MiniMonth
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class MiniMonth(QWidget):
    date_selected = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(240)
        self._selected    = date.today()
        self._view_year   = self._selected.year
        self._view_month  = self._selected.month
        self._events:    dict[date, list[str]] = {}
        self._holidays:  set[date]             = set()
        self._nav_buttons: list[QPushButton]   = []
        self._dow_labels:  list[QLabel]        = []
        self._title_btn:   QPushButton         = None  # type: ignore
        self._build()

    # ── Public ──────────────────────────────────────

    def set_events(self, by_date: dict[date, list[str]]):
        self._events = by_date; self._render()

    def set_holidays(self, holidays: set[date]):
        self._holidays = holidays; self._render()

    def set_selected(self, d: date):
        self._selected = d
        self._view_year = d.year; self._view_month = d.month
        self._render()

    def refresh_styles(self):
        """Re-apply palette colors to navigation buttons/labels."""
        nav_style = (
            f"QPushButton {{ background-color: {_p('surface')}; color: {_p('fg')}; "
            f"border: 1px solid {_p('border')}; border-radius: 4px; "
            f"font-weight: bold; font-size: 14px; padding: 0px; }}"
            f"QPushButton:hover {{ background-color: {_p('hover')}; "
            f"border-color: {_p('accent')}; color: {_p('accent')}; }}"
            f"QPushButton:pressed {{ background-color: {_p('border')}; }}"
        )
        for btn in self._nav_buttons:
            btn.setStyleSheet(nav_style)
        if self._title_btn:
            self._title_btn.setStyleSheet(
                f"QPushButton {{ background-color: transparent; color: {_p('fg')}; "
                f"border: none; font-weight: bold; font-size: 13px; }}"
                f"QPushButton:hover {{ color: {_p('accent')}; }}"
            )
        for lbl in self._dow_labels:
            lbl.setStyleSheet(f"font-size: 10px; font-weight: bold; color: {_p('muted')};")
        self._render()

    # ── Build ────────────────────────────────────────

    def _nav_style(self) -> str:
        return (
            f"QPushButton {{ background-color: {_p('surface')}; color: {_p('fg')}; "
            f"border: 1px solid {_p('border')}; border-radius: 4px; "
            f"font-weight: bold; font-size: 14px; padding: 0px; }}"
            f"QPushButton:hover {{ background-color: {_p('hover')}; "
            f"border-color: {_p('accent')}; color: {_p('accent')}; }}"
            f"QPushButton:pressed {{ background-color: {_p('border')}; }}"
        )

    def _build(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(8, 8, 8, 8); outer.setSpacing(2)

        nav = QHBoxLayout(); nav.setSpacing(0)
        for symbol, tip, handler in [
            ("«", "Previous year",  self._prev_year),
            ("‹", "Previous month", self._prev_month),
        ]:
            btn = QPushButton(symbol); btn.setFixedSize(26, 26)
            btn.setToolTip(tip); btn.clicked.connect(handler)
            btn.setStyleSheet(self._nav_style())
            self._nav_buttons.append(btn); nav.addWidget(btn)

        self._title_btn = QPushButton()
        self._title_btn.setFlat(True)
        self._title_btn.clicked.connect(self._go_today_month)
        self._title_btn.setStyleSheet(
            f"QPushButton {{ background-color: transparent; color: {_p('fg')}; "
            f"border: none; font-weight: bold; font-size: 13px; }}"
            f"QPushButton:hover {{ color: {_p('accent')}; }}"
        )
        nav.addWidget(self._title_btn, 1)

        for symbol, tip, handler in [
            ("›", "Next month", self._next_month),
            ("»", "Next year",  self._next_year),
        ]:
            btn = QPushButton(symbol); btn.setFixedSize(26, 26)
            btn.setToolTip(tip); btn.clicked.connect(handler)
            btn.setStyleSheet(self._nav_style())
            self._nav_buttons.append(btn); nav.addWidget(btn)

        outer.addLayout(nav)

        dow_row = QHBoxLayout(); dow_row.setSpacing(0)
        dow_row.setContentsMargins(0, 4, 0, 0)
        for label in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
            lbl = QLabel(label)
            lbl.setFixedSize(MiniMonthCell.CELL, 16)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet(f"font-size: 10px; font-weight: bold; color: {_p('muted')};")
            self._dow_labels.append(lbl); dow_row.addWidget(lbl)
        outer.addLayout(dow_row)

        self._grid_w = QWidget()
        self._grid   = QGridLayout(self._grid_w)
        self._grid.setSpacing(1); self._grid.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(self._grid_w)
        outer.addStretch()
        self._render()

    def _render(self):
        _clear_layout(self._grid)
        self._title_btn.setText(
            f"{calendar.month_abbr[self._view_month]} {self._view_year}"
        )
        today = date.today()
        for row, week in enumerate(
                calendar.Calendar(firstweekday=0).monthdayscalendar(
                    self._view_year, self._view_month)):
            for col, day in enumerate(week):
                if day == 0:
                    sp = QLabel(); sp.setFixedSize(MiniMonthCell.CELL, MiniMonthCell.CELL)
                    self._grid.addWidget(sp, row, col)
                else:
                    d = date(self._view_year, self._view_month, day)
                    cell = MiniMonthCell(
                        self._view_year, self._view_month, day,
                        is_today=(d == today), is_selected=(d == self._selected),
                        event_colors=self._events.get(d, []),
                        is_holiday=(d in self._holidays),
                    )
                    cell.clicked.connect(self._on_cell_click)
                    self._grid.addWidget(cell, row, col)

    def _on_cell_click(self, y, m, d):
        self._selected = date(y, m, d); self._render()
        self.date_selected.emit(self._selected)

    def _prev_month(self):
        if self._view_month == 1: self._view_month = 12; self._view_year -= 1
        else: self._view_month -= 1
        self._render()

    def _next_month(self):
        if self._view_month == 12: self._view_month = 1; self._view_year += 1
        else: self._view_month += 1
        self._render()

    def _prev_year(self): self._view_year -= 1; self._render()
    def _next_year(self): self._view_year += 1; self._render()

    def _go_today_month(self):
        t = date.today(); self._view_year = t.year; self._view_month = t.month; self._render()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  EventChip  — painted event chip in week grid
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class EventChip(QWidget):
    double_clicked = pyqtSignal(object)

    def __init__(self, event: Event, parent=None):
        super().__init__(parent)
        self.event = event; self._hovered = False
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        self.setMinimumHeight(28)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        time_str = ""
        if not event.all_day:
            try:
                dt = datetime.fromisoformat(event.start_time)
                time_str = dt.strftime("%H:%M")
                if event.end_time:
                    et = datetime.fromisoformat(event.end_time)
                    time_str += f"–{et.strftime('%H:%M')}"
            except Exception: pass
        self._time_str = time_str
        emoji = _cat_emoji(event.category)
        self._display = f"{emoji} {event.title}" if emoji else event.title
        tip = self._display
        if time_str: tip += f"\n{time_str}"
        if event.description: tip += f"\n{event.description[:80]}"
        self.setToolTip(tip)

    def enterEvent(self, ev): self._hovered = True;  self.update()
    def leaveEvent(self, ev): self._hovered = False; self.update()
    def mouseDoubleClickEvent(self, ev): self.double_clicked.emit(self.event)

    def paintEvent(self, ev):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        color = QColor(self.event.color)
        bg = QColor(color); bg.setAlpha(55 if self._hovered else 35)
        p.setBrush(QBrush(bg)); p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(0, 0, w, h, 4, 4)
        p.setBrush(QBrush(color)); p.drawRoundedRect(0, 0, 3, h, 2, 2)
        text_c = color.lighter(145 if self._hovered else 128)
        p.setPen(text_c)
        font = QFont()
        if self._time_str:
            font.setPixelSize(9); p.setFont(font)
            p.drawText(8, 0, w-10, h//2+2, Qt.AlignmentFlag.AlignVCenter, self._time_str)
            font.setPixelSize(11); font.setBold(True); p.setFont(font)
            fm = QFontMetrics(font)
            p.drawText(8, h//2-2, w-10, h//2+2, Qt.AlignmentFlag.AlignVCenter,
                       fm.elidedText(self._display, Qt.TextElideMode.ElideRight, w-14))
        else:
            font.setPixelSize(11); font.setBold(True); p.setFont(font)
            fm = QFontMetrics(font)
            p.drawText(8, 0, w-10, h, Qt.AlignmentFlag.AlignVCenter,
                       fm.elidedText(self._display, Qt.TextElideMode.ElideRight, w-14))
        p.end()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  DayColumn
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class DayColumn(QWidget):
    request_add  = pyqtSignal(object)
    request_edit = pyqtSignal(object)

    def __init__(self, d: date, events: list[Event], birthdays: list[Birthday],
                 is_today: bool, is_selected: bool, parent=None):
        super().__init__(parent)
        self.d = d; self._hovered = False
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        self._build(events, birthdays, is_today, is_selected)

    def _build(self, events, birthdays, is_today, is_selected):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(3, 4, 3, 4); layout.setSpacing(3)

        header = QWidget(); header.setFixedHeight(46)
        hl = QVBoxLayout(header); hl.setContentsMargins(0, 2, 0, 2); hl.setSpacing(0)

        name_lbl = QLabel(self.d.strftime("%a").upper())
        name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_lbl.setStyleSheet(f"font-size:10px; font-weight:bold; color:{_p('muted')};")
        hl.addWidget(name_lbl)

        num_lbl = QLabel(str(self.d.day))
        num_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if is_today:
            num_lbl.setStyleSheet(
                f"background-color:{_p('accent')};color:{_p('accent_fg')};"
                "border-radius:13px;font-size:16px;font-weight:bold;padding:0 4px;")
            num_lbl.setFixedSize(26, 26)
        elif is_selected:
            num_lbl.setStyleSheet(
                f"border:1.5px solid {_p('accent')};border-radius:13px;"
                f"font-size:16px;font-weight:bold;padding:0 4px;color:{_p('fg')};")
            num_lbl.setFixedSize(26, 26)
        else:
            num_lbl.setStyleSheet(f"font-size:16px;color:{_p('fg')};")
        hl.addWidget(num_lbl, 0, Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(header)

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"border:none;border-top:1px solid {_p('border')};")
        layout.addWidget(sep)

        for ev in sorted(events, key=lambda e: e.start_time):
            if ev.all_day:
                chip = EventChip(ev)
                chip.double_clicked.connect(self.request_edit.emit)
                layout.addWidget(chip)

        for b in birthdays:
            try: age = (self.d.year - b.year) if b.year else None
            except Exception: age = None
            age_str = f" ({age})" if age else ""
            # Format: "🎂 Name 🎂 (age)" — category emoji auto-prepended by EventChip
            fake = Event(
                id=b.id,
                title=f"{b.name} 🎂{age_str}",
                start_time=datetime(self.d.year, self.d.month, self.d.day).isoformat(),
                all_day=True, color=_p("red"), category="birthday",
            )
            layout.addWidget(EventChip(fake))

        for ev in sorted(events, key=lambda e: e.start_time):
            if not ev.all_day:
                chip = EventChip(ev)
                chip.double_clicked.connect(self.request_edit.emit)
                layout.addWidget(chip)

        layout.addStretch()

    def enterEvent(self, ev): self._hovered = True;  self.update()
    def leaveEvent(self, ev): self._hovered = False; self.update()
    def mouseDoubleClickEvent(self, ev): self.request_add.emit(self.d)

    def paintEvent(self, ev):
        p = QPainter(self)
        if self._hovered: p.fillRect(self.rect(), QColor(_p("hover")))
        p.end()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  MajorEventCard — clickable, opens editor on click
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class MajorEventCard(QFrame):
    clicked = pyqtSignal(str, bool)  # (item_id, is_birthday)

    def __init__(self, ev_date: date, title: str, category: str, color: str,
                 item_id: str, is_birthday: bool, parent=None):
        super().__init__(parent)
        self._item_id    = item_id
        self._is_birthday = is_birthday
        today = date.today(); delta = (ev_date - today).days

        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8); layout.setSpacing(10)

        bar = QFrame(); bar.setFixedWidth(3)
        bar.setStyleSheet(f"background-color:{color};border-radius:2px;")
        layout.addWidget(bar)

        emoji_text = _cat_emoji(category)
        if emoji_text:
            emoji_lbl = QLabel(emoji_text)
            emoji_lbl.setStyleSheet(
                "font-size:16px; background:transparent; border:none; padding:0;")
            emoji_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            emoji_lbl.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
            layout.addWidget(emoji_lbl)

        text_col = QVBoxLayout(); text_col.setSpacing(1)
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(f"font-size:12px;font-weight:bold;color:{_p('fg')};")
        title_lbl.setWordWrap(True); text_col.addWidget(title_lbl)
        date_lbl = QLabel(ev_date.strftime("%b %d, %Y"))
        date_lbl.setStyleSheet(f"font-size:10px;color:{_p('muted')};")
        text_col.addWidget(date_lbl); layout.addLayout(text_col, 1)

        if   delta == 0:   bt, bc = "Today",          color
        elif delta == 1:   bt, bc = "Tomorrow",        color
        elif delta < 0:    bt, bc = f"{abs(delta)}d ago", _p("muted")
        elif delta <= 7:   bt, bc = f"{delta}d",       color
        elif delta <= 30:  bt, bc = f"{delta}d",       _p("yellow")
        else:              bt, bc = f"{delta//7}w",    _p("muted")

        badge = QLabel(bt)
        badge.setStyleSheet(
            f"color:{bc};font-size:10px;font-weight:bold;"
            f"border:1px solid {bc};border-radius:8px;padding:2px 7px;"
            f"background:transparent;")
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter); layout.addWidget(badge)

        self.setStyleSheet(
            f"MajorEventCard{{border:1px solid {_p('border')};border-radius:6px;"
            f"background-color:{_p('header_bg')};}}"
            f"MajorEventCard:hover{{border-color:{color};"
            f"background-color:{_p('surface')};}}")

    def mousePressEvent(self, ev):
        if ev.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self._item_id, self._is_birthday)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  DayEventRow — single-click opens edit dialog
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class DayEventRow(QFrame):
    edit_requested = pyqtSignal(object)

    def __init__(self, event: Event, parent=None):
        super().__init__(parent)
        self.event = event
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0); layout.setSpacing(0)

        bar = QFrame(); bar.setFixedWidth(4)
        bar.setStyleSheet(f"background-color:{event.color};border-radius:2px 0 0 2px;")
        layout.addWidget(bar)

        body = QWidget(); bl = QHBoxLayout(body)
        bl.setContentsMargins(8, 6, 8, 6); bl.setSpacing(8)

        if not event.all_day:
            try: t = datetime.fromisoformat(event.start_time).strftime("%H:%M")
            except Exception: t = ""
            tl = QLabel(t)
            tl.setStyleSheet(f"font-size:11px;color:{_p('muted')};min-width:38px;")
            bl.addWidget(tl)

        emoji   = _cat_emoji(event.category)
        display = f"{emoji} {event.title}" if emoji else event.title
        tl2 = QLabel(display)
        tl2.setStyleSheet(f"font-size:13px;color:{_p('fg')};")
        tl2.setWordWrap(True); bl.addWidget(tl2, 1)

        if event.recurrence:
            rl = QLabel("↻")
            rl.setStyleSheet(f"color:{_p('muted')};font-size:14px;")
            rl.setToolTip("Recurring event"); bl.addWidget(rl)

        layout.addWidget(body, 1)
        self.setStyleSheet(
            f"DayEventRow{{border:1px solid {_p('border')};border-radius:4px;"
            f"background-color:{_p('header_bg')};}}"
            f"DayEventRow:hover{{border-color:{_p('muted')};"
            f"background-color:{_p('surface')};}}")

    def mousePressEvent(self, ev):
        if ev.button() == Qt.MouseButton.LeftButton:
            self.edit_requested.emit(self.event)

    def mouseDoubleClickEvent(self, ev):
        self.edit_requested.emit(self.event)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  CalendarPanel — main widget
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class CalendarPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.store = CalendarStore()
        self._selected_date = date.today()
        self._build_ui(); self._refresh()
        self._auto_timer = QTimer(self)
        self._auto_timer.setInterval(60_000)
        self._auto_timer.timeout.connect(self._refresh)
        self._auto_timer.start()

    # ── Palette ─────────────────────────────────────

    def set_palette(self, palette: dict):
        global _PALETTE
        _PALETTE = palette
        self._week_label.setStyleSheet(
            f"font-size:13px;font-weight:bold;color:{_p('muted')};")
        self._left_div.setStyleSheet(
            f"border:none;border-top:1px solid {_p('border')};margin:8px 0;")
        self._mini_frame.setStyleSheet(
            f"#miniMonthFrame{{border:1px solid {_p('border')};"
            f"border-radius:8px;background-color:{_p('header_bg')};}}")
        self._major_count_lbl.setStyleSheet(f"font-size:10px;color:{_p('muted')};")
        self._major_title_lbl.setStyleSheet(
            f"font-size:13px;font-weight:bold;color:{_p('fg')};")
        self._day_title.setStyleSheet(
            f"font-size:14px;font-weight:bold;color:{_p('fg')};")
        self.mini_month.refresh_styles()
        self._refresh()

    # ── Build UI ────────────────────────────────────

    def _build_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0); root.setSpacing(0)

        # ── Left column ──────────────────────────────
        left = QWidget()
        left_l = QVBoxLayout(left)
        left_l.setContentsMargins(14, 10, 8, 10); left_l.setSpacing(0)

        top_bar = QHBoxLayout(); top_bar.setSpacing(6)
        title = QLabel("Calendar"); title.setObjectName("sectionTitle")
        top_bar.addWidget(title); top_bar.addStretch()

        self._week_label = QLabel()
        self._week_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._week_label.setStyleSheet(
            f"font-size:13px;font-weight:bold;color:{_p('muted')};")
        top_bar.addWidget(self._week_label); top_bar.addSpacing(8)

        for text, tip, slot in [("‹", "Previous week", self._prev_week),
                                 ("›", "Next week",     self._next_week)]:
            if text == "›": top_bar.addWidget(self._today_btn())
            btn = QPushButton(text); btn.setObjectName("secondary")
            btn.setFixedSize(28, 28); btn.setToolTip(tip); btn.clicked.connect(slot)
            top_bar.addWidget(btn)

        top_bar.addSpacing(8)
        btn_add = QPushButton("＋ Event"); btn_add.clicked.connect(self._add_event)
        top_bar.addWidget(btn_add)
        left_l.addLayout(top_bar); left_l.addSpacing(8)

        self._week_container = QWidget()
        self._week_grid = QHBoxLayout(self._week_container)
        self._week_grid.setSpacing(0); self._week_grid.setContentsMargins(0, 0, 0, 0)
        week_scroll = QScrollArea()
        week_scroll.setWidgetResizable(True); week_scroll.setWidget(self._week_container)
        week_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        week_scroll.setMinimumHeight(220); week_scroll.setMaximumHeight(340)
        week_scroll.setFrameShape(QFrame.Shape.NoFrame)
        left_l.addWidget(week_scroll, 3)

        self._left_div = QFrame(); self._left_div.setFrameShape(QFrame.Shape.HLine)
        self._left_div.setStyleSheet(
            f"border:none;border-top:1px solid {_p('border')};margin:8px 0;")
        left_l.addWidget(self._left_div)

        detail_bar = QHBoxLayout()
        self._day_title = QLabel("Today")
        self._day_title.setStyleSheet(f"font-size:14px;font-weight:bold;color:{_p('fg')};")
        detail_bar.addWidget(self._day_title); detail_bar.addStretch()
        btn_add_here = QPushButton("＋"); btn_add_here.setObjectName("secondary")
        btn_add_here.setFixedSize(26, 26); btn_add_here.setToolTip("Add event on this day")
        btn_add_here.clicked.connect(lambda: self._add_event_on_date(self._selected_date))
        detail_bar.addWidget(btn_add_here); left_l.addLayout(detail_bar)
        left_l.addSpacing(4)

        self._day_list_layout = QVBoxLayout(); self._day_list_layout.setSpacing(4)
        day_list_w = QWidget(); day_list_w.setLayout(self._day_list_layout)
        day_scroll = QScrollArea(); day_scroll.setWidgetResizable(True)
        day_scroll.setWidget(day_list_w)
        day_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        day_scroll.setFrameShape(QFrame.Shape.NoFrame)
        left_l.addWidget(day_scroll, 2)
        root.addWidget(left, 1)

        # ── Right sidebar ────────────────────────────
        right = QWidget(); right.setFixedWidth(258)
        right_l = QVBoxLayout(right)
        right_l.setContentsMargins(0, 10, 12, 10); right_l.setSpacing(0)

        self._mini_frame = QFrame(); self._mini_frame.setObjectName("miniMonthFrame")
        self._mini_frame.setStyleSheet(
            f"#miniMonthFrame{{border:1px solid {_p('border')};"
            f"border-radius:8px;background-color:{_p('header_bg')};}}")
        mf_l = QVBoxLayout(self._mini_frame); mf_l.setContentsMargins(0, 0, 0, 0)
        self.mini_month = MiniMonth()
        self.mini_month.date_selected.connect(self._on_mini_date_selected)
        mf_l.addWidget(self.mini_month); right_l.addWidget(self._mini_frame)
        right_l.addSpacing(8)

        action_row = QHBoxLayout(); action_row.setSpacing(4)
        btn_bday = QPushButton("🎂 Birthdays"); btn_bday.setObjectName("secondary")
        btn_bday.clicked.connect(self._manage_birthdays); action_row.addWidget(btn_bday)
        btn_jump = QPushButton("Go to date…"); btn_jump.setObjectName("secondary")
        btn_jump.clicked.connect(self._jump_to_date); action_row.addWidget(btn_jump)
        right_l.addLayout(action_row); right_l.addSpacing(8)

        rdiv1 = QFrame(); rdiv1.setFrameShape(QFrame.Shape.HLine)
        rdiv1.setStyleSheet(f"border:none;border-top:1px solid {_p('border')};")
        right_l.addWidget(rdiv1); right_l.addSpacing(8)

        major_hdr = QHBoxLayout()
        self._major_title_lbl = QLabel("Upcoming Events")
        self._major_title_lbl.setStyleSheet(
            f"font-size:13px;font-weight:bold;color:{_p('fg')};")
        major_hdr.addWidget(self._major_title_lbl); major_hdr.addStretch()
        self._major_count_lbl = QLabel("")
        self._major_count_lbl.setStyleSheet(f"font-size:10px;color:{_p('muted')};")
        major_hdr.addWidget(self._major_count_lbl); right_l.addLayout(major_hdr)
        right_l.addSpacing(6)

        self._major_list_layout = QVBoxLayout(); self._major_list_layout.setSpacing(5)
        major_list_w = QWidget(); major_list_w.setLayout(self._major_list_layout)
        major_scroll = QScrollArea(); major_scroll.setWidgetResizable(True)
        major_scroll.setWidget(major_list_w)
        major_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        major_scroll.setFrameShape(QFrame.Shape.NoFrame)
        right_l.addWidget(major_scroll, 1)
        root.addWidget(right)

    def _today_btn(self) -> QPushButton:
        btn = QPushButton("Today"); btn.setObjectName("secondary")
        btn.setFixedHeight(28); btn.clicked.connect(self._go_today)
        return btn

    # ── Refresh ─────────────────────────────────────

    def _refresh(self):
        self._render_week(); self._render_day_detail()
        self._render_major_events(); self._update_mini_month_events()

    def _get_week_start(self) -> date:
        d = self._selected_date; return d - timedelta(days=d.weekday())

    def _render_week(self):
        _clear_layout(self._week_grid)
        ws = self._get_week_start(); we = ws + timedelta(days=6)
        self._week_label.setText(
            f"{ws.strftime('%b %d')} – {we.strftime('%b %d, %Y')}")

        events = self.store.get_events(ws.isoformat(), we.isoformat() + "T23:59:59")
        ebd: dict[date, list[Event]] = {}
        for ev in events:
            try: d = datetime.fromisoformat(ev.start_time).date()
            except Exception: continue
            ebd.setdefault(d, []).append(ev)
        for ev in self.store.get_all_recurring_events():
            for occ in expand_recurring_to_range(ev, ws, we):
                if ev not in ebd.get(occ, []): ebd.setdefault(occ, []).append(ev)

        bbd: dict[date, list[Birthday]] = {}
        for b in self.store.get_birthdays():
            try: bd = date(ws.year, b.month, b.day)
            except ValueError: continue
            if ws <= bd <= we: bbd.setdefault(bd, []).append(b)

        today = date.today()
        for i in range(7):
            d = ws + timedelta(days=i)
            if i > 0:
                sep = QFrame(); sep.setFrameShape(QFrame.Shape.VLine)
                sep.setStyleSheet(f"border:none;border-left:1px solid {_p('border')};")
                self._week_grid.addWidget(sep)
            col = DayColumn(d, ebd.get(d, []), bbd.get(d, []),
                            is_today=(d == today), is_selected=(d == self._selected_date))
            col.request_add.connect(self._add_event_on_date)
            col.request_edit.connect(self._edit_event)
            self._week_grid.addWidget(col, 1)

    def _render_day_detail(self):
        _clear_layout(self._day_list_layout)
        d = self._selected_date; today = date.today()
        if   d == today:               hdr = f"Today  ·  {d.strftime('%A, %B %d')}"
        elif d == today+timedelta(1):  hdr = f"Tomorrow  ·  {d.strftime('%A, %B %d')}"
        elif d == today-timedelta(1):  hdr = f"Yesterday  ·  {d.strftime('%A, %B %d')}"
        else:                          hdr = d.strftime("%A, %B %d, %Y")
        self._day_title.setText(hdr)

        events = self.store.get_events(d.isoformat(), d.isoformat() + "T23:59:59")
        for ev in self.store.get_all_recurring_events():
            if expand_recurring_to_range(ev, d, d) and ev not in events:
                events.append(ev)

        bday_evs: list[Event] = []
        for b in self.store.get_birthdays():
            if b.month == d.month and b.day == d.day:
                age = (d.year - b.year) if b.year else None
                age_str = f" (turns {age})" if age else ""
                bday_evs.append(Event(
                    id=b.id,
                    title=f"🎂 {b.name} 🎂{age_str}",
                    start_time=datetime(d.year, d.month, d.day).isoformat(),
                    all_day=True, color=_p("red"), category="birthday",
                ))

        all_evs = sorted(bday_evs + events,
                         key=lambda e: (0 if e.all_day else 1, e.start_time))
        if not all_evs:
            lbl = QLabel("No events — double-click a day to add one")
            lbl.setStyleSheet(f"color:{_p('muted')};font-size:12px;padding:8px 0;")
            self._day_list_layout.addWidget(lbl)
        else:
            for ev in all_evs:
                row = DayEventRow(ev)
                if ev.category == "birthday":
                    # Single-click on a birthday row opens the BirthdayDialog by id
                    row.edit_requested.connect(
                        lambda e: self._open_major_event(e.id, True))
                else:
                    row.edit_requested.connect(self._edit_event)
                self._day_list_layout.addWidget(row)
        self._day_list_layout.addStretch()

    def _render_major_events(self):
        _clear_layout(self._major_list_layout)
        majors = self.store.get_next_major_events(date.today(), limit=8)
        if not majors:
            lbl = QLabel("No upcoming major events")
            lbl.setStyleSheet(f"color:{_p('muted')};font-size:12px;padding:8px 0;")
            lbl.setWordWrap(True); self._major_list_layout.addWidget(lbl)
            self._major_count_lbl.setText("")
        else:
            self._major_count_lbl.setText(f"{len(majors)} upcoming")
            for ev_date, title, category, color, item_id, is_birthday in majors:
                card = MajorEventCard(ev_date, title, category, color,
                                      item_id, is_birthday)
                card.clicked.connect(self._open_major_event)
                self._major_list_layout.addWidget(card)
        self._major_list_layout.addStretch()

    def _update_mini_month_events(self):
        vy, vm = self.mini_month._view_year, self.mini_month._view_month
        first = date(vy, vm, 1)
        last  = date(vy + (vm == 12), 1 if vm == 12 else vm + 1, 1) - timedelta(days=1)
        by_date: dict[date, list[str]] = {}
        for ev in self.store.get_events(first.isoformat(), last.isoformat() + "T23:59:59"):
            try: d = datetime.fromisoformat(ev.start_time).date()
            except Exception: continue
            by_date.setdefault(d, []).append(ev.color)
        for ev in self.store.get_all_recurring_events():
            for occ in expand_recurring_to_range(ev, first, last):
                by_date.setdefault(occ, []).append(ev.color)
        for b in self.store.get_birthdays():
            if b.month == vm:
                try:
                    d = date(vy, b.month, b.day)
                    if first <= d <= last: by_date.setdefault(d, []).append(_p("red"))
                except ValueError: pass
        self.mini_month.set_events(by_date)
        try:
            from src.data.holidays_jp import get_japanese_holidays
            hset = {d for d in get_japanese_holidays(vy) if first <= d <= last}
            self.mini_month.set_holidays(hset)
        except Exception: pass

    # ── Navigation ──────────────────────────────────

    def _prev_week(self):
        self._selected_date -= timedelta(weeks=1)
        self.mini_month.set_selected(self._selected_date); self._refresh()

    def _next_week(self):
        self._selected_date += timedelta(weeks=1)
        self.mini_month.set_selected(self._selected_date); self._refresh()

    def _go_today(self):
        self._selected_date = date.today()
        self.mini_month.set_selected(self._selected_date); self._refresh()

    def _on_mini_date_selected(self, d: date):
        self._selected_date = d
        self._update_mini_month_events(); self._render_week(); self._render_day_detail()

    def _jump_to_date(self):
        dlg = QDialog(self); dlg.setWindowTitle("Go to date"); dlg.setModal(True)
        layout = QVBoxLayout(dlg); layout.addWidget(QLabel("Jump to date:"))
        de = QDateEdit(); de.setCalendarPopup(True); de.setDisplayFormat("dd MMM yyyy")
        sd = self._selected_date; de.setDate(QDate(sd.year, sd.month, sd.day))
        layout.addWidget(de)
        br = QHBoxLayout()
        cancel = QPushButton("Cancel"); cancel.setObjectName("secondary"); cancel.clicked.connect(dlg.reject)
        go = QPushButton("Go"); go.setDefault(True); go.clicked.connect(dlg.accept)
        br.addStretch(); br.addWidget(cancel); br.addWidget(go); layout.addLayout(br)
        if dlg.exec():
            qd = de.date(); self._selected_date = date(qd.year(), qd.month(), qd.day())
            self.mini_month.set_selected(self._selected_date); self._refresh()

    # ── Event CRUD ───────────────────────────────────

    def _add_event(self): self._add_event_on_date(self._selected_date)

    def _add_event_on_date(self, d: date):
        dlg = EventDialog(self, prefill_date=d)
        if dlg.exec(): self.store.add_event(**dlg.get_data()); self._refresh()

    def _edit_event(self, event: Event):
        dlg = EventDialog(self, event=event); result = dlg.exec()
        if dlg._delete_requested:
            if QMessageBox.question(
                self, "Delete Event", f'Delete "{event.title}"?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            ) == QMessageBox.StandardButton.Yes:
                self.store.delete_event(event.id); self._refresh()
        elif result:
            data = dlg.get_data()
            event.title       = data["title"];       event.description = data["description"]
            event.start_time  = data["start_time"];  event.end_time    = data["end_time"]
            event.all_day     = data["all_day"];     event.color       = data["color"]
            event.category    = data["category"];    event.recurrence  = data["recurrence"]
            self.store.update_event(event); self._refresh()

    def _open_major_event(self, item_id: str, is_birthday: bool):
        """Dispatcher: open the editor for a MajorEventCard or birthday DayEventRow."""
        if is_birthday:
            birthday = next(
                (b for b in self.store.get_birthdays() if b.id == item_id), None)
            if birthday is None:
                return
            dlg = BirthdayDialog(self, birthday); result = dlg.exec()
            if dlg._delete_requested:
                if QMessageBox.question(
                    self, "Delete Birthday",
                    f"Remove birthday for {birthday.name}?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                ) == QMessageBox.StandardButton.Yes:
                    self.store.delete_birthday(birthday.id); self._refresh()
            elif result:
                data = dlg.get_data()
                birthday.name  = data["name"];  birthday.month = data["month"]
                birthday.day   = data["day"];   birthday.year  = data["year"]
                birthday.note  = data["note"]
                self.store.update_birthday(birthday); self._refresh()
        else:
            event = self.store.get_event(item_id)
            if event:
                self._edit_event(event)

    def _manage_birthdays(self):
        BirthdayManagerDialog(self, self.store).exec(); self._refresh()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  BirthdayManagerDialog
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class BirthdayManagerDialog(QDialog):
    def __init__(self, parent, store: CalendarStore):
        super().__init__(parent); self.store = store
        self.setWindowTitle("Birthday Manager")
        self.setMinimumSize(420, 480); self.setModal(True)
        self._build_ui(); self._load()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16); layout.setSpacing(10)

        hdr = QHBoxLayout()
        title = QLabel("🎂  Birthdays")
        title.setStyleSheet("font-size:15px;font-weight:bold;")
        hdr.addWidget(title); hdr.addStretch()
        add_btn = QPushButton("＋ Add"); add_btn.clicked.connect(self._add_birthday)
        hdr.addWidget(add_btn); layout.addLayout(hdr)

        self._search = QLineEdit(); self._search.setPlaceholderText("Search by name…")
        self._search.textChanged.connect(self._filter); layout.addWidget(self._search)

        self._list_widget = QWidget(); self._list_layout = QVBoxLayout(self._list_widget)
        self._list_layout.setSpacing(4); self._list_layout.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea(); scroll.setWidgetResizable(True)
        scroll.setWidget(self._list_widget); scroll.setFrameShape(QFrame.Shape.NoFrame)
        layout.addWidget(scroll, 1)

        close_btn = QPushButton("Close"); close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, 0, Qt.AlignmentFlag.AlignRight)

    def _load(self):
        self._birthdays = self.store.get_birthdays(); self._filter(self._search.text())

    def _filter(self, text: str):
        _clear_layout(self._list_layout); q = text.lower(); today = date.today()
        filtered = [b for b in self._birthdays if q in b.name.lower()]

        def sk(b):
            try:
                c = date(today.year, b.month, b.day)
                if c < today: c = date(today.year + 1, b.month, b.day)
                return (c - today).days
            except ValueError: return 9999

        filtered.sort(key=sk)
        if not filtered:
            self._list_layout.addWidget(
                QLabel("No birthdays yet — add one!" if not text else "No matches"))
        for b in filtered:
            self._list_layout.addWidget(self._make_row(b))
        self._list_layout.addStretch()

    def _make_row(self, b: Birthday) -> QFrame:
        row = QFrame()
        row.setStyleSheet(
            f"QFrame{{border:1px solid {_p('border')};border-radius:6px;"
            f"background-color:{_p('header_bg')};padding:2px;}}"
            f"QFrame:hover{{border-color:{_p('muted')};"
            f"background-color:{_p('surface')};}}")
        rl = QHBoxLayout(row); rl.setContentsMargins(10, 8, 10, 8); rl.setSpacing(10)

        # Cake badge — fixed-size pill, no more font-size overflow
        cake_badge = QLabel("🎂")
        cake_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cake_badge.setFixedSize(32, 32)
        cake_badge.setStyleSheet(
            f"font-size:18px; background-color:{_p('surface')};"
            f"border:1px solid {_p('border')}; border-radius:16px; padding:0;")
        rl.addWidget(cake_badge)

        info = QVBoxLayout(); info.setSpacing(2)

        # Name row: "🎂 Name 🎂" style label
        name_lbl = QLabel(f"🎂  {b.name}  🎂")
        name_lbl.setStyleSheet(f"font-size:13px;font-weight:bold;color:{_p('fg')};")
        info.addWidget(name_lbl)

        today = date.today()
        try:
            nb = date(today.year, b.month, b.day)
            if nb < today: nb = date(today.year + 1, b.month, b.day)
            suffix = f"  ·  {(nb-today).days}d away" if (nb-today).days > 0 else "  ·  Today! 🎉"
        except ValueError:
            suffix = ""

        months = ["Jan","Feb","Mar","Apr","May","Jun",
                  "Jul","Aug","Sep","Oct","Nov","Dec"]
        ds = f"{months[b.month-1]} {b.day}"
        if b.year: ds += f", {b.year}  (turns {today.year - b.year})"
        ds += suffix

        dl = QLabel(ds); dl.setStyleSheet(f"font-size:11px;color:{_p('muted')};")
        info.addWidget(dl)

        if b.note:
            note_lbl = QLabel(b.note)
            note_lbl.setStyleSheet(
                f"font-size:11px;color:{_p('muted')};font-style:italic;")
            note_lbl.setWordWrap(True)
            info.addWidget(note_lbl)

        rl.addLayout(info, 1)

        edit_btn = QPushButton("Edit"); edit_btn.setObjectName("secondary")
        edit_btn.setFixedHeight(28)
        edit_btn.clicked.connect(lambda _, bd=b: self._edit_birthday(bd))
        rl.addWidget(edit_btn)
        return row

    def _add_birthday(self):
        dlg = BirthdayDialog(self)
        if dlg.exec(): self.store.add_birthday(**dlg.get_data()); self._load()

    def _edit_birthday(self, birthday: Birthday):
        dlg = BirthdayDialog(self, birthday); result = dlg.exec()
        if dlg._delete_requested:
            if QMessageBox.question(
                self, "Delete Birthday",
                f"Remove birthday for {birthday.name}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            ) == QMessageBox.StandardButton.Yes:
                self.store.delete_birthday(birthday.id); self._load()
        elif result:
            data = dlg.get_data()
            birthday.name  = data["name"];  birthday.month = data["month"]
            birthday.day   = data["day"];   birthday.year  = data["year"]
            birthday.note  = data["note"]
            self.store.update_birthday(birthday); self._load()
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
"""Earnings Tracker module UI — freelance income tracking with summaries.

Features:
- Quick-log preset jobs with one click (job pay, does not count toward goals)
- Manual earning / expense entry with USD or JPY currency selection
- Live USD→JPY exchange rate via open.er-api.com with offline fallback
- Dual-currency display throughout (USD + ¥JPY)
- Month's Goal section: Base Goal + Extra Goal progress bars
  (only additional income, not job pay, counts toward goals)
- Quick date-range buttons (This Month / Last Month / This Year / All Time)
- Period summary panel with category bars
"""

import threading
import urllib.request
import urllib.error
import json
from datetime import date, timedelta

from PyQt6.QtCore import Qt, QDate, QTimer, pyqtSignal, QObject
from PyQt6.QtGui import QColor, QBrush, QPainter, QPen, QFont
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QLabel, QPushButton, QDialog, QLineEdit, QComboBox,
    QDateEdit, QDoubleSpinBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QFrame, QMessageBox, QScrollArea, QSpinBox,
    QFormLayout, QSizePolicy, QAbstractItemView,
)

from src.config import load_config, save_config
from src.data.finance_store import FinanceStore, Transaction, JobPreset, DEFAULT_CATEGORIES

# ── Default fallback exchange rate ────────────────────────────────────────────
_FALLBACK_RATE = 150.0


# ── Exchange Rate Manager ─────────────────────────────────────────────────────

class RateSignals(QObject):
    updated = pyqtSignal(float)
    error = pyqtSignal(str)


class ExchangeRateManager:
    """Fetches USD→JPY rate in a background thread. Thread-safe."""

    _API_URL = "https://open.er-api.com/v6/latest/USD"

    def __init__(self):
        self.signals = RateSignals()
        self._rate: float = _FALLBACK_RATE
        self._fetching = False

    @property
    def rate(self) -> float:
        return self._rate

    def set_fallback(self, rate: float):
        self._rate = max(rate, 1.0)

    def refresh(self):
        if self._fetching:
            return
        self._fetching = True

        def _fetch():
            try:
                req = urllib.request.Request(
                    self._API_URL,
                    headers={"User-Agent": "LocalSync/1.0"},
                )
                with urllib.request.urlopen(req, timeout=8) as resp:
                    data = json.loads(resp.read().decode())
                rate = float(data["rates"]["JPY"])
                self._rate = rate
                self.signals.updated.emit(rate)
            except Exception as e:
                self.signals.error.emit(str(e))
            finally:
                self._fetching = False

        threading.Thread(target=_fetch, daemon=True).start()


# Module-level singleton so the panel and dialogs share one rate
_rate_mgr = ExchangeRateManager()


# ── Goal Progress Bar ─────────────────────────────────────────────────────────

class GoalProgressBar(QWidget):
    """Paints a two-tier progress bar: base goal and extra goal."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(36)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self._current = 0.0
        self._base = 1000.0
        self._extra = 2000.0
        self._green = "#a6e3a1"
        self._gold = "#f9e2af"
        self._accent = "#4a9eff"

    def set_values(self, current: float, base: float, extra: float,
                   green: str = "#a6e3a1", gold: str = "#f9e2af",
                   accent: str = "#4a9eff"):
        self._current = max(current, 0.0)
        self._base = max(base, 1.0)
        self._extra = max(extra, self._base + 1.0)
        self._green = green
        self._gold = gold
        self._accent = accent
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        bar_h = 18
        bar_y = (self.height() - bar_h) // 2

        cap = self._extra * 1.05   # a little breathing room past extra goal
        fill_ratio = min(self._current / cap, 1.0)
        base_ratio = self._base / cap
        extra_ratio = self._extra / cap

        # Background track
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor("#313244")))
        painter.drawRoundedRect(0, bar_y, w, bar_h, bar_h // 2, bar_h // 2)

        # Filled portion — colour shifts from accent → green (base) → gold (extra)
        fill_w = int(w * fill_ratio)
        if fill_w > 0:
            if self._current >= self._extra:
                fill_color = QColor(self._gold)
            elif self._current >= self._base:
                fill_color = QColor(self._green)
            else:
                fill_color = QColor(self._accent)
            painter.setBrush(QBrush(fill_color))
            painter.drawRoundedRect(0, bar_y, fill_w, bar_h, bar_h // 2, bar_h // 2)

        # Base goal marker
        base_x = int(w * base_ratio)
        pen = QPen(QColor("#cdd6f4"), 2)
        painter.setPen(pen)
        painter.drawLine(base_x, bar_y - 3, base_x, bar_y + bar_h + 3)

        # Extra goal marker
        extra_x = int(w * extra_ratio)
        pen.setColor(QColor(self._gold))
        painter.setPen(pen)
        painter.drawLine(extra_x, bar_y - 3, extra_x, bar_y + bar_h + 3)

        painter.end()


# ── Category Bar ──────────────────────────────────────────────────────────────

class CategoryBar(QWidget):

    def __init__(self, label: str, amount_usd: float, max_amount: float,
                 rate: float, bar_color: str = "#4a9eff", parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 2, 0, 2)
        layout.setSpacing(8)

        name_label = QLabel(label)
        name_label.setFixedWidth(110)
        layout.addWidget(name_label)

        bar_frame = QFrame()
        width_pct = (amount_usd / max_amount * 100) if max_amount > 0 else 0
        bar_frame.setStyleSheet(
            f"background-color: {bar_color}; border-radius: 3px; min-height: 14px;"
        )
        bar_frame.setFixedWidth(max(int(width_pct * 1.5), 4))
        layout.addWidget(bar_frame)

        jpy = int(amount_usd * rate)
        amt_label = QLabel(f"${amount_usd:,.0f}  ¥{jpy:,}")
        amt_label.setObjectName("subtitle")
        amt_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        amt_label.setFixedWidth(140)
        layout.addWidget(amt_label)

        layout.addStretch()


# ── Preset Manager Dialog ─────────────────────────────────────────────────────

class PresetManagerDialog(QDialog):
    """Add / edit / delete job presets."""

    def __init__(self, store: FinanceStore, parent=None):
        super().__init__(parent)
        self.store = store
        self.setWindowTitle("Manage Job Presets")
        self.setMinimumSize(460, 360)
        self._build_ui()
        self._refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # List
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Name", "Amount (USD)", "Category"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)

        # Add row
        add_frame = QFrame()
        add_frame.setObjectName("separator")
        add_frame.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(add_frame)

        form = QFormLayout()
        form.setSpacing(6)
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("e.g. Submission")
        form.addRow("Name:", self.name_edit)

        self.amount_spin = QDoubleSpinBox()
        self.amount_spin.setRange(0.01, 999999.99)
        self.amount_spin.setDecimals(2)
        self.amount_spin.setPrefix("$ ")
        self.amount_spin.setValue(300.00)
        form.addRow("Amount (USD):", self.amount_spin)

        self.cat_combo = QComboBox()
        self.cat_combo.addItems(DEFAULT_CATEGORIES)
        self.cat_combo.setCurrentText("Contract")
        self.cat_combo.setEditable(True)
        form.addRow("Category:", self.cat_combo)

        layout.addLayout(form)

        btn_row = QHBoxLayout()
        add_btn = QPushButton("Add Preset")
        add_btn.clicked.connect(self._add_preset)
        btn_row.addWidget(add_btn)

        edit_btn = QPushButton("Edit Selected")
        edit_btn.setObjectName("secondary")
        edit_btn.clicked.connect(self._edit_selected)
        btn_row.addWidget(edit_btn)

        del_btn = QPushButton("Delete Selected")
        del_btn.setObjectName("destructive")
        del_btn.clicked.connect(self._delete_selected)
        btn_row.addWidget(del_btn)

        btn_row.addStretch()
        close_btn = QPushButton("Close")
        close_btn.setObjectName("secondary")
        close_btn.clicked.connect(self.accept)
        btn_row.addWidget(close_btn)
        layout.addLayout(btn_row)

        self._preset_ids: list[str] = []

    def _refresh(self):
        presets = self.store.get_presets()
        self._preset_ids = [p.id for p in presets]
        self.table.setRowCount(len(presets))
        for i, p in enumerate(presets):
            self.table.setItem(i, 0, QTableWidgetItem(p.name))
            self.table.setItem(i, 1, QTableWidgetItem(f"${p.amount_usd:,.2f}"))
            self.table.setItem(i, 2, QTableWidgetItem(p.category))

    def _add_preset(self):
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Missing Name", "Please enter a preset name.")
            return
        self.store.add_preset(
            name=name,
            amount_usd=self.amount_spin.value(),
            category=self.cat_combo.currentText(),
        )
        self.name_edit.clear()
        self._refresh()

    def _edit_selected(self):
        rows = self.table.selectionModel().selectedRows()
        if not rows:
            return
        idx = rows[0].row()
        if idx >= len(self._preset_ids):
            return
        presets = self.store.get_presets()
        preset = next((p for p in presets if p.id == self._preset_ids[idx]), None)
        if not preset:
            return
        self.name_edit.setText(preset.name)
        self.amount_spin.setValue(preset.amount_usd)
        self.cat_combo.setCurrentText(preset.category)
        # Remove old and add updated
        self.store.delete_preset(preset.id)
        self._refresh()

    def _delete_selected(self):
        rows = self.table.selectionModel().selectedRows()
        if not rows:
            return
        reply = QMessageBox.question(
            self, "Delete Preset", "Delete selected preset(s)?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            for r in rows:
                if r.row() < len(self._preset_ids):
                    self.store.delete_preset(self._preset_ids[r.row()])
            self._refresh()


# ── Goal Settings Dialog ──────────────────────────────────────────────────────

class GoalSettingsDialog(QDialog):
    """Set base and extra monthly income goals (USD)."""

    def __init__(self, base: float, extra: float, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Set Monthly Goals")
        self.setMinimumWidth(320)
        self._build_ui(base, extra)

    def _build_ui(self, base: float, extra: float):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        info = QLabel(
            "Goals track additional income only.\n"
            "Job Pay (preset completions) does not count."
        )
        info.setObjectName("subtitle")
        info.setWordWrap(True)
        layout.addWidget(info)

        form = QFormLayout()
        form.setSpacing(8)

        self.base_spin = QDoubleSpinBox()
        self.base_spin.setRange(1.0, 9999999.0)
        self.base_spin.setDecimals(0)
        self.base_spin.setPrefix("$ ")
        self.base_spin.setSingleStep(100)
        self.base_spin.setValue(base)
        form.addRow("Base Goal (USD):", self.base_spin)

        self.extra_spin = QDoubleSpinBox()
        self.extra_spin.setRange(1.0, 9999999.0)
        self.extra_spin.setDecimals(0)
        self.extra_spin.setPrefix("$ ")
        self.extra_spin.setSingleStep(100)
        self.extra_spin.setValue(extra)
        form.addRow("Extra Goal (USD):", self.extra_spin)

        layout.addLayout(form)

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
        save_btn.clicked.connect(self._validate_and_accept)
        btn_row.addWidget(save_btn)
        layout.addLayout(btn_row)

    def _validate_and_accept(self):
        if self.extra_spin.value() <= self.base_spin.value():
            QMessageBox.warning(
                self, "Invalid Goals",
                "Extra goal must be greater than base goal.",
            )
            return
        self.accept()

    def get_goals(self) -> tuple[float, float]:
        return self.base_spin.value(), self.extra_spin.value()


# ── Transaction Dialog ────────────────────────────────────────────────────────

class TransactionDialog(QDialog):
    """Dialog to add/edit a transaction (earning or expense)."""

    def __init__(self, parent=None, txn: Transaction | None = None):
        super().__init__(parent)
        self.setWindowTitle("Edit Entry" if txn else "New Entry")
        self.setMinimumWidth(400)
        self.txn = txn
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        form = QFormLayout()
        form.setSpacing(8)

        # Type
        self.type_combo = QComboBox()
        self.type_combo.addItems(["income", "expense"])
        if self.txn:
            self.type_combo.setCurrentText(self.txn.type)
        self.type_combo.currentTextChanged.connect(self._on_type_changed)
        form.addRow("Type:", self.type_combo)

        # Currency
        self.currency_combo = QComboBox()
        self.currency_combo.addItems(["USD", "JPY"])
        if self.txn:
            self.currency_combo.setCurrentText(self.txn.currency)
        self.currency_combo.currentTextChanged.connect(self._on_currency_changed)
        form.addRow("Currency:", self.currency_combo)

        # Amount
        self.amount_spin = QDoubleSpinBox()
        self.amount_spin.setRange(0.01, 99999999.99)
        self.amount_spin.setDecimals(2)
        if self.txn:
            self.amount_spin.setValue(self.txn.amount)
        form.addRow("Amount:", self.amount_spin)

        # Date
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        if self.txn:
            parts = self.txn.date.split("-")
            self.date_edit.setDate(QDate(int(parts[0]), int(parts[1]), int(parts[2])))
        else:
            today = date.today()
            self.date_edit.setDate(QDate(today.year, today.month, today.day))
        form.addRow("Date:", self.date_edit)

        # Category
        self.cat_label = QLabel("Source")
        self.cat_combo = QComboBox()
        self.cat_combo.addItems(DEFAULT_CATEGORIES)
        self.cat_combo.setEditable(True)
        if self.txn:
            self.cat_combo.setCurrentText(self.txn.category)
        form.addRow(self.cat_label, self.cat_combo)

        # Description
        self.desc_edit = QLineEdit()
        self.desc_edit.setPlaceholderText("Client name, project, invoice #...")
        if self.txn:
            self.desc_edit.setText(self.txn.description)
        form.addRow("Description:", self.desc_edit)

        # Rate hint
        self.rate_hint = QLabel("")
        self.rate_hint.setObjectName("subtitle")
        form.addRow("", self.rate_hint)

        layout.addLayout(form)

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
        self._on_currency_changed(self.currency_combo.currentText())

    def _on_type_changed(self, txn_type: str):
        self.cat_label.setText("Source" if txn_type == "income" else "Category")

    def _on_currency_changed(self, currency: str):
        rate = _rate_mgr.rate
        if currency == "JPY":
            self.amount_spin.setPrefix("¥ ")
            self.amount_spin.setDecimals(0)
            self.amount_spin.setSingleStep(1000)
            self.rate_hint.setText(f"Rate: 1 USD = ¥{rate:,.0f}")
        else:
            self.amount_spin.setPrefix("$ ")
            self.amount_spin.setDecimals(2)
            self.amount_spin.setSingleStep(10)
            self.rate_hint.setText(f"Rate: ¥{rate:,.0f} = 1 USD")

    def get_data(self) -> dict:
        qd = self.date_edit.date()
        return {
            "date": f"{qd.year():04d}-{qd.month():02d}-{qd.day():02d}",
            "amount": self.amount_spin.value(),
            "txn_type": self.type_combo.currentText(),
            "category": self.cat_combo.currentText(),
            "description": self.desc_edit.text(),
            "currency": self.currency_combo.currentText(),
            "is_job_pay": False,
        }


# ── Quick Log Button ──────────────────────────────────────────────────────────

class PresetButton(QWidget):
    """A card-style button for one-click job logging."""

    clicked = pyqtSignal(object)  # emits JobPreset

    def __init__(self, preset: JobPreset, rate: float, parent=None):
        super().__init__(parent)
        self.preset = preset
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(2)

        name_lbl = QLabel(preset.name)
        name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_lbl.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(name_lbl)

        jpy = int(preset.amount_usd * rate)
        amt_lbl = QLabel(f"${preset.amount_usd:,.0f}  ¥{jpy:,}")
        amt_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        amt_lbl.setObjectName("subtitle")
        layout.addWidget(amt_lbl)

        log_btn = QPushButton("+ Log")
        log_btn.setFixedHeight(26)
        log_btn.clicked.connect(lambda: self.clicked.emit(self.preset))
        layout.addWidget(log_btn)

        self.setStyleSheet(
            "PresetButton { border: 1px solid #45475a; border-radius: 6px;"
            " background-color: #1e1e2e; }"
            "PresetButton:hover { background-color: #313244; }"
        )
        self.setFixedWidth(150)


# ── Main Finance Panel ────────────────────────────────────────────────────────

class FinancePanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.store = FinanceStore()
        self._palette: dict = {}
        self._cfg = load_config()
        self._txn_ids: list[str] = []

        # Load fallback rate from config
        fallback = float(self._cfg.get("usd_jpy_fallback_rate", _FALLBACK_RATE))
        _rate_mgr.set_fallback(fallback)
        _rate_mgr.signals.updated.connect(self._on_rate_updated)
        _rate_mgr.signals.error.connect(self._on_rate_error)

        self._build_ui()
        self._refresh()

        # Fetch rate on startup (non-blocking)
        _rate_mgr.refresh()

    def set_palette(self, palette: dict):
        self._palette = palette
        self._refresh()

    # ── UI Construction ───────────────────────────────────────────────────────

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)

        layout.addLayout(self._build_header())
        layout.addWidget(self._build_quick_log_bar())
        layout.addLayout(self._build_filter_row())
        layout.addWidget(self._build_goal_section())

        # Main content: table + summary
        content = QSplitter(Qt.Orientation.Horizontal)
        content.addWidget(self._build_table())
        content.addWidget(self._build_summary_panel())
        content.setSizes([560, 300])
        layout.addWidget(content, 1)

        layout.addWidget(self._build_rate_bar())

    def _build_header(self) -> QHBoxLayout:
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

        # All-time badge (stacked USD + JPY)
        badge_col = QVBoxLayout()
        badge_col.setSpacing(0)
        self.all_time_usd_label = QLabel("$0")
        self.all_time_usd_label.setStyleSheet(
            "font-size: 26px; font-weight: bold; padding: 2px 12px 0 12px;"
        )
        self.all_time_usd_label.setToolTip("Total earned all-time (USD)")
        badge_col.addWidget(self.all_time_usd_label)
        self.all_time_jpy_label = QLabel("¥0")
        self.all_time_jpy_label.setStyleSheet(
            "font-size: 13px; padding: 0 12px 2px 12px;"
        )
        self.all_time_jpy_label.setObjectName("subtitle")
        badge_col.addWidget(self.all_time_jpy_label)
        header.addLayout(badge_col)

        caption = QLabel("earned\nall-time")
        caption.setObjectName("subtitle")
        caption.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        header.addWidget(caption)

        header.addSpacing(16)

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
        btn_delete.setToolTip("Delete selected row(s)")
        btn_delete.clicked.connect(self._delete_transaction)
        header.addWidget(btn_delete)

        return header

    def _build_quick_log_bar(self) -> QWidget:
        container = QWidget()
        outer = QVBoxLayout(container)
        outer.setContentsMargins(0, 4, 0, 4)
        outer.setSpacing(4)

        title_row = QHBoxLayout()
        lbl = QLabel("Quick Log — Job Pay")
        lbl.setStyleSheet("font-weight: bold; font-size: 12px;")
        title_row.addWidget(lbl)
        title_row.addStretch()
        manage_btn = QPushButton("⚙ Manage Presets")
        manage_btn.setObjectName("secondary")
        manage_btn.setFixedHeight(22)
        manage_btn.clicked.connect(self._open_preset_manager)
        title_row.addWidget(manage_btn)
        outer.addLayout(title_row)

        # Scrollable row of preset buttons
        self._preset_scroll = QScrollArea()
        self._preset_scroll.setWidgetResizable(True)
        self._preset_scroll.setFixedHeight(100)
        self._preset_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self._preset_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self._preset_row_widget = QWidget()
        self._preset_row_layout = QHBoxLayout(self._preset_row_widget)
        self._preset_row_layout.setContentsMargins(4, 4, 4, 4)
        self._preset_row_layout.setSpacing(8)
        self._preset_row_layout.addStretch()

        self._preset_scroll.setWidget(self._preset_row_widget)
        outer.addWidget(self._preset_scroll)

        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine)
        outer.addWidget(sep)

        return container

    def _build_filter_row(self) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setSpacing(6)

        # Quick range buttons
        for label, fn in [
            ("This Month", self._filter_this_month),
            ("Last Month", self._filter_last_month),
            ("This Year", self._filter_this_year),
            ("All Time", self._filter_all_time),
        ]:
            btn = QPushButton(label)
            btn.setObjectName("secondary")
            btn.setFixedHeight(26)
            btn.clicked.connect(fn)
            row.addWidget(btn)

        row.addSpacing(12)
        row.addWidget(QLabel("Show:"))
        self.filter_type = QComboBox()
        self.filter_type.addItems(["All", "income", "expense"])
        self.filter_type.currentTextChanged.connect(self._refresh)
        row.addWidget(self.filter_type)

        row.addSpacing(8)
        row.addWidget(QLabel("From:"))
        self.filter_start = QDateEdit()
        self.filter_start.setCalendarPopup(True)
        today = date.today()
        self.filter_start.setDate(QDate(today.year, today.month, 1))
        self.filter_start.dateChanged.connect(self._refresh)
        row.addWidget(self.filter_start)

        row.addWidget(QLabel("To:"))
        self.filter_end = QDateEdit()
        self.filter_end.setCalendarPopup(True)
        self.filter_end.setDate(QDate(today.year, today.month, today.day))
        self.filter_end.dateChanged.connect(self._refresh)
        row.addWidget(self.filter_end)

        row.addStretch()
        return row

    def _build_goal_section(self) -> QWidget:
        container = QFrame()
        container.setObjectName("separator")
        container.setFrameShape(QFrame.Shape.NoFrame)
        container.setStyleSheet("background-color: #1e1e2e; border-radius: 8px; padding: 4px;")

        vbox = QVBoxLayout(container)
        vbox.setContentsMargins(12, 8, 12, 8)
        vbox.setSpacing(6)

        title_row = QHBoxLayout()
        goal_title = QLabel("Month's Goal  —  Additional Income")
        goal_title.setStyleSheet("font-weight: bold; font-size: 13px;")
        title_row.addWidget(goal_title)
        title_row.addStretch()

        self.goal_status_label = QLabel("")
        self.goal_status_label.setObjectName("subtitle")
        title_row.addWidget(self.goal_status_label)

        set_btn = QPushButton("⚙ Set Goals")
        set_btn.setObjectName("secondary")
        set_btn.setFixedHeight(24)
        set_btn.clicked.connect(self._open_goal_settings)
        title_row.addWidget(set_btn)
        vbox.addLayout(title_row)

        self.goal_bar = GoalProgressBar()
        vbox.addWidget(self.goal_bar)

        legend_row = QHBoxLayout()
        self.goal_base_label = QLabel("Base: $0")
        self.goal_base_label.setObjectName("subtitle")
        legend_row.addWidget(self.goal_base_label)
        legend_row.addSpacing(16)
        self.goal_extra_label = QLabel("Extra: $0")
        self.goal_extra_label.setObjectName("subtitle")
        legend_row.addWidget(self.goal_extra_label)
        legend_row.addStretch()
        self.goal_current_label = QLabel("Progress: $0")
        self.goal_current_label.setObjectName("subtitle")
        legend_row.addWidget(self.goal_current_label)
        vbox.addLayout(legend_row)

        return container

    def _build_table(self) -> QWidget:
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["Date", "Type", "Source", "Amount", "¥ Amount", "Description"]
        )
        hh = self.table.horizontalHeader()
        hh.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        hh.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.doubleClicked.connect(self._edit_transaction)
        return self.table

    def _build_summary_panel(self) -> QWidget:
        summary_widget = QWidget()
        self.summary_layout = QVBoxLayout(summary_widget)
        self.summary_layout.setContentsMargins(16, 12, 16, 12)
        self.summary_layout.setSpacing(8)

        period_title = QLabel("Period Summary")
        period_title.setObjectName("sectionTitle")
        self.summary_layout.addWidget(period_title)

        self.earned_usd_label = QLabel("Earned: $0")
        self.earned_usd_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.summary_layout.addWidget(self.earned_usd_label)

        self.earned_jpy_label = QLabel("¥0")
        self.earned_jpy_label.setObjectName("subtitle")
        self.earned_jpy_label.setStyleSheet("font-size: 13px; padding-left: 2px;")
        self.summary_layout.addWidget(self.earned_jpy_label)

        self.spent_label = QLabel("Spent: $0")
        self.spent_label.setStyleSheet("font-size: 15px; font-weight: bold;")
        self.summary_layout.addWidget(self.spent_label)

        sep = QFrame()
        sep.setObjectName("separator")
        sep.setFrameShape(QFrame.Shape.HLine)
        self.summary_layout.addWidget(sep)

        self.net_label = QLabel("Net: $0")
        self.net_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.summary_layout.addWidget(self.net_label)

        self.net_jpy_label = QLabel("¥0")
        self.net_jpy_label.setObjectName("subtitle")
        self.summary_layout.addWidget(self.net_jpy_label)

        self.txn_count_label = QLabel("0 transactions")
        self.txn_count_label.setObjectName("subtitle")
        self.summary_layout.addWidget(self.txn_count_label)

        sep2 = QFrame()
        sep2.setObjectName("separator")
        sep2.setFrameShape(QFrame.Shape.HLine)
        self.summary_layout.addWidget(sep2)

        cat_title = QLabel("By Source / Category")
        cat_title.setStyleSheet("font-weight: bold; font-size: 13px;")
        self.summary_layout.addWidget(cat_title)

        self.cat_bars_container = QWidget()
        self.cat_bars_layout = QVBoxLayout(self.cat_bars_container)
        self.cat_bars_layout.setContentsMargins(0, 0, 0, 0)
        self.cat_bars_layout.setSpacing(2)
        self.summary_layout.addWidget(self.cat_bars_container)

        self.summary_layout.addStretch()
        return summary_widget

    def _build_rate_bar(self) -> QWidget:
        bar = QFrame()
        bar.setFrameShape(QFrame.Shape.NoFrame)
        row = QHBoxLayout(bar)
        row.setContentsMargins(0, 2, 0, 2)
        row.setSpacing(8)

        self.rate_label = QLabel(f"USD → JPY: ¥{_rate_mgr.rate:,.0f}  (fallback)")
        self.rate_label.setObjectName("subtitle")
        row.addWidget(self.rate_label)

        refresh_btn = QPushButton("↻ Refresh Rate")
        refresh_btn.setObjectName("secondary")
        refresh_btn.setFixedHeight(22)
        refresh_btn.clicked.connect(self._refresh_rate)
        row.addWidget(refresh_btn)

        row.addStretch()
        return bar

    # ── Quick date range helpers ───────────────────────────────────────────────

    def _set_date_range(self, start: date, end: date):
        # Block signals while setting both to avoid double-refresh
        self.filter_start.blockSignals(True)
        self.filter_end.blockSignals(True)
        self.filter_start.setDate(QDate(start.year, start.month, start.day))
        self.filter_end.setDate(QDate(end.year, end.month, end.day))
        self.filter_start.blockSignals(False)
        self.filter_end.blockSignals(False)
        self._refresh()

    def _filter_this_month(self):
        today = date.today()
        self._set_date_range(today.replace(day=1), today)

    def _filter_last_month(self):
        today = date.today()
        first_this = today.replace(day=1)
        last_prev = first_this - timedelta(days=1)
        self._set_date_range(last_prev.replace(day=1), last_prev)

    def _filter_this_year(self):
        today = date.today()
        self._set_date_range(today.replace(month=1, day=1), today)

    def _filter_all_time(self):
        self._set_date_range(date(2000, 1, 1), date.today())

    # ── Rate helpers ──────────────────────────────────────────────────────────

    def _refresh_rate(self):
        self.rate_label.setText("Fetching rate…")
        _rate_mgr.refresh()

    def _on_rate_updated(self, rate: float):
        # Save as new fallback
        self._cfg["usd_jpy_fallback_rate"] = rate
        save_config(self._cfg)
        self.rate_label.setText(f"USD → JPY: ¥{rate:,.2f}  (live)")
        self._refresh()

    def _on_rate_error(self, msg: str):
        rate = _rate_mgr.rate
        self.rate_label.setText(f"USD → JPY: ¥{rate:,.0f}  (offline – {msg[:40]})")

    # ── Preset helpers ────────────────────────────────────────────────────────

    def _rebuild_preset_buttons(self):
        """Clear and repopulate the Quick Log button row."""
        # Remove all except the trailing stretch
        while self._preset_row_layout.count() > 1:
            item = self._preset_row_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        presets = self.store.get_presets()
        rate = _rate_mgr.rate
        for preset in presets:
            btn = PresetButton(preset, rate)
            btn.clicked.connect(self._log_preset)
            self._preset_row_layout.insertWidget(
                self._preset_row_layout.count() - 1, btn
            )

        if not presets:
            placeholder = QLabel("No presets yet — click ⚙ Manage Presets to add one.")
            placeholder.setObjectName("subtitle")
            self._preset_row_layout.insertWidget(0, placeholder)

    def _log_preset(self, preset: JobPreset):
        today_str = date.today().isoformat()
        self.store.log_preset(preset, count=1, on_date=today_str)
        self._refresh()

    def _open_preset_manager(self):
        dlg = PresetManagerDialog(self.store, self)
        dlg.exec()
        self._rebuild_preset_buttons()
        self._refresh()

    # ── Goal helpers ──────────────────────────────────────────────────────────

    def _open_goal_settings(self):
        base = float(self._cfg.get("monthly_base_goal", 500.0))
        extra = float(self._cfg.get("monthly_extra_goal", 1000.0))
        dlg = GoalSettingsDialog(base, extra, self)
        if dlg.exec():
            new_base, new_extra = dlg.get_goals()
            self._cfg["monthly_base_goal"] = new_base
            self._cfg["monthly_extra_goal"] = new_extra
            save_config(self._cfg)
            self._refresh()

    def _update_goal_section(self):
        base = float(self._cfg.get("monthly_base_goal", 500.0))
        extra = float(self._cfg.get("monthly_extra_goal", 1000.0))
        rate = _rate_mgr.rate
        green = self._palette.get("green", "#a6e3a1")
        gold = "#f9e2af"
        accent = self._palette.get("accent", "#4a9eff")

        today = date.today()
        month_start = today.replace(day=1).isoformat()
        month_end = today.isoformat()
        current = self.store.get_goal_income(month_start, month_end, rate)

        self.goal_bar.set_values(current, base, extra, green, gold, accent)

        jpy_base = int(base * rate)
        jpy_extra = int(extra * rate)
        self.goal_base_label.setText(f"● Base: ${base:,.0f}  ¥{jpy_base:,}")
        self.goal_extra_label.setText(f"★ Extra: ${extra:,.0f}  ¥{jpy_extra:,}")

        jpy_current = int(current * rate)
        self.goal_current_label.setText(
            f"Progress: ${current:,.0f}  ¥{jpy_current:,}"
        )

        if current >= extra:
            self.goal_status_label.setText("★ Extra goal reached!")
            self.goal_status_label.setStyleSheet(f"color: {gold}; font-weight: bold;")
        elif current >= base:
            self.goal_status_label.setText("✓ Base goal reached!")
            self.goal_status_label.setStyleSheet(f"color: {green}; font-weight: bold;")
        else:
            remaining = base - current
            pct = int(current / base * 100) if base > 0 else 0
            self.goal_status_label.setText(
                f"{pct}% — ${remaining:,.0f} to base goal"
            )
            self.goal_status_label.setStyleSheet(f"color: {accent};")

    # ── Main refresh ──────────────────────────────────────────────────────────

    def _get_filters(self) -> tuple[str, str, str | None]:
        qs = self.filter_start.date()
        qe = self.filter_end.date()
        start = f"{qs.year():04d}-{qs.month():02d}-{qs.day():02d}"
        end = f"{qe.year():04d}-{qe.month():02d}-{qe.day():02d}"
        txn_type = self.filter_type.currentText()
        if txn_type == "All":
            txn_type = None
        return start, end, txn_type

    def _refresh(self):
        self._cfg = load_config()
        rate = _rate_mgr.rate
        start, end, txn_type = self._get_filters()
        txns = self.store.get_transactions(start, end, txn_type)

        green = self._palette.get("green", "#a6e3a1")
        red = self._palette.get("red", "#f38ba8")
        accent = self._palette.get("accent", "#4a9eff")
        gold = "#f9e2af"

        # ── All-time badge ────────────────────────────────────────────────────
        all_time_usd = self.store.get_all_time_earned_usd(rate)
        all_time_jpy = int(all_time_usd * rate)
        self.all_time_usd_label.setText(f"${all_time_usd:,.0f}")
        self.all_time_usd_label.setStyleSheet(
            f"color: {green}; font-size: 26px; font-weight: bold;"
            " padding: 2px 12px 0 12px;"
        )
        self.all_time_jpy_label.setText(f"¥{all_time_jpy:,}")

        # ── Table ─────────────────────────────────────────────────────────────
        self.table.setRowCount(len(txns))
        self._txn_ids = []
        for row_idx, txn in enumerate(txns):
            self._txn_ids.append(txn.id)

            self.table.setItem(row_idx, 0, QTableWidgetItem(txn.date))

            type_text = "Earned" if txn.type == "income" else "Spent"
            if txn.is_job_pay:
                type_text = "Job Pay"
            type_item = QTableWidgetItem(type_text)
            color = QColor(green if txn.type == "income" else red)
            if txn.is_job_pay:
                color = QColor(gold)
            type_item.setForeground(QBrush(color))
            self.table.setItem(row_idx, 1, type_item)

            self.table.setItem(row_idx, 2, QTableWidgetItem(txn.category))

            # USD amount column
            prefix = "+" if txn.type == "income" else "-"
            curr_sym = "¥" if txn.currency == "JPY" else "$"
            if txn.currency == "JPY":
                amt_str = f"{prefix}{curr_sym}{int(txn.amount):,}"
            else:
                amt_str = f"{prefix}{curr_sym}{txn.amount:,.2f}"
            amt_item = QTableWidgetItem(amt_str)
            amt_item.setForeground(QBrush(color))
            amt_item.setTextAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )
            self.table.setItem(row_idx, 3, amt_item)

            # JPY column
            if txn.currency == "JPY":
                jpy_val = int(txn.amount)
            else:
                jpy_val = int(txn.amount * rate)
            jpy_item = QTableWidgetItem(f"{prefix}¥{jpy_val:,}")
            jpy_item.setForeground(QBrush(color))
            jpy_item.setTextAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )
            self.table.setItem(row_idx, 4, jpy_item)

            self.table.setItem(row_idx, 5, QTableWidgetItem(txn.description))

        # ── Summary panel ─────────────────────────────────────────────────────
        summary = self.store.get_summary(start, end)
        earned_usd = summary["earned"]
        spent_usd = summary["spent"]
        net_usd = summary["net"]

        earned_jpy = int(earned_usd * rate)
        spent_jpy = int(spent_usd * rate)
        net_jpy = int(net_usd * rate)

        self.earned_usd_label.setText(f"Earned: ${earned_usd:,.2f}")
        self.earned_usd_label.setStyleSheet(
            f"color: {green}; font-size: 18px; font-weight: bold;"
        )
        self.earned_jpy_label.setText(f"¥{earned_jpy:,}")

        self.spent_label.setText(f"Spent: ${spent_usd:,.2f}")
        self.spent_label.setStyleSheet(
            f"color: {red}; font-size: 15px; font-weight: bold;"
        )

        net_color = green if net_usd >= 0 else red
        sign = "+" if net_usd >= 0 else ""
        self.net_label.setText(f"Net: {sign}${net_usd:,.2f}")
        self.net_label.setStyleSheet(
            f"color: {net_color}; font-size: 20px; font-weight: bold;"
        )
        net_sign_jpy = "+" if net_jpy >= 0 else ""
        self.net_jpy_label.setText(f"{net_sign_jpy}¥{net_jpy:,}")

        self.txn_count_label.setText(f"{summary['count']} transaction(s) in period")

        # Category bars
        while self.cat_bars_layout.count():
            child = self.cat_bars_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        by_cat = summary["by_category"]
        if by_cat:
            max_amount = max(by_cat.values())
            bar_colors = [
                accent, green, "#cba6f7", "#fab387",
                "#f9e2af", "#94e2d5", red, "#f5c2e7",
            ]
            for i, (cat, amount) in enumerate(
                sorted(by_cat.items(), key=lambda x: -x[1])
            ):
                bar = CategoryBar(
                    cat, amount, max_amount, rate,
                    bar_colors[i % len(bar_colors)],
                )
                self.cat_bars_layout.addWidget(bar)
        else:
            no_data = QLabel("No transactions in this period")
            no_data.setObjectName("subtitle")
            self.cat_bars_layout.addWidget(no_data)

        # ── Goal section ──────────────────────────────────────────────────────
        self._update_goal_section()

        # ── Preset buttons ────────────────────────────────────────────────────
        self._rebuild_preset_buttons()

    # ── CRUD actions ──────────────────────────────────────────────────────────

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
            txn.currency = data["currency"]
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
                if idx.row() < len(self._txn_ids):
                    self.store.delete_transaction(self._txn_ids[idx.row()])
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
"""Theme stylesheets for PyQt6.

Themes included:
  Dark   — Catppuccin Mocha, Tokyo Night, Dracula, Monokai Pro, One Dark Pro, Rosé Pine
  Medium — Nord, Gruvbox Dark
  Light  — Catppuccin Latte, Solarized Light

Fixes over previous version:
  - Full QTabBar / QTabWidget styling (dialogs now have proper tabs)
  - QMenuBar / QMenu styling (menu bar no longer inherits OS chrome)
  - QToolButton styling (color swatches, weekday pickers, etc.)
  - QComboBox, QDateEdit, QTimeEdit, QSpinBox arrow-button subcontrols
    styled with visible backgrounds so arrows are legible on all themes
  - Secondary button contrast improved (explicit text color + stronger border)
  - QProgressBar added (used in dashboard)
  - QScrollArea viewport now transparent (no mismatched bg panels)
  - Solarized Light replaces Solarized Dark (fg was too muted for readability)
"""


def _build_theme(c: dict) -> str:
    """Generate a full QSS stylesheet from a color palette dict."""
    return f"""
/* ━━━━ Base ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
QMainWindow, QWidget {{
    background-color: {c['bg']};
    color: {c['fg']};
    font-family: "Segoe UI", "Ubuntu", "Noto Sans", sans-serif;
    font-size: 12px;
}}

/* Transparent scroll-area viewport so inner widgets set their own bg */
QScrollArea > QWidget > QWidget {{
    background-color: transparent;
}}

/* ━━━━ Menu bar ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
QMenuBar {{
    background-color: {c['header_bg']};
    color: {c['fg']};
    border-bottom: 1px solid {c['border']};
    padding: 2px 4px;
    font-size: 12px;
}}
QMenuBar::item {{
    background-color: transparent;
    padding: 4px 10px;
    border-radius: 4px;
}}
QMenuBar::item:selected {{
    background-color: {c['accent']};
    color: {c['accent_fg']};
}}
QMenuBar::item:pressed {{
    background-color: {c['accent_pressed']};
    color: {c['accent_fg']};
}}

QMenu {{
    background-color: {c['surface']};
    color: {c['fg']};
    border: 1px solid {c['border']};
    border-radius: 6px;
    padding: 4px;
}}
QMenu::item {{
    padding: 5px 24px 5px 12px;
    border-radius: 3px;
}}
QMenu::item:selected {{
    background-color: {c['accent']};
    color: {c['accent_fg']};
}}
QMenu::separator {{
    height: 1px;
    background-color: {c['border']};
    margin: 4px 8px;
}}

/* ━━━━ Tab widget ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
QTabWidget::pane {{
    border: 1px solid {c['border']};
    border-radius: 6px;
    background-color: {c['surface']};
    top: -1px;
}}
QTabWidget[documentMode="true"]::pane {{
    border: none;
    border-top: 1px solid {c['border']};
    background-color: transparent;
    border-radius: 0;
}}
QTabBar {{
    background-color: transparent;
}}
QTabBar::tab {{
    background-color: transparent;
    color: {c['muted']};
    padding: 7px 16px;
    border: none;
    border-bottom: 2px solid transparent;
    min-width: 60px;
    font-size: 12px;
}}
QTabBar::tab:selected {{
    color: {c['fg']};
    border-bottom: 2px solid {c['accent']};
    font-weight: bold;
}}
QTabBar::tab:hover:!selected {{
    color: {c['fg']};
    background-color: {c['hover']};
    border-radius: 4px 4px 0 0;
}}
QTabBar::tab:disabled {{
    color: {c['border']};
}}

/* ━━━━ Text inputs ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
QLineEdit, QTextEdit, QPlainTextEdit {{
    background-color: {c['surface']};
    color: {c['fg']};
    border: 1px solid {c['border']};
    border-radius: 4px;
    padding: 4px 6px;
    selection-background-color: {c['accent']};
    selection-color: {c['accent_fg']};
}}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
    border: 1px solid {c['accent']};
    outline: none;
}}
QLineEdit[readOnly="true"] {{
    background-color: {c['bg']};
    color: {c['muted']};
}}

/* ━━━━ Push buttons ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
QPushButton {{
    background-color: {c['accent']};
    color: {c['accent_fg']};
    border: none;
    border-radius: 5px;
    padding: 5px 14px;
    font-weight: bold;
    font-size: 12px;
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
QPushButton:flat {{
    background-color: transparent;
    border: none;
    color: {c['fg']};
    font-weight: normal;
}}
QPushButton:flat:hover {{
    background-color: {c['hover']};
}}

/* Destructive (delete) */
QPushButton#destructive {{
    background-color: {c['red']};
    color: #ffffff;
}}
QPushButton#destructive:hover {{
    background-color: {c['red_hover']};
}}
QPushButton#destructive:pressed {{
    background-color: {c['red']};
}}

/* Secondary (muted/ghost) — high contrast */
QPushButton#secondary {{
    background-color: {c['surface']};
    color: {c['fg']};
    border: 1px solid {c['border']};
    font-weight: normal;
}}
QPushButton#secondary:hover {{
    background-color: {c['hover']};
    border-color: {c['accent']};
    color: {c['fg']};
}}
QPushButton#secondary:pressed {{
    background-color: {c['border']};
}}
QPushButton#secondary:disabled {{
    color: {c['muted']};
    border-color: {c['border']};
}}

/* ━━━━ Tool buttons (color swatches, weekday pickers) ━━━━ */
QToolButton {{
    background-color: {c['surface']};
    color: {c['fg']};
    border: 1px solid {c['border']};
    border-radius: 4px;
    padding: 3px 6px;
    font-size: 11px;
}}
QToolButton:hover {{
    background-color: {c['hover']};
    border-color: {c['accent']};
}}
QToolButton:checked {{
    background-color: {c['accent']};
    color: {c['accent_fg']};
    border-color: {c['accent']};
    font-weight: bold;
}}
QToolButton:pressed {{
    background-color: {c['accent_pressed']};
    color: {c['accent_fg']};
}}
QToolButton::menu-indicator {{
    image: none;
}}

/* ━━━━ Lists ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
QListWidget {{
    background-color: {c['surface']};
    border: 1px solid {c['border']};
    border-radius: 6px;
    padding: 4px;
    outline: none;
}}
QListWidget::item {{
    padding: 5px 4px;
    border-radius: 4px;
}}
QListWidget::item:selected {{
    background-color: {c['accent']};
    color: {c['accent_fg']};
}}
QListWidget::item:hover:!selected {{
    background-color: {c['hover']};
}}

/* ━━━━ Tables ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
QTableWidget {{
    background-color: {c['surface']};
    border: 1px solid {c['border']};
    border-radius: 6px;
    gridline-color: {c['border']};
    outline: none;
    alternate-background-color: {c['alt_row']};
}}
QTableWidget::item {{
    padding: 4px;
}}
QTableWidget::item:selected {{
    background-color: {c['accent']};
    color: {c['accent_fg']};
}}
QHeaderView::section {{
    background-color: {c['header_bg']};
    color: {c['fg']};
    padding: 5px 6px;
    border: none;
    border-bottom: 2px solid {c['accent']};
    border-right: 1px solid {c['border']};
    font-weight: bold;
    font-size: 11px;
}}
QHeaderView::section:last {{
    border-right: none;
}}

/* ━━━━ Combo boxes ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
QComboBox {{
    background-color: {c['surface']};
    color: {c['fg']};
    border: 1px solid {c['border']};
    border-radius: 4px;
    padding: 4px 6px;
    min-width: 70px;
    font-size: 12px;
}}
QComboBox:hover {{
    border-color: {c['accent']};
}}
QComboBox:focus {{
    border-color: {c['accent']};
}}
QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 22px;
    background-color: {c['border']};
    border-left: 1px solid {c['border']};
    border-radius: 0 4px 4px 0;
}}
QComboBox::drop-down:hover {{
    background-color: {c['accent']};
}}
QComboBox::down-arrow {{
    width: 0;
    height: 0;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid {c['fg']};
}}
QComboBox::down-arrow:hover {{
    border-top-color: {c['accent_fg']};
}}
QComboBox QAbstractItemView {{
    background-color: {c['surface']};
    color: {c['fg']};
    selection-background-color: {c['accent']};
    selection-color: {c['accent_fg']};
    border: 1px solid {c['border']};
    border-radius: 4px;
    padding: 2px;
    outline: none;
}}

/* ━━━━ Spin boxes, Date/Time edits ━━━━━━━━━━━━━━━ */
QDateEdit, QTimeEdit, QSpinBox, QDoubleSpinBox {{
    background-color: {c['surface']};
    color: {c['fg']};
    border: 1px solid {c['border']};
    border-radius: 4px;
    padding: 4px 6px;
    font-size: 12px;
}}
QDateEdit:hover, QTimeEdit:hover, QSpinBox:hover, QDoubleSpinBox:hover {{
    border-color: {c['accent']};
}}
QDateEdit:focus, QTimeEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
    border-color: {c['accent']};
}}

/* Calendar popup button */
QDateEdit::drop-down, QTimeEdit::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 22px;
    background-color: {c['border']};
    border-left: 1px solid {c['border']};
    border-radius: 0 4px 4px 0;
}}
QDateEdit::drop-down:hover, QTimeEdit::drop-down:hover {{
    background-color: {c['accent']};
}}
QDateEdit::down-arrow, QTimeEdit::down-arrow {{
    width: 0;
    height: 0;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid {c['fg']};
}}
QDateEdit::down-arrow:hover, QTimeEdit::down-arrow:hover {{
    border-top-color: {c['accent_fg']};
}}

/* Spinbox increment buttons */
QSpinBox::up-button, QDoubleSpinBox::up-button {{
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 18px;
    background-color: {c['border']};
    border-left: 1px solid {c['border']};
    border-bottom: 1px solid {c['border']};
    border-radius: 0 4px 0 0;
}}
QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover {{
    background-color: {c['accent']};
}}
QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {{
    width: 0;
    height: 0;
    border-left: 3px solid transparent;
    border-right: 3px solid transparent;
    border-bottom: 4px solid {c['fg']};
}}
QSpinBox::down-button, QDoubleSpinBox::down-button {{
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    width: 18px;
    background-color: {c['border']};
    border-left: 1px solid {c['border']};
    border-radius: 0 0 4px 0;
}}
QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {{
    background-color: {c['accent']};
}}
QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {{
    width: 0;
    height: 0;
    border-left: 3px solid transparent;
    border-right: 3px solid transparent;
    border-top: 4px solid {c['fg']};
}}

/* Calendar popup widget (the calendar picker) */
QCalendarWidget QWidget {{
    background-color: {c['surface']};
    color: {c['fg']};
}}
QCalendarWidget QAbstractItemView:enabled {{
    background-color: {c['surface']};
    color: {c['fg']};
    selection-background-color: {c['accent']};
    selection-color: {c['accent_fg']};
}}
QCalendarWidget QAbstractItemView:disabled {{
    color: {c['muted']};
}}
QCalendarWidget QToolButton {{
    background-color: transparent;
    color: {c['fg']};
    border: none;
    font-weight: bold;
    font-size: 13px;
    padding: 4px 8px;
}}
QCalendarWidget QToolButton:hover {{
    background-color: {c['hover']};
    border-radius: 4px;
}}
QCalendarWidget #qt_calendar_navigationbar {{
    background-color: {c['header_bg']};
    border-bottom: 1px solid {c['border']};
    padding: 4px;
}}

/* ━━━━ Checkboxes ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
QCheckBox {{
    spacing: 8px;
    color: {c['fg']};
    font-size: 12px;
}}
QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 2px solid {c['border']};
    background-color: {c['surface']};
}}
QCheckBox::indicator:hover {{
    border-color: {c['accent']};
}}
QCheckBox::indicator:checked {{
    background-color: {c['accent']};
    border-color: {c['accent']};
}}
QCheckBox::indicator:checked:hover {{
    background-color: {c['accent_hover']};
}}

/* ━━━━ Progress bar ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
QProgressBar {{
    background-color: {c['surface']};
    border: 1px solid {c['border']};
    border-radius: 4px;
    text-align: center;
    color: {c['fg']};
    font-size: 11px;
    min-height: 10px;
}}
QProgressBar::chunk {{
    background-color: {c['accent']};
    border-radius: 4px;
}}

/* ━━━━ Labels ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
QLabel#sectionTitle {{
    font-size: 15px;
    font-weight: bold;
    color: {c['fg']};
}}
QLabel#subtitle {{
    font-size: 11px;
    color: {c['muted']};
}}
QLabel#statusOk {{
    color: {c['green']};
    font-size: 12px;
    font-weight: bold;
}}
QLabel#statusWarn {{
    color: {c['yellow']};
    font-size: 12px;
    font-weight: bold;
}}

/* ━━━━ Separators ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
QFrame#separator {{
    background-color: {c['border']};
    max-height: 1px;
    border: none;
}}

/* ━━━━ Splitter ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
QSplitter::handle {{
    background-color: {c['border']};
    width: 2px;
    margin: 4px 2px;
}}
QSplitter::handle:hover {{
    background-color: {c['accent']};
}}

/* ━━━━ Scroll bars ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
QScrollBar:vertical {{
    background-color: transparent;
    width: 8px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background-color: {c['border']};
    border-radius: 4px;
    min-height: 24px;
}}
QScrollBar::handle:vertical:hover {{
    background-color: {c['muted']};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    height: 0;
    background: transparent;
}}
QScrollBar:horizontal {{
    background-color: transparent;
    height: 8px;
    margin: 0;
}}
QScrollBar::handle:horizontal {{
    background-color: {c['border']};
    border-radius: 4px;
    min-width: 24px;
}}
QScrollBar::handle:horizontal:hover {{
    background-color: {c['muted']};
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal,
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
    width: 0;
    background: transparent;
}}

/* ━━━━ Tooltips ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
QToolTip {{
    background-color: {c['surface']};
    color: {c['fg']};
    border: 1px solid {c['border']};
    border-radius: 4px;
    padding: 5px 8px;
    font-size: 12px;
}}

/* ━━━━ Dialogs ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
QDialog {{
    background-color: {c['bg']};
}}
QMessageBox {{
    background-color: {c['bg']};
}}
QMessageBox QLabel {{
    color: {c['fg']};
    font-size: 13px;
}}

/* ━━━━ Status bar ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
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

/* ━━━━ Group boxes ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
QGroupBox {{
    border: 1px solid {c['border']};
    border-radius: 6px;
    margin-top: 14px;
    padding-top: 8px;
    font-weight: bold;
    color: {c['fg']};
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 4px;
    color: {c['accent']};
    font-size: 12px;
}}
"""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Dark themes
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Catppuccin Mocha — deep purple-dark, blue accent
_CATPPUCCIN_DARK = {
    "bg": "#1e1e2e",        "surface": "#313244",   "border": "#45475a",
    "fg": "#cdd6f4",        "muted": "#7f849c",      "hover": "#3b3d54",
    "accent": "#89b4fa",    "accent_fg": "#1e1e2e",
    "accent_hover": "#a0c5ff", "accent_pressed": "#74a4ea",
    "red": "#f38ba8",       "red_hover": "#f5a0b8",
    "green": "#a6e3a1",     "yellow": "#f9e2af",
    "header_bg": "#181825", "alt_row": "#252538",
}

# Tokyo Night — navy-dark, electric blue accent
_TOKYO_NIGHT = {
    "bg": "#1a1b26",        "surface": "#24283b",   "border": "#414868",
    "fg": "#c0caf5",        "muted": "#565f89",      "hover": "#2d3348",
    "accent": "#7aa2f7",    "accent_fg": "#1a1b26",
    "accent_hover": "#93b4fb", "accent_pressed": "#6090e5",
    "red": "#f7768e",       "red_hover": "#f88fa0",
    "green": "#9ece6a",     "yellow": "#e0af68",
    "header_bg": "#16161e", "alt_row": "#1f2335",
}

# Dracula — classic dark purple
_DRACULA = {
    "bg": "#282a36",        "surface": "#343746",   "border": "#44475a",
    "fg": "#f8f8f2",        "muted": "#8090c0",      "hover": "#3d4059",
    "accent": "#bd93f9",    "accent_fg": "#282a36",
    "accent_hover": "#cda7ff", "accent_pressed": "#ad83e9",
    "red": "#ff5555",       "red_hover": "#ff7070",
    "green": "#50fa7b",     "yellow": "#f1fa8c",
    "header_bg": "#21222c", "alt_row": "#2f303e",
}

# Monokai Pro — warm dark, golden accent
_MONOKAI = {
    "bg": "#2d2a2e",        "surface": "#403e41",   "border": "#5b595c",
    "fg": "#fcfcfa",        "muted": "#a9a7a7",      "hover": "#4a4849",
    "accent": "#ffd866",    "accent_fg": "#2d2a2e",
    "accent_hover": "#ffe085", "accent_pressed": "#e0be50",
    "red": "#ff6188",       "red_hover": "#ff7a9c",
    "green": "#a9dc76",     "yellow": "#ffd866",
    "header_bg": "#221f22", "alt_row": "#353135",
}

# One Dark Pro — Atom-inspired neutral dark
_ONE_DARK = {
    "bg": "#282c34",        "surface": "#353b45",   "border": "#4b5263",
    "fg": "#abb2bf",        "muted": "#7a8294",      "hover": "#3e4452",
    "accent": "#61afef",    "accent_fg": "#282c34",
    "accent_hover": "#7bbef5", "accent_pressed": "#519fd5",
    "red": "#e06c75",       "red_hover": "#e88090",
    "green": "#98c379",     "yellow": "#e5c07b",
    "header_bg": "#21252b", "alt_row": "#2c313c",
}

# Rosé Pine — muted, nature-inspired dark
_ROSE_PINE = {
    "bg": "#191724",        "surface": "#26233a",   "border": "#403d52",
    "fg": "#e0def4",        "muted": "#908caa",      "hover": "#2d2b3e",
    "accent": "#c4a7e7",    "accent_fg": "#191724",
    "accent_hover": "#d4b9f0", "accent_pressed": "#b498d4",
    "red": "#eb6f92",       "red_hover": "#f08098",
    "green": "#9ccfd8",     "yellow": "#f6c177",
    "header_bg": "#12111f", "alt_row": "#201e2e",
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Medium themes
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Nord — arctic teal palette
_NORD = {
    "bg": "#2e3440",        "surface": "#3b4252",   "border": "#4c566a",
    "fg": "#eceff4",        "muted": "#9199aa",      "hover": "#434c5e",
    "accent": "#88c0d0",    "accent_fg": "#2e3440",
    "accent_hover": "#9bcfde", "accent_pressed": "#79b0c0",
    "red": "#bf616a",       "red_hover": "#cc7079",
    "green": "#a3be8c",     "yellow": "#ebcb8b",
    "header_bg": "#272c36", "alt_row": "#333a47",
}

# Gruvbox Dark — warm earthy tones
_GRUVBOX = {
    "bg": "#282828",        "surface": "#3c3836",   "border": "#665c54",
    "fg": "#ebdbb2",        "muted": "#bdae93",      "hover": "#504945",
    "accent": "#fabd2f",    "accent_fg": "#282828",
    "accent_hover": "#ffd045", "accent_pressed": "#d9a520",
    "red": "#fb4934",       "red_hover": "#ff6147",
    "green": "#b8bb26",     "yellow": "#fabd2f",
    "header_bg": "#1d2021", "alt_row": "#32302f",
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Light themes
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Catppuccin Latte — soft warm light
_CATPPUCCIN_LIGHT = {
    "bg": "#eff1f5",        "surface": "#ffffff",   "border": "#bcc0cc",
    "fg": "#4c4f69",        "muted": "#7c7f93",      "hover": "#dce0ea",
    "accent": "#1e66f5",    "accent_fg": "#ffffff",
    "accent_hover": "#4080f7", "accent_pressed": "#1650d0",
    "red": "#d20f39",       "red_hover": "#e0304f",
    "green": "#40a02b",     "yellow": "#df8e1d",
    "header_bg": "#e6e9ef", "alt_row": "#f4f5f8",
}

# Solarized Light — high-readability warm ivory
_SOLARIZED_LIGHT = {
    "bg": "#fdf6e3",        "surface": "#eee8d5",   "border": "#d3cbbb",
    "fg": "#657b83",        "muted": "#93a1a1",      "hover": "#e2dac8",
    "accent": "#268bd2",    "accent_fg": "#fdf6e3",
    "accent_hover": "#3aa0e8", "accent_pressed": "#1a6da0",
    "red": "#dc322f",       "red_hover": "#e04545",
    "green": "#859900",     "yellow": "#b58900",
    "header_bg": "#ece7d6", "alt_row": "#f5f0e2",
}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Build registry
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

_ALL_PALETTES = {
    # Dark
    "Catppuccin Dark":  _CATPPUCCIN_DARK,
    "Tokyo Night":      _TOKYO_NIGHT,
    "Dracula":          _DRACULA,
    "Monokai Pro":      _MONOKAI,
    "One Dark Pro":     _ONE_DARK,
    "Rosé Pine":        _ROSE_PINE,
    # Medium
    "Nord":             _NORD,
    "Gruvbox Dark":     _GRUVBOX,
    # Light
    "Catppuccin Light": _CATPPUCCIN_LIGHT,
    "Solarized Light":  _SOLARIZED_LIGHT,
}

THEMES  = {name: _build_theme(pal) for name, pal in _ALL_PALETTES.items()}
PALETTES = dict(_ALL_PALETTES)


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
