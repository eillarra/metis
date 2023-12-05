from django.contrib import admin

from metis.models.places import Place, PlaceType

from .base import BaseModelAdmin
from .rel.files import FilesInline
from .rel.remarks import RemarksInline


@admin.register(Place)
class PlaceAdmin(BaseModelAdmin):
    """Place model representation on admin."""

    search_fields = ("code", "name")
    list_display = ("id", "code", "name", "education")
    list_filter = ("type", "education")
    # form
    inlines = (FilesInline, RemarksInline)
    raw_id_fields = ("parent",)

    def get_queryset(self, request):
        """Return queryset with prefetched related models."""
        return super().get_queryset(request).prefetch_related("education")


@admin.register(PlaceType)
class PlaceTypeAdmin(BaseModelAdmin):
    """PlaceType model representation on admin."""

    list_filter = ("education",)

    def has_module_permission(self, request) -> bool:
        """Hide PlaceType model from admin homepage."""
        return False  # pragma: no cover
