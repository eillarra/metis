from datetime import date, datetime, time

import holidays


def is_holiday(date: date, country_code: str = "BE") -> bool:
    """Check if a given date is a holiday in a given country.

    :param date: The date to check.
    :param country_code: The country code to check. Defaults to Belgium.
    :return: A boolean indicating whether or not the given date is a holiday in the given country.
    """
    return date in holidays.country_holidays(country_code, years=date.year)


def is_weekend(date: date) -> bool:
    """Check if a given date is in the weekend.

    :param date: The date to check.
    :return: A boolean indicating whether or not the given date is in the weekend.
    """
    return date.weekday() in [5, 6]


def remind_deadline(moment: datetime, deadline: datetime, remind_before: list[int] | None = None) -> bool:
    """For a given moment, determine if a deadline should be reminded.

    To determine if a deadline should be reminded, we check if the deadline is today or yesterday, or if the deadline
    is within the remind_before window. If the deadline is within the remind_before window, we only remind if we are
    not on a holiday or weekend.

    :param moment: The moment to check.
    :param deadline: The deadline to check.
    :param remind_before: The number of days before the deadline to remind. Defaults to [0, 3, 7].
    :return: A boolean indicating whether or not the deadline should be reminded.
    """
    if moment >= deadline:
        return False

    if remind_before is None:
        remind_before = [0, 3, 7]

    remind_before.sort(reverse=True)
    date = moment.date()
    deadline_date = deadline.date()

    if (deadline_date - date).days == 0:
        return True

    if (deadline_date - date).days in remind_before and not (is_weekend(date) or is_holiday(date)):
        return True

    return False


def get_minutes_difference(time1: time, time2: time) -> int:
    """Get the difference in minutes between two times.

    :param time1: The first time.
    :param time2: The second time.
    :return: The difference in minutes between the two times.
    """
    diff = get_time_difference(time1, time2)
    return diff.hour * 60 + diff.minute


def get_time_difference(time1: time, time2: time) -> time:
    """Get the time difference between two times.

    :param time1: The first time.
    :param time2: The second time.
    :return: The time difference between the two times.
    """
    diff = datetime.combine(date.today(), time2) - datetime.combine(date.today(), time1)
    return time(diff.seconds // 3600, (diff.seconds // 60) % 60)


def sum_times(times: list[time]) -> tuple[int, int]:
    """Sum a list of times.

    :param times: The list of times to sum.
    :return: The sum of the given times, as a tuple of hours and minutes.
    """
    hours = 0
    minutes = 0

    for t in times:
        minutes += t.minute
        hours += t.hour

    hours += minutes // 60
    minutes = minutes % 60

    return hours, minutes
