from typing import TYPE_CHECKING

from .base import get_template, schedule_template_email


if TYPE_CHECKING:
    from metis.models.stages.evaluations import Evaluation


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
        bcc=[education.office_email] if education.office_email else None,
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
