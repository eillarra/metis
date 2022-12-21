from django.db import models

from sparta.models.base import BaseModel
from sparta.models.files import FilesMixin


class Absence(FilesMixin, BaseModel):
    training = models.ForeignKey("sparta.Training", related_name="absences", on_delete=models.CASCADE)

    class Meta:
        db_table = "sparta_training_absence"
