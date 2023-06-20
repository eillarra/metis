import pytest

from django.core.exceptions import ValidationError

from metis.utils.factories import (
    PlaceFactory,
    PlaceTypeFactory,
    ProjectFactory,
    ProjectPlaceFactory,
    PeriodFactory,
    StudentFactory,
    InternshipFactory,
)
from metis.utils.fixtures.programs import create_audiology_program, create_logopedics_program
from metis.models import Discipline, Program, ProgramInternship, Track


@pytest.fixture
def audiology_program():
    program = create_audiology_program()
    hospital = PlaceTypeFactory(name="Hospital", education=program.education)
    PlaceFactory(education=program.education, name="UZ Gent", type=hospital)
    return program


@pytest.fixture
def logopedics_program():
    program = create_logopedics_program()
    hospital = PlaceTypeFactory(name="Hospital", education=program.education)
    PlaceFactory(education=program.education, name="UZ Gent", type=hospital)
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
    "program,track_name,internship_name,discipline_code",
    [
        ("audio", "B", "1B", "klinisch"),
        ("audio", "B", "2B", "prothetisch"),
        ("logo", "A", "2B", "logopedie"),
    ],
)
def test_available_disciplines(
    program,
    track_name,
    internship_name,
    discipline_code,
    audiology_program,
    logopedics_program,
):
    test_program = audiology_program if program == "audio" else logopedics_program
    project = ProjectFactory(program=test_program)
    student = StudentFactory(project=project)
    place = test_program.education.places.first()
    project_place = ProjectPlaceFactory(project=project, place=place)
    period = PeriodFactory(
        project=project, program_internship=ProgramInternship.objects.get(name=f"Internship {internship_name}")
    )

    with pytest.raises(ValidationError):
        InternshipFactory(
            project=project,
            track=Track.objects.get(program=test_program, name=f"Track {track_name}"),
            period=period,
            student=student,
            project_place=project_place,
            discipline=Discipline.objects.get(education=test_program.education, code=discipline_code),
        )


@pytest.mark.django_db
@pytest.mark.parametrize(
    "program,track_name,internships_done,new_internship",
    [
        ("audio", None, [], ["1A", "klinisch"]),
        ("audio", "A", [["1A", "prothetisch"], ["2A", "prothetisch"]], ["3A", "klinisch"]),
        ("audio", "A", [["1A", "prothetisch"], ["2A", "prothetisch"], ["3A", "klinisch"]], ["4A", "klinisch"]),
        ("audio", "A", [["1A", "prothetisch"], ["2A", "klinisch"], ["3A", "klinisch"]], ["4A", "prothetisch"]),
        ("logo", "A", [["1A", "logopedie"], ["2A", "logopedie"]], ["3A", "logopedie"]),
    ],
)
def test_previously_covered_disciplines(
    program,
    track_name,
    internships_done,
    new_internship,
    audiology_program,
    logopedics_program,
):
    test_program = audiology_program if program == "audio" else logopedics_program
    project = ProjectFactory(program=test_program)
    student = StudentFactory(project=project)
    track = Track.objects.get(program=test_program, name=f"Track {track_name}") if track_name else None
    place = test_program.education.places.first()
    project_place = ProjectPlaceFactory(project=project, place=place)

    for data in internships_done:
        program_internship = ProgramInternship.objects.get(block__program=test_program, name=f"Internship {data[0]}")
        period = PeriodFactory(project=project, program_internship=program_internship)
        internship = InternshipFactory(
            project=project,
            track=track,
            period=period,
            student=student,
            project_place=project_place,
            discipline=Discipline.objects.get(education=test_program.education, code=data[1]),
        )
        internship.clean()
        internship.save()

    program_internship = ProgramInternship.objects.get(
        block__program=test_program, name=f"Internship {new_internship[0]}"
    )
    period = PeriodFactory(
        project=project,
        program_internship=program_internship,
    )
    new_internship = InternshipFactory(
        project=project,
        track=track,
        period=period,
        student=student,
        project_place=project_place,
        discipline=Discipline.objects.get(education=test_program.education, code=new_internship[1]),
    )

    assert len(new_internship.get_covered_disciplines()) == len(internships_done)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "program,track_name,internships_done,failing_internship",
    [
        ("audio", "A", [["1A", "prothetisch"], ["2A", "prothetisch"]], ["3A", "not_a_discipline"]),
        ("audio", "A", [["1A", "prothetisch"], ["2A", "prothetisch"]], ["3A", "prothetisch"]),
        ("audio", "A", [["1A", "prothetisch"], ["2A", "prothetisch"], ["3A", "klinisch"]], ["4A", "prothetisch"]),
        ("audio", "A", [["1A", "prothetisch"], ["2A", "klinisch"], ["3A", "klinisch"]], ["4A", "klinisch"]),
        ("logo", "A", [["1A", "logopedie"], ["2A", "logopedie"]], ["3A", "not_a_discipline"]),
    ],
)
def test_validate_discipline_choice(
    program, track_name, internships_done, failing_internship, audiology_program, logopedics_program
):
    test_program = audiology_program if program == "audio" else logopedics_program
    project = ProjectFactory(program=test_program)
    student = StudentFactory(project=project)
    track = Track.objects.get(program=test_program, name=f"Track {track_name}")
    Discipline.objects.create(education=track.program.education, code="not_a_discipline", name="None")
    place = test_program.education.places.first()
    project_place = ProjectPlaceFactory(project=project, place=place)

    for data in internships_done:
        program_internship = ProgramInternship.objects.get(block__program=test_program, name=f"Internship {data[0]}")
        period = PeriodFactory(project=project, program_internship=program_internship)
        internship = InternshipFactory(
            project=project,
            track=track,
            period=period,
            student=student,
            project_place=project_place,
            discipline=Discipline.objects.get(education=test_program.education, code=data[1]),
        )
        internship.clean()
        internship.save()

    with pytest.raises(ValidationError):
        program_internship = ProgramInternship.objects.get(
            block__program=test_program, name=f"Internship {failing_internship[0]}"
        )
        period = PeriodFactory(project=project, program_internship=program_internship)
        new_internship = InternshipFactory(
            project=project,
            track=track,
            period=period,
            student=student,
            project_place=project_place,
            discipline=Discipline.objects.get(education=test_program.education, code=failing_internship[1]),
        )
        new_internship.clean()
        new_internship.save()
