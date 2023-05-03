import factory


class RegionFactory(factory.django.DjangoModelFactory):
    name = factory.Iterator(["Oost-Vlaanderen", "West-Vlaanderen", "Antwerpen", "Brussel"])

    class Meta:
        model = "metis.Region"


class InstitutionFactory(factory.django.DjangoModelFactory):
    region = factory.SubFactory(RegionFactory)
    name = factory.Sequence(lambda n: f"Place {n}")

    class Meta:
        model = "metis.Institution"
