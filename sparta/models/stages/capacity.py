from django.db import models

from ..base import BaseModel


class InternshipCapacity(BaseModel):
    """
    Assigned capacity for a place in a period.
    """

    place = models.ForeignKey("sparta.TrainingPlace", related_name="capacities", on_delete=models.CASCADE)
    period = models.ForeignKey("sparta.Period", related_name="capacities", on_delete=models.CASCADE)
    capacity = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = "sparta_internship_capacity"


# TODO: add some extra constraints per discipline. A place can have some limits for some disciplines.
