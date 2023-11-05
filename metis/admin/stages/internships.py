from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from metis.models.stages.internships import Internship

from ..base import BaseModelAdmin
from ..rel.remarks import RemarksInline


@admin.register(Internship)
class InternshipAdmin(BaseModelAdmin):
    # date_hierarchy = "start_date"
    list_display = ("id", "project", "student_name", "track", "period", "place", "discipline")
    list_filter = (
        ("project", admin.RelatedOnlyFieldListFilter),
        ("track", admin.RelatedOnlyFieldListFilter),
    )
    search_fields = ("student__first_name", "student__last_name")
    # form
    raw_id_fields = ("period", "student", "project_place")
    inlines = (RemarksInline,)

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("student__user")
            .prefetch_related("project", "track", "period", "project_place__place", "discipline")
        )

    def student_name(self, obj):
        url = reverse("admin:metis_user_changelist")
        if obj.student:
            return format_html(f'<a href="{url}{obj.student_id}/" target="admin_user">{obj.student.user.name}</a>')
        return "-"
