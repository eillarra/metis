from django.contrib import admin

from metis.models.stages.questionings import Questioning


class QuestioningsInline(admin.TabularInline):
    model = Questioning
    extra = 0
    # form
    raw_id_fields = ("period",)
