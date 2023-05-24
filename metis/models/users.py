from allauth.account.models import EmailAddress
from allauth.socialaccount.signals import pre_social_login
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from .rel import AddressesMixin, LinksMixin, PhoneNumbersMixin


class User(AddressesMixin, PhoneNumbersMixin, LinksMixin, AbstractUser):
    def __str__(self) -> str:
        return f"{self.username} ({self.name})"

    @property
    def name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def is_contact(self) -> bool:
        return self.contact_set.exists()  # type: ignore

    @property
    def is_office_member(self) -> bool:
        return self.education_set.exists()  # type: ignore

    @property
    def is_student(self) -> bool:
        return self.student_set.exists()  # type: ignore


def find_user_by_email(email: str, verified: bool = True) -> User | None:
    try:
        return EmailAddress.objects.get(email__iexact=email, verified=verified).user
    except EmailAddress.DoesNotExist:
        return None


@receiver(post_save, sender=User)
def check_invitations(sender, instance, created, **kwargs):
    if created:
        from metis.services.inviter import check_user_invitations

        check_user_invitations(instance)


@receiver(pre_social_login)
def link_to_existing_user(sender, request, sociallogin, **kwargs):
    if sociallogin.is_existing:
        return

    # for "ugent" social accounts, we can use the email address to find the user
    if sociallogin.account.provider == "ugent":
        try:
            email = sociallogin.account.extra_data["mail"]
            user = find_user_by_email(email)
            if user:
                sociallogin.connect(request, user)
        except KeyError:
            return
