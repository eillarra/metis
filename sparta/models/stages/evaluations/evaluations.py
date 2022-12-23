from django.db import models

from sparta.models.base import BaseModel


class TrainingEvaluation(BaseModel):
    training = models.ForeignKey("sparta.Training", related_name="evaluations", on_delete=models.CASCADE)

    class Meta:
        db_table = "sparta_training_evaluation"
