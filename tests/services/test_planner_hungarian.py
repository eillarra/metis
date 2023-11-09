import pytest

from metis.services.planner.hungarian import hungarian_optimizer


@pytest.mark.parametrize(
    "student_tops, project_place_availability, expected",
    [
        ([(1, [1, 2, 3]), (2, [2, 3, 1]), (3, [3, 1, 2])], {1: 1, 2: 1, 3: 1}, [(1, 1, 1), (2, 2, 1), (3, 3, 1)]),
        ([(1, [1, 2, 3]), (2, [2, 3, 1]), (3, [3, 1, 2])], {1: 0, 2: 0, 3: 0}, []),
        ([(1, [1, 2, 3]), (2, [2, 3, 1]), (3, [3, 1, 2])], {1: 1, 2: 1, 3: 1}, [(1, 1, 1), (2, 2, 1), (3, 3, 1)]),
        ([], {1: 1, 2: 1, 3: 1}, []),
        ([(1, [1, 2, 3]), (2, [2, 3, 1]), (3, [3, 1, 2])], {}, []),
        ([(1, None), (2, [2, 3, 1]), (3, [3, 1, 2])], {1: 1, 2: 1, 3: 1}, [(2, 2, 1), (3, 3, 1)]),
        # more availability than students
        (
            [(1, [1, 2, 3]), (2, [2, 3, 1]), (3, [3, 1, 2])],
            {1: 2, 2: 2, 3: 2},
            [(1, 1, 1), (2, 2, 1), (3, 3, 1)],
        ),
        # less availability than students > one student is left without a project
        (
            [(1, [1, 2, 3]), (2, [2, 3, 1]), (3, [3, 1, 2])],
            {1: 1, 2: 1},
            [(1, 1, 1), (2, 2, 1)],
        ),
        # only one project place available
        (
            [(1, [1, 2, 3]), (2, [1, 3, 2]), (3, [1, 2, 3])],
            {1: 1},  #
            [(1, 1, 1)],
        ),
        # all students have the same preferences
        (
            [(1, [1, 2, 3]), (2, [1, 2, 3]), (3, [1, 2, 3])],
            {1: 1, 2: 1, 3: 1},
            [(1, 1, 1), (2, 2, 2), (3, 3, 3)],
        ),
    ],
)
@pytest.mark.unit
def test_hungarian_optimizer(student_tops, project_place_availability, expected):
    """Test the hungarian_optimizer function."""
    result = hungarian_optimizer(student_tops, project_place_availability)
    assert result == expected


@pytest.mark.parametrize(
    "student_tops, project_place_availability, preassigned_pairs, expected",
    [
        (
            [(1, [1, 2, 3]), (2, [2, 3, 1]), (3, [3, 1, 2])],
            {1: 1, 2: 1, 3: 1},
            [(1, 2)],
            [(2, 3, 2), (3, 1, 2), (1, 2, -1)],
        ),
        (
            [(1, [1, 2, 3]), (2, [2, 3, 1]), (3, [3, 1, 2])],
            {1: 1, 2: 1, 3: 1},
            [(2, 3)],
            [(1, 2, 2), (3, 1, 2), (2, 3, -1)],
        ),
    ],
)
@pytest.mark.unit
def test_hungarian_optimizer_with_preassigned_pairs(
    student_tops, project_place_availability, preassigned_pairs, expected
):
    """Test the hungarian_optimizer function with preassigned pairs."""
    result = hungarian_optimizer(student_tops, project_place_availability, preassigned_pairs)
    assert result == expected
