from django.contrib import admin

from metis.models.education_places import EducationPlace
from .base import BaseModelAdmin
from .rel.remarks import RemarksInline


@admin.register(EducationPlace)
class EducationPlaceAdmin(BaseModelAdmin):
    list_filter = ("place__type",)
    # form
    inlines = (RemarksInline,)
