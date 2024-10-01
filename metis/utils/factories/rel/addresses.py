import factory

from metis.models.rel.addresses import Address


class AddressFactory(factory.django.DjangoModelFactory):
    """Factory for Address model."""

    class Meta:  # noqa: D106
        model = Address
