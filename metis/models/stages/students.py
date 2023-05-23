from django.db import models

from ..base import BaseModel
from ..rel.remarks import RemarksMixin


class Student(RemarksMixin, BaseModel):
    """
    A Student is a User that is linked to a Project.
    TODO: This model is used to register students' preferences too.
    """

    user = models.ForeignKey("metis.User", related_name="student_set", on_delete=models.PROTECT)
    project = models.ForeignKey("metis.Project", related_name="students", on_delete=models.PROTECT)
    block = models.ForeignKey("metis.ProgramBlock", related_name="students", on_delete=models.PROTECT)
    track = models.ForeignKey("metis.Track", related_name="students", null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ["project", "block__position"]
        unique_together = ("user", "project", "block")

    def can_be_managed_by(self, user):
        return self.project.can_be_managed_by(user)

    def has_signed_internship_agreement(self):
        return self.signatures.filter(content=self.project.internship_agreement).exists()  # type: ignore
