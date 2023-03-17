import factory

from sparta.models.places import Region, Place


class RegionFactory(factory.django.DjangoModelFactory):
    name = factory.Iterator(["Oost-Vlaanderen", "West-Vlaanderen", "Antwerpen", "Brussel"])

    class Meta:
        model = Region


class PlaceFactory(factory.django.DjangoModelFactory):
    region = factory.SubFactory(RegionFactory)
    name = factory.Sequence(lambda n: f"Place {n}")

    class Meta:
        model = Place
