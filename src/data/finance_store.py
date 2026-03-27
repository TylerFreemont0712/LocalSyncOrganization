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