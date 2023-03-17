import factory

from sparta.models.disciplines import Discipline


class DisciplineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Discipline
