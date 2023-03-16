from django.contrib import admin

from sparta.models.stages.internships import Internship
from ..rel.remarks import RemarksInline


@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    # form
    raw_id_fields = ("program_internship", "student", "place")
    inlines = (RemarksInline,)
