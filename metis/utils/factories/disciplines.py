import factory


class DisciplineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "metis.Discipline"

    code = factory.Sequence(lambda n: f"ed{n}")
