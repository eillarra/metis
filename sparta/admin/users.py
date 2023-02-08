from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from sparta.models.users import User
from .rel.remarks import RemarksInline


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # form
    inlines = (RemarksInline,)
