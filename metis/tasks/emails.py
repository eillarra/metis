from django.core.mail import EmailMultiAlternatives
from django.utils.timezone import now
from huey import crontab
from huey.contrib.djhuey import db_periodic_task
from markdown import markdown
from time import sleep

from metis.models.emails import EmailTemplate, EmailLog
from metis.models.stages.dates import ImportantDate, get_project_places_for_date
from metis.services.mailer import schedule_template_email


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
            from_email="Metis <metis@ugent.be>",
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
def schedule_important_date_emails():
    active_important_dates = ImportantDate.objects.filter_active()
    senders = {
        ImportantDate.PROJECT_PLACE_INFORMATION: schedule_project_place_information_email,
    }

    for important_date in active_important_dates:
        try:
            senders[important_date.type](important_date)
        except KeyError:
            raise Exception(f"Sender for ImportantDate `{important_date.type}` does not exist.")


def schedule_project_place_information_email(important_date: ImportantDate):
    project_places = get_project_places_for_date(important_date)

    for project_place in project_places:
        if project_place.form_responses.filter(form=important_date.form).exists():
            continue

        place = project_place.place
        admins = place.contacts.filter(is_admin=True)

        if admins:
            try:
                email_template = EmailTemplate.objects.get(
                    code=important_date.type, education=important_date.project.education
                )
            except EmailTemplate.DoesNotExist:
                raise Exception(f"EmailTemplate for {important_date.type} does not exist.")

            for admin in admins:
                schedule_template_email(
                    from_email=f"{place.education.short_name} UGent <metis@ugent.be>",
                    template=email_template,
                    to=[admin.user.email],
                    context={
                        "project": important_date.project,
                        "important_date": important_date,
                        "place": place,
                    },
                    log_user=admin.user,
                )
