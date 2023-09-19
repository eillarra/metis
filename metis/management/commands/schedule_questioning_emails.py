from django.core.management.base import BaseCommand

from metis.tasks.emails import schedule_questioning_emails


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        schedule_questioning_emails(force_send=True)
