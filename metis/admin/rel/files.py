from django.contrib.contenttypes.admin import GenericTabularInline

from metis.models.rel.files import File


class FilesInline(GenericTabularInline):
    """Reusable inline for File model."""

    model = File
    classes = ("collapse",)
    extra = 0
