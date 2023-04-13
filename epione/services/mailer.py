from django.core.mail import send_mail
from django.conf import settings


def send_mail_to_admins(subject: str, message: str) -> None:
    send_mail(
        subject if subject.startswith("[EPIONE] ") else f"[EPIONE] {subject}",
        message,
        "epione@ugent.be",
        settings.ADMINS,
        fail_silently=False,
    )
