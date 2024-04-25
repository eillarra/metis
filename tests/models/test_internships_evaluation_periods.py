from datetime import datetime

import pytest

from metis.models.stages.internships import get_evaluation_periods


@pytest.mark.parametrize(
    "start_date,end_date,intermediates,expected_periods",
    [
        (
            "2021-01-01",
            "2021-01-31",
            2,
            [
                (1, "2021-01-05", "2021-01-14", "2021-01-11"),
                (
                    2,
                    "2021-01-15",
                    "2021-01-24",
                    "2021-01-21",
                ),
                (0, "2021-01-25", "2021-03-17", "2021-01-31"),
            ],
        ),
        (
            "2021-01-01",
            "2021-01-31",
            1,
            [(1, "2021-01-05", "2021-01-19", "2021-01-16"), (0, "2021-01-20", "2021-03-17", "2021-01-31")],
        ),
        ("2021-01-01", "2021-01-31", 0, [(0, "2021-01-05", "2021-03-17", "2021-01-31")]),
    ],
)
def test_get_evaluation_periods(start_date, end_date, intermediates, expected_periods):
    """Test the get_evaluation_periods function."""
    # convert to datetime
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    expected_periods = [
        (
            intermediate,
            datetime.strptime(start_at, "%Y-%m-%d"),
            datetime.strptime(end_at, "%Y-%m-%d"),
            datetime.strptime(deadline, "%Y-%m-%d"),
        )
        for intermediate, start_at, end_at, deadline in expected_periods
    ]

    periods = get_evaluation_periods(start_date, end_date, intermediates)
    assert periods == expected_periods
