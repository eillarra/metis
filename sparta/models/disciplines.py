from django.db import models

from .base import BaseModel


class Discipline(BaseModel):
    name = models.CharField(max_length=255)
    external_name = models.CharField(max_length=255, null=True)
    color = models.CharField(max_length=16, null=True)

    class Meta:
        ordering = ["position", "name"]

    def __str__(self) -> str:
        return self.name
