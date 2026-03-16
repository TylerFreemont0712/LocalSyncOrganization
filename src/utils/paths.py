"""Cross-platform path utilities."""

from pathlib import Path, PurePosixPath


def normalize_path(path: str | Path) -> str:
    """Convert a path to forward-slash form for consistent storage."""
    return PurePosixPath(Path(path)).as_posix()


def ensure_parent(path: Path):
    """Create parent directories if they don't exist."""
    path.parent.mkdir(parents=True, exist_ok=True)
