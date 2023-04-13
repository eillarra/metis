from django.contrib import admin

from epione.models.stages.programs import Program, ProgramBlock, ProgramInternship, Track, TrackInternship
from ..base import BaseModelAdmin
from .constraints import DisciplineConstraintsInline


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


@admin.register(ProgramInternship)
class ProgramInternshipAdmin(BaseModelAdmin):
    list_filter = (("block__program", admin.RelatedOnlyFieldListFilter),)
    # form
    inlines = (DisciplineConstraintsInline,)


class TrackInternshipInline(admin.TabularInline):
    model = TrackInternship
    extra = 0


@admin.register(Track)
class TrackAdmin(BaseModelAdmin):
    list_filter = (("program", admin.RelatedOnlyFieldListFilter),)
    # form
    inlines = (TrackInternshipInline, DisciplineConstraintsInline)
