import datetime
import holidays


def is_holiday(date: datetime.date, country_code: str = "BE") -> bool:
    """
    Given a date, return True if it is a holiday (for the given country)
    """
    return date in holidays.country_holidays(country_code, years=date.year)


def is_weekend(date: datetime.date) -> bool:
    """
    Given a date, return True if it is a weekend
    """
    return date.weekday() in [5, 6]


def remind_deadline(
    moment: datetime.datetime, deadline: datetime.datetime, remind_before: list[int] = [0, 1, 3, 7]
) -> bool:
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
