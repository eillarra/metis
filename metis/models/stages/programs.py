from django.db import models
from django.utils import timezone
from modeltranslation.translator import TranslationOptions

from ..base import BaseModel
from .constraints import DisciplineConstraintsMixin


class Program(BaseModel):
    """
    A generic definition of an internship curriculum.
    Different constraints can be applied to the program.
    Constraints: cannot repeat place
    Choice of disciplines: can be repeated

    How many places can the student choose prefernecse
    """

    education = models.ForeignKey("metis.Education", related_name="programs", on_delete=models.CASCADE)
    name = models.CharField(max_length=160)
    valid_from = models.DateField()
    valid_until = models.DateField(null=True, blank=True)

    # evaluation_form = models.ForeignKey("metis.EvaluationForm", related_name="programs", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

    @property
    def is_valid(self):
        today = timezone.now().date()
        return self.valid_from <= today and (not self.valid_until or self.valid_until >= today)


class ProgramTranslationOptions(TranslationOptions):
    fields = ("name",)


class ProgramBlock(BaseModel):
    """
    Based on semesters or a natural year, a orientative block is defined.
    Normally these will be linked to an academic year, and they will be closely related to degrees (Ba3, Ma1, Ma2).
    """

    program = models.ForeignKey(Program, related_name="blocks", on_delete=models.CASCADE)
    name = models.CharField(max_length=160)
    position = models.PositiveSmallIntegerField()

    class Meta:
        db_table = "metis_program_blocks"
        unique_together = ("program", "position")
        ordering = ["program", "position"]

    def __str__(self) -> str:
        return self.name


class ProgramInternship(DisciplineConstraintsMixin, BaseModel):
    """
    An internship inside a ProgramBlock.
    The final Internship or stage will be linked to this model, so we can later check the dependencies
    and make sure the student has covered all the requirements for the Program / Track.
    A ProgramInternship defines some orientative 'dates' that will be used to create the actual
    internship periods for a Project.

    Extra constraints:
    - How many places can the student choose prefernecse
    - Choose place regions
    - Preferences for disciplines (ordered or unordered)
    """

    block = models.ForeignKey(ProgramBlock, related_name="internships", on_delete=models.CASCADE)
    name = models.CharField(max_length=160)
    position = models.PositiveSmallIntegerField(default=0)
    start_week = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)

    class Meta:
        db_table = "metis_program_internships"
        ordering = ["block__position", "position"]

    def __str__(self) -> str:
        return f"{self.block} / {self.name}"


class Track(DisciplineConstraintsMixin, BaseModel):
    """
    A Track is a set of program internships that are related and (can) have some constraints of their own.
    """

    program = models.ForeignKey(Program, related_name="tracks", on_delete=models.CASCADE)
    name = models.CharField(max_length=160)
    program_internships = models.ManyToManyField(ProgramInternship, through="metis.TrackInternship")

    class Meta:
        db_table = "metis_program_tracks"

    def __str__(self) -> str:
        return f"{self.program} / {self.name}"

    @property
    def is_available(self) -> bool:
        return self.program.is_valid


class TrackInternship(models.Model):
    """
    Related model that defines the order of the internships inside a Track.
    Special requirements for a Track are also saved here.
    """

    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    program_internship = models.ForeignKey(ProgramInternship, related_name="tracks", on_delete=models.CASCADE)
    position = models.PositiveIntegerField()

    class Meta:
        db_table = "metis_program_track_internships"
        ordering = ["track", "position"]

    def __str__(self) -> str:
        return f"{self.track} / {self.program_internship}"
