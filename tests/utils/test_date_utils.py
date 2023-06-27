import maya
import pytest

from metis.utils.dates import remind_deadline


@pytest.mark.parametrize(
    "date, deadline, expected",
    [
        (maya.when("2023-01-01 09:00").datetime(), maya.when("2023-01-05 10:00").datetime(), False),
        (maya.when("2023-01-01 09:00").datetime(), maya.when("2023-01-02 10:00").datetime(), True),
        (maya.when("2023-01-01 09:00").datetime(), maya.when("2023-01-01 10:00").datetime(), True),
        (maya.when("2023-01-01 11:00").datetime(), maya.when("2023-01-01 10:00").datetime(), False),
        (maya.when("2023-07-21 09:00").datetime(), maya.when("2023-07-24 10:00").datetime(), False),  # holiday
        (maya.when("2023-07-23 09:00").datetime(), maya.when("2023-07-26 10:00").datetime(), False),  # weekend
        (maya.when("2023-07-24 09:00").datetime(), maya.when("2023-07-27 10:00").datetime(), True),  # 3 days before
    ],
)
def test_definition_is_invalid(date, deadline, expected):
    assert remind_deadline(date, deadline) is expected
