from typing import TYPE_CHECKING, Optional

from metis.models.places import Contact
from metis.models.users import find_user_by_email

from .base import get_template, schedule_template_email


if TYPE_CHECKING:
    from metis.models.stages.projects import Project


def schedule_invitation_email(contact: Contact, *, project: Optional["Project"] = None) -> None:
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


def schedule_bouncing_email_notice(bouncing_email: str) -> None:
    """Schedule an email to notify the education office of an underivable email.

    :param bouncing_email: The email address that is bouncing.
    """
    user = find_user_by_email(bouncing_email)

    if not user:
        return

    for contact in Contact.objects.filter(user=user):
        template = get_template(contact.education, "automate.emails.bouncing")
        schedule_template_email(
            template=template,
            to=[contact.education.office_email],
            reply_to=["helpdesk.metis@ugent.be"],
            context={"contact": contact, "bouncing_email": bouncing_email},
            log_user=user,
            tags=["type:automate.emails.bouncing", f"user.id:{user.pk}", f"place.id:{contact.place.pk}"],
        )
