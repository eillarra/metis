import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from typing import Optional

from .programs import Program
from ..base import BaseModel
from ..rel.remarks import RemarksMixin


def validate_discipline_choice(obj: "Internship") -> None:
    available_disciplines = obj.program_internship.available_disciplines

    if obj.discipline not in available_disciplines:
        raise ValidationError(f"Chosen discipline is not available for this internship: {obj.program_internship}")

    covered_disciplines = obj.student.internships.values_list("discipline", flat=True)
    remaining_constraints = obj.program_internship.get_remaining_discipline_constraints(covered_disciplines)

    valid_choice = False
    for constraint in remaining_constraints:
        if obj.discipline in constraint.disciplines.all():
            valid_choice = True
            break

    if not valid_choice:
        raise ValidationError(
            f"Chosen discipline does not meet the remaining constraints for this internship: {obj.program_internship}"
        )


class Internship(RemarksMixin, BaseModel):
    """
    An internship by a student.
    """

    program_internship = models.ForeignKey(
        "sparta.ProgramInternship", related_name="internships", on_delete=models.CASCADE
    )
    student = models.ForeignKey("sparta.User", related_name="internships", on_delete=models.CASCADE)
    place = models.ForeignKey("sparta.Place", related_name="internships", on_delete=models.CASCADE)
    custom_start_date = models.DateField(null=True)  # by default start date is period's start date
    custom_end_date = models.DateField(null=True)  # by default end date is period's end date

    discipline = models.ForeignKey(
        "sparta.Discipline", related_name="internships", null=True, on_delete=models.SET_NULL
    )
    # evaluation_deadline = models.DateField()  # this can be used for cases > reviews

    def clean(self) -> None:
        """
        Things to check:
        - if student has a training in the same Program (via block) check if DisciplineRule allows it
        - if Education has place rules, check if the place is allowed
        """
        validate_discipline_choice(self)
        return super().clean()

    @property
    def start_date(self) -> datetime.date:
        return self.custom_start_date if self.custom_start_date else self.period.start_date

    @property
    def end_date(self) -> datetime.date:
        return self.custom_end_date if self.custom_end_date else self.period.end_date

    @property
    def duration(self) -> datetime.timedelta:
        return self.end_at - self.start_at

    @property
    def is_active(self) -> bool:
        return self.start_date <= timezone.now().date() <= self.end_date

    @property
    def program(self) -> Optional[Program]:
        return self.program_internship.block.program if self.period.program_period else None

    def accepts_cases(self) -> bool:
        raise NotImplementedError
