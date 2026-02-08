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


def misthos_hour_diff(year: int, misthos: float):
    hour = misthos / 25 * 6 / 40
    oktaoro = hour * 8
    total_delta = 0
    total_days = 0
    for month in range(1, 13):
        days = month_monday2friday_days(year, month)
        apodoxes = days * oktaoro
        delta = misthos - apodoxes
        total_delta = total_delta + delta
        total_days += days
    return year, total_days, round(total_delta, 2)


def orthodox_easter(year: int) -> date:
    """
    Υπολογισμός Ορθόδοξου Πάσχα (Gregorian ημερομηνία)
    με παραλλαγή του Meeus για το Ιουλιανό Πάσχα + διόρθωση 13 ημερών (1900–2099).
    """
    # Meeus Julian algorithm για Πάσχα στο Ιουλιανό ημερολόγιο
    a = year % 4
    b = year % 7
    c = year % 19
    d = (19 * c + 15) % 30
    e = (2 * a + 4 * b - d + 34) % 7
    month = (d + e + 114) // 31  # 3 = Μάρτιος, 4 = Απρίλιος (Ιουλιανό)
    day = ((d + e + 114) % 31) + 1

    julian_easter = date(year, month, day)

    # Μετατροπή σε Γρηγοριανό: +13 ημέρες για 1900–2099
    gregorian_easter = julian_easter + timedelta(days=13)
    return gregorian_easter


def greek_holidays(year: int) -> dict:
    pascha = orthodox_easter(year)

    clean_monday = pascha - timedelta(days=48)
    good_friday = pascha - timedelta(days=2)
    easter_monday = pascha + timedelta(days=1)
    holy_spirit_monday = pascha + timedelta(days=50)

    return {
        "Πρωτοχρονιά": date(year, 1, 1),
        "Θεοφάνεια": date(year, 1, 6),
        "Επανάσταση του 1821": date(year, 3, 25),
        "Πρωτομαγιά": date(year, 5, 1),
        "Κοίμηση της Θεοτόκου": date(year, 8, 15),
        "Επέτειος του Όχι": date(year, 10, 28),
        "Χριστούγεννα": date(year, 12, 25),
        "Σύναξη της Θεοτόκου": date(year, 12, 26),
        "Καθαρά Δευτέρα": clean_monday,
        "Μεγάλη Παρασκευή": good_friday,
        "Κυριακή του Πάσχα": pascha,
        "Δευτέρα του Πάσχα": easter_monday,
        "Δευτέρα του Αγίου Πνεύματος": holy_spirit_monday,
    }
