from django.db import models

from .base import BaseModel


class Discipline(BaseModel):
    education = models.ForeignKey("metis.Education", related_name="disciplines", on_delete=models.PROTECT)
    code = models.CharField(max_length=16)
    name = models.CharField(max_length=160)
    color = models.CharField(max_length=16, null=True)

    class Meta:
        ordering = ["code"]
        unique_together = ["education", "code"]

    def __str__(self) -> str:
        return self.code