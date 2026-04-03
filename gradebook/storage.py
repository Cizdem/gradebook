"""Persistence layer: load/save gradebook data as JSON."""

import json
import logging
from pathlib import Path

from .models import Student, Course, Enrollment

logger = logging.getLogger(__name__)

DEFAULT_PATH = Path("data/gradebook.json")


def load_data(path: Path = DEFAULT_PATH) -> dict:
    """Load gradebook data from a JSON file.

    Returns a dict with keys 'students', 'courses', 'enrollments'.
    Starts empty on FileNotFoundError; logs and returns empty on JSONDecodeError.
    """
    empty = {"students": [], "courses": [], "enrollments": []}
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        logger.info("Data loaded from %s", path)
        return {
            "students": [Student.from_dict(s) for s in raw.get("students", [])],
            "courses": [Course.from_dict(c) for c in raw.get("courses", [])],
            "enrollments": [Enrollment.from_dict(e) for e in raw.get("enrollments", [])],
        }
    except FileNotFoundError:
        logger.info("No data file found at %s — starting fresh.", path)
        return empty
    except json.JSONDecodeError as exc:
        logger.error("Could not parse %s: %s — starting fresh.", path, exc)
        print(f"Warning: '{path}' contains invalid JSON. Starting with an empty gradebook.")
        return empty


def save_data(data: dict, path: Path = DEFAULT_PATH) -> None:
    """Save gradebook data to a JSON file.

    Args:
        data: dict with keys 'students', 'courses', 'enrollments' holding model objects.
        path: destination path (parent directories are created if needed).
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        payload = {
            "students": [s.to_dict() for s in data.get("students", [])],
            "courses": [c.to_dict() for c in data.get("courses", [])],
            "enrollments": [e.to_dict() for e in data.get("enrollments", [])],
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        logger.info("Data saved to %s", path)
    except OSError as exc:
        logger.error("Failed to save data to %s: %s", path, exc)
        raise
