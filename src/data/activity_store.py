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

# Quick-tap card categories shown as large cards in the activity panel.
# Users can rename these via config key "activity_quick_categories".
QUICK_CATEGORIES = ["Food", "Work", "Side Job", "Break", "Family", "Free Time"]

# Colors for activity bars and quick cards
ACTIVITY_COLORS = {
    # Quick categories
    "Food":         "#fab387",  # peach
    "Work":         "#89b4fa",  # blue
    "Side Job":     "#a6e3a1",  # green
    "Break":        "#9399b2",  # overlay2 / grey
    "Family":       "#f5c2e7",  # pink
    "Free Time":    "#cba6f7",  # mauve
    # Legacy activities (kept for backwards compat)
    "Deep Work":    "#89b4fa",
    "Meetings":     "#f38ba8",
    "Email / Comms":"#fab387",
    "Learning":     "#a6e3a1",
    "Exercise":     "#94e2d5",
    "Errands":      "#f9e2af",
    "Commute":      "#cba6f7",
    "Coding":       "#74c7ec",
    "Writing":      "#b4befe",
    "Reading":      "#f2cdcd",
    "Admin":        "#eba0ac",
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