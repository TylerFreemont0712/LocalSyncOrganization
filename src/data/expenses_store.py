"""Expense tracking — receipts, line items, and a small item-price catalogue.

The earnings ledger lives in `finance_store.transactions`. This module layers
*structured* expense data on top: every receipt also writes one transaction
row (`type='expense'`, tagged `[Receipt] <vendor>`) so the existing summary,
goal, and chart aggregates keep working without per-call branching.

Data model
──────────
Receipt        — header (date, vendor, category, currency, totals, notes)
ReceiptItem    — line items (name, qty, unit_price, line_total)
ExpenseItem    — item catalogue with rolling last/avg/min/max price stats,
                 updated automatically as receipts are saved. Use
                 `search_items(query)` for autocomplete in entry forms.

A receipt's `transaction_id` points to the linked row in `transactions`;
saving / updating / soft-deleting a receipt keeps the transaction in sync.
Standalone expenses (e.g. "rent", "gas") that don't need line-item detail
can still be entered directly via FinanceStore.add_transaction.
"""

from __future__ import annotations

import re
import uuid
from dataclasses import dataclass, field
from datetime import date as _date

from src.data.database import get_connection
from src.data.finance_store import FinanceStore
from src.utils.timestamps import now_utc


# ── Categories ────────────────────────────────────────────────────────────────
# A friendly, opinionated default set that covers the user's mentioned
# buckets (Groceries, Utilities, Education, Side Expenses, Rent…). The list
# is duplicated in the Earnings tab's existing EXPENSE_CATEGORIES for
# transactions written directly through the ledger; here we add Groceries
# and Side Expenses which the ledger lacked.
EXPENSE_CATEGORIES = [
    "Groceries",
    "Rent / Housing",
    "Utilities",
    "Transportation",
    "Food & Drink",
    "Education",
    "Side Expenses",
    "Software / Tools",
    "Hardware",
    "Office Supplies",
    "Travel",
    "Health / Medical",
    "Subscriptions",
    "Entertainment",
    "Taxes",
    "Fees & Banking",
    "Gifts",
    "Other",
]

PAYMENT_METHODS = ["cash", "card", "bank", "ic / e-money", "other"]


# ── Dataclasses ───────────────────────────────────────────────────────────────

@dataclass
class ReceiptItem:
    id:         str
    receipt_id: str
    item_id:    str   = ""
    name:       str   = ""
    qty:        float = 1.0
    unit_price: float = 0.0
    line_total: float = 0.0
    notes:      str   = ""
    sort_order: int   = 0


@dataclass
class Receipt:
    id:             str
    date:           str
    vendor:         str            = ""
    category:       str            = "Other"
    currency:       str            = "JPY"
    subtotal:       float          = 0.0
    tax:            float          = 0.0
    total:          float          = 0.0
    payment_method: str            = "cash"
    notes:          str            = ""
    transaction_id: str            = ""
    updated_at:     str            = ""
    deleted:        bool           = False
    items:          list[ReceiptItem] = field(default_factory=list)


@dataclass
class ExpenseItem:
    id:              str
    name:            str
    normalized_name: str
    category:        str   = ""
    last_price:      float = 0.0
    last_currency:   str   = "JPY"
    last_seen_date:  str   = ""
    times_seen:      int   = 0
    avg_price:       float = 0.0
    min_price:       float = 0.0
    max_price:       float = 0.0
    updated_at:      str   = ""
    deleted:         bool  = False


# ── Helpers ───────────────────────────────────────────────────────────────────

_NORM_RE = re.compile(r"[^a-z0-9]+")


def _normalize(name: str) -> str:
    """Lowercase + strip non-alphanumerics for fuzzy item matching."""
    return _NORM_RE.sub(" ", (name or "").lower()).strip()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ExpensesStore
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ExpensesStore:
    """Receipts, receipt items, and item-price catalogue."""

    def __init__(self, finance_store: FinanceStore | None = None):
        # Receipts mirror into the existing transactions ledger so everything
        # else (earnings summary, charts, tax export) keeps working unchanged.
        self._fs = finance_store or FinanceStore()

    # ── Receipts ──────────────────────────────────────────────────────────────

    def save_receipt(self, receipt: Receipt,
                     items: list[ReceiptItem] | None = None) -> Receipt:
        """Insert or update a receipt + items + linked transaction.

        Items, if supplied, REPLACE any existing line items on the receipt.
        Each item updates the catalogue's rolling price stats.
        """
        if items is None:
            items = receipt.items
        if not receipt.id:
            receipt.id = str(uuid.uuid4())
        receipt.updated_at = now_utc()

        # Recompute totals from items if any were given (defensive — UI
        # already does this but we re-derive so the DB stays consistent).
        if items:
            receipt.subtotal = sum(it.line_total for it in items)
            receipt.total    = receipt.subtotal + (receipt.tax or 0.0)

        conn = get_connection()
        try:
            conn.execute(
                """INSERT INTO receipts
                   (id, transaction_id, date, vendor, category, currency,
                    subtotal, tax, total, payment_method, notes,
                    updated_at, deleted)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(id) DO UPDATE SET
                     transaction_id=excluded.transaction_id,
                     date=excluded.date, vendor=excluded.vendor,
                     category=excluded.category, currency=excluded.currency,
                     subtotal=excluded.subtotal, tax=excluded.tax,
                     total=excluded.total,
                     payment_method=excluded.payment_method,
                     notes=excluded.notes, updated_at=excluded.updated_at,
                     deleted=excluded.deleted""",
                (receipt.id, receipt.transaction_id, receipt.date,
                 receipt.vendor, receipt.category, receipt.currency,
                 receipt.subtotal, receipt.tax, receipt.total,
                 receipt.payment_method, receipt.notes,
                 receipt.updated_at, int(receipt.deleted)),
            )

            # Items: wipe and re-insert. Receipts are small and this keeps
            # the implementation honest about line-item identity.
            conn.execute("DELETE FROM receipt_items WHERE receipt_id=?",
                         (receipt.id,))
            for i, item in enumerate(items):
                if not item.id:
                    item.id = str(uuid.uuid4())
                item.receipt_id = receipt.id
                if not item.sort_order:
                    item.sort_order = i
                conn.execute(
                    """INSERT INTO receipt_items
                       (id, receipt_id, item_id, name, qty, unit_price,
                        line_total, notes, sort_order)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (item.id, item.receipt_id, item.item_id or "",
                     item.name, float(item.qty), float(item.unit_price),
                     float(item.line_total), item.notes or "",
                     int(item.sort_order)),
                )
            conn.commit()
        finally:
            conn.close()

        # Update catalogue stats outside of the transaction; failures here
        # must not roll back the receipt write.
        for item in items:
            if (item.name or "").strip() and item.unit_price > 0:
                self._upsert_item_stats(
                    name=item.name,
                    price=float(item.unit_price),
                    currency=receipt.currency,
                    seen_date=receipt.date,
                    category=receipt.category,
                )

        # Mirror into the transactions ledger
        self._sync_transaction_for_receipt(receipt)

        receipt.items = items
        return receipt

    def get_receipt(self, receipt_id: str) -> Receipt | None:
        conn = get_connection()
        try:
            row = conn.execute(
                "SELECT * FROM receipts WHERE id=? AND deleted=0",
                (receipt_id,),
            ).fetchone()
            if not row:
                return None
            r = self._row_to_receipt(row)
            r.items = self._items_for(conn, receipt_id)
            return r
        finally:
            conn.close()

    def get_receipts(self, start: str | None = None, end: str | None = None,
                     category: str | None = None,
                     vendor_query: str | None = None,
                     ) -> list[Receipt]:
        q = "SELECT * FROM receipts WHERE deleted=0"
        params: list = []
        if start:
            q += " AND date >= ?"; params.append(start)
        if end:
            q += " AND date <= ?"; params.append(end)
        if category and category != "All":
            q += " AND category = ?"; params.append(category)
        if vendor_query:
            q += " AND lower(vendor) LIKE ?"; params.append(f"%{vendor_query.lower()}%")
        q += " ORDER BY date DESC, updated_at DESC"
        conn = get_connection()
        try:
            rows = conn.execute(q, params).fetchall()
            results: list[Receipt] = []
            for row in rows:
                r = self._row_to_receipt(row)
                r.items = self._items_for(conn, r.id)
                results.append(r)
            return results
        finally:
            conn.close()

    def delete_receipt(self, receipt_id: str) -> None:
        """Soft-delete the receipt and its linked transaction."""
        rec = self.get_receipt(receipt_id)
        conn = get_connection()
        try:
            conn.execute(
                "UPDATE receipts SET deleted=1, updated_at=? WHERE id=?",
                (now_utc(), receipt_id),
            )
            conn.commit()
        finally:
            conn.close()
        if rec and rec.transaction_id:
            self._fs.delete_transaction(rec.transaction_id)

    def _sync_transaction_for_receipt(self, receipt: Receipt) -> None:
        """Create or update the ledger row that represents this receipt."""
        desc = f"[Receipt] {receipt.vendor or receipt.category}"
        if receipt.transaction_id:
            txns = [t for t in self._fs.get_transactions()
                    if t.id == receipt.transaction_id]
            if txns:
                t = txns[0]
                t.date        = receipt.date
                t.amount      = float(receipt.total)
                t.type        = "expense"
                t.category    = receipt.category
                t.description = desc
                t.currency    = receipt.currency
                t.is_job_pay  = False
                self._fs.update_transaction(t)
                # Stamp receipt_id on the row (FinanceStore doesn't carry it
                # in the dataclass but we set it directly here).
                conn = get_connection()
                try:
                    conn.execute(
                        "UPDATE transactions SET receipt_id=? WHERE id=?",
                        (receipt.id, t.id),
                    )
                    conn.commit()
                finally:
                    conn.close()
                return

        # No linked transaction yet — create one
        new_txn = self._fs.add_transaction(
            date=receipt.date,
            amount=float(receipt.total),
            txn_type="expense",
            category=receipt.category,
            description=desc,
            currency=receipt.currency,
            is_job_pay=False,
        )
        # Patch the receipt row with the linkage and tag the txn with the receipt
        conn = get_connection()
        try:
            conn.execute(
                "UPDATE receipts SET transaction_id=? WHERE id=?",
                (new_txn.id, receipt.id),
            )
            conn.execute(
                "UPDATE transactions SET receipt_id=? WHERE id=?",
                (receipt.id, new_txn.id),
            )
            conn.commit()
        finally:
            conn.close()
        receipt.transaction_id = new_txn.id

    @staticmethod
    def _row_to_receipt(row) -> Receipt:
        return Receipt(
            id=row["id"], date=row["date"],
            vendor=row["vendor"] or "",
            category=row["category"] or "Other",
            currency=row["currency"] or "JPY",
            subtotal=row["subtotal"] or 0.0,
            tax=row["tax"] or 0.0,
            total=row["total"] or 0.0,
            payment_method=row["payment_method"] or "cash",
            notes=row["notes"] or "",
            transaction_id=row["transaction_id"] or "",
            updated_at=row["updated_at"] or "",
            deleted=bool(row["deleted"]),
        )

    @staticmethod
    def _items_for(conn, receipt_id: str) -> list[ReceiptItem]:
        rows = conn.execute(
            "SELECT * FROM receipt_items WHERE receipt_id=? "
            "ORDER BY sort_order ASC, rowid ASC",
            (receipt_id,),
        ).fetchall()
        return [ReceiptItem(
            id=r["id"], receipt_id=r["receipt_id"],
            item_id=r["item_id"] or "",
            name=r["name"], qty=r["qty"], unit_price=r["unit_price"],
            line_total=r["line_total"], notes=r["notes"] or "",
            sort_order=r["sort_order"] or 0,
        ) for r in rows]

    # ── Item catalogue ────────────────────────────────────────────────────────

    def search_items(self, query: str, limit: int = 12) -> list[ExpenseItem]:
        """Fuzzy-match items by normalized name. Empty query returns
        the most-frequently-seen items."""
        conn = get_connection()
        try:
            if not query.strip():
                rows = conn.execute(
                    "SELECT * FROM expense_items WHERE deleted=0 "
                    "ORDER BY times_seen DESC, last_seen_date DESC LIMIT ?",
                    (limit,),
                ).fetchall()
            else:
                norm = _normalize(query)
                rows = conn.execute(
                    "SELECT * FROM expense_items WHERE deleted=0 "
                    "AND normalized_name LIKE ? "
                    "ORDER BY times_seen DESC, last_seen_date DESC LIMIT ?",
                    (f"%{norm}%", limit),
                ).fetchall()
            return [self._row_to_item(r) for r in rows]
        finally:
            conn.close()

    def get_all_items(self, sort_by: str = "name") -> list[ExpenseItem]:
        order = {
            "name":    "name COLLATE NOCASE ASC",
            "price":   "last_price DESC",
            "seen":    "times_seen DESC",
            "recent":  "last_seen_date DESC",
        }.get(sort_by, "name COLLATE NOCASE ASC")
        conn = get_connection()
        try:
            rows = conn.execute(
                f"SELECT * FROM expense_items WHERE deleted=0 ORDER BY {order}"
            ).fetchall()
            return [self._row_to_item(r) for r in rows]
        finally:
            conn.close()

    def delete_item(self, item_id: str) -> None:
        conn = get_connection()
        try:
            conn.execute(
                "UPDATE expense_items SET deleted=1, updated_at=? WHERE id=?",
                (now_utc(), item_id),
            )
            conn.commit()
        finally:
            conn.close()

    def _upsert_item_stats(self, name: str, price: float, currency: str,
                           seen_date: str, category: str = "") -> None:
        """Insert or roll the price stats for `name` after a receipt write."""
        norm = _normalize(name)
        if not norm:
            return
        conn = get_connection()
        try:
            row = conn.execute(
                "SELECT * FROM expense_items WHERE normalized_name=? AND deleted=0",
                (norm,),
            ).fetchone()
            now = now_utc()
            if row is None:
                conn.execute(
                    """INSERT INTO expense_items
                       (id, name, normalized_name, category, last_price,
                        last_currency, last_seen_date, times_seen,
                        avg_price, min_price, max_price, updated_at, deleted)
                       VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?, ?, ?, ?, 0)""",
                    (str(uuid.uuid4()), name.strip(), norm, category,
                     price, currency, seen_date, price, price, price, now),
                )
            else:
                seen     = (row["times_seen"] or 0) + 1
                avg      = ((row["avg_price"] or 0.0) * (seen - 1) + price) / seen
                min_p    = min(row["min_price"] or price, price)
                max_p    = max(row["max_price"] or price, price)
                # Prefer the more specific name we already have
                conn.execute(
                    """UPDATE expense_items SET
                         last_price=?, last_currency=?, last_seen_date=?,
                         times_seen=?, avg_price=?, min_price=?, max_price=?,
                         category=COALESCE(NULLIF(category,''), ?),
                         updated_at=?
                       WHERE id=?""",
                    (price, currency, seen_date, seen, avg, min_p, max_p,
                     category, now, row["id"]),
                )
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def _row_to_item(row) -> ExpenseItem:
        return ExpenseItem(
            id=row["id"], name=row["name"],
            normalized_name=row["normalized_name"],
            category=row["category"] or "",
            last_price=row["last_price"] or 0.0,
            last_currency=row["last_currency"] or "JPY",
            last_seen_date=row["last_seen_date"] or "",
            times_seen=row["times_seen"] or 0,
            avg_price=row["avg_price"] or 0.0,
            min_price=row["min_price"] or 0.0,
            max_price=row["max_price"] or 0.0,
            updated_at=row["updated_at"] or "",
            deleted=bool(row["deleted"]),
        )

    def get_item_vendor_stats(self, item_name: str) -> list[dict]:
        """Per-vendor price stats for an item, derived from receipt line items."""
        norm = _normalize(item_name)
        if not norm:
            return []
        conn = get_connection()
        try:
            rows = conn.execute(
                """SELECT r.vendor, ri.currency,
                          COUNT(*) AS times_seen,
                          MIN(ri.unit_price) AS min_price,
                          MAX(ri.unit_price) AS max_price,
                          AVG(ri.unit_price) AS avg_price,
                          MAX(r.date) AS last_date
                   FROM receipt_items ri
                   JOIN receipts r ON ri.receipt_id = r.id
                   WHERE r.deleted = 0
                     AND lower(ri.name) LIKE ?
                   GROUP BY r.vendor, ri.currency
                   ORDER BY times_seen DESC""",
                (f"%{norm}%",),
            ).fetchall()
            return [
                {
                    "vendor":     r["vendor"] or "Unknown",
                    "currency":   r["currency"] or "JPY",
                    "times_seen": r["times_seen"],
                    "min_price":  r["min_price"] or 0.0,
                    "max_price":  r["max_price"] or 0.0,
                    "avg_price":  r["avg_price"] or 0.0,
                    "last_date":  r["last_date"] or "",
                }
                for r in rows
            ]
        finally:
            conn.close()

    # ── Aggregates ────────────────────────────────────────────────────────────

    def summary(self, start: str, end: str,
                rate: float = 150.0) -> dict:
        """Period summary across both receipt and standalone expenses."""
        txns = [t for t in self._fs.get_transactions(start, end, "expense")]
        total_usd = 0.0
        by_cat: dict[str, float] = {}
        for t in txns:
            usd = t.amount / rate if t.currency == "JPY" else t.amount
            total_usd += usd
            by_cat[t.category] = by_cat.get(t.category, 0.0) + usd
        return {
            "total_usd": total_usd,
            "by_category": by_cat,
            "count": len(txns),
        }
