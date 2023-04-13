from django.db import models

from ..base import BaseModel


class Preference(BaseModel):
    """
    A student's preference for places and disciplines.
    """

    """
    TODO: link with ProgramInternship instead?
    """

    student = models.ForeignKey("epione.User", related_name="preferences", on_delete=models.CASCADE)
    internship = models.ForeignKey("epione.Internship", related_name="preferences", on_delete=models.CASCADE)
    regions = models.ManyToManyField("epione.Region", through="RegionPreference")
    places = models.ManyToManyField("epione.Place", through="PlacePreference")
    disciplines = models.ManyToManyField("epione.Discipline", through="DisciplinePreference")


class RegionPreference(models.Model):
    """
    A student's preference for a region.
    """

    preference = models.ForeignKey(Preference, on_delete=models.CASCADE)
    region = models.ForeignKey("epione.Region", related_name="preferences", on_delete=models.CASCADE)
    position = models.PositiveIntegerField()

    class Meta:
        db_table = "epione_preference_region"
        ordering = ["preference", "position"]


class PlacePreference(models.Model):
    """
    A student's preference for a place.
    """

    preference = models.ForeignKey(Preference, on_delete=models.CASCADE)
    place = models.ForeignKey("epione.Place", related_name="preferences", on_delete=models.CASCADE)
    position = models.PositiveIntegerField()

    class Meta:
        db_table = "epione_preference_place"
        ordering = ["preference", "position"]


class DisciplinePreference(models.Model):
    """
    A student's preference for disciplines.
    """

    preference = models.ForeignKey(Preference, on_delete=models.CASCADE)
    discipline = models.ForeignKey("epione.Discipline", related_name="preferences", on_delete=models.CASCADE)
    position = models.PositiveIntegerField()

    class Meta:
        db_table = "epione_preference_discipline"
        ordering = ["preference", "position"]
