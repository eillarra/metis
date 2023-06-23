from django.db import models

from ..base import BaseModel


class Preference(BaseModel):
    """
    A student's preference for places and disciplines.
    """

    """
    TODO: link with ProgramInternship instead?
    """

    student = models.ForeignKey("metis.Student", related_name="preferences", on_delete=models.CASCADE)
    internship = models.ForeignKey("metis.Internship", related_name="preferences", on_delete=models.CASCADE)
    places = models.ManyToManyField("metis.Place", through="PlacePreference")
    disciplines = models.ManyToManyField("metis.Discipline", through="DisciplinePreference")


class PlacePreference(models.Model):
    """
    A student's preference for a place.
    """

    preference = models.ForeignKey(Preference, on_delete=models.CASCADE)
    place = models.ForeignKey("metis.Place", related_name="preferences", on_delete=models.CASCADE)
    position = models.PositiveIntegerField()

    class Meta:
        db_table = "metis_preference_places"
        ordering = ["preference", "position"]


class DisciplinePreference(models.Model):
    """
    A student's preference for disciplines.
    """

    preference = models.ForeignKey(Preference, on_delete=models.CASCADE)
    discipline = models.ForeignKey("metis.Discipline", related_name="preferences", on_delete=models.CASCADE)
    position = models.PositiveIntegerField()

    class Meta:
        db_table = "metis_preference_disciplines"
        ordering = ["preference", "position"]
