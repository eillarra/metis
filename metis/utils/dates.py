import holidays

from datetime import date, datetime, time


def is_holiday(date: date, country_code: str = "BE") -> bool:
    """
    Given a date, return True if it is a holiday (for the given country)
    """
    return date in holidays.country_holidays(country_code, years=date.year)


def is_weekend(date: date) -> bool:
    """
    Given a date, return True if it is a weekend
    """
    return date.weekday() in [5, 6]


def remind_deadline(moment: datetime, deadline: datetime, remind_before: list[int] = [0, 1, 3, 7]) -> bool:
    """
    Given a deadline, return True if the deadline hasn't passed and:
        - the deadline is today or yesterday
        - the deadline is within the remind_before window, but only if we are not on a holiday or weekend
    """

    if moment > deadline:
        return False

    remind_before.sort(reverse=True)
    date = moment.date()
    deadline_date = deadline.date()

    if (deadline_date - date).days in [0, 1]:
        return True

    if (deadline_date - date).days in remind_before:
        return not is_weekend(date) and not is_holiday(date)

    return False


def get_minutes_difference(time1: time, time2: time) -> int:
    diff = get_time_difference(time1, time2)
    return diff.hour * 60 + diff.minute


def get_time_difference(time1: time, time2: time) -> time:
    """
    Get the time difference between two times.

    :param datetime.time time1: The first time.
    :param datetime.time time2: The second time.
    :return: The difference between the two times.
    """

    if time1 > time2:
        time1, time2 = time2, time1

    diff = datetime.combine(date.today(), time2) - datetime.combine(date.today(), time1)
    return time(diff.seconds // 3600, (diff.seconds // 60) % 60)


def sum_times(times: list[time]) -> time:
    """
    Sum a list of times.

    :param list[datetime.time] times: The times to sum.
    :return: The sum of the times.
    """

    total = datetime.combine(date.today(), time())

    for t in times:
        minutes = total.minute + t.minute
        total = time(total.hour + t.hour + minutes // 60, minutes % 60)

    return time(total.hour, total.minute)
