from datetime import date, datetime

import pytest

from utils.datetimes import (
    date2gr,
    delta_hours,
    gr2date,
    gr2iso,
    is_greek_date,
    iso2gr,
    iso2yearmonth,
    month_monday2friday_days,
    month_specific_days,
    month_specific_days_gr,
    round_half,
)


@pytest.mark.parametrize(
    "iso_date,gr_date",
    [
        ("2024-06-15", "15/06/2024"),
        ("1999-12-31", "31/12/1999"),
        ("2000-01-01", "01/01/2000"),
    ],
)
def test_iso2gr(iso_date, gr_date):
    assert iso2gr(iso_date) == gr_date


@pytest.mark.parametrize(
    "gr_date,iso_date",
    [
        ("15/06/2024", "2024-06-15"),
        ("31/12/1999", "1999-12-31"),
        ("01/01/2000", "2000-01-01"),
    ],
)
def test_gr2iso(gr_date, iso_date):
    assert gr2iso(gr_date) == iso_date


@pytest.mark.parametrize(
    "date_obj,expected_gr_date",
    [
        (date(2024, 6, 15), "15/06/2024"),
        (date(1999, 12, 31), "31/12/1999"),
        (date(2000, 1, 1), "01/01/2000"),
    ],
)
def test_date2gr(date_obj, expected_gr_date):
    assert date2gr(date_obj) == expected_gr_date


@pytest.mark.parametrize(
    "gr_date,expected_date_obj",
    [
        ("15/06/2024", date(2024, 6, 15)),
        ("31/12/1999", date(1999, 12, 31)),
        ("01/01/2000", date(2000, 1, 1)),
    ],
)
def test_gr2date(gr_date, expected_date_obj):
    assert gr2date(gr_date) == expected_date_obj


@pytest.mark.parametrize(
    "isodate,expected_yearmonth",
    [
        ("2024-06-15", "2024-06"),
        ("1999-12-31", "1999-12"),
        ("2000-01-01", "2000-01"),
    ],
)
def test_iso2yearmonth(isodate, expected_yearmonth):
    assert iso2yearmonth(isodate) == expected_yearmonth


@pytest.mark.parametrize(
    "date,expected_greek",
    [
        ("15/06/2024", True),
        ("31/12/1999", True),
        ("01/01/2000", True),
        ("2024-06-15", False),
        ("1999-12-31", False),
        ("2000-01-01", False),
    ],
)
def test_is_greek_date(date, expected_greek):
    assert is_greek_date(date) == expected_greek


@pytest.mark.parametrize(
    "date_from,date_to,expected_hours",
    [
        ("2024-06-15T08:00", "2024-06-15T12:00", 4.0),
        ("2024-06-15T12:00", "2024-06-15T08:00", 4.0),
        ("2024-06-15T22:00", "2024-06-16T02:00", 4.0),
        ("2024-06-15T10:30", "2024-06-15T13:15", 2.8),
        ("2024-06-15T23:45", "2024-06-16T00:15", 0.5),
    ],
)
def test_delta_hours(date_from, date_to, expected_hours):
    dtfrom = datetime.fromisoformat(date_from)
    dtto = datetime.fromisoformat(date_to)
    assert delta_hours(dtfrom, dtto) == expected_hours


@pytest.mark.parametrize(
    "value,expected_rounded",
    [
        (2.3, 2.5),
        (2.1, 2.0),
        (3.75, 4.0),
        (4.25, 4.0),
        (5.0, 5.0),
    ],
)
def test_round_half(value, expected_rounded):
    assert round_half(value) == expected_rounded


@pytest.mark.parametrize(
    "year,month,expected",
    [(2024, 6, 20), (2024, 7, 23), (2024, 8, 22), (2026, 1, 22)],
)
def test_month_monday2friday_days(year, month, expected):
    assert month_monday2friday_days(year, month) == expected


@pytest.mark.parametrize(
    "year,month,weekdays,expected",
    [
        (2024, 6, {0}, 4),  # Mondays in June 2024
        (2024, 7, {1}, 5),  # Tuesdays in July 2024
        (2024, 8, {2}, 4),  # Wednesdays in August 2024
        (2026, 1, {3, 4}, 10),  # Thursdays and Fridays in January 2026
    ],
)
def test_month_specific_days(year, month, weekdays, expected):
    assert month_specific_days(year, month, weekdays) == expected


@pytest.mark.parametrize(
    "year,month,wdays,expected",
    [
        (2024, 6, "ΔΕΥΤΕΡΑ", 4),  # Mondays in June 2024
        (2024, 7, "ΤΡΙΤΗ", 5),  # Tuesdays in July 2024
        (2024, 8, "ΤΕΤΑΡΤΗ", 4),  # Wednesdays in August 2024
        (2026, 1, "ΠΕΜΠΤΗ, ΠΑΡΑΣΚΕΥΗ", 10),
        (2026, 1, "ΔΕΥΤΕΡΑ-ΠΑΡΑΣΚΕΥΗ", 22),
        (2026, 1, "ΔΕΥΤΕΡΑ,ΠΑΡΑΣΚΕΥΗ", 9),
        (2026, 1, "ΤΕΤΑΡΤΗ-ΠΑΡΑΣΚΕΥΗ", 14),
        (2026, 1, "ΤΕΤΑΡΤΗ-ΔΕΥΤΕΡΑ", 27),
    ],
)
def test_month_specific_days_gr(year, month, wdays, expected):
    assert month_specific_days_gr(year, month, wdays) == expected


def test_month_specific_days_gr_default_days():
    # Default is Monday to Friday
    assert month_specific_days_gr(2024, 6) == 20  # June 2024 has 20 working weekdays


def test_month_specific_days_gr_error():
    with pytest.raises(KeyError):
        month_specific_days_gr(2024, 6, "INVALID_DAY")
