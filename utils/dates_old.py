from datetime import date, datetime, time, timedelta

from .datetimes import delta_hours


def daynight_hours(dfrom: datetime, dto: datetime) -> dict[str, float]:
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
        night_hours += delta_hours(dfrom, dt_next_day_start)
    # 7
    elif dt_day_end <= dfrom < dt_next_day_start and dt_next_day_start < dto:
        night_hours += delta_hours(dfrom, dt_next_day_start)
        day_hours += delta_hours(dt_next_day_start, dto)
    else:
        raise ValueError(f"Wrong TimeRange {dfrom}-{dto}")

    return {"day_hours": day_hours, "night_hours": night_hours}


def do_overlap(from1: datetime, to1: datetime, from2: datetime, to2: datetime) -> bool:
    """Checks if two time ranges overlap"""
    return from1 < to2 and from2 < to1


def iso2dtime(isodatetime: str) -> datetime:
    return datetime.fromisoformat(isodatetime)


def time_range(trange: str) -> tuple[datetime, datetime]:
    """
    2024-01-01T08:00T16:00 -> 2024-01-01T08:00, 2024-01-01T16:00
    """
    dat, tfrom, tto = trange.split("T")
    datefrom = date.fromisoformat(dat)
    dateto = date.fromisoformat(dat)
    timefrom = time.fromisoformat(tfrom)
    timeto = time.fromisoformat(tto)
    if timefrom > timeto:
        dateto += timedelta(days=1)
    dfrom = datetime.combine(datefrom, timefrom)
    dto = datetime.combine(dateto, timeto)
    return dfrom, dto
