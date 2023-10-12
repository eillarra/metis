import pandas as pd

from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

from metis.models import User, Student, Project, ProgramBlock, Track


class Command(BaseCommand):
    """Read a Excel file and create students on Metis.

    This command takes a Excel file as first argument and uses it to create users and students on Metis.
    The Excel file needs to have 4 columns: "email", "first_name", "last_name", "student_number", "block".
    Second argument is the Project.id to which the students will be added.

    :usage:
    >>> python manage.py create_students "<file_path>" <project_id>
    """

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)
        parser.add_argument("project_id", type=int)

    def handle(self, *args, **options):
        df = pd.read_excel(options["file_path"])
        df = df.fillna("")
        df = df.astype(str)

        metis_bot = User.objects.get(username="metis")
        project = Project.objects.get(id=options["project_id"])

        for _, row in df.iterrows():
            track = Track.objects.get(program__education=project.education)
            block = ProgramBlock.objects.get(name=row["block"], program__education=project.education)
            email = row["email"].lower().strip()
            first_name = row["first_name"].strip()
            last_name = row["last_name"].strip()
            student_number = row["student_number"].zfill(8)

            # create a user, withouth a password
            user, _ = User.objects.get_or_create(
                email=email,
                username=email.split("@")[0],
                defaults={
                    "password": f"!{get_random_string(40)}",  # not a usable password, they will use UGent OAuth
                    "first_name": first_name,
                    "last_name": last_name,
                },
            )

            # create a student
            Student.objects.get_or_create(
                user=user,
                project_id=options["project_id"],
                block=block,
                track=track,
                defaults={
                    "created_by": metis_bot,
                    "updated_by": metis_bot,
                    "number": student_number,
                },
            )

            print(f"Created student {first_name} {last_name} <{email}> with student number {student_number}...")
