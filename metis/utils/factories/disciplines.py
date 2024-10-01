import factory

from .educations import EducationFactory


class DisciplineFactory(factory.django.DjangoModelFactory):
    """Factory for Discipline model."""

    class Meta:  # noqa: D106
        model = "metis.Discipline"

    education = factory.SubFactory(EducationFactory)
    code = factory.Sequence(lambda n: f"dis{n}")
    name = factory.Sequence(lambda n: f"Discipline {n}")
