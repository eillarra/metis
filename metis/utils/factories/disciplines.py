import factory

from .educations import EducationFactory


class DisciplineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "metis.Discipline"

    education = factory.SubFactory(EducationFactory)
    code = factory.Sequence(lambda n: f"dis{n}")
    name = factory.Sequence(lambda n: f"Discipline {n}")
