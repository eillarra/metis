from django.db import models

from ..base import BaseModel


class InternshipCapacity(BaseModel):
    """
    Assigned capacity for a place in a period.
    This can be copied from previous project.
    """

    place = models.ForeignKey("epione.TrainingPlace", related_name="capacities", on_delete=models.CASCADE)
    period = models.ForeignKey("epione.Period", related_name="capacities", on_delete=models.CASCADE)
    capacity = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = "epione_internship_capacity"


# TODO: add some extra constraints per discipline. A place can have some limits for some disciplines.
