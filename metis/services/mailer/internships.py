from typing import TYPE_CHECKING

from .base import get_template, schedule_template_email


if TYPE_CHECKING:
    from metis.models.stages.internships import Internship


def schedule_internship_approved_email(internship: "Internship", to: str = "student") -> None:
    """Schedule an email for an approved internship.

    :param internship: The internship to remind about.
    :param to: "student" or "place", the recipient of the email.
    """
    if to not in ["student", "place"]:
        raise ValueError(f"Invalid recipient: {to}")

    education = internship.education
    place_language = internship.place.default_language if internship.place else "nl"
    template_code = "internship.approved" if to == "student" else "internship.approved.to_place"

    try:
        template = get_template(education, template_code, language=place_language)
    except ValueError:
        return

    user = internship.student.user if to == "student" else internship.place.admins.first().user  # type: ignore
    context = {
        "internship": internship,
        "user": user,
    }

    tags = [
        f"type:{template_code}",
        f"internship.id:{internship.id}",
        f"user.id:{user.id}",
    ]

    if internship.place:
        tags.append(f"place.id:{internship.place.pk}")

    schedule_template_email(
        template=template,
        to=[user.email],
        context=context,
        log_user=user,
        log_project=internship.project,
        tags=tags,
    )
