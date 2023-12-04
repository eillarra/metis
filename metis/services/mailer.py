from textwrap import dedent
from typing import TYPE_CHECKING, Optional

from django.conf import settings
from django.core.mail import send_mail as django_send_mail
from django.template import Context, Template
from django.template.defaultfilters import date as date_filter


if TYPE_CHECKING:
    from metis.models import Contact, Education, EmailTemplate, Evaluation, User


def get_template(education: "Education", code: str, language: str = "nl") -> Optional["EmailTemplate"]:
    """Get an email template for an education."""
    from metis.models import EmailTemplate

    try:
        return EmailTemplate.objects.get(code=code, education=education, language=language)
    except EmailTemplate.DoesNotExist:
        try:
            return EmailTemplate.objects.get(code=code, education=None, language=language)
        except EmailTemplate.DoesNotExist:
            send_email_to_admins(f"Email template not found for {education} EOM", f"{code} - {language}")

    return None


def render_context(body: str, context: dict) -> str:
    """Render a body with a context."""
    templ = Template(body)
    return templ.render(Context(context))


def send_email_to_admins(subject: str, message: str = "") -> None:
    django_send_mail(
        subject if subject.startswith("[METIS] ") else f"[METIS] {subject}",
        message,
        "UGent <metis@ugent.be>",
        settings.ADMINS,
        fail_silently=False,
    )


def schedule_email(
    *,
    from_email: str = "UGent <metis@ugent.be>",
    to: list[str],
    subject: str,
    text_content: str,
    bcc: list[str] | None = None,
    reply_to: list[str] | None = None,
    log_template: Optional["EmailTemplate"] = None,
    log_user: Optional["User"] = None,
    log_education: Optional["Education"] = None,
    tags: list[str] | None = None,
):
    from metis.models.emails import EmailLog

    tags = tags or []

    if log_user and f"to.id:{log_user.pk}" not in tags:
        tags.append(f"to.id:{log_user.pk}")

    EmailLog.objects.create(
        template=log_template,
        from_email=from_email,
        to=to,
        bcc=bcc or [],
        reply_to=reply_to or [],
        subject=subject,
        body=text_content,
        education=log_template.education if (log_template and log_template.education) else log_education,
        tags=tags,
    )


def schedule_template_email(
    *,
    template: "EmailTemplate",
    to: list[str],
    bcc: list[str] | None = None,
    context: dict | None = None,
    log_user: Optional["User"] = None,
    log_education: Optional["Education"] = None,
) -> None:
    try:
        from_email = (
            f"{template.education.short_name} UGent <metis@ugent.be>"
            if template.education
            else "UGent <metis@ugent.be>"
        )

        schedule_email(
            from_email=from_email,
            to=to,
            subject=render_context(template.subject, context or {}),
            text_content=render_context(template.body, context or {}),
            bcc=template.bcc + (bcc or []),
            reply_to=template.reply_to,
            log_template=template,
            log_user=log_user,
            log_education=log_education,
        )

    except Exception as e:
        send_email_to_admins("Email error", f"Error while sending email: {e}")
        raise e


def schedule_invitation_email(invitation_type: str, content_object: "Contact") -> None:
    from metis.models import EmailTemplate

    if invitation_type == "contact":
        contact: "Contact" = content_object
    else:
        raise ValueError(f"Unknown invitation type: {invitation_type}")

    try:
        template = EmailTemplate.objects.get(education=contact.education, code=f"invitation.{invitation_type}")
    except EmailTemplate.DoesNotExist:
        send_email_to_admins("Invitation email template not found", f"invitation.{invitation_type}")
        return

    schedule_template_email(
        to=[contact.user.email],
        template=template,
        context={"contact": contact},
        log_user=contact.user,
    )


def schedule_evaluation_notification(evaluation: "Evaluation") -> None:
    education = evaluation.internship.project.education
    subject = "[Metis] Nieuwe evaluatie ontvangen"
    body = dedent(
        f"""
        Beste {evaluation.internship.student.user.name},

        Er is een nieuwe evaluatie ontvangen voor je stage bij {evaluation.internship.place.name}.

        Je kan deze bekijken op <https://metis.ugent.be/nl/stages/{education.code}/>

        - **{evaluation.name}**
        - Opgeslagen door: {evaluation.updated_by.name}
        - Opgeslagen op: {date_filter(evaluation.updated_at, 'DATETIME_FORMAT')}
        """
    )

    schedule_email(
        from_email=f"{education.short_name} UGent <metis@ugent.be>",
        to=[evaluation.internship.student.user.email],
        bcc=[education.office_email],
        reply_to=[education.office_email],
        subject=subject,
        text_content=body.strip(),
        log_education=education,
        log_user=evaluation.internship.student.user,
    )
