from django.contrib import admin

from metis.models.emails import EmailTemplate

from .base import BaseModelAdmin


@admin.register(EmailTemplate)
class FacultyAdmin(BaseModelAdmin):
    list_filter = ("education",)
