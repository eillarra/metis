from django.core.management.base import BaseCommand

from metis.models.emails import EmailTemplate
from metis.models.stages import Internship, Period, ProjectPlaceAvailability
from metis.services.mailer import schedule_template_email


class Command(BaseCommand):
    """Send emails to target groups for a project.

    :usage:
    >>> python manage.py send_emails "<email_code>" <period_id>
    """

    def add_arguments(self, parser):
        parser.add_argument("email_code", type=str)
        parser.add_argument("period_id", type=int)

    def handle(self, *args, **options):
        email_code = options["email_code"]
        project = Period.objects.get(id=options["period_id"]).project
        education = project.education

        try:
            email_template = EmailTemplate.objects.get(education=education, code=email_code)
        except EmailTemplate.DoesNotExist as exc:
            raise ValueError(f"Unknown email code: {email_code}") from exc

        if email_code == "internship.first_info_place":
            internships = Internship.objects.filter(period_id=options["period_id"], status=Internship.DEFINITIVE)

            for internship in internships.all():
                admin_contact = internship.place.contacts.filter(is_admin=True).first()
                mentors_no_admin = internship.mentors.exclude(user=admin_contact.user)

                schedule_template_email(
                    template=email_template,
                    from_email=f"{education.short_name} UGent <metis@ugent.be>",
                    to=[admin_contact.user.email],
                    bcc=[mentor.user.email for mentor in mentors_no_admin],
                    context={
                        "contact": admin_contact,
                        "internship": internship,
                        "student": internship.student,
                        "period": internship.period,
                        "project": project,
                    },
                    log_education=education,
                    log_user=admin_contact.user,
                )

        if email_code == "internship.first_info_student":
            internships = Internship.objects.filter(period_id=options["period_id"], status=Internship.DEFINITIVE)

            for internship in internships.all():
                schedule_template_email(
                    template=email_template,
                    from_email=f"{education.short_name} UGent <metis@ugent.be>",
                    to=[internship.student.user.email],
                    context={
                        "internship": internship,
                        "student": internship.student,
                        "period": internship.period,
                        "project": project,
                    },
                    log_education=education,
                    log_user=internship.student.user,
                )

        if email_code == "internship.place_not_selected":
            period = project.periods.get(id=options["period_id"])
            internships = Internship.objects.filter(period_id=options["period_id"], status=Internship.DEFINITIVE)
            availability = ProjectPlaceAvailability.objects.filter(period=period, min__gt=0)
            project_place_ids_with_internship = set(internships.values_list("project_place_id", flat=True))

            for avail in availability.all():
                if avail.project_place_id not in project_place_ids_with_internship:
                    place = avail.project_place.place
                    admin_contact = place.contacts.filter(is_admin=True).first()
                    mentors_contacts_no_admin = place.contacts.exclude(is_mentor=True, user=admin_contact.user)

                    schedule_template_email(
                        template=email_template,
                        from_email=f"{education.short_name} UGent <metis@ugent.be>",
                        to=[admin_contact.user.email],
                        bcc=[contact.user.email for contact in mentors_contacts_no_admin],
                        context={
                            "contact": admin_contact,
                            "place": place,
                            "project": project,
                        },
                        log_education=education,
                        log_user=admin_contact.user,
                    )
