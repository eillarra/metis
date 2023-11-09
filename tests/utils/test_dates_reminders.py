import maya
import pytest

from metis.utils.dates import is_holiday, is_weekend, remind_deadline


@pytest.mark.parametrize(
    "moment,deadline,remind_before,expected",
    [
        ("2023-07-24 09:00", "2023-07-27 12:00", None, True),
        ("2023-01-03 09:00", "2023-01-04 12:00", None, False),
        ("2023-01-03 09:00", "2023-01-03 12:00", None, True),
        ("2023-01-03 13:00", "2023-01-03 12:00", None, False),
        ("2023-01-03 09:00", "2023-01-04 12:00", [0, 1], True),
        ("2023-07-24 09:00", "2023-07-27 12:00", None, True),
    ],
)
@pytest.mark.unit
def test_remind_deadline(moment, deadline, remind_before, expected):
    """Test the remind_deadline function."""
    moment, deadline = maya.when(moment).datetime(), maya.when(deadline).datetime()
    assert not is_weekend(moment) and not is_holiday(moment)
    assert remind_deadline(moment, deadline, remind_before) is expected


@pytest.mark.parametrize(
    "moment,deadline,remind_before,expected",
    [
        ("2021-05-01 09:00", "2021-05-01 12:00", [0, 1, 3], True),
        ("2021-05-01 09:00", "2021-05-02 12:00", [0, 1, 3], False),
        ("2021-05-01 12:00", "2021-05-01 12:00", [0, 1, 3], False),
        ("2021-05-02 09:00", "2021-05-01 12:00", [0, 1], False),
        ("2021-05-01 09:00", "2021-05-03 12:00", None, False),
    ],
)
@pytest.mark.unit
def test_remind_deadline_on_weekend(moment, deadline, remind_before, expected):
    """Test the remind_deadline function on a weekend."""
    moment, deadline = maya.when(moment).datetime(), maya.when(deadline).datetime()
    assert is_weekend(moment)
    assert remind_deadline(moment, deadline, remind_before) is expected


@pytest.mark.parametrize(
    "moment,deadline,remind_before,expected",
    [
        ("2021-05-13 09:00", "2021-05-13 12:00", [0, 1, 2], True),
        ("2021-05-13 09:00", "2021-05-14 12:00", [0, 1, 2], False),
    ],
)
@pytest.mark.unit
def test_remind_deadline_on_holiday(moment, deadline, remind_before, expected):
    """Test the remind_deadline function on a holiday."""
    moment, deadline = maya.when(moment).datetime(), maya.when(deadline).datetime()
    assert is_holiday(moment) and not is_weekend(moment)
    assert remind_deadline(moment, deadline, remind_before) is expected
