from django.contrib import admin

from metis.models.places import Region, Place
from .base import BaseModelAdmin
from .rel.remarks import RemarksInline


@admin.register(Region)
class RegionAdmin(BaseModelAdmin):
    def has_module_permission(self, request) -> bool:
        return False  # pragma: no cover


@admin.register(Place)
class PlaceAdmin(BaseModelAdmin):
    search_fields = ("code", "name")
    list_display = ("id", "code", "name", "education")
    list_filter = ("type", "education")
    # form
    inlines = (RemarksInline,)
    raw_id_fields = ("parent",)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("education")
