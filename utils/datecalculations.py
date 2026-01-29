from calendar import SATURDAY, SUNDAY, monthrange
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta


@dataclass(frozen=True)
class DayNightHours:
    day_hours: float
    night_hours: float

    @property
    def total_hours(self) -> float:
        return self.day_hours + self.night_hours


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
    assert month in range(1, 13), "Month must be between 1 and 12"
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
    :param wdays: A string representing the weekdays to count in Greek
                  e.g. "ΔΕΥΤΕΡΑ-ΠΑΡΑΣΚΕΥΗ" for Monday to Friday
                  or "ΔΕΥΤΕΡΑ,ΤΕΤΑΡΤΗ,ΠΑΡΑΣΚΕΥΗ" for Monday, Wednesday, and Friday.
                  οr "ΠΑΡΑΣΚΕΥΗ" for Friday only.
                  or "ΠΑΡΑΣΚΕΥΗ-ΔΕΥΤΕΡΑ" for Friday, Saturday, Sunday and Monday.
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


def month_total_days(year: int, month: int) -> int:
    """Returns the number of days in a month for a given year."""
    return monthrange(year, month)[1]


def daynight_hours(dfrom: datetime, dto: datetime) -> DayNightHours:
    """
    Calculate the number of day and night hours between two datetime objects.

    Parameters:
    - dfrom: datetime object representing the start datetime
    - dto: datetime object representing the end datetime

    Returns:
    - HOURS object containing the number of day and night hours
    """
    day_start = time(6, 0)  # 6:00 AM
    day_end = time(22, 0)  # 10:00 PM
    dt_day_start = datetime.combine(dfrom, day_start)
    dt_day_end = datetime.combine(dfrom, day_end)
    dt_next_day_start = dt_day_start + timedelta(days=1)

    # dts: dt_day_start, dte: dt_day_end, ndts: dt_next_day_start
    #
    #       dts            dte       ndts
    # 0     6              22        6                22
    #  -----|---------------|--+-----|----------------|--
    # 1  *-*|               |        |
    # 2  *--|----------*    |        |
    #    *--|---------------|-*      |    impossible
    # 3     |  *--------*   |        |
    # 4     |            *--|------* |
    # 5     |             *-|--------|--*
    # 6     |               |   *---*|
    # 7     |               |   *----|-------*

    night_hours = 0
    day_hours = 0

    # 1
    if dfrom < dt_day_start and dto <= dt_day_start:
        night_hours += delta_hours(dfrom, dto)
    # 2
    elif dfrom < dt_day_start and dt_day_start <= dto <= dt_day_end:
        night_hours += delta_hours(dfrom, dt_day_start)
        day_hours += delta_hours(dt_day_start, dto)
    # 3
    elif dt_day_start <= dfrom <= dt_day_end and dt_day_start < dto <= dt_day_end:
        day_hours += delta_hours(dfrom, dto)
    # 4
    elif dt_day_start < dfrom < dt_day_end and dt_day_end < dto <= dt_next_day_start:
        day_hours += delta_hours(dfrom, dt_day_end)
        night_hours += delta_hours(dt_day_end, dto)
    # 5
    elif dt_day_start < dfrom < dt_day_end and dt_next_day_start < dto:
        day_hours += delta_hours(dfrom, dt_day_end)
        night_hours += delta_hours(dt_day_end, dt_next_day_start)
        day_hours += delta_hours(dt_next_day_start, dto)
    # 6
    elif (
        dt_day_end <= dfrom < dt_next_day_start
        and dt_day_end < dto <= dt_next_day_start
    ):
        night_hours += delta_hours(dfrom, dto)
    # 7
    elif dt_day_end <= dfrom < dt_next_day_start and dt_next_day_start < dto:
        night_hours += delta_hours(dfrom, dt_next_day_start)
        day_hours += delta_hours(dt_next_day_start, dto)
    else:
        raise ValueError(f"Wrong TimeRange {dfrom}-{dto}")

    return DayNightHours(day_hours=day_hours, night_hours=night_hours)


def do_overlap(from1: datetime, to1: datetime, from2: datetime, to2: datetime) -> bool:
    """Checks if two time ranges overlap"""
    return from1 < to2 and from2 < to1


def time_range(trange: str) -> tuple[datetime, datetime]:
    """
    2024-01-01T08:00T16:00 -> 2024-01-01T08:00, 2024-01-01T16:00
    2024-01-01 09:00 17:00 -> 2024-01-01T09:00, 2024-01-01T17:00
    """
    if "T" in trange:
        dat, tfrom, tto = trange.split("T")
    elif " " in trange:
        dat, tfrom, tto = trange.split()
    else:
        raise ValueError(f"Wrong TimeRange format: {trange}")
    datefrom = date.fromisoformat(dat)
    dateto = date.fromisoformat(dat)
    timefrom = time.fromisoformat(tfrom)
    timeto = time.fromisoformat(tto)

    if timefrom > timeto:
        dateto += timedelta(days=1)

    dfrom = datetime.combine(datefrom, timefrom)
    dto = datetime.combine(dateto, timeto)
    return dfrom, dto


def day_night_hours_from_range(trange: str) -> DayNightHours:
    dfrom, dto = time_range(trange)
    return daynight_hours(dfrom, dto)
