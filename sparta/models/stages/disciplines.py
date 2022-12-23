from django.db import models

from sparta.models.base import BaseModel


class TrainingDisciplineGroup(BaseModel):
    code = models.CharField(max_length=32)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "sparta_training_discipline_group"

    def __str__(self) -> str:
        return self.name


class TrainingDiscipline(BaseModel):
    group = models.ForeignKey(TrainingDisciplineGroup, null=True, related_name="disciplines", on_delete=models.SET_NULL)
    discipline = models.OneToOneField("sparta.Discipline", null=True, on_delete=models.SET_NULL)
    code = models.CharField(max_length=32)

    is_visible_for_planner = models.BooleanField(default=True)  # TODO: define at relation level with project?

    class Meta:
        db_table = "sparta_training_discipline"
        ordering = ["position", "discipline__name"]

    def __str__(self) -> str:
        return self.name

    @property
    def name(self) -> str:
        return str(self.discipline)
