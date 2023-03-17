from django.core.management.base import BaseCommand

from sparta.utils import factories as f
from sparta.utils.fixtures import programs as p


class Command(BaseCommand):
    help = "Load fixtures"

    def handle(self, *args, **options):
        # Create some users
        f.AdminFactory.create()
        f.UserFactory.create_batch(100)
        # TODO: management users per education / faculty

        # places
        f.RegionFactory.create_batch(4)
        f.PlaceFactory.create_batch(50)

        # programs
        p.create_audiology_program()
        p.create_logopedics_program()
