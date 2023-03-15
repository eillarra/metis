from django.db import models

from ..base import BaseModel


class Preference(BaseModel):
    """
    A student's preference for places and disciplines.
    """

    """
    TODO: link with ProgramInternship instead?
    """

    student = models.ForeignKey("sparta.User", related_name="preferences", on_delete=models.CASCADE)
    internship = models.ForeignKey("sparta.Internship", related_name="preferences", on_delete=models.CASCADE)
    regions = models.ManyToManyField("sparta.Region", through="RegionPreference")
    places = models.ManyToManyField("sparta.Place", through="PlacePreference")
    disciplines = models.ManyToManyField("sparta.Discipline", through="DisciplinePreference")


class RegionPreference(models.Model):
    """
    A student's preference for a region.
    """

    preference = models.ForeignKey(Preference, on_delete=models.CASCADE)
    region = models.ForeignKey("sparta.Region", related_name="preferences", on_delete=models.CASCADE)
    position = models.PositiveIntegerField()

    class Meta:
        db_table = "sparta_preference_region"
        ordering = ["preference", "position"]


class PlacePreference(models.Model):
    """
    A student's preference for a place.
    """

    preference = models.ForeignKey(Preference, on_delete=models.CASCADE)
    place = models.ForeignKey("sparta.Place", related_name="preferences", on_delete=models.CASCADE)
    position = models.PositiveIntegerField()

    class Meta:
        db_table = "sparta_preference_place"
        ordering = ["preference", "position"]


class DisciplinePreference(models.Model):
    """
    A student's preference for disciplines.
    """

    preference = models.ForeignKey(Preference, on_delete=models.CASCADE)
    discipline = models.ForeignKey("sparta.Discipline", related_name="preferences", on_delete=models.CASCADE)
    position = models.PositiveIntegerField()

    class Meta:
        db_table = "sparta_preference_discipline"
        ordering = ["preference", "position"]
