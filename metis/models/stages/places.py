from django.core.exceptions import ValidationError
from django.db import models

from ..base import BaseModel
from ..rel.remarks import RemarksMixin


class Place(RemarksMixin, BaseModel):
    """
    Each Place has some specific information for each Project @ Education.
    Contact information can also be different for each project.
    """

    project = models.ForeignKey("metis.Project", related_name="places", on_delete=models.CASCADE)
    institution = models.ForeignKey("metis.Institution", related_name="places", on_delete=models.CASCADE)
    code = models.CharField(max_length=16, null=True, blank=True)

    practical_information = models.TextField(blank=True, null=True)
    disciplines = models.ManyToManyField("metis.Discipline", related_name="places")

    class Meta:
        db_table = "metis_project_place"
        unique_together = ("institution", "project")

    def __str__(self) -> str:
        return f"{self.institution.name} ({self.project.name})"

    def clean(self) -> None:
        if self.disciplines.filter(education__id__ne=self.project.education.id).exists():
            raise ValidationError("Disciplines are limited to the disciplines of the education.")
        return super().clean()


class Capacity(BaseModel):
    """
    Assigned capacity for a place in a period.
    This can be copied from previous project.
    """

    place = models.ForeignKey(Place, related_name="capacities", on_delete=models.CASCADE)
    period = models.ForeignKey("metis.Period", related_name="capacities", on_delete=models.CASCADE)
    capacity = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = "metis_project_place_capacities"


# TODO: add some extra constraints per discipline. A place can have some limits for some disciplines.


class Contact(BaseModel):
    """
    Contact information for a place.
    Contacts can have administrative rights for a place for a certain project (`is_staff`).
    Contacts can also be designed as mentors. These mentors can be then assigned to specific internships.
    Contacts that are no staff or mentor have limited read-only access to the place information.
    """

    place = models.ForeignKey(Place, related_name="contacts", on_delete=models.CASCADE)
    user = models.ForeignKey("metis.User", related_name="contact_objects", on_delete=models.CASCADE)
    is_staff = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=True)

    class Meta:
        db_table = "metis_project_place_contacts"
        unique_together = ("place", "user")
