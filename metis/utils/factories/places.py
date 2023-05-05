import factory

from .educations import EducationFactory


class RegionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "metis.Region"

    name = factory.Iterator(["Oost-Vlaanderen", "West-Vlaanderen", "Antwerpen", "Brussel"])


class PlaceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "metis.Place"

    region = factory.SubFactory(RegionFactory)
    name = factory.Sequence(lambda n: f"Place {n}")


class EducationPlaceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "metis.EducationPlace"

    education = factory.SubFactory(EducationFactory)
    place = factory.SubFactory(PlaceFactory)
    code = factory.Sequence(lambda n: f"EducationPlace code {n}")
