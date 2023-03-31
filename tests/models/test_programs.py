import pytest

from django.core.exceptions import ValidationError

from sparta.utils.factories import UserFactory, InternshipFactory
from sparta.utils.fixtures.programs import create_audiology_program
from sparta.models import Discipline, Program, ProgramInternship, Track


@pytest.fixture
def audiology_program():
    return create_audiology_program()


@pytest.mark.django_db
def test_program_creation(audiology_program):
    assert isinstance(audiology_program, Program)
    assert audiology_program.name == "Audiology"


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
    "track_name,internship_name,discipline_name",
    [
        ("B", "1B", "clinical"),
        ("B", "2B", "prosthetic"),
    ],
)
def test_available_disciplines(audiology_program, track_name, internship_name, discipline_name):
    user = UserFactory()

    with pytest.raises(ValidationError):
        InternshipFactory(
            track=Track.objects.get(name=f"Track {track_name}"),
            program_internship=ProgramInternship.objects.get(name=f"Internship {internship_name}"),
            student=user,
            discipline=Discipline.objects.get(code=discipline_name),
        )


@pytest.mark.django_db
@pytest.mark.parametrize(
    "track_name,internships_done,new_internship",
    [
        (None, [], ["1A", "clinical"]),
        ("A", [["1A", "prosthetic"], ["2A", "prosthetic"]], ["3A", "clinical"]),
        ("A", [["1A", "prosthetic"], ["2A", "prosthetic"], ["3A", "clinical"]], ["4A", "clinical"]),
        ("A", [["1A", "prosthetic"], ["2A", "clinical"], ["3A", "clinical"]], ["4A", "prosthetic"]),
    ],
)
def test_previously_covered_disciplines(audiology_program, track_name, internships_done, new_internship):
    user = UserFactory()
    track = Track.objects.get(name=f"Track {track_name}") if track_name else None

    for data in internships_done:
        internship = InternshipFactory(
            track=track,
            program_internship=ProgramInternship.objects.get(name=f"Internship {data[0]}"),
            student=user,
            discipline=Discipline.objects.get(code=data[1]),
        )
        internship.clean()
        internship.save()

    new_internship = InternshipFactory(
        track=track,
        program_internship=ProgramInternship.objects.get(name=f"Internship {new_internship[0]}"),
        student=user,
        discipline=Discipline.objects.get(code=new_internship[1]),
    )

    assert len(new_internship.get_covered_disciplines()) == len(internships_done)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "track_name,internships_done,failing_internship",
    [
        ("A", [["1A", "prosthetic"], ["2A", "prosthetic"]], ["3A", "not_a_discipline"]),
        ("A", [["1A", "prosthetic"], ["2A", "prosthetic"]], ["3A", "prosthetic"]),
        ("A", [["1A", "prosthetic"], ["2A", "prosthetic"], ["3A", "clinical"]], ["4A", "prosthetic"]),
        ("A", [["1A", "prosthetic"], ["2A", "clinical"], ["3A", "clinical"]], ["4A", "clinical"]),
    ],
)
def test_validate_discipline_choice(audiology_program, track_name, internships_done, failing_internship):
    user = UserFactory()
    track = Track.objects.get(name=f"Track {track_name}")
    Discipline.objects.create(education=track.program.education, code="not_a_discipline", name="None")

    for data in internships_done:
        internship = InternshipFactory(
            track=track,
            program_internship=ProgramInternship.objects.get(name=f"Internship {data[0]}"),
            student=user,
            discipline=Discipline.objects.get(code=data[1]),
        )
        internship.clean()
        internship.save()

    with pytest.raises(ValidationError):
        new_internship = InternshipFactory(
            track=track,
            program_internship=ProgramInternship.objects.get(name=f"Internship {failing_internship[0]}"),
            student=user,
            discipline=Discipline.objects.get(code=failing_internship[1]),
        )
        new_internship.clean()
        new_internship.save()
