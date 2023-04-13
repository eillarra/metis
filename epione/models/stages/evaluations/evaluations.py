from django.db import models

from epione.models.base import BaseModel


class InternshipEvaluation(BaseModel):
    internship = models.ForeignKey("epione.Internship", related_name="evaluations", on_delete=models.CASCADE)

    class Meta:
        db_table = "epione_internship_evaluation"
