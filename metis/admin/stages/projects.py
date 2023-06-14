from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html

from metis.models.stages.projects import Project, Period
from ..base import BaseModelAdmin
from .dates import ImportantDatesInline


@admin.register(Period)
class PeriodAdmin(BaseModelAdmin):
    list_display = ("id", "project", "program_internship", "start_date", "end_date")
    list_filter = (("program_internship__block__program__education", admin.RelatedOnlyFieldListFilter),)

    def has_module_permission(self, request) -> bool:
        return False


class PeriodsInline(admin.TabularInline):
    model = Period
    extra = 0


@admin.register(Project)
class ProjectAdmin(BaseModelAdmin):
    list_display = ("name", "education", "is_active", "internships_link")
    list_filter = (("education", admin.RelatedOnlyFieldListFilter), "is_active")
    # form
    raw_id_fields = ("education",)
    inlines = (PeriodsInline, ImportantDatesInline)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(Count("internships", distinct=True))

    def internships_link(self, obj):
        if obj.internships__count == 0:
            return "-"
        url = reverse("admin:metis_internship_changelist")
        return format_html(f'<a href="{url}?project__id__exact={obj.id}">{obj.internships__count}</a>')
