from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property
from typing import TYPE_CHECKING

from ..base import BaseModel
from ..rel.remarks import RemarksMixin

if TYPE_CHECKING:
    from ..places import Place


class ProjectPlace(RemarksMixin, BaseModel):
    """
    The stagebureau works with a subset of all the places availablke for each Project.
    This can be copied from previous project.
    """

    project = models.ForeignKey("metis.Project", related_name="place_set", on_delete=models.CASCADE)
    education_place = models.ForeignKey("metis.EducationPlace", related_name="projects", on_delete=models.PROTECT)

    practical_information = models.TextField(blank=True, null=True)
    disciplines = models.ManyToManyField("metis.Discipline", related_name="places")

    # TODO: planner
    # is_visible_to_planner = models.BooleanField(default=True)

    class Meta:
        db_table = "metis_project_places"
        unique_together = ("project", "education_place")

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

    @cached_property
    def place(self) -> "Place":
        return self.education_place.place


class PlaceCapacity(BaseModel):
    """
    Assigned capacity for a place in a period.
    This can be copied from previous project.
    """

    # TODO: change to project_place
    place = models.ForeignKey("metis.ProjectPlace", related_name="capacities", on_delete=models.CASCADE)
    period = models.ForeignKey("metis.Period", related_name="capacities", on_delete=models.CASCADE)
    capacity = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = "metis_project_place_capacities"
        unique_together = ("place", "period")
