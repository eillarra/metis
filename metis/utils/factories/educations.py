import factory


class FacultyFactory(factory.django.DjangoModelFactory):
    """Factory for Faculty model."""

    class Meta:  # noqa: D106
        model = "metis.Faculty"

    name = factory.Sequence(lambda n: f"Faculty {n}")


class EducationFactory(factory.django.DjangoModelFactory):
    """Factory for Education model."""

    class Meta:  # noqa: D106
        model = "metis.Education"

    faculty = factory.SubFactory(FacultyFactory)
    code = factory.Sequence(lambda n: f"ed{n}")
    name = factory.Sequence(lambda n: f"Education {n}")
