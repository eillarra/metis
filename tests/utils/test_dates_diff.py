import arrow
import pytest

from metis.utils.dates import get_minutes_difference, sum_times


@pytest.mark.parametrize(
    "time1, time2, expected",
    [
        ("09:00", "10:30", 90),
        ("12:00", "12:00", 0),
        ("23:59", "00:01", 2),
        ("00:01", "23:59", 1438),
        ("09:00", "09:00", 0),
        ("09:00", "08:00", 1380),
        ("08:00", "09:00", 60),
        ("23:59", "23:59", 0),
        ("00:00", "00:00", 0),
    ],
)
@pytest.mark.unit
def test_get_minutes_difference(time1, time2, expected):
    """Test the get_minutes_difference function."""
    time1 = arrow.get(time1, "HH:mm").time()
    time2 = arrow.get(time2, "HH:mm").time()
    assert get_minutes_difference(time1, time2) == expected


@pytest.mark.parametrize(
    "times, expected",
    [
        ([], (0, 0)),
        (["00:00", "00:00", "00:00"], (0, 0)),
        (["00:01", "00:01", "00:01"], (0, 3)),
        (["10:00", "12:00"], (22, 0)),
        (["00:01", "00:01", "00:01", "00:57"], (1, 0)),
        (["13:23", "08:11", "10:01", "03:55"], (35, 30)),
    ],
)
@pytest.mark.unit
def test_sum_times(times, expected):
    """Test the sum_times function."""
    times = [arrow.get(t, "HH:mm").time() for t in times]
    assert sum_times(times) == expected
