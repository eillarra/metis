from django.contrib import admin

from sparta.models.faculties import Faculty, Education
from .rel.permissions import ManagersInline


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ("name", "full_name")


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name", "faculty")
    list_filter = ("faculty", "type")
    # form
    inlines = (ManagersInline,)
