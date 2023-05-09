import os

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from typing import Optional


def get_upload_path(instance, filename):
    return f"private/{instance.content_type_id}/{instance.object_id}/{filename}".lower()


class File(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="files")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    file = models.FileField(upload_to=get_upload_path)
    position = models.PositiveSmallIntegerField(default=0)
    code = models.CharField(max_length=32, null=True, blank=True)
    version = models.PositiveSmallIntegerField(default=1)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "metis_rel_file"
        indexes = [models.Index(fields=["file"])]
        ordering = ["content_type", "object_id", "position"]
        unique_together = ("content_type", "object_id", "code", "version")

    def delete(self, *args, **kwargs):
        if os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super().delete(*args, **kwargs)


class FilesMixin(models.Model):
    files = GenericRelation(File)

    class Meta:
        abstract = True

    def get_file(self, code: str, version: Optional[int] = None) -> File:
        if version is not None:
            return self.files.get(code=code, version=version)
        return self.files.get(code=code)
