import factory

from epione.models.rel.addresses import Address


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address
