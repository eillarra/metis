import pytest

from metis.services.planner.utils import find_students_for_places


@pytest.mark.parametrize(
    "student_tops, project_places, expected",
    [
        ([(1, [1, 2, 3]), (2, [2, 3, 1]), (3, [3, 1, 2])], [1, 2, 3], {1: [1, 3, 2], 2: [2, 1, 3], 3: [3, 2, 1]}),
        ([(1, [1, 2, 3]), (2, [2, 3, 1]), (3, [3, 1, 2])], [1, 2], {1: [1, 3, 2], 2: [2, 1, 3]}),
        (
            [(1, [1, 2, 3]), (2, [2, 3, 1]), (3, [3, 1, 2])],
            [1, 2, 3, 4],
            {1: [1, 3, 2], 2: [2, 1, 3], 3: [3, 2, 1], 4: []},
        ),
        ([(1, [1, 2, 3]), (2, [2, 3, 1]), (3, [3, 1, 2])], [], {}),
        ([(1, [1, 2, 3]), (2, [2, 3, 1]), (3, [3, 1, 2])], [4], {4: []}),
        ([(1, [1, 2, 3]), (2, [2, 3, 1]), (3, [3, 1, 2])], [1, 2, 3], {1: [1, 3, 2], 2: [2, 1, 3], 3: [3, 2, 1]}),
        (
            [(1, [1, 2, 3]), (2, [2, 3, 1]), (3, [3, 1, 2]), (4, [1, 2, 3]), (5, [2, 3, 1]), (6, [3, 1, 2])],
            [1, 2, 3],
            {1: [1, 4, 3, 6, 2, 5], 2: [2, 5, 1, 4, 3, 6], 3: [3, 6, 2, 5, 1, 4]},
        ),
    ],
)
@pytest.mark.unit
def test_student_finder_for_places(student_tops, project_places, expected):
    """Test the hungarian optimizer with preassigned pairs."""
    result = find_students_for_places(student_tops, project_places)
    assert result == expected
