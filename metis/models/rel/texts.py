from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from modeltranslation.translator import TranslationOptions
from typing import Optional

from ..base import BaseModel
from .files import FilesMixin


class TextEntry(FilesMixin, BaseModel):
    """
    Texts (information, notes, etc.).
    Files can be attached to the text entry.
    """

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="contents")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    code = models.CharField(max_length=32)
    version = models.PositiveSmallIntegerField(default=1)
    title = models.CharField(max_length=160)
    text = models.TextField()

    created_by = models.ForeignKey("metis.User", related_name="contents", on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "metis_rel_text"
        unique_together = ("content_type", "object_id", "code", "version")


class TextEntryTranslationOptions(TranslationOptions):
    fields = ("title", "text")


class TextEntriesMixin(models.Model):
    texts = GenericRelation(TextEntry)

    class Meta:
        abstract = True

    def get_text(self, code: str) -> Optional["TextEntry"]:
        try:
            return self.texts.filter(code=code).order_by("-version").first()
        except TextEntry.DoesNotExist:
            return None
