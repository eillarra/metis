from django.contrib import admin

from metis.models.stages.questionings import Questioning


class QuestioningsInline(admin.TabularInline):
    """Inline for Questioning model. Used in Project."""

    model = Questioning
    extra = 0
    # form
    raw_id_fields = ("period",)
