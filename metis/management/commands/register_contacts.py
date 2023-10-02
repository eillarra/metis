from django.core.management.base import BaseCommand

from metis.services.graph import GraphAPI


class Command(BaseCommand):
    """Use Microsoft Graph API to register emails on Metis.

    This command takes one or more email addresses as arguments and registers them on the UGent tenant.
    For each email address, the command prints whether the email was newly registered or already registered,
    the corresponding Graph API ID, and whether the email is enabled or disabled.

    :usage:
    >>> python manage.py register_contacts <email> [<email> ...]
    """

    def add_arguments(self, parser):
        parser.add_argument("emails", nargs="*", type=str)

    def handle(self, *args, **options):
        with GraphAPI() as graph:
            for email in options["emails"]:
                new_registration, graph_id, enabled = graph.register_email(email)
                print(
                    f"Registered {email}:" if new_registration else f"{email} already registered:",
                    graph_id,
                    "(enabled)" if enabled else "(disabled)",
                )
