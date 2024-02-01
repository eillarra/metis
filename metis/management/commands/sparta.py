from allauth.account.models import EmailAddress
from django.core.management.base import BaseCommand, CommandParser
from django.utils.crypto import get_random_string

from metis.models import Internship, Student, User
from metis.services.sparta import Lacedeamon
from metis.tasks.custom.geneeskunde import sync_huisartsen_internships_with_sparta


class Command(BaseCommand):
    """Command used to test the connection with the legacy SPARTA database.

    :usage:
    >>> python manage.py sparta <education_code> <year> <command>
    """

    def add_arguments(self, parser: CommandParser) -> None:
        """Add arguments to the command."""
        parser.add_argument("education_code", type=str)
        parser.add_argument("year", type=int)
        parser.add_argument("command", type=str)

    def handle(self, *args, **options):
        """Connect with 'sparta' database and do whatever you want."""
        education_code = options["education_code"]
        year = options["year"]
        command = options["command"]

        project_id, block_id, track_id, period_id = {
            "2023": (11, 8, 5, 32),
            "2024": (8, 8, 5, 32),
        }[str(year)]
        student_map = {}
        metis_bot = User.objects.get(username="metis")

        if command in {"create_students", "create_internships"}:
            qs = (
                Lacedeamon(education_code, year)
                .get_students()
                .filter(internships__discipline__name__icontains="stichelen")
            )

            for student in qs:
                email = student.email.lower().strip()
                user, _ = User.objects.get_or_create(
                    email=student.email.lower().strip(),
                    username=email.split("@")[0],
                    defaults={
                        "password": f"!{get_random_string(40)}",  # not a usable password, they will use UGent OAuth
                        "first_name": student.first_name,
                        "last_name": student.last_name,
                    },
                )

                EmailAddress.objects.get_or_create(user=user, email=email, verified=True, primary=True)

                s, _ = Student.objects.get_or_create(
                    user=user,
                    project_id=project_id,
                    block_id=block_id,
                    track_id=track_id,
                    defaults={
                        "created_by": metis_bot,
                        "updated_by": metis_bot,
                        "number": student.number or "00000000",
                    },
                )

                student_map[student.id] = s.pk
                print(f"Created student {student}...")

        if command == "create_internships":
            qs = (
                Lacedeamon(education_code, year)
                .get_internships()
                .filter(is_active=True, discipline__name__icontains="stichelen")
            )

            for internship in qs:
                if internship.student_id not in student_map:
                    print(f"Student {internship.student_id} not found, skipping...")
                    continue

                Internship.objects.get_or_create(
                    project_id=project_id,
                    track_id=track_id,
                    student_id=student_map[internship.student_id],
                    start_date=internship.start_date,
                    end_date=internship.end_date,
                    status=Internship.PREPLANNING,
                    discipline_id=5,
                    defaults={
                        "created_by": metis_bot,
                        "updated_by": metis_bot,
                        "is_approved": False,
                    },
                )

        if command == "update_internships":
            sync_huisartsen_internships_with_sparta()

        else:
            qs = (
                Lacedeamon(education_code, year)
                .get_students()
                .filter(internships__discipline__name__icontains="stichelen")
            )

            for i, student in enumerate(qs):
                print(f"{i}: {student}")
