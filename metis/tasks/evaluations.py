from datetime import datetime

from django.utils import timezone
from huey import crontab
from huey.contrib.djhuey import db_periodic_task

from metis.models.stages.internships import Internship
from metis.services.mailer import get_template, schedule_template_email
from metis.utils.dates import remind_deadline


@db_periodic_task(crontab(hour="8", minute="0"))
def schedule_evaluation_emails() -> None:
    """Check which evaluations need to happen and schedule the emails to mentors."""
    now = timezone.now()
    active_internships = Internship.objects.filter(status=Internship.DEFINITIVE, start_date__lte=now, end_date__gte=now)

    for internship in active_internships:
        education = internship.education
        evaluation_periods: list[tuple[int, datetime, datetime]] = internship.evaluation_periods

        try:
            email_template = get_template(education, "internship.evaluation")
        except ValueError:
            continue

        for intermediate, start_at, end_at in evaluation_periods:
            if not (start_at <= now <= end_at):
                continue

            if not remind_deadline(now, end_at, remind_before=[0, 1, 3, 5, 7]):
                continue

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
                "type:evaluation.reminder",
                f"internship.id:{internship.id}",
                f"intermediate:{intermediate}",
            ]
            tags += [f"user.id:{mentor.user.id}" for mentor in mentors]

            if internship.place:
                tags.append(f"place.id:{internship.place.pk}")

            schedule_template_email(
                template=email_template,
                to=[mentor.user.email for mentor in mentors],
                context=context,
                log_project=internship.project,
                tags=tags,
            )
