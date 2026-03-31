"""Soft event storage — lightweight recurring reminders with per-day logs."""

import uuid
from dataclasses import dataclass
from datetime import date, timedelta

from src.data.database import get_connection
from src.data.calendar_store import expand_recurring_to_range, Event, parse_recurrence
from src.utils.timestamps import now_utc


@dataclass
class SoftEventTemplate:
    id: str
    title: str
    note: str = ""
    color: str = "#a6e3a1"
    recurrence: str = ""
    updated_at: str = ""
    deleted: bool = False


@dataclass
class SoftEventLog:
    id: str
    template_id: str
    log_date: str        # YYYY-MM-DD
    log_text: str = ""
    updated_at: str = ""
    deleted: bool = False


class SoftEventStore:

    # ── Template CRUD ────────────────────────────────────

    def add_template(self, title: str, note: str = "", color: str = "#a6e3a1",
                     recurrence: str = "") -> SoftEventTemplate:
        now = now_utc()
        tpl = SoftEventTemplate(
            id=str(uuid.uuid4()), title=title, note=note,
            color=color, recurrence=recurrence, updated_at=now,
        )
        self._upsert_template(tpl)
        return tpl

    def update_template(self, template: SoftEventTemplate) -> SoftEventTemplate:
        template.updated_at = now_utc()
        self._upsert_template(template)
        return template

    def delete_template(self, template_id: str):
        """Soft-delete a template."""
        conn = get_connection()
        try:
            conn.execute(
                "UPDATE soft_event_templates SET deleted=1, updated_at=? WHERE id=?",
                (now_utc(), template_id),
            )
            conn.commit()
        finally:
            conn.close()

    def get_templates(self) -> list[SoftEventTemplate]:
        """Return all non-deleted templates."""
        conn = get_connection()
        try:
            rows = conn.execute(
                "SELECT * FROM soft_event_templates WHERE deleted=0 ORDER BY title"
            ).fetchall()
            return [self._row_to_template(r) for r in rows]
        finally:
            conn.close()

    def get_template(self, template_id: str) -> SoftEventTemplate | None:
        conn = get_connection()
        try:
            row = conn.execute(
                "SELECT * FROM soft_event_templates WHERE id=?", (template_id,)
            ).fetchone()
            return self._row_to_template(row) if row else None
        finally:
            conn.close()

    def get_upcoming(self, from_date: date, days_ahead: int = 7) -> list[tuple[date, SoftEventTemplate]]:
        """Expand each template's recurrence and return sorted (date, template) tuples.

        For templates with empty recurrence, they are skipped (no base date to anchor).
        days_ahead=0 means only from_date itself is checked.
        """
        templates = self.get_templates()
        range_end = from_date + timedelta(days=max(days_ahead, 0))
        results: list[tuple[date, SoftEventTemplate]] = []

        for tpl in templates:
            rec = parse_recurrence(tpl.recurrence)
            if rec["type"] == "none":
                # No recurrence — skip (no base date to match)
                continue

            # Build a lightweight Event-like object for expand_recurring_to_range
            # We need a start_time in ISO format; use epoch start as a safe anchor
            # for daily/weekly, or use recurrence info for monthly/yearly.
            # The expand function reads start_time to extract the anchor date.
            # We'll use 2020-01-01 as a generic anchor for daily/weekly,
            # which still produces correct results since those patterns
            # are relative to weekday, not an absolute date.
            dummy_event = Event(
                id=tpl.id, title=tpl.title,
                start_time="2020-01-01T00:00:00",
                recurrence=tpl.recurrence,
            )
            dates = expand_recurring_to_range(dummy_event, from_date, range_end)
            for d in dates:
                results.append((d, tpl))

        results.sort(key=lambda x: x[0])
        return results

    # ── Log CRUD ─────────────────────────────────────────

    def get_or_create_log(self, template_id: str, log_date: str) -> SoftEventLog:
        """Return existing log or create a new one with a date header."""
        existing = self.get_log(template_id, log_date)
        if existing:
            return existing
        now = now_utc()
        log = SoftEventLog(
            id=str(uuid.uuid4()),
            template_id=template_id,
            log_date=log_date,
            log_text=f"— {log_date} —",
            updated_at=now,
        )
        self._upsert_log(log)
        return log

    def update_log(self, log: SoftEventLog) -> SoftEventLog:
        log.updated_at = now_utc()
        self._upsert_log(log)
        return log

    def get_log(self, template_id: str, log_date: str) -> SoftEventLog | None:
        conn = get_connection()
        try:
            row = conn.execute(
                "SELECT * FROM soft_event_logs WHERE template_id=? AND log_date=? AND deleted=0",
                (template_id, log_date),
            ).fetchone()
            return self._row_to_log(row) if row else None
        finally:
            conn.close()

    def get_logs_for_template(self, template_id: str) -> list[SoftEventLog]:
        """Return all non-deleted logs for a template, sorted newest first."""
        conn = get_connection()
        try:
            rows = conn.execute(
                "SELECT * FROM soft_event_logs WHERE template_id=? AND deleted=0 "
                "ORDER BY log_date DESC",
                (template_id,),
            ).fetchall()
            return [self._row_to_log(r) for r in rows]
        finally:
            conn.close()

    # ── Internal helpers ─────────────────────────────────

    def _upsert_template(self, tpl: SoftEventTemplate):
        conn = get_connection()
        try:
            conn.execute(
                """INSERT INTO soft_event_templates
                   (id, title, note, color, recurrence, updated_at, deleted)
                   VALUES (?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(id) DO UPDATE SET
                   title=excluded.title, note=excluded.note, color=excluded.color,
                   recurrence=excluded.recurrence, updated_at=excluded.updated_at,
                   deleted=excluded.deleted""",
                (tpl.id, tpl.title, tpl.note, tpl.color,
                 tpl.recurrence, tpl.updated_at, int(tpl.deleted)),
            )
            conn.commit()
        finally:
            conn.close()

    def _upsert_log(self, log: SoftEventLog):
        conn = get_connection()
        try:
            conn.execute(
                """INSERT INTO soft_event_logs
                   (id, template_id, log_date, log_text, updated_at, deleted)
                   VALUES (?, ?, ?, ?, ?, ?)
                   ON CONFLICT(id) DO UPDATE SET
                   template_id=excluded.template_id, log_date=excluded.log_date,
                   log_text=excluded.log_text, updated_at=excluded.updated_at,
                   deleted=excluded.deleted""",
                (log.id, log.template_id, log.log_date,
                 log.log_text, log.updated_at, int(log.deleted)),
            )
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def _row_to_template(row) -> SoftEventTemplate:
        return SoftEventTemplate(
            id=row["id"], title=row["title"],
            note=row["note"] or "", color=row["color"] or "#a6e3a1",
            recurrence=row["recurrence"] or "",
            updated_at=row["updated_at"],
            deleted=bool(row["deleted"]),
        )

    @staticmethod
    def _row_to_log(row) -> SoftEventLog:
        return SoftEventLog(
            id=row["id"], template_id=row["template_id"],
            log_date=row["log_date"], log_text=row["log_text"] or "",
            updated_at=row["updated_at"],
            deleted=bool(row["deleted"]),
        )