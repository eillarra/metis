from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from metis.models.stages.internships import Internship

from ..base import BaseModelAdmin
from ..rel.files import FilesInline
from ..rel.remarks import RemarksInline


@admin.register(Internship)
class InternshipAdmin(BaseModelAdmin):
    """Internship model representation on admin."""

    date_hierarchy = "start_date"
    list_display = ("id", "project", "student_name", "track", "period", "place", "discipline")
    list_filter = (
        ("project", admin.RelatedOnlyFieldListFilter),
        ("track", admin.RelatedOnlyFieldListFilter),
    )
    search_fields = ("student__user__first_name", "student__user__last_name")
    # form
    raw_id_fields = ("period", "student", "project_place")
    inlines = (FilesInline, RemarksInline)

    def get_queryset(self, request):
        """Return queryset with prefetched related models."""
        return (
            super()
            .get_queryset(request)
            .select_related("student__user")
            .prefetch_related("project", "track", "period", "project_place__place", "discipline")
        )

    def student_name(self, obj) -> str:
        """Return link to User admin."""
        url = reverse("admin:metis_user_changelist")
        if obj.student:
            return format_html(
                '<a href="{}{}" target="admin_user">{}</a>', url, obj.student.user_id, obj.student.user.name
            )
        return "-"
