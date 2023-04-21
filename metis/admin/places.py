from django.contrib import admin

from metis.models.places import Region, Place
from .base import BaseModelAdmin
from .rel.remarks import RemarksInline


@admin.register(Region)
class RegionAdmin(BaseModelAdmin):
    def has_module_permission(self, request) -> bool:
        return False


@admin.register(Place)
class PlaceAdmin(BaseModelAdmin):
    list_filter = ("type",)
    # form
    autocomplete_fields = ("disciplines",)
    inlines = (RemarksInline,)
