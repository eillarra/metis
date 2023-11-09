from datetime import date, datetime, time

import holidays


def is_holiday(date: date, country_code: str = "BE") -> bool:
    """Check if a given date is a holiday in a given country.

    Args:
        date: The date to check.
        country_code: The country code to check. Defaults to Belgium.

    Returns:
        A boolean indicating whether or not the given date is a holiday in the given country.
    """
    return date in holidays.country_holidays(country_code, years=date.year)


def is_weekend(date: date) -> bool:
    """Check if a given date is in the weekend.

    Args:
        date: The date to check.

    Returns:
        A boolean indicating whether or not the given date is in the weekend.
    """
    return date.weekday() in [5, 6]


def remind_deadline(moment: datetime, deadline: datetime, remind_before: list[int] | None = None) -> bool:
    """For a given moment, determine if a deadline should be reminded.

    To determine if a deadline should be reminded, we check if the deadline is today or yesterday, or if the deadline
    is within the remind_before window. If the deadline is within the remind_before window, we only remind if we are
    not on a holiday or weekend.

    Args:
        moment: The moment to check.
        deadline: The deadline to check.
        remind_before: The number of days before the deadline to remind. Defaults to [0, 1, 3, 7].

    Returns:
        A boolean indicating whether or not the deadline should be reminded.
    """
    if moment > deadline:
        return False

    if remind_before is None:
        remind_before = [0, 1, 3, 7]

    remind_before.sort(reverse=True)
    date = moment.date()
    deadline_date = deadline.date()

    if (deadline_date - date).days in [0, 1]:
        return True

    if (deadline_date - date).days in remind_before:
        return not is_weekend(date) and not is_holiday(date)

    return False


def get_minutes_difference(time1: time, time2: time) -> int:
    """Get the difference in minutes between two times.

    Args:
        time1: The first time.
        time2: The second time.

    Returns:
        The difference in minutes between the two times.
    """
    diff = get_time_difference(time1, time2)
    return diff.hour * 60 + diff.minute


def get_time_difference(time1: time, time2: time) -> time:
    """Get the time difference between two times.

    Args:
        time1: The first time.
        time2: The second time.

    Returns:
        The time difference between the two times.
    """
    if time1 > time2:
        time1, time2 = time2, time1

    diff = datetime.combine(date.today(), time2) - datetime.combine(date.today(), time1)
    return time(diff.seconds // 3600, (diff.seconds // 60) % 60)


def sum_times(times: list[time]) -> time:
    """Sum a list of times.

    Args:
        times: The list of times to sum.

    Returns:
        The sum of the given times, in time.
    """
    total = datetime.combine(date.today(), time())

    for t in times:
        minutes = total.minute + t.minute
        total = time(total.hour + t.hour + minutes // 60, minutes % 60)

    return time(total.hour, total.minute)
