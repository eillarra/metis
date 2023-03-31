from django.contrib import admin

from sparta.models.stages.programs import Program, ProgramBlock, Track, TrackInternship
from ..base import BaseModelAdmin


class ProgramBlockInline(admin.TabularInline):
    model = ProgramBlock
    extra = 0


@admin.register(Program)
class ProgramAdmin(BaseModelAdmin):
    date_hierarchy = "valid_from"
    list_display = ("name", "education", "valid_from", "valid_until")
    list_filter = (("education", admin.RelatedOnlyFieldListFilter),)
    # form
    inlines = (ProgramBlockInline,)


class TrackInternshipInline(admin.TabularInline):
    model = TrackInternship
    extra = 0


@admin.register(Track)
class TrackAdmin(BaseModelAdmin):
    list_filter = (("program", admin.RelatedOnlyFieldListFilter),)
    # form
    inlines = (TrackInternshipInline,)
