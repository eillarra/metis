from django.core.management.base import BaseCommand
from time import sleep

from metis.models.stages import Student
from metis.services.mailer import send_mail


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        students = Student.objects.filter(
            project__name="AJ23-24", block__name="Ma1"
        ).prefetch_related("project__education", "block")

        for student in students:
            data = {
                "from_email": "Metis <metis@ugent.be>",
                "reply_to": "stagelaw@ugent.be",
                "to": [student.user.email],
                "subject": f"{student.project.education} academiejaar 2023-24 Ma1-stages",
                "template": "_tmp_emails/audiologo_ma1.md",
                "context_data": {
                    "block_name": student.block.name,
                    "user_first_name": student.user.first_name,
                    "education_student_url": student.project.education.get_student_area_url(),
                },
            }
            send_mail(**data)
            sleep(24)
            # metis.tasks.emails.send_template_email(*email)
