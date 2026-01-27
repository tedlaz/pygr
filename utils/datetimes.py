import re
from calendar import SATURDAY, SUNDAY, monthrange
from datetime import datetime


def iso2gr(iso_date_str: str) -> str:
    """
    Convert an ISO 8601 date string (YYYY-MM-DD) to a Gregorian date tuple (year, month, day).

    Parameters:
    iso_date_str (str): Date string in ISO 8601 format.

    Returns:
    tuple: A tuple containing (year, month, day) as integers.
    """
    year, month, day = iso_date_str.split("-")
    return f"{day}/{month}/{year}"


def gr2iso(gr_date: str) -> str:
    """
    Convert a Gregorian date string (DD/MM/YYYY) to an ISO 8601 date string (YYYY-MM-DD).

    Parameters:
    gr_date_str (str): Date string in Gregorian format.

    Returns:
    str: Date string in ISO 8601 format.
    """
    day, month, year = gr_date.split("/")
    return f"{year}-{month}-{day}"


def date2gr(date_obj: datetime.date) -> str:
    """
    Convert a date object to a Gregorian date string (DD/MM/YYYY).

    Parameters:
    date_obj (date): A date object.

    Returns:
    str: Date string in Gregorian format.
    """
    return date_obj.strftime("%d/%m/%Y")


def gr2date(gr_date: str) -> datetime.date:
    """
    Convert a Gregorian date string (DD/MM/YYYY) to a date object.

    Parameters:
    gr_date_str (str): Date string in Gregorian format.

    Returns:
    date: A date object.
    """

    return datetime.strptime(gr_date, "%d/%m/%Y").date()


def iso2yearmonth(isodate: str) -> str:
    """2023-01-15 => 2023-01"""
    return isodate[:7]


def is_greek_date(grdate: str) -> bool:
    return re.match(r"\d{2}\/\d{2}\/\d{4}", grdate, re.I) is not None


def delta_hours(date_from: datetime, date_to: datetime) -> float:
    """Returns hours between two datetime objects"""
    delta = abs(date_to - date_from)
    return round(delta.seconds / 3600, 1)


def round_half(hours: float) -> float:
    """Hours rounded to nearest half hour"""
    return round(hours * 2) / 2


def month_monday2friday_days(year: int, month: int) -> int:
    """Calculate the number of working days in a given month, excluding weekends and specified holidays."""

    total_days = monthrange(year, month)[1]
    working_days = 0

    for day in range(1, total_days + 1):
        current_date = datetime(year, month, day).date()
        if current_date.weekday() not in (SATURDAY, SUNDAY):
            working_days += 1

    return working_days


def month_specific_days(year: int, month: int, weekdays: set[int]) -> int:
    """Calculate the number of specific weekdays in a given month.

    :param year: The year as an integer.
    :param month: The month as an integer (1-12).
    :param weekdays: A set of integers representing the weekdays to count (0=Monday, 6=Sunday).
    :return: The count of specified weekdays in the month.
    """
    total_days = monthrange(year, month)[1]
    specific_days_count = 0

    for day in range(1, total_days + 1):
        current_date = datetime(year, month, day).date()
        if current_date.weekday() in weekdays:
            specific_days_count += 1

    return specific_days_count


def month_specific_days_gr(
    year: int, month: int, wdays: str = "ΔΕΥΤΕΡΑ-ΠΑΡΑΣΚΕΥΗ"
) -> int:
    """Calculate the number of specific weekdays in a given month.

    :param year: The year as an integer.
    :param month: The month as an integer (1-12).
    :param wdays: A string representing the weekdays to count (Δ=0, Τ=1, Τρ=2, Π=3, Πρ=4, Σ=5, Κ=6).
    :return: The count of specified weekdays in the month.
    """
    weekday_map = {
        "ΔΕΥΤΕΡΑ": 0,
        "ΤΡΙΤΗ": 1,
        "ΤΕΤΑΡΤΗ": 2,
        "ΠΕΜΠΤΗ": 3,
        "ΠΑΡΑΣΚΕΥΗ": 4,
        "ΣΑΒΒΑΤΟ": 5,
        "ΚΥΡΙΑΚΗ": 6,
    }

    if "-" in wdays:
        start_day, end_day = wdays.split("-")
        start_idx = weekday_map[start_day]
        end_idx = weekday_map[end_day]
        if start_idx > end_idx:
            end_idx += 7
        weekdays = {i % 7 for i in range(start_idx, end_idx + 1)}

    elif "," in wdays:
        days = wdays.split(",")
        weekdays = {weekday_map[day.strip()] for day in days}

    else:
        weekdays = {weekday_map[wdays.strip()]}

    return month_specific_days(year, month, weekdays)
