from typing import TYPE_CHECKING, Optional

from .base import get_template, schedule_template_email


if TYPE_CHECKING:
    from metis.models import Contact, Project


def schedule_invitation_email(contact: "Contact", *, project: Optional["Project"] = None) -> None:
    """Schedule an invitation email for a contact.

    :param contact: The contact to send the invitation to.
    :param project: The project to log the invitation for (if any).
    """
    place_language = contact.place.default_language

    try:
        template = get_template(contact.education, "invitation.contact", language=place_language)
    except ValueError:
        return

    schedule_template_email(
        template=template,
        to=[contact.user.email],
        context={"contact": contact},
        log_user=contact.user,
        log_project=project,
        tags=["type:contact.invitation", f"user.id:{contact.user.id}", f"place.id:{contact.place.id}"],
    )
