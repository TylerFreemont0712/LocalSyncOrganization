"""Financial/earnings storage backed by SQLite.

Reframed for freelance work tracking: income categories focus on client/project
types, and the summary is oriented around "Amount Earned" rather than generic
income/expense tracking.
"""

import uuid
from dataclasses import dataclass

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
    date: str  # YYYY-MM-DD
    amount: float
    type: str  # 'income' or 'expense'
    category: str = "Freelance"
    description: str = ""
    updated_at: str = ""
    deleted: bool = False


class FinanceStore:

    def add_transaction(self, date: str, amount: float, txn_type: str,
                        category: str = "Freelance", description: str = "") -> Transaction:
        txn = Transaction(
            id=str(uuid.uuid4()),
            date=date,
            amount=amount,
            type=txn_type,
            category=category,
            description=description,
            updated_at=now_utc(),
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
        """Return earnings/expense totals and by-category breakdown."""
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

    def get_all_time_earned(self) -> float:
        """Total income across all time."""
        conn = get_connection()
        try:
            row = conn.execute(
                "SELECT COALESCE(SUM(amount), 0) as total FROM transactions "
                "WHERE deleted=0 AND type='income'"
            ).fetchone()
            return row["total"]
        finally:
            conn.close()

    def _upsert(self, txn: Transaction):
        conn = get_connection()
        try:
            conn.execute(
                """INSERT INTO transactions (id, date, amount, type, category,
                   description, updated_at, deleted)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(id) DO UPDATE SET
                   date=excluded.date, amount=excluded.amount, type=excluded.type,
                   category=excluded.category, description=excluded.description,
                   updated_at=excluded.updated_at, deleted=excluded.deleted""",
                (txn.id, txn.date, txn.amount, txn.type, txn.category,
                 txn.description, txn.updated_at, int(txn.deleted)),
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
        )
