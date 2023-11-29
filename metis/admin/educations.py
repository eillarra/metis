from django.contrib import admin

from metis.models.educations import Education, Faculty

from .base import BaseModelAdmin


@admin.register(Faculty)
class FacultyAdmin(BaseModelAdmin):
    """Faculty model representation on admin."""

    list_display = ("name",)


@admin.register(Education)
class EducationAdmin(BaseModelAdmin):
    """Education model representation on admin."""

    search_fields = ("code", "name")
    list_display = ("code", "name", "faculty")
    list_filter = ("faculty",)
    # form
    autocomplete_fields = ("office_members",)
