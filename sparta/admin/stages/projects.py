from django.contrib import admin

from sparta.models.stages.projects import Project, Period


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    def has_module_permission(self, request) -> bool:
        return False


class PeriodInline(admin.TabularInline):
    model = Period
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "education", "is_active")
    list_filter = (("education", admin.RelatedOnlyFieldListFilter), "is_active")
    # form
    raw_id_fields = ("education",)
    inlines = (PeriodInline,)
