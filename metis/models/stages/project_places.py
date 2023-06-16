from django.core.exceptions import ValidationError
from django.db import models

from ..base import BaseModel
from ..rel.forms import CustomFormResponsesMixin
from ..rel.remarks import RemarksMixin
from ..rel.texts import TextEntriesMixin


class ProjectPlace(CustomFormResponsesMixin, RemarksMixin, TextEntriesMixin, BaseModel):
    """
    The stagebureau works with a subset of all the places availablke for each Project.
    This can be copied from previous project.
    """

    project = models.ForeignKey("metis.Project", related_name="place_set", on_delete=models.CASCADE)
    place = models.ForeignKey("metis.Place", related_name="project_place_set", on_delete=models.PROTECT)
    disciplines = models.ManyToManyField("metis.Discipline", related_name="places")

    # TODO: planner
    # is_visible_to_planner = models.BooleanField(default=True)

    class Meta:
        db_table = "metis_project_places"
        unique_together = ("project", "place")

    def clean(self) -> None:
        """
        Things to check:
        - the selected place is one of the available places for the Education
        - the selected disciplines are limited to the disciplines of the Education
        """
        if self.place not in self.project.education.places.all():
            raise ValidationError("Place is not available for this education.")
        if self.disciplines.filter(education__id__ne=self.project.education.id).exists():
            raise ValidationError("Disciplines are limited to the disciplines of the education.")
        return super().clean()

    def can_be_managed_by(self, user) -> bool:
        return self.project.can_be_managed_by(user) or self.place.contacts.filter(user=user, is_admin=True).exists()


class ProjectPlaceAvailability(BaseModel):
    """
    Assigned availability for a place in a period.
    This can be copied from previous project.
    """

    project_place = models.ForeignKey("metis.ProjectPlace", related_name="availability_set", on_delete=models.CASCADE)
    period = models.ForeignKey("metis.Period", related_name="availability_set", on_delete=models.CASCADE)
    min = models.PositiveSmallIntegerField(default=0)
    max = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = "metis_project_place_availability"
        unique_together = ("project_place", "period")

    def clean(self) -> None:
        """
        Things to check:
        - the period is one of the available periods for the Project
        - max is greater than min
        """
        if self.period not in self.project_place.project.periods.all():
            raise ValidationError("Period is not available for this project.")
        if self.max < self.min:
            raise ValidationError("Max is smaller than min.")
        return super().clean()
