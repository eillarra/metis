import factory

from django.utils import timezone


class AdminFactory(factory.django.DjangoModelFactory):
    username = "sparta"
    first_name = "SPARTA"
    last_name = "Admin"
    email = "sparta@ugent.be"
    is_staff = True
    is_superuser = True

    class Meta:
        model = "sparta.User"


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    last_login = factory.LazyFunction(timezone.now)

    username = factory.LazyAttribute(lambda self: self.email.split("@")[0])

    class Meta:
        model = "sparta.User"
