import factory

from .educations import EducationFactory
from .users import UserFactory


class PlaceLocationFactory(factory.django.DjangoModelFactory):
    """Factory for PlaceLocation model."""

    class Meta:  # noqa: D106
        model = "metis.PlaceLocation"

    education = factory.SubFactory(EducationFactory)
    code = factory.Sequence(lambda n: f"placelocationcode{n}")
    name = factory.Sequence(lambda n: f"Place Location {n}")


class PlaceTypeFactory(factory.django.DjangoModelFactory):
    """Factory for PlaceType model."""

    class Meta:  # noqa: D106
        model = "metis.PlaceType"

    education = factory.SubFactory(EducationFactory)


class PlaceFactory(factory.django.DjangoModelFactory):
    """Factory for Place model."""

    class Meta:  # noqa: D106
        model = "metis.Place"

    education = factory.SubFactory(EducationFactory)
    name = factory.Sequence(lambda n: f"Place {n}")
    code = factory.Sequence(lambda n: f"placecode{n}")
    location = factory.SubFactory(PlaceLocationFactory)
    type = factory.SubFactory(PlaceTypeFactory)


class ContactFactory(factory.django.DjangoModelFactory):
    """Factory for Contact model."""

    class Meta:  # noqa: D106
        model = "metis.Contact"

    place = factory.SubFactory(PlaceFactory)
    user = factory.SubFactory(UserFactory)
