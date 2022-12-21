from django.db import models

from ..base import BaseModel


class Group(BaseModel):
    project = models.ForeignKey("sparta.Project", related_name="groups", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    # TODO: QUESTION: there are dates in the old database, do we need them or do we use the period/project dates?

    def __str__(self) -> str:
        return self.name
