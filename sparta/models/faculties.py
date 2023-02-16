from django.db import models

from .base import BaseModel
from .rel.permissions import PermissionsMixin


class Faculty(BaseModel):
    name = models.CharField(max_length=32)
    full_name = models.CharField(max_length=160)

    class Meta:
        verbose_name_plural = "faculties"

    def __str__(self) -> str:
        return self.name


class Education(PermissionsMixin, BaseModel):
    faculty = models.ForeignKey(Faculty, null=True, related_name="educations", on_delete=models.SET_NULL)
    name = models.CharField(max_length=160)

    def __str__(self) -> str:
        return self.name
