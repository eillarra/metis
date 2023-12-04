from datetime import datetime

from django.utils import timezone
from huey import crontab
from huey.contrib.djhuey import db_periodic_task

from metis.models.stages.internships import Internship
from metis.services.mailer import get_template, render_context, schedule_email


@db_periodic_task(crontab(hour="8", minute="0"))
def schedule_evaluation_emails() -> None:
    """Check which evaluations need to happen and schedule the emails to mentors."""
    now = timezone.now()
    active_internships = Internship.objects.filter(status=Internship.DEFINITIVE, start_date__lte=now, end_date__gte=now)

    for internship in active_internships:
        education = internship.education
        evaluation_periods: list[tuple[int, datetime, datetime]] = internship.evaluation_periods
        email_template = get_template(education, "internship.evaluation")

        if email_template is None:
            continue

        for intermediate, start_at, end_at in evaluation_periods:
            if internship.evaluations.filter(intermediate=intermediate).exists():  # type: ignore
                continue

            mentors = internship.mentors.all()  # type: ignore

            if not mentors.count():
                continue

            context = {
                "internship": internship,
                "evaluation_period": (intermediate, start_at, end_at),
            }

            tags = [
                email_template.code,
                f"internship.id:{internship.id}",
                f"intermediate:{intermediate}",
            ]
            tags += [f"to.id:{mentor.user.id}" for mentor in mentors]

            if internship.place:
                tags.append(f"place.id:{internship.place.pk}")

            schedule_email(
                from_email=f"{education.short_name} UGent <metis@ugent.be>",
                to=[mentor.user.email for mentor in mentors],
                reply_to=[education.office_email],
                subject=render_context(email_template.subject, context),
                text_content=render_context(email_template.body, context),
                log_template=email_template,
                log_education=education,
                tags=tags,
            )
