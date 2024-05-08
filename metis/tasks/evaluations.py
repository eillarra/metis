from datetime import datetime

from django.utils import timezone
from huey import crontab
from huey.contrib.djhuey import db_periodic_task

from metis.models.stages.internships import Internship
from metis.services.mailer.evaluations import schedule_evaluation_reminder
from metis.utils.dates import remind_deadline


@db_periodic_task(crontab(hour="8", minute="0"))
def schedule_evaluation_emails() -> None:
    """Check which evaluations need to happen and schedule the emails to mentors."""
    now = timezone.now()
    active_internships = Internship.objects.filter(
        status=Internship.DEFINITIVE, start_date__lte=now, end_date__gte=now
    ).prefetch_related("project__education")

    for internship in active_internships:
        education = internship.education
        remind_before = education.configuration["email_remind_before"] if education.configuration else [0, 3, 7]

        for evaluation_period in internship.evaluation_periods:
            if not (evaluation_period.start_at <= now <= evaluation_period.end_at):
                continue

            if not remind_deadline(
                now,
                datetime.fromisoformat(evaluation_period.official_deadline.isoformat()),
                remind_before=remind_before,
            ):
                continue

            if internship.evaluations.filter(intermediate=evaluation_period.intermediate).exists():  # type: ignore
                continue

            schedule_evaluation_reminder(internship, evaluation_period)
