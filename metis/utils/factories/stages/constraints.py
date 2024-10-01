import factory

from metis.models.stages.constraints import DisciplineConstraint


class DisciplineConstraintFactory(factory.django.DjangoModelFactory):
    """Factory for DisciplineConstraint model."""

    class Meta:  # noqa: D106
        model = DisciplineConstraint
