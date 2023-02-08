from django.contrib.contenttypes.admin import GenericTabularInline

from sparta.models.rel.permissions import Permission


class PermissionsInline(GenericTabularInline):
    model = Permission
    classes = ("collapse",)
    extra = 0
    title = "permissions"
    # form
    raw_id_fields = ("user",)


class ManagersInline(PermissionsInline):
    verbose_name = "manager"
    verbose_name_plural = "managers"
