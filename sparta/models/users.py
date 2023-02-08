from django.contrib.auth.models import AbstractUser

from .rel.links import LinksMixin
from .rel.remarks import RemarksMixin


class User(LinksMixin, RemarksMixin, AbstractUser):
    pass
