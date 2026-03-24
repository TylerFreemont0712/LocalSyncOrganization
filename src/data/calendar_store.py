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
