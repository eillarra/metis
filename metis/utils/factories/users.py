import factory
from django.utils import timezone


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for creating a user."""

    class Meta:  # noqa: D106
        model = "metis.User"

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    last_login = factory.LazyFunction(timezone.now)

    username = factory.Sequence(lambda n: f"usename{n}")
    password = factory.django.Password("metis")


class AdminFactory(UserFactory):
    """Factory for creating an admin user."""

    username = "metis"
    first_name = "Metis"
    last_name = "Admin"
    email = "metis@ugent.be"
    is_staff = True
    is_superuser = True
