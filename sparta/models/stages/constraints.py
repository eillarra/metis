from collections import Counter
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.utils.functional import cached_property
from typing import List, Set, Tuple


from sparta.models import Discipline


class DisciplineConstraint(models.Model):
    """
    A disciplines constraint for a program, track, or internship.
    This model can be used to define constraints like:

    1. Choose 3 out of 5 disciplines:
       min_count=3, max_count=3, max_repeat=1, disciplines=[1, 2, 3, 4, 5]
    2. Maximum 1 out of 3 disciplines:
       min_count=0, max_count=1, max_repeat=1, disciplines=[1, 2, 3]
    3. Choose 2 and repeat each 2 times:
       min_count=4, max_count=4, max_repeat=2, disciplines=[1, 2]
    4. Choose at least 2 out of 6 disciplines:
       min_count=2, max_count=6, max_repeat=1, disciplines=[1, 2, 3, 4, 5, 6]
    5. Choose any number of disciplines, but don't repeat any:
       min_count=0, max_count=None, max_repeat=1, disciplines=[1, 2, 3, 4, 5, 6]
    6. Choose up to 5 disciplines from a set, with no limits on how many can be repeated:
       min_count=0, max_count=5, max_repeat=None, disciplines=[1, 2, 3, 4, 5, 6]

    Attributes:
        content_type (ForeignKey): The type of the related object (program, track, or internship).
        object_id (IntegerField): The ID of the related object.
        content_object (GenericForeignKey): Generic foreign key to the related object.
        disciplines (ManyToManyField): Many-to-many relationship with disciplines.
        min_count (PositiveIntegerField): Minimum number of disciplines required (inclusive).
        max_count (PositiveIntegerField): Maximum number of disciplines allowed (inclusive), or None if no limit.
        max_repeat (PositiveIntegerField): Maximum number of times a discipline can be repeated, or None if no limit.
    """

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="rules")
    object_id = models.IntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    disciplines = models.ManyToManyField("sparta.Discipline", related_name="constraints")
    min_count = models.PositiveIntegerField(null=True, blank=True)
    max_count = models.PositiveIntegerField(null=True, blank=True)
    max_repeat = models.PositiveIntegerField(null=True, blank=True, default=1)

    class Meta:
        db_table = "sparta_discipline_constraint"


@receiver(post_save, sender=DisciplineConstraint)
def check_constraints(sender, instance, **kwargs):
    content_object = instance.content_object

    if not content_object.check_constraints_compatibility():
        raise ValidationError("The new constraint conflicts with existing constraints.")


@receiver(m2m_changed, sender=DisciplineConstraint.disciplines.through)
def check_constraints_on_disciplines_update(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        content_object = instance.content_object

        if not content_object.check_constraints_compatibility():
            raise ValidationError("The constraint's disciplines conflict with another constraint.")


class DisciplineConstraintsMixin(models.Model):
    constraints = GenericRelation(DisciplineConstraint)

    class Meta:
        abstract = True

    @cached_property
    def available_disciplines(self) -> models.QuerySet:
        """
        Returns a set of all available disciplines included in the constraints.

        Returns:
            QuerySet: A QuerySet of Discipline objects.
        """
        return Discipline.objects.filter(constraints__in=self.constraints.all())

    def _constraints_conflict(self, constraint1: DisciplineConstraint, constraint2: DisciplineConstraint) -> bool:
        allowed_disciplines1 = set(constraint1.disciplines.values_list("id", flat=True))
        allowed_disciplines2 = set(constraint2.disciplines.values_list("id", flat=True))

        common_disciplines = allowed_disciplines1.intersection(allowed_disciplines2)

        if not common_disciplines:
            return False

        min_count1, max_count1 = self._get_count_bounds(constraint1)
        min_count2, max_count2 = self._get_count_bounds(constraint2)

        if max_count1 < min_count2 or max_count2 < min_count1:
            return False

        if constraint1.max_repeat is not None and constraint2.max_repeat is not None:
            if constraint1.max_repeat != constraint2.max_repeat:
                return True

        return False

    def _get_count_bounds(self, constraint: DisciplineConstraint) -> Tuple[int, int]:
        min_count = constraint.min_count or 0
        max_count = constraint.max_count or float("inf")

        return min_count, max_count

    def check_constraints_compatibility(self) -> bool:
        constraints = self.constraints.all()

        for constraint1 in constraints:
            for constraint2 in constraints:
                if constraint1 == constraint2:
                    continue

                if self._constraints_conflict(constraint1, constraint2):
                    return False

        return True

    def validate_discipline_constraints(self, discipline_ids: List[int]) -> bool:
        return validate_discipline_constraints(discipline_ids, list(self.constraints.all()))


def validate_discipline_constraints(
    discipline_ids: List[int], remaining_constraints: List[DisciplineConstraint]
) -> bool:
    """
    Validate a list of discipline_ids against the remaining constraints.

    Args:
        discipline_ids (List[int]): A list of discipline IDs to be validated.
        remaining_constraints (List[DisciplineConstraint]): A list of remaining DisciplineConstraint objects
        that define the constraints.

    Returns:
        bool: True if the list of discipline_ids satisfies the remaining constraints, False otherwise.

    Checks:
        1. The total number of disciplines is within the remaining min_count and max_count constraints.
        2. Each discipline is within the remaining max_repeat constraint.
        3. The selected disciplines are within the allowed set of disciplines defined by the remaining constraints.
    """

    for constraint in remaining_constraints:
        # Count the occurrences of each discipline
        discipline_counts = Counter(discipline_ids)

        # Get allowed_disciplines for the constraint
        allowed_disciplines = set(constraint.disciplines.values_list("id", flat=True))

        # Calculate the intersection of discipline_ids and allowed_disciplines
        intersecting_disciplines = set(discipline_ids) & allowed_disciplines
        intersecting_discipline_counts = sum(
            discipline_counts[discipline_id] for discipline_id in intersecting_disciplines
        )

        # Check if the total number of intersecting disciplines is within the remaining min_count and max_count
        if constraint.min_count is not None and intersecting_discipline_counts < constraint.min_count:
            return False
        if constraint.max_count is not None and intersecting_discipline_counts > constraint.max_count:
            return False

        # Check if each intersecting discipline is within the remaining max_repeat constraint
        if constraint.max_repeat is not None:
            for discipline_id in intersecting_disciplines:
                if discipline_counts[discipline_id] > constraint.max_repeat:
                    return False

    return True
