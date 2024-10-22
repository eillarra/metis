from datetime import date

from metis.models import (
    Discipline,
    Education,
    Faculty,
    Program,
    ProgramBlock,
    ProgramInternship,
    Track,
    TrackInternship,
)

from .config import get_basic_education_config


def create_logopedics_program() -> Program:
    """Create a Logopedics program.

    Structure:
    - Program has internships: 1A, 2A, 3A
    - Internships are distributed across 3 blocks: Ba3, Ma1, Ma2
    - There is one track: A (1A, 2A, 3A)

    Track discipline constraints:
    - Track A: 3 times logopedics

    :returns: An instance of program with the specified structure.
    """
    # Create Education
    faculty, _ = Faculty.objects.get_or_create(
        name_nl="Faculteit Geneeskunde en Gezondheidswetenschappen",
        name_en="Faculty of Medicine and Health Sciences",
    )
    education, _ = Education.objects.get_or_create(
        code="logo",
        faculty=faculty,
        name_nl="Logopedie",
        name_en="Logopedics",
        short_name_nl="Logopedie",
        short_name_en="Logopedics",
        config=get_basic_education_config(),
    )

    # Create Program
    try:
        program = Program.objects.get(education=education, name_nl="Logopedie")
        return program
    except Program.DoesNotExist:
        pass

    program = Program.objects.create(
        education=education,
        name_nl="Logopedie",
        name_en="Logopedics",
        valid_from=date(2020, 1, 1),
        valid_until=date(2030, 12, 31),
    )

    # Create Program Blocks
    ba3 = ProgramBlock.objects.create(program=program, name="Ba3", position=1)
    ma1 = ProgramBlock.objects.create(program=program, name="Ma1", position=2)
    ma2 = ProgramBlock.objects.create(program=program, name="Ma2", position=3)

    # Create Disciplines
    logopedics, _ = Discipline.objects.get_or_create(
        id=20001,
        education=education,
        code="logopedie",
        name_nl="Logopedie",
        name_en="Logopedics",
    )

    # Create Program Internships
    for i, code in enumerate(["1A", "2A", "3A"]):
        block = [ba3, ma1, ma2][i]
        ProgramInternship.objects.create(block=block, name=f"Internship {code}", position=1)

    internships = ProgramInternship.objects.filter(block__program=program).order_by("name")

    # Create Tracks
    track_a = Track.objects.create(program=program, name="Track A")

    track_a.constraints.create(min_count=3, max_count=3, max_repeat=None)
    track_a.constraints.first().disciplines.set([logopedics])

    # Create Track Internships
    for i, internship in enumerate(internships):
        TrackInternship.objects.create(track=track_a, program_internship=internship, position=i)

    # Create internship constraints
    for internship in internships:
        internship.add_required_discipline(logopedics)

    return program
