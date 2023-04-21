import factory

from django.utils import timezone


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    last_login = factory.LazyFunction(timezone.now)

    username = factory.LazyAttribute(lambda self: self.email.split("@")[0])
    password = factory.PostGenerationMethodCall("set_password", "metis")

    class Meta:
        model = "metis.User"


class AdminFactory(UserFactory):
    username = "metis"
    first_name = "Metis"
    last_name = "Admin"
    email = "metis@ugent.be"
    is_staff = True
    is_superuser = True
