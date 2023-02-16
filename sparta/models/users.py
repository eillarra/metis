from django.contrib.auth.models import AbstractUser

from .rel.addresses import AddressesMixin
from .rel.links import LinksMixin
from .rel.remarks import RemarksMixin


class User(AddressesMixin, LinksMixin, RemarksMixin, AbstractUser):
    pass
