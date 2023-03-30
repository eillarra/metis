from django.db import models

from .base import BaseModel


class Discipline(BaseModel):
    education = models.ForeignKey("sparta.Education", related_name="disciplines", on_delete=models.PROTECT)
    name = models.CharField(max_length=160)
    external_name = models.CharField(max_length=160, null=True)
    color = models.CharField(max_length=16, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name
