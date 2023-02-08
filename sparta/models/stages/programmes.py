from django.db import models

from ..base import BaseModel


class Programme(BaseModel):
    education = models.ForeignKey("sparta.Education", related_name="programmes", on_delete=models.CASCADE)
    name = models.CharField(max_length=160)
    valid_from = models.DateField()
    valid_until = models.DateField(null=True, blank=True)

    # evaluation_form = models.ForeignKey("sparta.EvaluationForm", related_name="programmes", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.education} - {self.name}"


class ProgrammeBlock(BaseModel):
    """
    A block normally runs for a year, but can be shorter or longer.
    It is closely related to student groups.
    """

    programme = models.ForeignKey(Programme, related_name="blocks", on_delete=models.CASCADE)
    name = models.CharField(max_length=160)
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = "sparta_programme_block"
        unique_together = ("programme", "position")
        ordering = ["programme", "position"]

    def __str__(self) -> str:
        return f"{self.programme} - {self.name}"


class DisciplineRule(BaseModel):
    REQUIRED = "required"
    OPTIONAL = "optional"
    TYPES = (
        (REQUIRED, "Required"),
        (OPTIONAL, "Optional"),
    )

    programme = models.ForeignKey(Programme, related_name="discipline_rules", on_delete=models.CASCADE)
    type = models.CharField(max_length=16, choices=TYPES, default=REQUIRED)
    disciplines = models.ManyToManyField("sparta.Discipline", related_name="rules")
    choices = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ["programme", "type"]
        unique_together = ("programme", "type")

    """
    there is sometimes a project that is not part of the programme,+
    that takes the space of a period
    """

    def clean(self) -> None:
        pass

    """
    other rules: what period should be used
    """
