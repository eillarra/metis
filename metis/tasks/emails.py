from django.core.mail import EmailMultiAlternatives
from django.utils.timezone import now
from huey import crontab
from huey.contrib.djhuey import db_periodic_task
from markdown import markdown
from time import sleep

from metis.models.emails import EmailTemplate, EmailLog
from metis.models.stages.questionings import Questioning
from metis.services.mailer import schedule_template_email
from metis.utils.dates import remind_deadline


@db_periodic_task(crontab(minute="*"))
def send_email():
    """
    We have rate limits to send emails via UGent, so we only try to send two emails every minute.
    TODO: see if we can increase this limit!
    """

    emails = EmailLog.objects.filter(sent_at=None).order_by("created_at")[:2]

    for email in emails:
        html_content = markdown(email.body)
        msg = EmailMultiAlternatives(
            email.subject,
            email.body,
            from_email=email.from_email,
            to=email.to,
            bcc=email.bcc,
            reply_to=email.reply_to,
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        email.sent_at = now()
        email.save()
        sleep(26)


@db_periodic_task(crontab(hour="8", minute="0"))
def schedule_questioning_emails(*, force_send: bool = False):
    active_questionings = Questioning.objects.filter_active()
    senders = {
        Questioning.PROJECT_PLACE_INFORMATION: schedule_project_place_information_email,
        Questioning.STUDENT_TOPS: schedule_student_tops_email,
    }

    for questioning in active_questionings:
        if not force_send and not remind_deadline(now(), questioning.end_at):
            continue

        try:
            senders[questioning.type](questioning)
        except KeyError:
            raise Exception(f"Sender for Questioning `{questioning.type}` does not exist.")


def schedule_project_place_information_email(questioning: Questioning, filtered_ids: list | None = None):
    """
    TODO: move from task to a service, as it is reused by the API.
    """
    try:
        email_template = EmailTemplate.objects.get(code=questioning.type, education=questioning.project.education)
    except EmailTemplate.DoesNotExist:
        raise Exception(f"EmailTemplate for {questioning.type} does not exist.")

    target_group = questioning.get_target_group()

    if filtered_ids:
        target_group = target_group.filter(id__in=filtered_ids)

    for project_place in target_group:
        if project_place.form_responses.filter(questioning=questioning).exists():
            continue

        place = project_place.place
        admins = place.contacts.filter(is_admin=True)

        if admins:
            for admin in admins:
                schedule_template_email(
                    from_email=f"{place.education.short_name} UGent <metis@ugent.be>",
                    template=email_template,
                    to=[admin.user.email],
                    context={
                        "project": questioning.project,
                        "questioning": questioning,
                        "place": place,
                    },
                    log_user=admin.user,
                )


def schedule_student_tops_email(questioning: Questioning, filtered_ids: list | None = None):
    """
    TODO: move from task to a service, as it is reused by the API.
    And there are things that can be cleaned up, now that we have target groups as model method...
    And fix typing...
    """
    target_group = questioning.get_target_group()

    if filtered_ids:
        target_group = target_group.filter(id__in=filtered_ids)

    if target_group:
        try:
            email_template = EmailTemplate.objects.get(code=questioning.type, education=questioning.project.education)
        except EmailTemplate.DoesNotExist:
            raise Exception(f"EmailTemplate for {questioning.type} does not exist.")

        for student in target_group:
            if student.form_responses.filter(questioning=questioning).exists():
                continue

            schedule_template_email(
                from_email=f"{questioning.project.education.short_name} UGent <metis@ugent.be>",
                template=email_template,
                to=[student.user.email],
                context={},
                log_user=student.user,
            )
