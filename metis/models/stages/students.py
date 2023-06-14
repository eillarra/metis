from django.db import models
from typing import TYPE_CHECKING

from ..base import BaseModel
from ..rel.forms import CustomFormResponsesMixin
from ..rel.remarks import RemarksMixin

if TYPE_CHECKING:
    from .programs import ProgramInternship


class Student(CustomFormResponsesMixin, RemarksMixin, BaseModel):
    """
    A Student is a User that is linked to a Project.
    TODO: This model is used to register students' preferences too.
    """

    user = models.ForeignKey("metis.User", related_name="student_set", on_delete=models.PROTECT)
    project = models.ForeignKey("metis.Project", related_name="students", on_delete=models.PROTECT)
    block = models.ForeignKey("metis.ProgramBlock", related_name="students", on_delete=models.PROTECT)
    track = models.ForeignKey("metis.Track", related_name="students", null=True, blank=True, on_delete=models.SET_NULL)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["project", "block__position"]
        unique_together = ("user", "project", "block")

    def __str__(self):
        return f"{self.user} ({self.project})"

    def can_be_managed_by(self, user):
        return self.project.can_be_managed_by(user)

    def has_signed_required_texts(self) -> bool:
        return self.signatures.filter(text_entry__in=self.project.required_texts).count() == len(
            self.project.required_texts
        )

    def internships(self) -> list["ProgramInternship"]:
        return self.block.internships.filter(block=self.block)
