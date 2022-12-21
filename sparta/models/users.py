from django.contrib.auth.models import User
from django.db import models

from .base import BaseModel
from .links import LinksMixin


class Contact(LinksMixin, BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=32)
    is_active = models.BooleanField(default=True)


class Student(LinksMixin, BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=32)
    is_active = models.BooleanField(default=True)
