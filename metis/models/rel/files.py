from typing import TYPE_CHECKING

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse

from metis.services.file_guard import check_file_access
from metis.services.s3 import delete_s3_object


if TYPE_CHECKING:
    from metis.models.users import User


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
        try:
            delete_s3_object(self.s3_object_key)
        except Exception:
            pass
        super().delete(*args, **kwargs)

    def is_accessible_by_user(self, user: "User") -> bool:
        if self.file.name.startswith("public/"):
            return True
        return check_file_access(self, user)

    @property
    def s3_object_key(self):
        return self.file.name

    @property
    def url(self):
        return reverse("media_file", args=[self.file.name])


class FilesMixin(models.Model):
    files = GenericRelation(File)

    class Meta:
        abstract = True

    def get_file(self, code: str, version: int | None = None) -> File:
        if version is not None:
            return self.files.get(code=code, version=version)
        return self.files.filter(code=code).order_by("-version").first()
