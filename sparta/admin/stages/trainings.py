from django.contrib import admin

from sparta.models.stages.trainings import Training
from ..rel.remarks import RemarksInline


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    # form
    raw_id_fields = ("block", "period", "student", "place")
    inlines = (RemarksInline,)
