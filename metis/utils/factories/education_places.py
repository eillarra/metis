import factory

from .educations import EducationFactory
from .places import PlaceFactory


class EducationPlaceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "metis.EducationPlace"

    education = factory.SubFactory(EducationFactory)
    place = factory.SubFactory(PlaceFactory)
    code = factory.Sequence(lambda n: f"EducationPlace code {n}")
