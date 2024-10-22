from allauth.account.models import EmailAddress
from django.utils.crypto import get_random_string
from huey import crontab
from huey.contrib.djhuey import db_periodic_task

from metis.models import Internship, Student, User
from metis.services.sparta import Lacedeamon


SPARTA_PROJECTS = {
    "2023": (11, 8, 5, 32),
    "2024": (8, 8, 5, 32),
}


def sync_students(
    education_code: str, year: int, qs_filters: dict, project_id: int, block_id: int, track_id: int
) -> dict:
    """Sync students with Sparta.

    :param education_code: The education code of the students to sync.
    :param year: The year of the students to sync.
    :param qs_filters: Filters to apply to the students queryset.
    :returns: A dictionary mapping the SPARTA student IDs to the Metis student IDs.
    """
    student_map = {}
    metis_bot = User.objects.get(username="metis")
    qs = Lacedeamon(education_code, year).get_students().filter(**qs_filters)

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

    return student_map


@db_periodic_task(crontab(hour="*/2", minute="0"))
def sync_huisartsen_internships_with_sparta() -> None:
    """Sync huisartsen internships with Sparta."""
    education_code = "geneeskunde"
    year = 2024
    project_id, block_id, track_id, period_id = SPARTA_PROJECTS[str(year)]

    metis_bot = User.objects.get(username="metis")
    student_map = sync_students(
        education_code, year, {"internships__discipline__name__icontains": "stichelen"}, project_id, block_id, track_id
    )

    qs = (
        Lacedeamon(education_code, year)
        .get_internships()
        .filter(is_active=True, discipline__name__icontains="stichelen")
    )

    for internship in qs:
        if internship.student_id not in student_map:
            print(f"Student {internship.student_id} not found...")

        try:
            obj = Internship.objects.get(
                project_id=project_id,
                student_id=student_map[internship.student_id],
                status__in=[Internship.PREPLANNING, Internship.CONCEPT, Internship.DEFINITIVE],
            )

            if obj.start_date.day != internship.start_date.day or obj.end_date.day != internship.end_date.day:
                print(
                    f"Updating internship {obj} from {obj.start_date.day} to {internship.start_date.day}"
                    f" and from {obj.end_date.day} to {internship.end_date.day}"
                )
                obj.start_date = internship.start_date
                obj.end_date = internship.end_date
                obj.save()

        except Internship.MultipleObjectsReturned:
            print(f"Multiple internships found for SPARTA id {internship}...")

        except Internship.DoesNotExist:
            print(f"Internship does not exist on Metis... SPARTA id {internship.id}; creating...")

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
