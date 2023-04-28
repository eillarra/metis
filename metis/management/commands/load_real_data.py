from django.core.management.base import BaseCommand
from typing import NamedTuple

from metis import models as m
from metis.utils import factories as f
from metis.utils.fixtures import programs as p
from metis.utils.data_importer import audiology as real_audio
from metis.utils.data_importer import logopedics as real_logo


class Period(NamedTuple):
    project_name: str
    block_name: str
    period: int
    link_places: bool = True


class Command(BaseCommand):
    help = "Load existing data"

    def handle(self, *args, **options):
        # Create some users
        try:
            m.User.objects.get(username="metis")
        except m.User.DoesNotExist:
            f.AdminFactory.create()

        # programs
        audio = p.create_audiology_program()
        logo = p.create_logopedics_program()

        # projects
        audio_periods = [
            Period("AJ21-22", "Ba3", 1),
            Period("AJ21-22", "Ma1", 1),
            Period("AJ21-22", "Ma1", 2),
            Period("AJ21-22", "Ma2", 1),
            Period("AJ22-23", "Ma1", 1, False),
            Period("AJ22-23", "Ma1", 2, False),
            Period("AJ22-23", "Ma2", 1, False),
        ]

        for period in audio_periods:
            m.Project.objects.get_or_create(
                education=audio.education,
                name=period.project_name,
            )

        for i, year in enumerate(range(2021, 2024), start=1):
            f.ProjectFactory.create(education=logo.education, name=f"LOGO {year}")

        # places
        # real_audio.load_places(project=m.Project.objects.get(name="AJ22-23"))
        # real_logo.load_places(project=m.Project.objects.get(name="LOGO 2023"))

        # internships
        real_audio.load_internships(audio_periods, education=audio.education)
