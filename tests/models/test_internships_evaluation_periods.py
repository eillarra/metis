from datetime import datetime

import pytest
from django.utils import timezone

from metis.models.stages.internships import EvaluationPeriod, get_evaluation_periods


@pytest.mark.parametrize(
    "start_date,end_date,intermediates,expected_periods",
    [
        (
            "2021-01-01",
            "2021-01-31",
            2,
            [
                (1, "2021-01-01 06:00", "2021-01-17 23:59", "2021-01-11"),
                (2, "2021-01-11 06:00", "2021-01-27 23:59", "2021-01-21"),
                (0, "2021-01-28 06:00", "2021-02-07 23:59", "2021-01-31"),
            ],
        ),
        (
            "2021-01-01",
            "2021-01-31",
            1,
            [
                (1, "2021-01-01 06:00", "2021-01-22 23:59", "2021-01-16"),
                (0, "2021-01-23 06:00", "2021-02-07 23:59", "2021-01-31"),
            ],
        ),
        (
            "2021-01-01",
            "2021-01-31",
            0,
            [
                (0, "2021-01-08 06:00", "2021-02-07 23:59", "2021-01-31"),
            ],
        ),
    ],
)
def test_get_evaluation_periods(start_date, end_date, intermediates, expected_periods):
    """Test the get_evaluation_periods function."""
    # convert to datetime
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    # and make aware
    expected_periods = [
        EvaluationPeriod(
            intermediate=intermediate,
            start_at=timezone.make_aware(
                datetime.strptime(start_at, "%Y-%m-%d %H:%M"), timezone=timezone.get_current_timezone()
            ),
            end_at=timezone.make_aware(
                datetime.strptime(end_at, "%Y-%m-%d %H:%M"), timezone=timezone.get_current_timezone()
            ),
            official_deadline=datetime.strptime(deadline, "%Y-%m-%d"),
        )
        for intermediate, start_at, end_at, deadline in expected_periods
    ]

    periods = get_evaluation_periods(start_date, end_date, intermediates)
    assert periods == expected_periods
