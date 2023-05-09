import factory

from .educations import EducationFactory
from .places import PlaceFactory
from .users import UserFactory


class EducationPlaceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "metis.EducationPlace"

    education = factory.SubFactory(EducationFactory)
    place = factory.SubFactory(PlaceFactory)
    code = factory.Sequence(lambda n: f"EducationPlace code {n}")


class ContactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "metis.Contact"

    education_place = factory.SubFactory(EducationPlaceFactory)
    user = factory.SubFactory(UserFactory)
