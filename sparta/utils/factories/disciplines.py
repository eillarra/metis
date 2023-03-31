import factory


class DisciplineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "sparta.Discipline"

    code = factory.Sequence(lambda n: f"ed{n}")
