import factory

from sparta.models.stages.constraints import DisciplineConstraint


class DisciplineConstraintFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DisciplineConstraint
