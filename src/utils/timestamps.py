"""Timestamp utilities for sync and data."""

from datetime import datetime, timezone


def now_utc() -> str:
    """ISO-8601 UTC timestamp string."""
    return datetime.now(timezone.utc).isoformat()


def parse_ts(ts: str) -> datetime:
    """Parse an ISO-8601 timestamp string."""
    return datetime.fromisoformat(ts)
