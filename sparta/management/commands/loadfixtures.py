from django.core.management.base import BaseCommand
from model_bakery import baker

from sparta import factories as f


class Command(BaseCommand):
    help = "Load fixtures"

    def handle(self, *args, **options):
        # Create some users
        f.AdminFactory.create()
        f.UserFactory.create_batch(100)

        # places
        f.RegionFactory.create_batch(4)
        f.PlaceFactory.create_batch(50)
