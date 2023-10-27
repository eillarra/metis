from django.core.management.base import BaseCommand

from metis.tasks.emails import schedule_active_questioning_emails


class Command(BaseCommand):
    """Command to schedule questioning emails."""

    def handle(self, *args, **kwargs):
        """Handle command."""
        schedule_active_questioning_emails(force_send=True)
