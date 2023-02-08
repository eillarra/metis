from django.contrib import admin

from sparta.models.stages.programmes import Programme, DisciplineRule


class DisciplineRuleInline(admin.TabularInline):
    model = DisciplineRule
    extra = 0
    # form
    autocomplete_fields = ("disciplines",)


@admin.register(Programme)
class ProgrammeAdmin(admin.ModelAdmin):
    date_hierarchy = "valid_from"
    list_display = ("name", "education", "valid_from", "valid_until")
    list_filter = (("education", admin.RelatedOnlyFieldListFilter),)
    # form
    raw_id_fields = ("education",)
    inlines = (DisciplineRuleInline,)
