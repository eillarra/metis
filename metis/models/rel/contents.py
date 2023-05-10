from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from modeltranslation.translator import TranslationOptions

from ..base import BaseModel
from .files import FilesMixin


class Content(FilesMixin, BaseModel):
    """
    Text contents (information, notes, etc.).
    Files can be attached to the content.
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
        db_table = "metis_rel_content"
        unique_together = ("content_type", "object_id", "code", "version")

    @classmethod
    def duplicate(cls, code: str) -> "Content":
        content = cls.objects.filter(code=code).order_by("-version").first()
        if content is None:
            raise cls.DoesNotExist
        content.pk = None
        content.version += 1
        content.save()
        return content


class ContentTranslationOptions(TranslationOptions):
    fields = ("title", "text")


class ContentsMixin(models.Model):
    contents = GenericRelation(Content)

    class Meta:
        abstract = True

    def get_content(self, code: str) -> Content:
        return self.contents.get(code=code)
