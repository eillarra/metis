from django.contrib.auth.models import AbstractUser

from .rel.addresses import AddressesMixin
from .rel.links import LinksMixin
from .rel.remarks import RemarksMixin


class User(AddressesMixin, LinksMixin, RemarksMixin, AbstractUser):
    pass


# add RemarksMixin: stagebureasus can add remarks to any user and these would be visible for other stage bureau users
