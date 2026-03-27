"""Financial/earnings storage backed by SQLite."""

import calendar as _calendar
import uuid
from dataclasses import dataclass
from datetime import date as _date

from src.data.database import get_connection
from src.utils.timestamps import now_utc


INCOME_CATEGORIES = ["Main Job", "Side Job"]

EXPENSE_CATEGORIES = [
    "Rent / Housing",
    "Software / Tools",
    "Hardware",
    "Office Supplies",
    "Travel",
    "Education",
    "Food & Drink",
    "Subscriptions",
    "Utilities",
    "Taxes",
    "Fees & Banking",
    "Uncategorized",
]

DEFAULT_CATEGORIES = INCOME_CATEGORIES + EXPENSE_CATEGORIES


@dataclass
class Transaction:
    id: str
    date: str
    amount: float
    type: str
    category: str = "Side Job"
    description: str = ""
    updated_at: str = ""
    deleted: bool = False
    currency: str = "USD"
    is_job_pay: bool = False


@dataclass
class JobPreset:
    id: str
    name: str
    amount_usd: float
    category: str = "Main Job"
    updated_at: str = ""
    deleted: bool = False


@dataclass
class SideIncomeGoal:
    id: str
    year: int
    month: int
    min_goal: float
    major_goal: float
    updated_at: str = ""


class FinanceStore:

    # ── Transactions ──────────────────────────────────────────────────────────

    def add_transaction(self, date: str, amount: float, txn_type: str,
                        category: str = "Side Job", description: str = "",
                        currency: str = "USD", is_job_pay: bool = False) -> Transaction:
        txn = Transaction(
            id=str(uuid.uuid4()),
            date=date, amount=amount, type=txn_type,
            category=category, description=description,
            updated_at=now_utc(), currency=currency, is_job_pay=is_job_pay,
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
                query += " AND date >= ?"; params.append(start_date)
            if end_date:
                query += " AND date <= ?"; params.append(end_date)
            if txn_type:
                query += " AND type = ?"; params.append(txn_type)
            query += " ORDER BY date DESC"
            rows = conn.execute(query, params).fetchall()
            return [self._row_to_txn(r) for r in rows]
        finally:
            conn.close()

    def has_monthly_tag(self, year: int, month: int) -> bool:
        """Return True if any [Monthly] tagged expense exists for this month."""
        import calendar as _cal
        last_day = _cal.monthrange(year, month)[1]
        first = _date(year, month, 1).isoformat()
        last  = _date(year, month, last_day).isoformat()
        conn = get_connection()
        try:
            row = conn.execute(
                "SELECT COUNT(*) as cnt FROM transactions "
                "WHERE deleted=0 AND type='expense' "
                "AND description LIKE '[Monthly]%' "
                "AND date >= ? AND date <= ?",
                (first, last),
            ).fetchone()
            return row["cnt"] > 0
        finally:
            conn.close()

    def get_summary(self, start_date: str | None = None,
                    end_date: str | None = None) -> dict:
        txns = self.get_transactions(start_date, end_date)
        earned = sum(t.amount for t in txns if t.type == "income")
        spent  = sum(t.amount for t in txns if t.type == "expense")
        by_category: dict[str, float] = {}
        for t in txns:
            by_category[t.category] = by_category.get(t.category, 0) + t.amount
        return {"earned": earned, "spent": spent, "net": earned - spent,
                "by_category": by_category, "count": len(txns)}

    def get_goal_income(self, start_date: str, end_date: str,
                        usd_jpy_rate: float = 150.0) -> float:
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
        total = 0.0
        for r in rows:
            total += r["amount"] / usd_jpy_rate if r["currency"] == "JPY" else r["amount"]
        return total

    def get_side_income(self, year: int, month: int,
                        usd_jpy_rate: float = 150.0) -> float:
        last_day = _calendar.monthrange(year, month)[1]
        return self.get_goal_income(
            _date(year, month, 1).isoformat(),
            _date(year, month, last_day).isoformat(),
            usd_jpy_rate,
        )

    def get_all_time_earned_usd(self, usd_jpy_rate: float = 150.0) -> float:
        conn = get_connection()
        try:
            rows = conn.execute(
                "SELECT amount, currency FROM transactions WHERE deleted=0 AND type='income'"
            ).fetchall()
        finally:
            conn.close()
        total = 0.0
        for r in rows:
            total += r["amount"] / usd_jpy_rate if r["currency"] == "JPY" else r["amount"]
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
                   category: str = "Main Job") -> JobPreset:
        preset = JobPreset(id=str(uuid.uuid4()), name=name,
                           amount_usd=amount_usd, category=category,
                           updated_at=now_utc())
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
        """Log a preset as income. is_job_pay follows the preset's category."""
        day = on_date or _date.today().isoformat()
        is_job_pay = (preset.category == "Main Job")
        txns = []
        for _ in range(count):
            txns.append(self.add_transaction(
                date=day,
                amount=preset.amount_usd,
                txn_type="income",
                category=preset.category,
                description=f"[Job] {preset.name}",
                currency="USD",
                is_job_pay=is_job_pay,
            ))
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

    # ── Side Income Goals ─────────────────────────────────────────────────────

    def get_goal(self, year: int, month: int) -> SideIncomeGoal | None:
        conn = get_connection()
        try:
            row = conn.execute(
                "SELECT * FROM side_income_goals WHERE year=? AND month=?",
                (year, month),
            ).fetchone()
            return self._row_to_goal(row) if row else None
        finally:
            conn.close()

    def set_goal(self, year: int, month: int,
                 min_goal: float, major_goal: float) -> SideIncomeGoal:
        conn = get_connection()
        now = now_utc()
        try:
            existing = conn.execute(
                "SELECT id FROM side_income_goals WHERE year=? AND month=?",
                (year, month),
            ).fetchone()
            goal_id = existing["id"] if existing else str(uuid.uuid4())
            conn.execute(
                """INSERT INTO side_income_goals
                   (id, year, month, min_goal, major_goal, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?)
                   ON CONFLICT(year, month) DO UPDATE SET
                   min_goal=excluded.min_goal, major_goal=excluded.major_goal,
                   updated_at=excluded.updated_at""",
                (goal_id, year, month, min_goal, major_goal, now),
            )
            conn.commit()
        finally:
            conn.close()
        return SideIncomeGoal(id=goal_id, year=year, month=month,
                              min_goal=min_goal, major_goal=major_goal,
                              updated_at=now)

    @staticmethod
    def _row_to_goal(row) -> SideIncomeGoal:
        return SideIncomeGoal(
            id=row["id"], year=row["year"], month=row["month"],
            min_goal=row["min_goal"], major_goal=row["major_goal"],
            updated_at=row["updated_at"],
        )