from django.contrib import admin

from metis.models.emails import EmailTemplate

from .base import BaseModelAdmin


@admin.register(EmailTemplate)
class EmailTemplateAdmin(BaseModelAdmin):
    """EmailTemplate model representation on admin."""

    list_filter = ("education",)
