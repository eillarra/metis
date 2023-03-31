from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html

from sparta.models.stages.projects import Project, Period
from ..base import BaseModelAdmin


@admin.register(Period)
class PeriodAdmin(BaseModelAdmin):
    def has_module_permission(self, request) -> bool:
        return False


class PeriodInline(admin.TabularInline):
    model = Period
    extra = 0


@admin.register(Project)
class ProjectAdmin(BaseModelAdmin):
    list_display = ("name", "education", "is_active", "internships_link")
    list_filter = (("education", admin.RelatedOnlyFieldListFilter), "is_active")
    # form
    raw_id_fields = ("education",)
    inlines = (PeriodInline,)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(Count("internships", distinct=True))

    def internships_link(self, obj):
        if obj.internships__count == 0:
            return "-"
        url = reverse("admin:sparta_internship_changelist")
        return format_html(f'<a href="{url}?project__id__exact={obj.id}">{obj.internships__count}</a>')
