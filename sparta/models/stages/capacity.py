from django.db import models

from ...._pre.models.base import BaseModel


class TrainingCapacity(BaseModel):
    project = models.ForeignKey("sparta.Project", related_name="capacities", on_delete=models.CASCADE)
    place = models.ForeignKey("sparta.TrainingPlace", related_name="capacities", on_delete=models.CASCADE)
    period = models.ForeignKey("sparta.Period", related_name="capacities", on_delete=models.CASCADE)

    class Meta:
        db_table = "sparta_training_capacity"
