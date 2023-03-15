import factory


class DisciplineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "sparta.Discipline"
