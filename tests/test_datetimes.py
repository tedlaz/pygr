from datetime import date

import pytest

from utils.datetimes import (
    date2gr,
    gr2date,
    gr2iso,
    is_greek_date,
    iso2gr,
    iso2yearmonth,
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
