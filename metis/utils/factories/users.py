import factory
from allauth.account.models import EmailAddress
from django.utils import timezone


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for creating a user."""

    class Meta:  # noqa: D106
        model = "metis.User"

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    last_login = factory.LazyFunction(timezone.now)

    username = factory.Sequence(lambda n: f"username{n}")
    password = factory.django.Password("metis")

    @factory.post_generation
    def create_email_address(obj, create, extracted, **kwargs):
        """Create an email address for the user at EmailAddress."""
        if not create:
            return

        EmailAddress.objects.create(user=obj, email=obj.email, primary=True, verified=True)


class AdminFactory(UserFactory):
    """Factory for creating an admin user."""

    username = "metis"
    first_name = "Metis"
    last_name = "Admin"
    email = "metis@ugent.be"
    is_staff = True
    is_superuser = True
