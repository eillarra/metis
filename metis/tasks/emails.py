from huey.contrib.djhuey import task

from metis.services.mailer import send_mail


@task()  # rate_limit="2/m")
def send_template_mail(template: str, subject: str, from_email: str, to: list[str], context_data: dict = {}):
    send_email(
        template=template,
        subject=subject,
        from_email=from_email,
        to=to,
        context_data=context_data,
    )
