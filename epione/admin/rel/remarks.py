from django.contrib.contenttypes.admin import GenericTabularInline

from epione.models.rel.remarks import Remark


class RemarksInline(GenericTabularInline):
    model = Remark
    classes = ("collapse",)
    extra = 0
    # form
    readonly_fields = ("created_by", "created_at")
