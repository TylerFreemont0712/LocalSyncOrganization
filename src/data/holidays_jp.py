"""Japanese national holidays calculator.

Covers all 16 national holidays defined by Japanese law, including
substitute holidays (振替休日) and special rules for vernal/autumnal equinox.
"""

from datetime import date, timedelta


def _vernal_equinox_day(year: int) -> int:
    """Approximate day of vernal equinox (春分の日) for a given year."""
    if year <= 1947:
        return 21
    if year <= 1979:
        return int(20.8357 + 0.242194 * (year - 1980) - int((year - 1983) / 4))
    if year <= 2099:
        return int(20.8431 + 0.242194 * (year - 1980) - int((year - 1980) / 4))
    return 21


def _autumnal_equinox_day(year: int) -> int:
    """Approximate day of autumnal equinox (秋分の日) for a given year."""
    if year <= 1947:
        return 23
    if year <= 1979:
        return int(23.2588 + 0.242194 * (year - 1980) - int((year - 1983) / 4))
    if year <= 2099:
        return int(23.2488 + 0.242194 * (year - 1980) - int((year - 1980) / 4))
    return 23


def _monday_of_week(year: int, month: int, nth: int) -> date:
    """Return the nth Monday of a given month (1-indexed)."""
    first = date(year, month, 1)
    # Days until first Monday
    offset = (7 - first.weekday()) % 7
    first_monday = first + timedelta(days=offset)
    return first_monday + timedelta(weeks=nth - 1)


def get_japanese_holidays(year: int) -> dict[date, str]:
    """Return a dict mapping date -> holiday name for a given year.

    All holiday names are provided in English with Japanese in parentheses.
    """
    holidays: dict[date, str] = {}

    # Fixed-date holidays
    holidays[date(year, 1, 1)] = "New Year's Day (元日)"
    holidays[date(year, 2, 11)] = "National Foundation Day (建国記念の日)"
    holidays[date(year, 2, 23)] = "Emperor's Birthday (天皇誕生日)"
    holidays[date(year, 4, 29)] = "Shōwa Day (昭和の日)"
    holidays[date(year, 5, 3)] = "Constitution Memorial Day (憲法記念日)"
    holidays[date(year, 5, 4)] = "Greenery Day (みどりの日)"
    holidays[date(year, 5, 5)] = "Children's Day (こどもの日)"
    holidays[date(year, 8, 11)] = "Mountain Day (山の日)"
    holidays[date(year, 11, 3)] = "Culture Day (文化の日)"
    holidays[date(year, 11, 23)] = "Labour Thanksgiving Day (勤労感謝の日)"

    # Happy Monday holidays (moved to specific Mondays)
    holidays[_monday_of_week(year, 1, 2)] = "Coming of Age Day (成人の日)"
    holidays[_monday_of_week(year, 7, 3)] = "Marine Day (海の日)"
    holidays[_monday_of_week(year, 9, 3)] = "Respect for the Aged Day (敬老の日)"
    holidays[_monday_of_week(year, 10, 2)] = "Sports Day (スポーツの日)"

    # Equinox days
    ve_day = _vernal_equinox_day(year)
    holidays[date(year, 3, ve_day)] = "Vernal Equinox Day (春分の日)"

    ae_day = _autumnal_equinox_day(year)
    holidays[date(year, 9, ae_day)] = "Autumnal Equinox Day (秋分の日)"

    # Substitute holidays (振替休日):
    # If a holiday falls on Sunday, the next non-holiday weekday is a holiday.
    substitute: dict[date, str] = {}
    for d, name in sorted(holidays.items()):
        if d.weekday() == 6:  # Sunday
            sub = d + timedelta(days=1)
            while sub in holidays or sub in substitute:
                sub += timedelta(days=1)
            substitute[sub] = f"Substitute Holiday ({name})"

    holidays.update(substitute)

    # Citizen's Holiday (国民の休日):
    # If a day is sandwiched between two holidays, it becomes a holiday.
    all_dates = sorted(holidays.keys())
    for i in range(len(all_dates) - 1):
        d1, d2 = all_dates[i], all_dates[i + 1]
        if (d2 - d1).days == 2:
            between = d1 + timedelta(days=1)
            if between not in holidays and between.weekday() != 6:
                holidays[between] = "Citizen's Holiday (国民の休日)"

    return holidays


def is_japanese_holiday(d: date) -> str | None:
    """Return holiday name if the date is a Japanese national holiday, else None."""
    holidays = get_japanese_holidays(d.year)
    return holidays.get(d)
