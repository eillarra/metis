from typing import Optional

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from modeltranslation.translator import TranslationOptions

from ..base import BaseModel
from .files import FilesMixin


class TextEntry(FilesMixin, BaseModel):
    """Texts (information, notes, etc.)."""

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="contents")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    code = models.CharField(max_length=32)
    version = models.PositiveSmallIntegerField(default=1)
    title = models.CharField(max_length=160)
    text = models.TextField()

    class Meta:  # noqa: D106
        db_table = "metis_rel_text"
        unique_together = ("content_type", "object_id", "code", "version")


class TextEntryTranslationOptions(TranslationOptions):
    """Translation options for the TextEntry model."""

    fields = ("title", "text")


class TextEntriesMixin(models.Model):
    """Mixin for models that can have text entries."""

    texts = GenericRelation(TextEntry)

    class Meta:  # noqa: D106
        abstract = True

    def get_text(self, code: str) -> Optional["TextEntry"]:
        """Get the text entry with the given code."""
        try:
            return self.texts.filter(code=code).order_by("-version").first()
        except TextEntry.DoesNotExist:
            return None
