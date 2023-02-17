from django.db import models

from ..base import BaseModel


class TrainingCapacity(BaseModel):
    """
    This should include Bachelor, Master... block/degree.
    """

    project = models.ForeignKey("sparta.Project", related_name="capacities", on_delete=models.CASCADE)
    place = models.ForeignKey("sparta.TrainingPlace", related_name="capacities", on_delete=models.CASCADE)
    period = models.ForeignKey("sparta.Period", related_name="capacities", on_delete=models.CASCADE)
    # degree
    # discipline
    capacity = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = "sparta_internship_capacity"
