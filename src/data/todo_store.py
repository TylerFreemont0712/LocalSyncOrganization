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
