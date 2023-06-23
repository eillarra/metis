import factory

from .educations import EducationFactory
from .users import UserFactory


class PlaceTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "metis.PlaceType"

    education = factory.SubFactory(EducationFactory)


class PlaceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "metis.Place"

    education = factory.SubFactory(EducationFactory)
    name = factory.Sequence(lambda n: f"Place {n}")
    code = factory.Sequence(lambda n: f"placecode{n}")
    type = factory.SubFactory(PlaceTypeFactory)


class ContactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "metis.Contact"

    place = factory.SubFactory(PlaceFactory)
    user = factory.SubFactory(UserFactory)
