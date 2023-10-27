from django.contrib.contenttypes.admin import GenericTabularInline

from metis.models.rel.files import File


class FilesInline(GenericTabularInline):
    model = File
    classes = ("collapse",)
    extra = 0
