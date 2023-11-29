from django.contrib.contenttypes.admin import GenericTabularInline

from metis.models.rel.remarks import Remark


class RemarksInline(GenericTabularInline):
    """Reusable inline for Remark model."""

    model = Remark
    classes = ("collapse",)
    extra = 0
    # form
    readonly_fields = ("created_by", "created_at")
