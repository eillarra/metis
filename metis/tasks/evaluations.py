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
    active_internships = Internship.objects.filter(status=Internship.DEFINITIVE, start_date__lte=now, end_date__gte=now)

    for internship in active_internships:
        for evaluation_period in internship.evaluation_periods:
            if not (evaluation_period.start_date <= now <= evaluation_period.end_date):
                continue

            if not remind_deadline(
                now,
                datetime.fromisoformat(evaluation_period.official_deadline.isoformat()),
                remind_before=[0, 1, 3, 5, 7],
            ):
                continue

            if internship.evaluations.filter(intermediate=evaluation_period.intermediate).exists():  # type: ignore
                continue

            schedule_evaluation_reminder(internship, evaluation_period)
