from django.contrib import admin

from metis.models.places import Place, PlaceType
from .base import BaseModelAdmin
from .rel.remarks import RemarksInline


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


@admin.register(PlaceType)
class PlaceTypeAdmin(BaseModelAdmin):
    list_filter = ("education",)

    def has_module_permission(self, request) -> bool:
        return False  # pragma: no cover
