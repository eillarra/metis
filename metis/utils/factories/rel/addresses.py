import factory


class AddressFactory(factory.django.DjangoModelFactory):
    """Factory for Address model."""

    class Meta:  # noqa: D106
        model = "metis.Address"
