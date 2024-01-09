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
    """A file attached to a model."""

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="files")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    file = models.FileField(upload_to=get_upload_path)
    position = models.PositiveSmallIntegerField(default=0)
    code = models.CharField(max_length=32, null=True, blank=True)  # noqa: DJ001
    version = models.PositiveSmallIntegerField(default=1)
    description = models.TextField(default="", blank=True)

    class Meta:
        db_table = "metis_rel_file"
        indexes = [models.Index(fields=["file"])]
        ordering = ["content_type", "object_id", "position"]
        unique_together = ("content_type", "object_id", "code", "version")

    def __str__(self) -> str:
        return f"{self.file.name} (v{self.version})"

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
    """A mixin to add files to a model."""

    files = GenericRelation(File)

    class Meta:  # noqa: D106
        abstract = True

    def get_latest_files(self) -> list[File]:
        """Returns the latest version only of each file.

        We are not dealing with a lot of files and DISTINCT ON is not supported by MySQL,
        so this should fine to get the latest version of the files.
        """
        files = self.files.all()
        versions = {}

        for file in files:
            versions[file.code] = max(versions.get(file.code, 0), file.version)

        return [file for file in files if file.code and file.version == versions[file.code]]

    def get_file(self, code: str, version: int | None = None) -> File:
        """Returns a file by its code and version."""
        if version is not None:
            return self.files.get(code=code, version=version)
        return self.files.filter(code=code).order_by("-version").first()
