from typing import TYPE_CHECKING, Optional

from django.conf import settings
from django.core.mail import send_mail as django_send_mail
from django.template import Context, Template


if TYPE_CHECKING:
    from metis.models import Education, EmailTemplate, Project, User


def render_context(body: str, context: dict) -> str:
    """Render a body with a context.

    :param body: The body to render.
    :param context: The context to render the body with.
    :return: The rendered body.
    """
    templ = Template(body)
    return templ.render(Context(context))


def get_template(education: "Education", code: str, language: str = "nl") -> "EmailTemplate":
    """Get an email template for an education.

    :param education: The education to get the email template for.
    :param code: The code of the email template to get.
    :param language: The language of the email template to get.
    :return: The email template for the education, code and language.
    :raises ValueError: If the email template is not found.
    """
    from metis.models import EmailTemplate

    try:
        return EmailTemplate.objects.get(code=code, education=education, language=language)
    except EmailTemplate.DoesNotExist:
        try:
            return EmailTemplate.objects.get(code=code, education=None, language=language)
        except EmailTemplate.DoesNotExist:
            send_email_to_admins(f"Email template not found for {education} EOM", f"{code} - {language}")

    raise ValueError(f"Email template not found for {education} - {code} - {language}")


def send_email_to_admins(subject: str, message: str = "") -> None:
    """Send an email to the admins.

    :param subject: The subject of the email.
    :param message: The message of the email.
    """
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
    log_user: Optional["User"] = None,
    log_project: Optional["Project"] = None,
    tags: list[str] | None = None,
) -> None:
    """Schedule an email to be sent.

    :param from_email: The email address to send the email from.
    :param to: The email addresses to send the email to.
    :param subject: The subject of the email.
    :param text_content: The text content of the email.
    :param bcc: The email addresses to send the email bcc to.
    :param reply_to: The email addresses to set as reply-to.
    :param log_user: The user to log the email for.
    :param log_project: The project to log the email for.
    :param tags: The tags to log the email with.
    """
    from metis.models.emails import EmailLog

    tags = tags or []

    if log_user and f"user.id:{log_user.pk}" not in tags:
        tags.append(f"user.id:{log_user.pk}")

    unique_to = list(set(to))  # Remove duplicate entries from to list
    unique_bcc = list(set(bcc or []))  # Remove duplicate entries from bcc list
    unique_tags = list(set(tags))  # Remove duplicate entries from tags list

    EmailLog.objects.create(
        from_email=from_email,
        to=unique_to,
        bcc=unique_bcc,
        reply_to=reply_to or [],
        subject=subject,
        body=text_content,
        project=log_project,
        tags=unique_tags,
    )


def schedule_template_email(
    *,
    template: "EmailTemplate",
    to: list[str],
    bcc: list[str] | None = None,
    context: dict | None = None,
    log_user: Optional["User"] = None,
    log_project: Optional["Project"] = None,
    tags: list[str] | None = None,
) -> None:
    """Schedule an email based on a template.

    :param template: The email template to use.
    :param to: The email addresses to send the email to.
    :param bcc: The email addresses to send the email bcc to.
    :param context: The context to render the email with.
    :param log_user: The user to log the email for.
    :param log_project: The project to log the email for.
    :param tags: The tags to log the email with.
    """
    try:
        from_email = (
            f"{log_project.education.short_name} UGent <metis@ugent.be>" if log_project else "UGent <metis@ugent.be>"
        )

        schedule_email(
            from_email=from_email,
            to=to,
            subject=render_context(template.subject, context or {}),
            text_content=render_context(template.body, context or {}),
            bcc=template.bcc + (bcc or []),
            reply_to=log_project.reply_to if log_project and log_project.reply_to else template.reply_to,
            log_user=log_user,
            log_project=log_project,
            tags=tags,
        )

    except Exception as exc:
        send_email_to_admins("Email error", f"Error while sending email: {exc}")
        raise exc
