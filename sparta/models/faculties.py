from django.db import models

from .base import BaseModel


class Faculty(BaseModel):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "faculties"

    def __str__(self) -> str:
        return self.name


class Degree(BaseModel):
    MASTER = "master"
    BACHELOR = "bachelor"
    TYPES = (
        (MASTER, "Master"),
        (BACHELOR, "Bachelor"),
    )

    faculty = models.ForeignKey(Faculty, null=True, related_name="degrees", on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=16, choices=TYPES)

    def __str__(self) -> str:
        return self.name
