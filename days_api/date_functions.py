"""Functions for working with dates."""

from datetime import datetime, date


def convert_to_datetime(date_val: str) -> datetime:
    """Change from sting to datetime"""
    try:
        return datetime.strptime(date_val, "%d.%m.%Y")
    except ValueError as error:
        raise ValueError("Unable to convert value to datetime.") from error


def get_days_between(first: datetime, last: datetime) -> int:
    """Find the number of days between the first and last date"""
    if isinstance(first, datetime) and isinstance(last, datetime):
        return (last - first).days
    raise TypeError("Datetimes required.")


def get_day_of_week_on(date_val: datetime) -> str:
    """Find the name of the day the week is on"""
    if isinstance(date_val, datetime):
        return date_val.strftime("%A")
    raise TypeError("Datetime required.")


def get_current_age(birthdate: date) -> int:
    """Find your current age from your birthday"""
    if isinstance(birthdate, date):
        return int((date.today() - birthdate).days//365.25)
    raise TypeError("Date required.")
