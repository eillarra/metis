from django.db import models

from ..base import BaseModel


class StudentGroup(BaseModel):
    """
    TODO: QUESTION: do we realy need this when we have ProgramBlock?
    """

    project = models.ForeignKey("epione.Project", related_name="groups", on_delete=models.CASCADE)
    name = models.CharField(max_length=160)

    # TODO: QUESTION: there are dates in the old database, do we need them or do we use the period/project dates?

    # number_of_periods = ???
    # min_place_choices
    # max_place_choices
    # min_region_choices
    # max_region_choices
    # dates: select_period,

    def __str__(self) -> str:
        return self.name