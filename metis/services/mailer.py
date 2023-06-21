from django.conf import settings
from django.core.mail import send_mail as django_send_mail
from django.template import Context, Template
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from metis.models import User, Education, EmailTemplate, Invitation, Contact


def send_email_to_admins(subject: str, message: str) -> None:
    django_send_mail(
        subject if subject.startswith("[METIS] ") else f"[METIS] {subject}",
        message,
        "Metis <metis@ugent.be>",
        settings.ADMINS,
        fail_silently=False,
    )


def schedule_email(
    *,
    from_email: str = "Metis <metis@ugent.be>",
    to: list[str],
    subject: str,
    text_content: str,
    bcc: list[str] = [],
    reply_to: list[str] = [],
    log_template: Optional["EmailTemplate"] = None,
    log_user: Optional["User"] = None,
    log_education: Optional["Education"] = None,
):
    from metis.models.emails import EmailLog

    EmailLog.objects.create(
        template=log_template,
        from_email=from_email,
        to=to,
        to_user=log_user,
        bcc=bcc,
        reply_to=reply_to,
        subject=subject,
        body=text_content,
        education=log_template.education if log_template else log_education,
    )


def schedule_template_email(
    *,
    from_email: str = "Metis <metis@ugent.be>",
    to: list[str],
    template: "EmailTemplate",
    context: dict = {},
    log_user: Optional["User"] = None,
) -> None:
    try:
        templ = Template(template.body)
        text_content = templ.render(Context(context))
        subject = Template(template.subject)

        schedule_email(
            from_email=from_email,
            to=to,
            subject=subject.render(Context(context)),
            text_content=text_content,
            bcc=template.bcc,
            reply_to=template.reply_to,
            log_template=template,
            log_user=log_user,
        )

    except Exception as e:
        send_email_to_admins("Email error", f"Error while sending email: {e}")
        raise e


def schedule_invitation_email(invitation: "Invitation", education: Optional["Education"] = None) -> None:
    from metis.models import EmailTemplate

    try:
        template = EmailTemplate.objects.get(education=education, code=f"invitation.{invitation.type}")
    except EmailTemplate.DoesNotExist:
        send_email_to_admins("Invitation email template not found", str(invitation))
        return

    if invitation.type == "existing_contact" and invitation.content_object:
        contact: "Contact" = invitation.content_object
        invited_user = contact.user
    else:
        invited_user = None

    schedule_template_email(
        from_email=f"{education.short_name} UGent <metis@ugent.be>" if education else "Metis <metis@ugent.be>",
        to=[invitation.email],
        template=template,
        context={"invitation": invitation},
        log_user=invited_user,
    )
