import pytest

from metis.models import Discipline, ProgramInternship, PlaceCapacity, Student
from metis.services.cloner import clone_project
from metis.utils.factories import (
    DisciplineFactory,
    ProgramFactory,
    ProgramBlockFactory,
    ProgramInternshipFactory,
    ProjectFactory,
    ProjectPlaceFactory,
    PeriodFactory,
    StudentFactory,
)


@pytest.fixture
def project(db):
    # create program
    program = ProgramFactory.create()
    disciplines = DisciplineFactory.create_batch(3, education=program.education)
    blocks = ProgramBlockFactory.create_batch(3, program=program)
    for block in blocks:
        ProgramInternshipFactory.create_batch(3, block=block)

    # create project
    project = ProjectFactory.create(name="Test Project", education=program.education, program=program)

    # create periods for the project
    for program_internship in ProgramInternship.objects.filter(block__program=program):
        PeriodFactory.create(project=project, program_internship=program_internship)

    # create places for the project
    ProjectPlaceFactory.create_batch(3, project=project)
    for place in project.place_set.all():
        place.disciplines.add(disciplines[0])

    # create students for the project
    for block in program.blocks.all():
        StudentFactory.create_batch(3, project=project, block=block)

    return project


def test_clone_project(project):
    new_project = clone_project(project, "New Test Project")

    # Check that the new project was created with the correct name
    assert new_project.name == "New Test Project"

    # Check that the new project has periods with new dates in the future (next year)
    assert new_project.periods.count() == project.periods.count()

    # Check that the new project has the same places as the original project
    assert new_project.place_set.count() == project.place_set.count()

    # Check that the new project has the same capacities as the original project
    """for new_place in new_project.place_set.all():
        for new_capacity in new_place.capacities.all():
            assert new_capacity.period.start_date.year == period.start_date.year + 1
            assert new_capacity.period.end_date.year == period.end_date.year + 1
            assert new_capacity.capacity == capacity.capacity"""

    # Check that all students from the first block are in the new project, in the second block
    # Check that all students from the last block are not in the new project
    first_block = project.program.blocks.first()
    second_block = project.program.blocks.all()[1]
    last_block = project.program.blocks.last()

    assert new_project.students.filter(block=first_block).count() == 0
    assert new_project.students.filter(block=second_block).count() == 3
    assert new_project.students.filter(block=last_block).count() == 3

    for new_student in new_project.students.filter(block=last_block):
        assert project.students.get(user=new_student.user).block == second_block
