"""SQLite database setup and connection for all LocalSync modules."""

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

    # --- activities table ---
    act_cols = {r["name"] for r in conn.execute("PRAGMA table_info(activities)").fetchall()}
    # Future activity migrations go here

    # --- soft event tables (new tables, guard via sqlite_master) ---
    tables = {r["name"] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()}
    if "soft_event_templates" not in tables:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS soft_event_templates (
                id          TEXT PRIMARY KEY,
                title       TEXT NOT NULL,
                note        TEXT DEFAULT '',
                color       TEXT DEFAULT '#a6e3a1',
                recurrence  TEXT DEFAULT '',
                updated_at  TEXT NOT NULL,
                deleted     INTEGER DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS soft_event_logs (
                id           TEXT PRIMARY KEY,
                template_id  TEXT NOT NULL,
                log_date     TEXT NOT NULL,
                log_text     TEXT DEFAULT '',
                updated_at   TEXT NOT NULL,
                deleted      INTEGER DEFAULT 0,
                UNIQUE(template_id, log_date)
            );
        """)


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

CREATE TABLE IF NOT EXISTS side_income_goals (
    id          TEXT PRIMARY KEY,
    year        INTEGER NOT NULL,
    month       INTEGER NOT NULL,
    min_goal    REAL NOT NULL DEFAULT 0,
    major_goal  REAL NOT NULL DEFAULT 0,
    updated_at  TEXT NOT NULL,
    UNIQUE(year, month)
);

CREATE TABLE IF NOT EXISTS sync_meta (
    key   TEXT PRIMARY KEY,
    value TEXT
);

CREATE TABLE IF NOT EXISTS soft_event_templates (
    id          TEXT PRIMARY KEY,
    title       TEXT NOT NULL,
    note        TEXT DEFAULT '',
    color       TEXT DEFAULT '#a6e3a1',
    recurrence  TEXT DEFAULT '',
    updated_at  TEXT NOT NULL,
    deleted     INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS soft_event_logs (
    id           TEXT PRIMARY KEY,
    template_id  TEXT NOT NULL,
    log_date     TEXT NOT NULL,
    log_text     TEXT DEFAULT '',
    updated_at   TEXT NOT NULL,
    deleted      INTEGER DEFAULT 0,
    UNIQUE(template_id, log_date)
);
"""