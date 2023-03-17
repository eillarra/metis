import factory

from sparta.models.rel.addresses import Address


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address
