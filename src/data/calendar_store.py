"""Calendar event storage backed by SQLite."""

import uuid
from dataclasses import dataclass

from src.data.database import get_connection
from src.utils.timestamps import now_utc


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


class CalendarStore:

    def add_event(self, title: str, start_time: str, end_time: str | None = None,
                  description: str = "", all_day: bool = False, color: str = "#4a9eff") -> Event:
        ev = Event(
            id=str(uuid.uuid4()),
            title=title,
            start_time=start_time,
            end_time=end_time,
            description=description,
            all_day=all_day,
            color=color,
            updated_at=now_utc(),
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
        """Get non-deleted events, optionally filtered by date range."""
        conn = get_connection()
        try:
            query = "SELECT * FROM events WHERE deleted=0"
            params: list = []
            if start:
                query += " AND start_time >= ?"
                params.append(start)
            if end:
                query += " AND start_time <= ?"
                params.append(end)
            query += " ORDER BY start_time"
            rows = conn.execute(query, params).fetchall()
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
                   all_day, color, updated_at, deleted)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(id) DO UPDATE SET
                   title=excluded.title, description=excluded.description,
                   start_time=excluded.start_time, end_time=excluded.end_time,
                   all_day=excluded.all_day, color=excluded.color,
                   updated_at=excluded.updated_at, deleted=excluded.deleted""",
                (ev.id, ev.title, ev.description, ev.start_time, ev.end_time,
                 int(ev.all_day), ev.color, ev.updated_at, int(ev.deleted)),
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
        )
