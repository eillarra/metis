import factory


class FacultyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "metis.Faculty"

    name = factory.Sequence(lambda n: f"Faculty {n}")


class EducationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "metis.Education"

    faculty = factory.SubFactory(FacultyFactory)
    code = factory.Sequence(lambda n: f"ed{n}")
    name = factory.Sequence(lambda n: f"Education {n}")
