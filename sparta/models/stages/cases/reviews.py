from django.db import models
from django.utils.translation import pgettext_lazy

from sparta.models.base import BaseModel
from .cases import Case


class Review(BaseModel):
    UNFINISHED = 0  # `onafgewerkt` (= not sent on time)
    NEW = 1  # `nieuw`
    CONCEPT = 5  # `concept` => `onafgewerkt` ? (= niet definitief na einde evaluatieperiode)
    FINAL = 9  # `definitief`
    STATUSES = (
        (NEW, pgettext_lazy("cases.Review.status", "New")),
        (CONCEPT, pgettext_lazy("cases.Review.status", "Concept")),
        (FINAL, pgettext_lazy("cases.Review.status", "Final")),
        (UNFINISHED, pgettext_lazy("cases.Review.status", "Unfinished")),
    )

    case = models.OneToOneField(Case, null=True, related_name="review", on_delete=models.SET_NULL)
    status = models.PositiveSmallIntegerField(choices=STATUSES, default=NEW)
    evaluation = models.JSONField(default=dict)

    class Meta:
        db_table = "sparta_training_case_review"

    def can_be_managed_by(self, user) -> bool:
        return self.case.reviewer == user
