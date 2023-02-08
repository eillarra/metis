from django.contrib import admin

from sparta.models.places import Place
from .rel.remarks import RemarksInline


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_filter = ("type",)
    # form
    autocomplete_fields = ("disciplines",)
    inlines = (RemarksInline,)
