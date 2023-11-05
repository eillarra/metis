from django.contrib import admin

from metis.models.educations import Education, Faculty

from .base import BaseModelAdmin


@admin.register(Faculty)
class FacultyAdmin(BaseModelAdmin):
    list_display = ("name",)


@admin.register(Education)
class EducationAdmin(BaseModelAdmin):
    search_fields = ("code", "name")
    list_display = ("code", "name", "faculty")
    list_filter = ("faculty",)
    # form
    autocomplete_fields = ("office_members",)
