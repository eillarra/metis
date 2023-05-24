from django.core.management.base import BaseCommand
from typing import NamedTuple

from metis import models as m
from metis.services.cloner import clone_project
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

        # audio

        audio = p.create_audiology_program()

        audio_periods = [
            Period("AJ21-22", "Ba3", 1),
            Period("AJ21-22", "Ma1", 1),
            Period("AJ21-22", "Ma1", 2),
            Period("AJ21-22", "Ma2", 1),
            Period("AJ22-23", "Ba3", 1),
            Period("AJ22-23", "Ma1", 1),
            Period("AJ22-23", "Ma1", 2),
            Period("AJ22-23", "Ma2", 1),
        ]

        for period in audio_periods:
            m.Project.objects.get_or_create(
                education=audio.education,
                program=audio,
                name=period.project_name,
            )

        last_audio_project = m.Project.objects.get(program=audio, name="AJ22-23")
        real_audio.load_places(project=last_audio_project)
        real_audio.load_internships(audio_periods, education=audio.education)
        clone_project(last_audio_project, "AJ23-24")

        # logo

        logo = p.create_logopedics_program()

        logo_periods = [
            Period("AJ21-22", "Ba3", 1),
            Period("AJ21-22", "Ma1", 1),
            Period("AJ21-22", "Ma2", 1),
            Period("AJ22-23", "Ba3", 1),
            Period("AJ22-23", "Ma1", 1),
            Period("AJ22-23", "Ma2", 1),
        ]

        for period in logo_periods:
            m.Project.objects.get_or_create(
                education=logo.education,
                program=logo,
                name=period.project_name,
            )

        last_logo_project = m.Project.objects.get(program=logo, name="AJ22-23")
        real_logo.load_places(project=last_logo_project)
        real_logo.load_internships(logo_periods, education=logo.education)
        clone_project(last_logo_project, "AJ23-24")
