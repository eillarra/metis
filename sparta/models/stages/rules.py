from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Rule(models.Model):
    """
    Program rules. They can be applied at a generic level (Program), or down to a certain Internship or Track.
    """

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="rules")
    object_id = models.IntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    required_discipline = models.ForeignKey(
        "sparta.Discipline", on_delete=models.CASCADE, related_name="rules_required"
    )
    optional_disciplines = models.ManyToManyField("sparta.Discipline", related_name="rules_optional")
    num_required_internships = models.PositiveIntegerField()
    num_optional_internships = models.PositiveIntegerField()


class RulesMixin(models.Model):
    rules = GenericRelation(Rule)

    class Meta:
        abstract = True
