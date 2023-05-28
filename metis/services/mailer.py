from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail as django_send_mail
from django.template.loader import render_to_string
from markdown import markdown


def send_mail(
    *,
    from_email: str = "Metis <metis@ugent.be>",
    to: list[str],
    subject: str,
    template: str,
    context_data: dict,
    bcc: list[str] = [],
    reply_to: str | None = None,
):
    text_content = render_to_string(template, context_data)
    html_content = markdown(text_content)
    msg = EmailMultiAlternatives(
        subject, text_content, from_email=from_email, to=to, bcc=bcc, reply_to=[reply_to] if reply_to else None
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_mail_to_admins(subject: str, message: str) -> None:
    django_send_mail(
        subject if subject.startswith("[METIS] ") else f"[METIS] {subject}",
        message,
        "metis@ugent.be",
        settings.ADMINS,
        fail_silently=False,
    )
