from django.contrib import admin

from metis.models.institutions import Region, Institution
from .base import BaseModelAdmin
from .rel.remarks import RemarksInline


@admin.register(Region)
class RegionAdmin(BaseModelAdmin):
    def has_module_permission(self, request) -> bool:
        return False


@admin.register(Institution)
class InstitutionAdmin(BaseModelAdmin):
    list_filter = ("type",)
    # form
    inlines = (RemarksInline,)
