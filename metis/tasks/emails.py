import datetime
import os
from smtplib import SMTPRecipientsRefused
from time import sleep

from django.core.mail import EmailMultiAlternatives
from django.utils.timezone import now
from huey import crontab
from huey.contrib.djhuey import db_periodic_task
from markdown import markdown

from metis.models.emails import EmailLog
from metis.models.stages.questionings import Questioning
from metis.services.mailer import render_context, schedule_email, send_email_to_admins
from metis.utils.dates import remind_deadline


EMAILS_PER_MINUTE = int(os.getenv("UGENT_EMAILS_PER_MINUTE", 2))


@db_periodic_task(crontab(minute="*"))
def send_email() -> None:
    """Send the emails that are scheduled.

    TODO: if we get access to mass mailing, use EMAILS_PER_MINUTE to adjust the amount of emails sent
    TODO: see what should be done here and what in the service
    """
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
            email.sent_at = datetime.datetime.fromtimestamp(0, datetime.UTC)
            email.save()
            send_email_to_admins("Email error", f"Recipient refused: {e}")
            raise e
        except Exception as e:
            send_email_to_admins("Email error", f"Error while sending email: {e}")
            raise e

        sleep(60 / EMAILS_PER_MINUTE)


@db_periodic_task(crontab(hour="8", minute="0"))
def schedule_active_questioning_emails(*, force_send: bool = False):
    """Schedule the emails for the active questionings.

    This is an automated task that runs every day at 8:00.

    Args:
    ----
        force_send: Whether to send the emails even if we are not in the remind window.

    """
    active_questionings = Questioning.objects.filter_active()

    for questioning in active_questionings:
        if not questioning.has_email:
            continue

        if not force_send and not remind_deadline(now(), questioning.end_at):
            continue

        schedule_questioning_email(questioning)


def schedule_questioning_email(questioning: Questioning, *, filtered_ids: list | None = None):
    """Schedule the emails for the given questioning."""
    senders = {
        Questioning.PROJECT_PLACE_INFORMATION: schedule_project_place_information_email,
        Questioning.STUDENT_INFORMATION: schedule_student_questioning_email,
        Questioning.STUDENT_TOPS: schedule_student_questioning_email,
    }

    if not questioning.has_email:
        return

    try:
        senders[questioning.type](questioning, filtered_ids)
    except KeyError as exc:
        raise Exception(f"Sender for Questioning `{questioning.type}` does not exist.") from exc


def schedule_project_place_information_email(questioning: Questioning, filtered_ids: list | None = None) -> None:
    """TODO: move from task to a service, as it is reused by the API."""
    target_group = questioning.get_target_group()

    if filtered_ids:
        target_group = target_group.filter(id__in=filtered_ids)

    for project_place in target_group:
        if project_place.form_responses.filter(questioning=questioning).exists():
            continue

        place = project_place.place
        admins = place.contacts.filter(is_admin=True)

        context = {
            "project": questioning.project,
            "questioning": questioning,
            "place": place,
        }

        if admins:
            for admin in admins:
                schedule_email(
                    from_email=f"{place.education.short_name} UGent <metis@ugent.be>",
                    to=[admin.user.email],
                    reply_to=[questioning.project.education.office_email],
                    subject=render_context(questioning.email_subject, context),
                    text_content=render_context(questioning.email_body, context),
                    log_user=admin.user,
                    log_project=questioning.project,
                    tags=[
                        "type:questioning.reminder",
                        f"questioning.id:{questioning.id}",
                        f"user.id:{admin.user.id}",
                        f"place.id:{place.id}",
                    ],
                )


def schedule_student_questioning_email(questioning: Questioning, filtered_ids: list | None = None) -> None:
    """TODO: move from task to a service, as it is reused by the API.
    And there are things that can be cleaned up, now that we have target groups as model method...
    And fix typing...
    """
    target_group = questioning.get_target_group()

    if filtered_ids:
        target_group = target_group.filter(id__in=filtered_ids)

    for student in target_group:
        if student.form_responses.filter(questioning=questioning).exists():
            continue

        context = {
            "project": questioning.project,
            "questioning": questioning,
            "student": student,
        }

        schedule_email(
            from_email=f"{questioning.project.education.short_name} UGent <metis@ugent.be>",
            to=[student.user.email],
            reply_to=[questioning.project.education.office_email],
            subject=render_context(questioning.email_subject, context),
            text_content=render_context(questioning.email_body, context),
            log_user=student.user,
            log_project=questioning.project,
            tags=["type:questioning.reminder", f"questioning.id:{questioning.id}", f"user.id:{student.user.id}"],
        )
