"""Current system date and time helpers."""

from datetime import datetime


def get_current_date() -> str:
    """Return today's system date in a readable format."""
    return datetime.now().strftime("%A, %B %d, %Y")


def get_current_time() -> str:
    """Return the current system time in 12-hour format."""
    return datetime.now().strftime("%I:%M:%S %p")
