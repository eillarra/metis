import pytest

from django.core.exceptions import ValidationError

from metis.utils.factories import (
    PlaceFactory,
    PlaceFactory,
    ProjectPlaceFactory,
    PeriodFactory,
    StudentFactory,
    InternshipFactory,
)
from metis.utils.fixtures.programs import create_audiology_program
from metis.models import Discipline, Program, ProgramInternship, Track


@pytest.fixture
def audiology_program():
    program = create_audiology_program()
    PlaceFactory(education=program.education, name="UZ Gent", type=1)
    return program


@pytest.mark.django_db
def test_program_creation(audiology_program):
    assert isinstance(audiology_program, Program)
    assert audiology_program.name == "Audiologie"


@pytest.mark.django_db
def test_related_models_created(audiology_program):
    program_internships = ProgramInternship.objects.filter(block__program=audiology_program)
    assert program_internships.count() == 7

    tracks = Track.objects.filter(program=audiology_program)
    assert tracks.count() == 2

    for track in tracks:
        assert track.program_internships.count() == (4 if track.name == "Track A" else 3)


@pytest.mark.django_db
def test_wrong_track_chosen(audiology_program):
    program_internships = ProgramInternship.objects.filter(block__program=audiology_program)
    assert program_internships.count() == 7

    tracks = Track.objects.filter(program=audiology_program)
    assert tracks.count() == 2

    for track in tracks:
        assert track.program_internships.count() == (4 if track.name == "Track A" else 3)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "track_name,internship_name,discipline_code",
    [
        ("B", "1B", "klinisch"),
        ("B", "2B", "prothetisch"),
    ],
)
def test_available_disciplines(audiology_program, track_name, internship_name, discipline_code):
    student = StudentFactory()
    place = audiology_program.education.places.first()
    project_place = ProjectPlaceFactory(project=student.project, place=place)
    period = PeriodFactory(
        project=student.project, program_internship=ProgramInternship.objects.get(name=f"Internship {internship_name}")
    )

    with pytest.raises(ValidationError):
        InternshipFactory(
            project=student.project,
            track=Track.objects.get(name=f"Track {track_name}"),
            period=period,
            student=student,
            project_place=project_place,
            discipline=Discipline.objects.get(education=audiology_program.education, code=discipline_code),
        )


@pytest.mark.django_db
@pytest.mark.parametrize(
    "track_name,internships_done,new_internship",
    [
        (None, [], ["1A", "klinisch"]),
        ("A", [["1A", "prothetisch"], ["2A", "prothetisch"]], ["3A", "klinisch"]),
        ("A", [["1A", "prothetisch"], ["2A", "prothetisch"], ["3A", "klinisch"]], ["4A", "klinisch"]),
        ("A", [["1A", "prothetisch"], ["2A", "klinisch"], ["3A", "klinisch"]], ["4A", "prothetisch"]),
    ],
)
def test_previously_covered_disciplines(audiology_program, track_name, internships_done, new_internship):
    student = StudentFactory()
    track = Track.objects.get(name=f"Track {track_name}") if track_name else None
    place = audiology_program.education.places.first()
    project_place = ProjectPlaceFactory(project=student.project, place=place)

    for data in internships_done:
        period = PeriodFactory(
            project=student.project, program_internship=ProgramInternship.objects.get(name=f"Internship {data[0]}")
        )
        internship = InternshipFactory(
            project=student.project,
            track=track,
            period=period,
            student=student,
            project_place=project_place,
            discipline=Discipline.objects.get(education=audiology_program.education, code=data[1]),
        )
        internship.clean()
        internship.save()

    period = PeriodFactory(
        project=student.project,
        program_internship=ProgramInternship.objects.get(name=f"Internship {new_internship[0]}"),
    )
    new_internship = InternshipFactory(
        project=student.project,
        track=track,
        period=period,
        student=student,
        project_place=project_place,
        discipline=Discipline.objects.get(education=audiology_program.education, code=new_internship[1]),
    )

    assert len(new_internship.get_covered_disciplines()) == len(internships_done)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "track_name,internships_done,failing_internship",
    [
        ("A", [["1A", "prothetisch"], ["2A", "prothetisch"]], ["3A", "not_a_discipline"]),
        ("A", [["1A", "prothetisch"], ["2A", "prothetisch"]], ["3A", "prothetisch"]),
        ("A", [["1A", "prothetisch"], ["2A", "prothetisch"], ["3A", "klinisch"]], ["4A", "prothetisch"]),
        ("A", [["1A", "prothetisch"], ["2A", "klinisch"], ["3A", "klinisch"]], ["4A", "klinisch"]),
    ],
)
def test_validate_discipline_choice(audiology_program, track_name, internships_done, failing_internship):
    student = StudentFactory()
    track = Track.objects.get(name=f"Track {track_name}")
    Discipline.objects.create(education=track.program.education, code="not_a_discipline", name="None")
    place = audiology_program.education.places.first()
    project_place = ProjectPlaceFactory(project=student.project, place=place)

    for data in internships_done:
        period = PeriodFactory(
            project=student.project, program_internship=ProgramInternship.objects.get(name=f"Internship {data[0]}")
        )
        internship = InternshipFactory(
            project=student.project,
            track=track,
            period=period,
            student=student,
            project_place=project_place,
            discipline=Discipline.objects.get(education=audiology_program.education, code=data[1]),
        )
        internship.clean()
        internship.save()

    with pytest.raises(ValidationError):
        period = PeriodFactory(
            program_internship=ProgramInternship.objects.get(name=f"Internship {failing_internship[0]}")
        )
        new_internship = InternshipFactory(
            project=student.project,
            track=track,
            period=period,
            student=student,
            project_place=project_place,
            discipline=Discipline.objects.get(education=audiology_program.education, code=failing_internship[1]),
        )
        new_internship.clean()
        new_internship.save()
