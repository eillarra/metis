from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import pgettext_lazy

from sparta.models.base import BaseModel
from sparta.models.rel.files import File, FilesMixin
from sparta.models.rel.remarks import RemarksMixin


STAGE_DAYS_LIMIT = 4


class Case(FilesMixin, RemarksMixin, BaseModel):
    """
    `reviewer` is a User in Sparta. it can be suggested by the student, in that case a new account is created.
    Files can be uploaded by the student and can be viewed by student/reviewers.
    """

    REGULAR = "regular"
    INTERACTIVE = "interactive"
    TYPES = (
        (REGULAR, pgettext_lazy("cases.Case.type", "Regular")),
        (INTERACTIVE, pgettext_lazy("cases.Case.type", "Interactive")),
    )

    training = models.ForeignKey("sparta.Training", related_name="cases", on_delete=models.CASCADE)
    reviewer = models.ForeignKey("sparta.User", null=True, related_name="cases", on_delete=models.SET_NULL)
    title = models.CharField(max_length=160)
    type = models.CharField(max_length=16, default=REGULAR, choices=TYPES)
    submission_date = models.DateField()  # automatic on final submission? this seems to be same as created_at

    reviewer_is_approved = models.BooleanField(default=False)
    reviewer_name = models.CharField(max_length=160, null=True, blank=True)
    reviewer_email = models.EmailField(null=True, blank=True)

    class Meta:
        db_table = "sparta_training_case"

    def clean(self) -> None:
        if not self.training.accepts_cases():
            raise ValidationError("Training is not accepting case submissions anymore.")

    def save(self, *args, **kwargs):
        """
        1) make sure a review is created once the case is submitted.
        2) run a task to check if the provided email can bve reached, if not, the student gets an email to fix this => student can edit the case: once a reviewer account has been assigned the student cannot edit the case anymore?
        3) if a new account is needed, the reviewer can get an email with instructions to create a new account => link.
        4) the mentor or internship coordinator needs to validate the reviewer
        """
        """
        `reviewer_is_approved`: when is direct? who and how approves?
        """
        super().save(*args, **kwargs)

    def file(self) -> File:
        return self.files.first()
