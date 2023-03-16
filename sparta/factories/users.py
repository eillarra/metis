import factory

from django.utils import timezone


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    last_login = factory.LazyFunction(timezone.now)

    username = factory.LazyAttribute(lambda self: self.email.split("@")[0])
    password = factory.PostGenerationMethodCall("set_password", "sparta")

    class Meta:
        model = "sparta.User"


class AdminFactory(UserFactory):
    username = "sparta"
    first_name = "SPARTA"
    last_name = "Admin"
    email = "sparta@ugent.be"
    is_staff = True
    is_superuser = True
