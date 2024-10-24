from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from metis.models.users import User

from .rel.remarks import RemarksInline


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """User model representation on admin."""

    search_fields = ("username", "email", "first_name", "last_name")
    # form
    inlines = (RemarksInline,)
