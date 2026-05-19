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
    # Exchange rate at the moment this JPY transaction was entered.
    # 0 means "legacy row — fall back to the current live rate."
    rate_at_entry: float = 0.0


@dataclass
class JobPreset:
    id: str
    name: str
    amount_usd: float
    category: str = "Main Job"
    updated_at: str = ""
    deleted: bool = False
    # pay_unit:
    #   "flat"         – fixed payment per log entry
    #   "hour"         – rate × decimal hours
    #   "minute"       – rate × decimal minutes
    #   "audio_second" – rate is per *audio hour*; input is raw seconds
    pay_unit: str = "flat"


PAY_UNITS = ("flat", "hour", "minute", "audio_second")


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
                        currency: str = "USD", is_job_pay: bool = False,
                        rate_at_entry: float = 0.0) -> Transaction:
        txn = Transaction(
            id=str(uuid.uuid4()),
            date=date, amount=amount, type=txn_type,
            category=category, description=description,
            updated_at=now_utc(), currency=currency, is_job_pay=is_job_pay,
            rate_at_entry=rate_at_entry,
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
        """Side-job income for the date range, normalised to USD.

        For JPY rows that have a locked rate_at_entry the historical rate is
        used; legacy rows (rate_at_entry == 0) fall back to the live rate.
        """
        conn = get_connection()
        try:
            rows = conn.execute(
                "SELECT amount, currency, rate_at_entry FROM transactions "
                "WHERE deleted=0 AND type='income' AND is_job_pay=0 "
                "AND date >= ? AND date <= ?",
                (start_date, end_date),
            ).fetchall()
        finally:
            conn.close()
        total = 0.0
        for r in rows:
            total += self._to_usd(r["amount"], r["currency"],
                                  r["rate_at_entry"], usd_jpy_rate)
        return total

    def get_period_income_usd(self, start_date: str, end_date: str,
                              usd_jpy_rate: float = 150.0) -> float:
        """All income (side + main job) for a date range, normalised to USD."""
        conn = get_connection()
        try:
            rows = conn.execute(
                "SELECT amount, currency, rate_at_entry FROM transactions "
                "WHERE deleted=0 AND type='income' "
                "AND date >= ? AND date <= ?",
                (start_date, end_date),
            ).fetchall()
        finally:
            conn.close()
        total = 0.0
        for r in rows:
            total += self._to_usd(r["amount"], r["currency"],
                                  r["rate_at_entry"], usd_jpy_rate)
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
        """All-time income normalised to USD.

        JPY rows use rate_at_entry (locked at entry time) so the total does
        not drift as the live rate changes.  Legacy rows with rate_at_entry=0
        fall back to the supplied live rate.
        """
        conn = get_connection()
        try:
            rows = conn.execute(
                "SELECT amount, currency, rate_at_entry "
                "FROM transactions WHERE deleted=0 AND type='income'"
            ).fetchall()
        finally:
            conn.close()
        total = 0.0
        for r in rows:
            total += self._to_usd(r["amount"], r["currency"],
                                  r["rate_at_entry"], usd_jpy_rate)
        return total

    # ── Internal helpers ──────────────────────────────────────────────────────

    @staticmethod
    def _to_usd(amount: float, currency: str,
                rate_at_entry: float, live_rate: float) -> float:
        """Convert *amount* to USD using the locked or live rate."""
        if currency == "JPY":
            rate = rate_at_entry if rate_at_entry else live_rate
            return amount / rate if rate else 0.0
        return amount

    def _upsert(self, txn: Transaction):
        conn = get_connection()
        try:
            conn.execute(
                """INSERT INTO transactions
                   (id, date, amount, type, category, description,
                    updated_at, deleted, currency, is_job_pay, rate_at_entry)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(id) DO UPDATE SET
                   date=excluded.date, amount=excluded.amount, type=excluded.type,
                   category=excluded.category, description=excluded.description,
                   updated_at=excluded.updated_at, deleted=excluded.deleted,
                   currency=excluded.currency, is_job_pay=excluded.is_job_pay,
                   rate_at_entry=excluded.rate_at_entry""",
                (txn.id, txn.date, txn.amount, txn.type, txn.category,
                 txn.description, txn.updated_at, int(txn.deleted),
                 txn.currency, int(txn.is_job_pay), txn.rate_at_entry),
            )
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def _row_to_txn(row) -> Transaction:
        try:
            rate_at_entry = float(row["rate_at_entry"] or 0.0)
        except (IndexError, KeyError, TypeError):
            rate_at_entry = 0.0
        return Transaction(
            id=row["id"], date=row["date"], amount=row["amount"],
            type=row["type"], category=row["category"],
            description=row["description"], updated_at=row["updated_at"],
            deleted=bool(row["deleted"]),
            currency=row["currency"] if row["currency"] else "USD",
            is_job_pay=bool(row["is_job_pay"]),
            rate_at_entry=rate_at_entry,
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
                   category: str = "Main Job",
                   pay_unit: str = "flat") -> JobPreset:
        preset = JobPreset(id=str(uuid.uuid4()), name=name,
                           amount_usd=amount_usd, category=category,
                           updated_at=now_utc(),
                           pay_unit=pay_unit if pay_unit in PAY_UNITS else "flat")
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
                   units: float = 1.0,
                   on_date: str | None = None,
                   rate_at_entry: float = 0.0) -> list[Transaction]:
        """Log a preset as income.

        pay_unit behaviour:
          flat         – amount_usd × count  (one log per count)
          hour         – amount_usd × units hours  (single log)
          minute       – amount_usd × units minutes  (single log)
          audio_second – amount_usd is the rate per *audio hour*;
                         units is the raw number of seconds processed;
                         payment = amount_usd × (units / 3600)  (single log)
        """
        day  = on_date or _date.today().isoformat()
        is_job_pay = (preset.category == "Main Job")
        unit = (preset.pay_unit or "flat").lower()

        if unit == "hour":
            amount = preset.amount_usd * float(units)
            desc   = (f"[Job] {preset.name} "
                      f"({units:g}h @ ${preset.amount_usd:,.2f}/hr)")
            n_logs = 1

        elif unit == "minute":
            amount = preset.amount_usd * float(units)
            desc   = (f"[Job] {preset.name} "
                      f"({units:g}m @ ${preset.amount_usd:,.2f}/min)")
            n_logs = 1

        elif unit == "audio_second":
            secs = int(units)
            audio_hours = secs / 3600.0
            amount = preset.amount_usd * audio_hours
            # Format seconds as Xm Ys (or Xh Ym Zs if > 1 h)
            mins_total, secs_rem = divmod(secs, 60)
            hrs_part,   mins_rem = divmod(mins_total, 60)
            if hrs_part > 0:
                time_str = f"{hrs_part}h {mins_rem}m {secs_rem}s"
            else:
                time_str = f"{mins_rem}m {secs_rem}s"
            desc   = (f"[Job] {preset.name} "
                      f"({secs}s = {time_str} "
                      f"@ ${preset.amount_usd:,.2f}/audio hr)")
            n_logs = 1

        else:  # flat
            amount = preset.amount_usd
            desc   = f"[Job] {preset.name}"
            n_logs = max(int(count), 1)

        txns = []
        for _ in range(n_logs):
            txns.append(self.add_transaction(
                date=day,
                amount=amount,
                txn_type="income",
                category=preset.category,
                description=desc,
                currency="USD",
                is_job_pay=is_job_pay,
                rate_at_entry=0.0,   # USD — no conversion needed
            ))
        return txns

    def _upsert_preset(self, preset: JobPreset):
        conn = get_connection()
        try:
            conn.execute(
                """INSERT INTO job_presets
                   (id, name, amount_usd, category, updated_at, deleted, pay_unit)
                   VALUES (?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(id) DO UPDATE SET
                   name=excluded.name, amount_usd=excluded.amount_usd,
                   category=excluded.category, updated_at=excluded.updated_at,
                   deleted=excluded.deleted, pay_unit=excluded.pay_unit""",
                (preset.id, preset.name, preset.amount_usd,
                 preset.category, preset.updated_at, int(preset.deleted),
                 preset.pay_unit or "flat"),
            )
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def _row_to_preset(row) -> JobPreset:
        try:
            unit = row["pay_unit"] or "flat"
        except (IndexError, KeyError):
            unit = "flat"
        return JobPreset(
            id=row["id"], name=row["name"], amount_usd=row["amount_usd"],
            category=row["category"], updated_at=row["updated_at"],
            deleted=bool(row["deleted"]),
            pay_unit=unit if unit in PAY_UNITS else "flat",
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