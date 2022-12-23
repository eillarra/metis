from django.contrib.auth.models import AbstractUser

from .rel.links import LinksMixin


class User(LinksMixin, AbstractUser):
    pass


class Contact(User):
    class Meta:
        proxy = True


class Student(User):
    class Meta:
        proxy = True
