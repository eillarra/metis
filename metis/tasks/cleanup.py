from datetime import timedelta
from django.core.management import call_command
from django.utils.timezone import now
from huey import crontab
from huey.contrib.djhuey import db_periodic_task

from metis.models.rel import Invitation


@db_periodic_task(crontab(hour="*/4", minute="0"))
def clear_expired_sessions():
    return call_command("clearsessions")


@db_periodic_task(crontab(hour="*/4", minute="5"))
def clear_expired_invitations():
    two_days_ago = now() - timedelta(days=2)
    return Invitation.objects.filter(created_at__lt=two_days_ago).delete()
