from django.contrib import admin

from metis.models.stages.programs import Program, ProgramBlock, ProgramInternship, Track, TrackInternship

from ..base import BaseModelAdmin
from .constraints import DisciplineConstraintsInline


class ProgramBlockInline(admin.TabularInline):
    """ProgramBlock inline for Program admin."""

    model = ProgramBlock
    extra = 0


@admin.register(Program)
class ProgramAdmin(BaseModelAdmin):
    """Program model representation on admin."""

    date_hierarchy = "valid_from"
    list_display = ("name", "education", "valid_from", "valid_until")
    list_filter = (("education", admin.RelatedOnlyFieldListFilter),)
    # form
    inlines = (ProgramBlockInline,)


@admin.register(ProgramInternship)
class ProgramInternshipAdmin(BaseModelAdmin):
    """ProgramInternship model representation on admin."""

    list_filter = (("block__program", admin.RelatedOnlyFieldListFilter),)
    # form
    inlines = (DisciplineConstraintsInline,)


class TrackInternshipInline(admin.TabularInline):
    """TrackInternship inline for Track admin."""

    model = TrackInternship
    extra = 0


@admin.register(Track)
class TrackAdmin(BaseModelAdmin):
    """Track model representation on admin."""

    list_filter = (("program", admin.RelatedOnlyFieldListFilter),)
    # form
    inlines = (TrackInternshipInline, DisciplineConstraintsInline)
