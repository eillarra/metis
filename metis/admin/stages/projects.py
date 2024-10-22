from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html

from metis.models.stages.projects import Period, Project

from ..base import BaseModelAdmin
from ..rel.files import FilesInline
from .questionings import QuestioningsInline


@admin.register(Period)
class PeriodAdmin(BaseModelAdmin):
    """Period model representation on admin."""

    list_display = ("id", "project", "program_internship", "start_date", "end_date")
    list_filter = (("program_internship__block__program__education", admin.RelatedOnlyFieldListFilter),)

    def has_module_permission(self, request) -> bool:
        """Hide Period model from admin homepage."""
        return False  # pragma: no cover


class PeriodsInline(admin.TabularInline):
    """Periods inline for Project admin."""

    model = Period
    extra = 0


@admin.register(Project)
class ProjectAdmin(BaseModelAdmin):
    """Project model representation on admin."""

    list_display = ("name", "education", "is_active", "internships_link")
    list_filter = (("education", admin.RelatedOnlyFieldListFilter), "is_active")
    # form
    raw_id_fields = ("education",)
    inlines = (PeriodsInline, QuestioningsInline, FilesInline)

    def get_queryset(self, request):
        """Return queryset with internship count."""
        return super().get_queryset(request).annotate(Count("internships", distinct=True))

    def internships_link(self, obj) -> str:
        """Return link to Internship list filtered by project."""
        if obj.internships__count == 0:
            return "-"
        url = reverse("admin:metis_internship_changelist")
        return format_html('<a href="{}?project__id__exact={}">{}</a>', url, obj.id, obj.internships__count)
