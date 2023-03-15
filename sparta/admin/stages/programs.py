from django.contrib import admin

from sparta.models.stages.programs import Program, Track


class TrackInline(admin.TabularInline):
    model = Track
    extra = 0


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    date_hierarchy = "valid_from"
    list_display = ("name", "education", "valid_from", "valid_until")
    list_filter = (("education", admin.RelatedOnlyFieldListFilter),)
    # form
    raw_id_fields = ("education",)
    inlines = (TrackInline,)
