from django.contrib import admin

from metis.models.disciplines import Discipline
from .base import BaseModelAdmin


@admin.register(Discipline)
class DisciplineAdmin(BaseModelAdmin):
    list_filter = ("education",)
    search_fields = ("code", "name")
