from sparta.models import Discipline, Education, Program, ProgramBlock, ProgramInternship, Track, TrackInternship


def create_audiology():
    """
    Create an Audiology program with the following structure:

    - Program has internships: 1A, 1B, 2A, 2B, 3A, 3B, 4A
    - Internships are distributed across 3 blocks: Ba3, Ma1, Ma2
    - There are 2 tracks: A (1A, 2A, 3A, 4A) and B (1B, 2B, 3B)

    Track discipline constraints:
    - Track A: 2 clinical, 2 prosthetic
    - Track B: 1 clinical, 2 prosthetic

    Internship discipline constraints:
    - Track A internships allow a choice between clinical and prosthetic disciplines
    - Track B internships have limited discipline choice: 1B - prosthetic, 2B - clinical, 3B - prosthetic

    Returns:
        Program: An instance of program with the specified structure
    """

    # Create Education
    education = Education.objects.create(name="Hearing Sciences")

    # Create Program
    program = Program.objects.create(
        education=education, name="Audiology", valid_from="2020-01-01", valid_until="2025-12-31"
    )

    # Create Program Blocks
    ba3 = ProgramBlock.objects.create(program=program, name="Ba3", position=1)
    ma1 = ProgramBlock.objects.create(program=program, name="Ma1", position=2)
    ma2 = ProgramBlock.objects.create(program=program, name="Ma2", position=3)

    # Create Disciplines
    clinical = Discipline.objects.create(name="clinical")
    prosthetic = Discipline.objects.create(name="prosthetic")

    # Create Program Internships
    for i, code in enumerate(["1A", "2A", "3A", "4A", "1B", "2B", "3B"]):
        block = [ba3, ma1, ma1, ma2, ba3, ma1, ma2][i]
        ProgramInternship.objects.create(block=block, name=f"Internship {code}")

    internships = ProgramInternship.objects.order_by("id")

    # Create Tracks
    track_a = Track.objects.create(program=program, name="Track A")
    track_b = Track.objects.create(program=program, name="Track B")

    track_a.constraints.create(min_count=4, max_count=4, max_repeat=2)
    track_a.constraints.first().disciplines.set([clinical, prosthetic])

    track_b.constraints.create(min_count=3, max_count=3, max_repeat=2)
    track_b.constraints.first().disciplines.set([prosthetic, clinical])

    # Create Track Internships
    for i, internship in enumerate(internships[:4], start=1):
        TrackInternship.objects.create(track=track_a, internship=internship, position=i)

    for i, internship in enumerate(internships[4:], start=1):
        TrackInternship.objects.create(track=track_b, internship=internship, position=i)

    # Create internship constraints
    for internship in internships:
        if "1B" in internship.name or "3B" in internship.name:
            internship.add_required_discipline(prosthetic)

        elif "2B" in internship.name:
            internship.add_required_discipline(clinical)

        else:
            internship.constraints.create(min_count=1, max_count=1)
            internship.constraints.first().disciplines.set([clinical, prosthetic])

    return program
