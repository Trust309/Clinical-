"""Utility helpers for the Airbnb business agents."""

import json
import uuid
from datetime import date, datetime, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


def generate_id(prefix: str = "") -> str:
    """Generate a unique ID with an optional prefix."""
    short_id = uuid.uuid4().hex[:8]
    return f"{prefix}_{short_id}" if prefix else short_id


def date_range(start: date, end: date):
    """Yield each date in the range [start, end)."""
    current = start
    while current < end:
        yield current
        current += timedelta(days=1)


def load_json(filepath: str | Path) -> dict:
    """Load JSON data from a file."""
    filepath = Path(filepath)
    if not filepath.exists():
        return {}
    with open(filepath, "r") as f:
        return json.load(f)


def save_json(filepath: str | Path, data: dict) -> None:
    """Save data as JSON to a file."""
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2, default=str)


def format_currency(amount: float) -> str:
    """Format a number as currency."""
    return f"${amount:,.2f}"


def days_between(d1: date, d2: date) -> int:
    """Return the number of days between two dates."""
    return abs((d2 - d1).days)


def is_weekend(d: date) -> bool:
    """Check if a date falls on a weekend."""
    return d.weekday() >= 5


def get_season(d: date) -> str:
    """Determine the season for a given date (Northern Hemisphere)."""
    month = d.month
    if month in (12, 1, 2):
        return "winter"
    elif month in (3, 4, 5):
        return "spring"
    elif month in (6, 7, 8):
        return "summer"
    else:
        return "fall"


def occupancy_rate(booked_nights: int, total_nights: int) -> float:
    """Calculate occupancy rate as a percentage."""
    if total_nights == 0:
        return 0.0
    return round((booked_nights / total_nights) * 100, 1)
