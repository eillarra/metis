from datetime import date

import pytest
from django.db.models import QuerySet

from metis.models.disciplines import Discipline
from metis.models.educations import Education, Faculty
from metis.models.stages.constraints import (
    DisciplineConstraint,
    get_disciplines_from_constraints,
    validate_discipline_constraints,
)
from metis.models.stages.programs import Program, Track


@pytest.fixture
def program():
    faculty = Faculty.objects.create(name="Faculty 1")
    education = Education.objects.create(faculty=faculty, name="Education 1")
    program = Program.objects.create(
        id=1, education=education, name="Program 1", valid_from=date(2020, 1, 1), valid_until=date(2030, 12, 31)
    )

    return program


@pytest.fixture
def disciplines(program):
    return [
        Discipline.objects.create(education=program.education, code=f"dis{i}", name=f"Discipline {i}")
        for i in range(1, 7)
    ]


@pytest.fixture
def track(disciplines, program):
    track = Track.objects.create(program=program, name="Test Track")
    return track


@pytest.fixture
def track_with_constraints(disciplines, program):
    track = Track.objects.create(program=program, name="Test Track")

    constraint1 = DisciplineConstraint.objects.create(
        content_object=track,
        min_count=2,
        max_count=2,
        max_repeat=2,
    )
    constraint1.disciplines.set([disciplines[0]])  # 1

    constraint2 = DisciplineConstraint.objects.create(
        content_object=track,
        min_count=5,
        max_count=5,
        max_repeat=None,
    )
    constraint2.disciplines.set(disciplines[1:])  # 2, 3, 4, 5, 6

    return track


@pytest.fixture
def create_constraint(request, track):
    min_count, max_count, max_repeat = request.param
    constraint = DisciplineConstraint.objects.create(
        content_object=track, min_count=min_count, max_count=max_count, max_repeat=max_repeat
    )
    constraint.disciplines.set([1, 2, 3])

    return constraint


@pytest.mark.django_db
@pytest.mark.parametrize(
    "create_constraint,discipline_ids,expected_result",
    [
        ((1, 2, 1), [1, 3], True),
        ((1, 2, 1), [2, 3], True),
        ((1, 2, 1), [1, 2, 3], False),
        ((1, 2, 1), [4], False),
        ((1, 2, 1), [1, 1], False),
        ((1, 2, 2), [1, 1], True),
        ((2, 3, 1), [1, 2, 3], True),
        ((2, 3, 1), [1, 2], True),
        ((2, 3, 1), [1], False),
        ((1, 5, 2), [1, 1, 2, 2, 3], True),
        ((1, 4, 2), [1, 1, 1, 2], False),
        ((1, 4, 2), [1, 1, 2, 2], True),
        # min_count is None
        ((None, 3, 1), [1], True),
        ((None, 3, 1), [1, 2], True),
        ((None, 3, 1), [1, 2, 3], True),
        ((None, 3, 1), [1, 1, 2, 2, 3], False),
        # max_count is None
        ((2, None, 1), [1], False),
        ((2, None, 1), [1, 2], True),
        ((2, None, 1), [1, 2, 3], True),
        ((2, None, 1), [1, 1, 2, 2, 3], False),
        # max_repeat is None
        ((2, 3, None), [1, 1], True),
        ((2, 3, None), [1, 1, 2], True),
        ((2, 3, None), [1, 1, 1, 2], False),
        # min_count, max_count, and max_repeat are None
        ((None, None, None), [1], True),
        ((None, None, None), [1, 2, 3], True),
        ((None, None, None), [1, 1, 1, 2, 2, 3], True),
    ],
    indirect=["create_constraint"],
)
def test_validate_discipline_constraints(
    create_constraint,
    discipline_ids: list[int],
    expected_result: bool,
):
    constraint = create_constraint
    assert validate_discipline_constraints(discipline_ids, [constraint]) is expected_result


@pytest.mark.django_db
@pytest.mark.parametrize(
    "discipline_ids,expected_result",
    [
        ([1, 1, 2, 3, 4, 5, 6], True),  # OK
        ([1, 1, 2, 2, 2, 5, 6], True),  # OK
        ([1, 1, 2, 3, 4, 5], False),  # Total count is not 7
        ([1, 1, 1, 2, 3, 4, 5], False),  # Discipline 1 must be repeated exactly twice
        ([1, 1, 2, 3, 4, 5, 7], False),  # Discipline 7 not allowed
    ],
)
def test_track_with_multiple_constraints(track_with_constraints, discipline_ids, expected_result):
    assert track_with_constraints.validate_discipline_constraints(discipline_ids) == expected_result


@pytest.mark.django_db
def test_get_disciplines_from_constraints_no_constraints():
    constraints = DisciplineConstraint.objects.none()
    disciplines = get_disciplines_from_constraints(constraints)

    assert isinstance(disciplines, QuerySet)
    assert disciplines.count() == 0
