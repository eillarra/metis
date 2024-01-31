from typing import TYPE_CHECKING

from allauth.account.models import EmailAddress
from allauth.socialaccount.signals import pre_social_login
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.utils.functional import cached_property

from metis.services.graph import GraphAPI
from metis.services.mailer import send_email_to_admins

from .rel import AddressesMixin, LinksMixin, PhoneNumbersMixin


if TYPE_CHECKING:
    from .rel.files import File


class User(AddressesMixin, PhoneNumbersMixin, LinksMixin, AbstractUser):
    """Custom user model."""

    def __str__(self) -> str:
        return f"{self.username} ({self.name})"

    def can_be_managed_by(self, user: "User") -> bool:
        return user.is_superuser or user == self

    def has_file_access(self, file: "File") -> bool:
        return file.is_accessible_by_user(self)

    @property
    def name(self) -> str:
        """Name of the user."""
        return self.get_full_name() or self.username

    @cached_property
    def ugent_id(self) -> str | None:
        """UGent ID of the user."""
        try:
            return self.socialaccount_set.all()[0].uid  # type: ignore
        except IndexError:
            return None

    @property
    def photo_url(self) -> str | None:
        """URL to the student's photo."""
        # TODO: this is currently taken from SPARTA, but should be taken from OASIS / DICT in the future
        # TODO: this is not protected on SPARTA, but it should
        return f"https://sparta.ugent.be/_Document/PersonImage/{self.ugent_id}.jpeg" if self.ugent_id else None

    @property
    def reverse_name(self) -> str:
        """Name in reverse order, e.g. 'Doe, John'."""
        return f"{self.last_name}, {self.first_name}"

    @property
    def is_contact(self) -> bool:
        return self.contact_set.exists()  # type: ignore

    @property
    def is_office_member(self) -> bool:
        return self.education_set.exists()  # type: ignore

    @property
    def is_student(self) -> bool:
        return self.student_set.exists()  # type: ignore

    @classmethod
    def bot(cls) -> "User":
        return cls.objects.get(username="metis")

    @classmethod
    def create_from_name_emails(cls, name: str, emails: list[str]) -> "User":
        """Create a user from a name and a list of emails."""
        if not emails or not all(emails):
            raise ValueError("At least one email is required")

        emails = [email.lower() for email in emails]
        primary_email = emails[0]
        username = primary_email.split("@")[0]

        if cls.objects.filter(username=username).exists():
            username = f"{username}.{get_random_string(4)}"

        user = cls.objects.create(
            username=username,
            password=f"!{get_random_string(40)}",  # not a usable password, they will use UGent OAuth anyway
            first_name=name.split()[0],
            last_name=" ".join(name.split()[1:]),
            email=primary_email,
        )

        for email in emails:
            EmailAddress.objects.create(user=user, email=email, verified=False, primary=email == primary_email)

        if settings.ENV == "production":
            with GraphAPI() as graph:
                for email in emails:
                    _, _, enabled = graph.register_email(email)
                    if not enabled:
                        send_email_to_admins(f"Email disabled at UGent: {email} EOM")

        return user


def find_user_by_email(email: str) -> User | None:
    """Find a user by email address."""
    try:
        return EmailAddress.objects.get(email__iexact=email).user
    except EmailAddress.DoesNotExist:
        return None


@receiver(pre_social_login)
def link_to_existing_user(sender, request, sociallogin, **kwargs):
    """Link social login to existing user."""
    if sociallogin.is_existing:
        return

    try:
        email = sociallogin.account.extra_data["mail"]
        user = find_user_by_email(email)
        if user:
            EmailAddress.objects.filter(user=user, email__iexact=email).update(verified=True)
            sociallogin.connect(request, user)
    except KeyError:
        return
