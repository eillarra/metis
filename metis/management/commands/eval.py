from django.core.management.base import BaseCommand

from metis.tasks.evaluations import schedule_evaluation_emails


class Command(BaseCommand):
    """Command to schedule questioning emails."""

    def handle(self, *args, **kwargs):
        """Handle command."""
        schedule_evaluation_emails()
