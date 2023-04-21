from django.db import models

from metis.models.base import BaseModel


class InternshipEvaluation(BaseModel):
    internship = models.ForeignKey("metis.Internship", related_name="evaluations", on_delete=models.CASCADE)

    class Meta:
        db_table = "metis_internship_evaluation"
