import pandas as pd
from django.core.management.base import BaseCommand

from metis.models import Student


class Command(BaseCommand):
    """Update student numbers from a standard OASIS CSV export.

    :usage:
    >>> python manage.py update_studentnummer <file_path>
    """

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        # read csv contents
        df = pd.read_csv(options["file_path"], encoding="Latin-1", sep=";")
        df = df.fillna("")

        # go through each row and update student.number, in bulk
        bulk = []

        for _, row in df.iterrows():
            for student in Student.objects.filter(user__email=row["EMAIL"].lower().strip()):
                student.number = str(int(row["UGENTSTUDENTID"])).zfill(8)
                print("Updating", student.user.email, student.number)
                bulk.append(student)

        Student.objects.bulk_update(bulk, ["number"])
