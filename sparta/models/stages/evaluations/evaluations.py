from django.db import models

from sparta.models.base import BaseModel


class InternshipEvaluation(BaseModel):
    internship = models.ForeignKey("sparta.Internship", related_name="evaluations", on_delete=models.CASCADE)

    class Meta:
        db_table = "sparta_internship_evaluation"
