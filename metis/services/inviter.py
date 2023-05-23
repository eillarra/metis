from django.core.exceptions import ValidationError

from metis.models import User, Invitation, Place, Project, Contact, Student
from .mailer import send_mail_to_admins


def check_user_invitations(user: User):
    invitations = Invitation.objects.filter(email=user.email)

    for invitation in invitations:
        processor = {
            "contact": process_contact_invitation,
            "student": process_student_invitation,
        }

        try:
            processor[invitation.type](invitation, user)
            invitation.delete()
        except Exception:
            send_mail_to_admins("Invitation failed", f"Invitation {invitation} failed for user {user}")


def process_contact_invitation(invitation: Invitation, user: User):
    if not invitation.data:
        raise ValueError("Invitation data is empty")

    try:
        if invitation.data:
            place: Place = invitation.content_object  # type: ignore
            Contact.objects.create(
                place=place, user=user, is_staff=invitation.data["is_staff"], is_mentor=invitation.data["is_mentor"]
            )
    except (KeyError, ValidationError) as e:
        raise ValueError(str(e))


def process_student_invitation(invitation: Invitation, user: User):
    if not invitation.data:
        raise ValueError("Invitation data is empty")

    try:
        project: Project = invitation.content_object  # type: ignore
        Student.objects.create(project=project, user=user, block_id=invitation.data["block_id"])
    except (KeyError, ValidationError) as e:
        raise ValueError(str(e))
