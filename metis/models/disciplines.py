from django.db import models
from modeltranslation.translator import TranslationOptions

from .base import BaseModel


class Discipline(BaseModel):
    """A discipline is a subject or field of study that is part of an education."""

    education = models.ForeignKey("metis.Education", related_name="disciplines", on_delete=models.PROTECT)
    code = models.CharField(max_length=16)
    name = models.CharField(max_length=160)
    color = models.CharField(max_length=16, default="")

    class Meta:  # noqa: D106
        ordering = ["code"]
        unique_together = ["education", "code"]

    def __str__(self) -> str:
        return self.code


class DisciplineTranslationOptions(TranslationOptions):
    """Translation options for Discipline model."""

    fields = ("name",)
