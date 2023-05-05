from django.contrib import admin

from metis.models.places import Region, Place, EducationPlace
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
    inlines = (RemarksInline,)


@admin.register(EducationPlace)
class EducationPlaceAdmin(BaseModelAdmin):
    list_filter = ("place__type",)
    # form
    inlines = (RemarksInline,)
