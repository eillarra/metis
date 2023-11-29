from typing import TYPE_CHECKING

from django.contrib.contenttypes.models import ContentType
from django.db import models

from ..base import BaseModel
from ..rel.forms import FormResponsesMixin
from ..rel.remarks import RemarksMixin
from ..rel.texts import TextEntry


if TYPE_CHECKING:
    from .programs import ProgramInternship


class Student(FormResponsesMixin, RemarksMixin, BaseModel):
    """A Student is a User that is linked to a Project."""

    user = models.ForeignKey("metis.User", related_name="student_set", on_delete=models.PROTECT)
    project = models.ForeignKey("metis.Project", related_name="students", on_delete=models.PROTECT)
    block = models.ForeignKey("metis.ProgramBlock", related_name="students", on_delete=models.PROTECT)
    track = models.ForeignKey("metis.Track", related_name="students", null=True, blank=True, on_delete=models.SET_NULL)
    number = models.CharField(max_length=8, default="", blank=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["project", "block__position"]
        unique_together = ("user", "project", "block")

    def __str__(self):
        return f"{self.user} ({self.project})"

    def can_be_managed_by(self, user):
        return self.project.can_be_managed_by(user) or self.user == user

    def has_signed_required_texts(self) -> bool:
        required_text_ids = self.project.required_texts.values_list("id", flat=True)
        text_entry_content_type = ContentType.objects.get_for_model(TextEntry)
        return self.user.signatures.filter(
            content_type=text_entry_content_type, object_id__in=required_text_ids
        ).count() == len(self.project.required_texts)

    def internships(self) -> list["ProgramInternship"]:
        """TODO: does this make any sense?"""
        return self.block.internships.filter(block=self.block)

    @property
    def name(self) -> str:
        return self.user.name
