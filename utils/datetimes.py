import re
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
