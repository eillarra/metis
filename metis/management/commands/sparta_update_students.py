from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandParser
from phonenumbers import PhoneNumberFormat, format_number, parse

from metis.models import Student, User
from metis.models.rel import Address, PhoneNumber
from metis.services.sparta import Lacedeamon


class Command(BaseCommand):
    """This command is used to test the connection with the legacy SPARTA database.

    TODO: integrate this with the metis/management/commands/sparta.py command

    :usage:
    >>> python manage.py sparta_update_students <education_code> <year>
    """

    def add_arguments(self, parser: CommandParser) -> None:
        """Add arguments to the command."""
        parser.add_argument("education_code", type=str)
        parser.add_argument("year", type=int)

    def handle(self, *args, **options):
        """Connect with 'sparta' database and do whatever you want."""
        education_code = options["education_code"]
        year = options["year"]

        deamon = Lacedeamon(education_code, year)
        metis_bot = User.objects.get(username="metis")
        user_type = ContentType.objects.get_for_model(User)

        project_id = {
            "2023": 11,
            "2024": 8,
        }[str(year)]

        for student in Student.objects.filter(project_id=project_id).select_related("user"):
            sparta_student = deamon.get_student_by_email(student.user.email)

            if sparta_student:
                student.oasis_data = {
                    "uuid": sparta_student.oasis_uuid,
                    "image_filename": sparta_student.image_filename,
                }
                student.updated_by = metis_bot
                student.save()

                country_code = None

                if sparta_student.address_street:
                    country_code = "NL" if sparta_student.address_country == "2" else "BE"
                    Address.objects.get_or_create(
                        object_id=student.user.id,
                        content_type=user_type,
                        address=sparta_student.address_street,
                        city=sparta_student.address_city,
                        postcode=sparta_student.address_postcode,
                        country=country_code,
                    )

                if sparta_student.mobile:
                    n = parse(sparta_student.mobile, country_code)
                    number = format_number(n, PhoneNumberFormat.INTERNATIONAL)

                    PhoneNumber.objects.get_or_create(
                        object_id=student.user.id,
                        content_type=user_type,
                        type=PhoneNumber.MOBILE,
                        number=number,
                    )
