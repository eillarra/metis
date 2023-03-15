import factory

from sparta.models import Region


class RegionFactory(factory.django.DjangoModelFactory):
    name = factory.Iterator(["Oost-Vlaanderen", "West-Vlaanderen", "Antwerpen", "Brussel"])

    class Meta:
        model = Region


class PlaceFactory(factory.django.DjangoModelFactory):
    region = factory.Iterator(Region.objects.all())

    class Meta:
        model = "sparta.Place"
