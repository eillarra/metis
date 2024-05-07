from typing import TYPE_CHECKING

from .base import get_template, schedule_template_email


if TYPE_CHECKING:
    from metis.models.stages.evaluations import Evaluation
    from metis.models.stages.internships import EvaluationPeriod, Internship


def schedule_evaluation_reminder(internship: "Internship", evaluation_period: "EvaluationPeriod") -> None:
    """Schedule an email reminder for an evaluation.

    :param internship: The internship to remind about.
    :param evaluation_period: The evaluation period to remind about.
    """
    education = internship.education
    mentors = internship.mentors.all()  # type: ignore
    place_language = internship.place.default_language if internship.place else "nl"

    try:
        template = get_template(education, "evaluation.reminder", language=place_language)
    except ValueError:
        return

    if not mentors.count():
        return

    context = {
        "internship": internship,
        "evaluation_period": evaluation_period,
    }

    tags = [
        "type:evaluation.reminder",
        f"internship.id:{internship.id}",
        f"intermediate:{evaluation_period.intermediate}",
    ]
    tags += [f"user.id:{mentor.user.id}" for mentor in mentors]

    if internship.place:
        tags.append(f"place.id:{internship.place.pk}")

    schedule_template_email(
        template=template,
        to=[mentor.user.email for mentor in mentors],
        context=context,
        log_project=internship.project,
        tags=tags,
    )


def schedule_evaluation_notification(evaluation: "Evaluation") -> None:
    """Schedule an email notification for a new evaluation.

    :param evaluation: The evaluation to notify about.
    """
    education = evaluation.internship.education

    try:
        template = get_template(education, "evaluation.approved")
    except ValueError:
        return

    schedule_template_email(
        template=template,
        to=[evaluation.internship.student.user.email],
        context={"education": education, "evaluation": evaluation},
        log_user=evaluation.internship.student.user,
        log_project=evaluation.internship.project,
        tags=[
            "type:evaluation.approved",
            f"intermediate:{evaluation.intermediate}",
            f"internship.id:{evaluation.internship.id}",
            f"place.id:{evaluation.internship.place.id}",
        ],
    )
