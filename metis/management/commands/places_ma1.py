from django.core.management.base import BaseCommand

from metis.tasks.emails import schedule_important_date_emails


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        schedule_important_date_emails()
