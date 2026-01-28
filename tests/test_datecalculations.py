from datetime import datetime

import pytest

from utils.datecalculations import (
    day_night_hours_from_range,
    daynight_hours,
    delta_hours,
    do_overlap,
    month_monday2friday_days,
    month_specific_days,
    month_specific_days_gr,
    round_half,
    time_range,
)


@pytest.mark.parametrize(
    "year,month,expected",
    [(2024, 6, 20), (2024, 7, 23), (2024, 8, 22), (2026, 1, 22)],
)
def test_month_monday2friday_days(year, month, expected):
    assert month_monday2friday_days(year, month) == expected


def test_month_specific_days_gr_default_days():
    # Default is Monday to Friday
    assert month_specific_days_gr(2024, 6) == 20  # June 2024 has 20 working weekdays


def test_month_specific_days_gr_error():
    with pytest.raises(KeyError):
        month_specific_days_gr(2024, 6, "INVALID_DAY")


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
    "dfrom,dto,expected_day_hours,expected_night_hours",
    [
        (
            datetime(2023, 1, 1, 5, 0),
            datetime(2023, 1, 1, 10, 0),
            4.0,
            1.0,
        ),
        (
            datetime(2023, 1, 1, 21, 0),
            datetime(2023, 1, 2, 7, 0),
            2.0,
            8.0,
        ),
        (
            datetime(2023, 1, 1, 23, 0),
            datetime(2023, 1, 2, 5, 0),
            0.0,
            6.0,
        ),
        (
            datetime(2023, 1, 1, 8, 0),
            datetime(2023, 1, 1, 18, 0),
            10.0,
            0.0,
        ),
        (
            datetime(2023, 1, 1, 18, 0),
            datetime(2023, 1, 2, 8, 0),
            6.0,
            8.0,
        ),
        (
            datetime(2026, 1, 1, 0, 0),
            datetime(2026, 1, 1, 6, 0),
            0.0,
            6.0,
        ),
        (
            datetime(2026, 1, 1, 6, 0),
            datetime(2026, 1, 1, 22, 0),
            16.0,
            0.0,
        ),
        (
            datetime(2026, 1, 1, 22, 0),
            datetime(2026, 1, 2, 6, 0),
            0,
            8.0,
        ),
        (
            datetime(2026, 1, 1, 0, 0),
            datetime(2026, 1, 1, 10, 0),
            4.0,
            6.0,
        ),
        (
            datetime(2026, 1, 1, 0, 30),
            datetime(2026, 1, 1, 10, 30),
            4.5,
            5.5,
        ),
        (
            datetime(2026, 1, 1, 0, 25),
            datetime(2026, 1, 1, 10, 34),
            4.6,
            5.6,
        ),
    ],
)
def test_daynight_hours(dfrom, dto, expected_day_hours, expected_night_hours):
    hours = daynight_hours(dfrom, dto)
    assert hours.day_hours == expected_day_hours
    assert hours.night_hours == expected_night_hours
    assert hours.total_hours == expected_day_hours + expected_night_hours


@pytest.mark.parametrize(
    "dfrom1,dto1,dfrom2,dto2,expected",
    [
        (
            datetime(2023, 1, 1, 5, 0),
            datetime(2023, 1, 1, 10, 0),
            datetime(2023, 1, 1, 8, 0),
            datetime(2023, 1, 1, 12, 0),
            True,
        ),
        (
            datetime(2023, 1, 1, 8, 0),
            datetime(2023, 1, 1, 12, 0),
            datetime(2023, 1, 1, 5, 0),
            datetime(2023, 1, 1, 10, 0),
            True,
        ),
        (
            datetime(2023, 1, 1, 5, 0),
            datetime(2023, 1, 1, 10, 0),
            datetime(2023, 1, 1, 10, 0),
            datetime(2023, 1, 1, 12, 0),
            False,
        ),
        (
            datetime(2023, 1, 1, 10, 0),
            datetime(2023, 1, 1, 12, 0),
            datetime(2023, 1, 1, 5, 0),
            datetime(2023, 1, 1, 10, 0),
            False,
        ),
        (
            datetime(2023, 1, 1, 5, 0),
            datetime(2023, 1, 1, 10, 0),
            datetime(2023, 1, 1, 4, 0),
            datetime(2023, 1, 1, 6, 0),
            True,
        ),
        (
            datetime(2023, 1, 1, 5, 0),
            datetime(2023, 1, 1, 10, 0),
            datetime(2023, 1, 1, 11, 0),
            datetime(2023, 1, 1, 12, 0),
            False,
        ),
    ],
)
def test_do_overlap(dfrom1, dto1, dfrom2, dto2, expected):
    result = do_overlap(dfrom1, dto1, dfrom2, dto2)
    assert result == expected


@pytest.mark.parametrize(
    "dfromto,expected",
    [
        (
            "2024-01-01T08:00T16:00",
            (datetime(2024, 1, 1, 8, 0), datetime(2024, 1, 1, 16, 0)),
        ),
        (
            "2024-12-31T22:30T06:30",
            (datetime(2024, 12, 31, 22, 30), datetime(2025, 1, 1, 6, 30)),
        ),
        (
            "2024-12-31T22:33T06:45",
            (datetime(2024, 12, 31, 22, 33), datetime(2025, 1, 1, 6, 45)),
        ),
    ],
)
def test_time_range(dfromto, expected):
    result = time_range(dfromto)
    assert result == expected


@pytest.mark.parametrize(
    "trange,expected_day_hours,expected_night_hours",
    [
        ("2024-01-01T05:00T10:00", 4.0, 1.0),
        ("2024-01-01T21:00T07:00", 2.0, 8.0),
        ("2024-01-01T23:00T05:00", 0.0, 6.0),
        ("2024-01-01T08:00T18:00", 10.0, 0.0),
        ("2024-01-01T18:00T08:00", 6.0, 8.0),
    ],
)
def test_day_night_hours_from_range(trange, expected_day_hours, expected_night_hours):
    hours = day_night_hours_from_range(trange)
    assert hours.day_hours == expected_day_hours
    assert hours.night_hours == expected_night_hours
    assert hours.total_hours == expected_day_hours + expected_night_hours
