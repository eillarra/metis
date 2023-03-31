import factory


class FacultyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "sparta.Faculty"

    # Add any required fields or default values here
    name = factory.Sequence(lambda n: f"Faculty {n}")


class EducationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "sparta.Education"

    # Add any required fields or default values here
    code = factory.Sequence(lambda n: f"ed{n}")
    faculty = factory.SubFactory(FacultyFactory)
    name = factory.Sequence(lambda n: f"Education {n}")
