from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand

from sparta import models as m
from sparta.utils import factories as f
from sparta.utils.fixtures import programs as p


class Command(BaseCommand):
    help = "Load fixtures"

    def handle(self, *args, **options):
        # Create some users
        f.AdminFactory.create()
        users = f.UserFactory.create_batch(100)

        # places
        f.RegionFactory.create_batch(4)
        f.PlaceFactory.create_batch(50)

        # programs
        audio = p.create_audiology_program()
        logo = p.create_logopedics_program()

        # internships for audio
        # we create 6 groups of users and we distribute them per year and track, first group starting with
        # year 1 and block 1, second on year 2, etc.
        user_groups = [
            (users[10:20], 2021, "Track A"),
            (users[20:30], 2021, "Track B"),
            (users[30:40], 2022, "Track A"),
            (users[40:50], 2022, "Track B"),
            (users[50:60], 2023, "Track A"),
            (users[60:70], 2023, "Track B"),
        ]

        for i, year in enumerate(range(2021, 2024), start=1):
            project = f.ProjectFactory.create(education=audio.education, name=f"AUDIO {year}")
            block = audio.blocks.get(position=i)

            for group in user_groups:
                track = m.Track.objects.get(program=audio, name=group[2])
                program_internship = track.program_internships.filter(block=block).first()

                if group[1] <= year:
                    for user in group[0]:
                        try:
                            # TODO: fix this
                            f.InternshipFactory.create(
                                project=project,
                                student=user,
                                track=track,
                                program_internship=program_internship,
                                discipline=program_internship.get_available_disciplines().first()
                            )
                        except ValidationError:
                            f.InternshipFactory.create(
                                project=project,
                                student=user,
                                track=track,
                                program_internship=program_internship,
                                discipline=program_internship.get_available_disciplines().last()
                            )
