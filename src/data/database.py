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
