from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail as django_send_mail
from django.template import Context, Template
from django.template.loader import render_to_string
from markdown import markdown
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from metis.models import User, Education, EmailTemplate, Invitation


def send_raw_email(
    *,
    from_email: str = "Metis <metis@ugent.be>",
    to: list[str],
    subject: str,
    text_content: str,
    bcc: list[str] = [],
    reply_to: list[str] = [],
    log_template: Optional["EmailTemplate"] = None,
    log_user: Optional["User"] = None,
):
    html_content = markdown(text_content)
    msg = EmailMultiAlternatives(subject, text_content, from_email=from_email, to=to, bcc=bcc, reply_to=reply_to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    from metis.models.emails import EmailLog

    EmailLog.objects.create(
        template=log_template,
        user=log_user,
        to=", ".join(to),
        bcc=", ".join(bcc) if bcc else None,
        reply_to=", ".join(reply_to) if reply_to else None,
        subject=subject,
        body=text_content,
    )


def send_email(
    *,
    from_email: str = "Metis <metis@ugent.be>",
    to: list[str],
    subject: str,
    template: str,
    context_data: dict,
    bcc: list[str] = [],
    reply_to: list[str] = [],
):
    text_content = render_to_string(template, context_data)
    html_content = markdown(text_content)
    msg = EmailMultiAlternatives(subject, text_content, from_email=from_email, to=to, bcc=bcc, reply_to=reply_to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_email_to_admins(subject: str, message: str) -> None:
    django_send_mail(
        subject if subject.startswith("[METIS] ") else f"[METIS] {subject}",
        message,
        "metis@ugent.be",
        settings.ADMINS,
        fail_silently=False,
    )


def send_template_email(
    *, from_email: str = "Metis <metis@ugent.be>", to: list[str], template: "EmailTemplate", instance
) -> None:
    try:
        subject = template.subject
        templ = Template(template.body)
        text_content = templ.render(Context({"obj": instance}))
        html_content = markdown(text_content)
        msg = EmailMultiAlternatives(
            subject, text_content, from_email=from_email, to=to, bcc=template.bcc, reply_to=template.reply_to
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        from metis.models.emails import EmailLog

        EmailLog.objects.create(
            template=template,
            user=instance.user if hasattr(instance, "user") else None,
            to=", ".join(to),
            bcc=", ".join(template.bcc) if template.bcc else None,
            reply_to=", ".join(template.reply_to) if template.reply_to else None,
            subject=subject,
            body=text_content,
        )

    except Exception as e:
        send_email_to_admins("Email error", f"Error while sending email: {e}")
        raise e


def send_invitation_email(invitation: "Invitation", education: Optional["Education"] = None) -> None:
    from metis.models import EmailTemplate

    try:
        template = EmailTemplate.objects.get(education=education, code=f"invitation.{invitation.type}")
    except EmailTemplate.DoesNotExist:
        send_email_to_admins("Invitation email template not found", str(invitation))
        return

    send_template_email(to=[invitation.email], template=template, instance=invitation)
