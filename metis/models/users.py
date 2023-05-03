from django.contrib.auth.models import AbstractUser

from .rel.addresses import AddressesMixin
from .rel.links import LinksMixin
from .rel.phone_numbers import PhoneNumbersMixin


class User(AddressesMixin, PhoneNumbersMixin, LinksMixin, AbstractUser):
    def __str__(self) -> str:
        return f"{self.username} ({self.name})"

    @property
    def name(self) -> str:
        return f"{self.first_name} {self.last_name}"
