import factory


class DisciplineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "epione.Discipline"

    code = factory.Sequence(lambda n: f"ed{n}")
