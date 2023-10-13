from django.core.management.base import BaseCommand

from metis.models.rel.signatures import Signature


class Command(BaseCommand):
    """Print the signed text of an encrypted signature.

    :usage:
    >>> python manage.py read_signature <signature_id>
    """

    def add_arguments(self, parser):
        parser.add_argument("signature_id", type=int)

    def handle(self, *args, **options):
        signature = Signature.objects.get(id=options["signature_id"])
        print(signature.signed_text)
