import datetime
import os

from django.core.mail import EmailMultiAlternatives
from django.utils.timezone import now
from huey import crontab
from huey.contrib.djhuey import db_periodic_task
from markdown import markdown
from smtplib import SMTPRecipientsRefused
from time import sleep

from metis.models.emails import EmailTemplate, EmailLog
from metis.models.stages.questionings import Questioning
from metis.services.mailer import schedule_template_email, send_email_to_admins
from metis.utils.dates import remind_deadline


EMAILS_PER_MINUTE = int(os.getenv("UGENT_EMAILS_PER_MINUTE", 2))


@db_periodic_task(crontab(minute="*"))
def send_email():
    """
    Send the emails that are scheduled.
    If we get access to mass mailing, use EMAILS_PER_MINUTE to adjust the amount of emails sent.
    """

    # TODO: see what should be done here and what in the service

    emails = EmailLog.objects.filter(sent_at=None).order_by("created_at")[:EMAILS_PER_MINUTE]

    for email in emails:
        try:
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
        except SMTPRecipientsRefused as e:
            # set sent at as epoch 0 to prevent retrying
            email.sent_at = datetime.datetime.utcfromtimestamp(0)
            email.save()
            send_email_to_admins("Email error", f"Recipient refused: {e}")
            raise e
        except Exception as e:
            send_email_to_admins("Email error", f"Error while sending email: {e}")
            raise e

        sleep((60 / EMAILS_PER_MINUTE))


@db_periodic_task(crontab(hour="8", minute="0"))
def schedule_questioning_emails(*, force_send: bool = False):
    active_questionings = Questioning.objects.filter_active()
    senders = {
        Questioning.PROJECT_PLACE_INFORMATION: schedule_project_place_information_email,
        Questioning.STUDENT_TOPS: schedule_student_tops_email,
    }

    for questioning in active_questionings:
        if not questioning.has_email:
            continue

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
