"""Datetime handling utilities for the Virtual Gas Meter integration."""
from datetime import datetime, timedelta, date

# Supported datetime formats (in order of precedence)
DATETIME_FORMATS = [
    '%Y-%m-%d %H:%M:%S.%f%z',  # Full with microseconds and timezone
    '%Y-%m-%d %H:%M:%S%z',     # With timezone
    '%Y-%m-%d %H:%M:%S.%f',    # With microseconds
    '%Y-%m-%d %H:%M:%S',       # Standard datetime
    '%Y-%m-%d %H:%M',          # Without seconds
    '%Y-%m-%d',                # Date only (defaults to midnight)
    '%m/%d/%Y',                # US format date only
    '%m/%d/%Y %H:%M',          # US format with time
]


def string_to_datetime(datetime_string: str) -> datetime:
    """
    Parse a datetime string into a datetime object.

    Supports multiple formats including date-only (defaults to midnight).
    """
    if not datetime_string:
        raise ValueError("Empty datetime string")

    datetime_string = str(datetime_string).strip()

    for fmt in DATETIME_FORMATS:
        try:
            return datetime.strptime(datetime_string, fmt)
        except ValueError:
            continue

    # If no format matched, raise an error with helpful message
    raise ValueError(
        f"Unable to parse datetime '{datetime_string}'. "
        f"Supported formats: YYYY-MM-DD, YYYY-MM-DD HH:MM, MM/DD/YYYY"
    )
