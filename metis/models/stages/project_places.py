from django.core.exceptions import ValidationError
from django.db import models

from ..base import BaseModel
from ..rel.texts import TextEntriesMixin
from ..rel.remarks import RemarksMixin


class ProjectPlace(RemarksMixin, TextEntriesMixin, BaseModel):
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
        return self.project.can_be_managed_by(user)


class PlaceCapacity(BaseModel):
    """
    Assigned capacity for a place in a period.
    This can be copied from previous project.
    """

    project_place = models.ForeignKey("metis.ProjectPlace", related_name="capacities", on_delete=models.CASCADE)
    period = models.ForeignKey("metis.Period", related_name="capacities", on_delete=models.CASCADE)
    capacity = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = "metis_project_place_capacities"
        unique_together = ("project_place", "period")
