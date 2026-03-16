"""Data layer — storage backends for all modules."""

from src.data.database import get_connection, init_db
from src.data.notes_store import NotesStore, Note
from src.data.calendar_store import CalendarStore, Event
from src.data.finance_store import FinanceStore, Transaction, DEFAULT_CATEGORIES

__all__ = [
    "get_connection", "init_db",
    "NotesStore", "Note",
    "CalendarStore", "Event",
    "FinanceStore", "Transaction", "DEFAULT_CATEGORIES",
]
