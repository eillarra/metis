from typing import TYPE_CHECKING

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from metis.models.base import TagsMixin
from metis.services.file_guard import check_file_access
from metis.services.s3 import delete_s3_object


if TYPE_CHECKING:
    from metis.models.users import User


def append_files_tags(obj, *, tags: list[str]) -> list[str]:
    """For an object, process the tags."""
    tags = [tag for tag in tags if not tag.startswith("files.")]
    tags.append(f"files.count:{obj.files.count()}")
    return tags


def get_upload_path(instance, filename) -> str:
    """Return the path to upload a file."""
    return f"private/{instance.content_type_id}/{instance.object_id}/{filename}".lower()


class File(TagsMixin, models.Model):
    """A file attached to a model."""

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="files")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    file = models.FileField(upload_to=get_upload_path)
    position = models.PositiveSmallIntegerField(default=0)
    code = models.CharField(max_length=32, null=True, blank=True)  # noqa: DJ001
    version = models.PositiveSmallIntegerField(default=1)
    description = models.TextField(default="", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:  # noqa: D106
        db_table = "metis_rel_file"
        indexes = [models.Index(fields=["file"])]
        ordering = ["content_type", "object_id", "position"]
        unique_together = ("content_type", "object_id", "code", "version")

    def __str__(self) -> str:
        return f"{self.file.name} (v{self.version})"

    def delete(self, *args, **kwargs):
        """Delete the file from S3 before deleting the model."""
        try:
            delete_s3_object(self.s3_object_key)
        except Exception:
            pass
        super().delete(*args, **kwargs)

    def is_accessible_by_user(self, user: "User") -> bool:
        """Check if the file is accessible by the user."""
        if self.file.name.startswith("public/"):
            return True
        return check_file_access(self, user)

    def is_visible_for_target_group(self, target_group: str) -> bool:
        """Check if the file is visible for the target group."""
        return any(tag.startswith(f"_visible:{target_group}") for tag in self.tags)

    @property
    def s3_object_key(self):
        """The S3 object key."""
        return self.file.name

    @property
    def url(self):
        """The URL to the file."""
        return reverse("media_file", args=[self.file.name])


class FilesMixin(models.Model):
    """A mixin to add files to a model."""

    files = GenericRelation(File)

    class Meta:  # noqa: D106
        abstract = True

    def get_latest_files(self, target_group: str | None = None) -> list[File]:
        """Return the latest version only of each file.

        We are not dealing with a lot of files and DISTINCT ON is not supported by MySQL,
        so this should fine to get the latest version of the files.
        """
        valid_target_groups = {"place", "student", "mentor"}
        files = self.files.all()

        if target_group:
            if target_group not in valid_target_groups:
                raise ValueError(f"Invalid target group: {target_group}")

            files = files.filter(tags__contains=[f"_visible:{target_group}"])

        """
        TODO: remove code that deals with codes and versions, as we will simply use tags.
        versions = {}

        for file in files:
            versions[file.code] = max(versions.get(file.code, 0), file.version)

        return [file for file in files if file.code and file.version == versions[file.code]]
        """

        return files

    def get_file(self, code: str, version: int | None = None) -> File:
        """Return a file by its code and version."""
        if version is not None:
            return self.files.get(code=code, version=version)
        return self.files.filter(code=code).order_by("-version").first()


@receiver(post_save, sender=File)
def update_internship_tags(sender, instance, **kwargs):
    """Update the tags of the associated internship when an evaluation is saved."""
    from metis.models import Internship, Place

    if isinstance(instance.content_object, Internship):
        Internship.update_tags(instance.content_object, type="files")

    if isinstance(instance.content_object, Place):
        Place.update_tags(instance.content_object, type="files")
