from http import HTTPStatus as status
from typing import TYPE_CHECKING

from allauth.account.models import EmailAddress
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import validate_email
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from metis.models import Contact, Place, Project, User, find_user_by_email
from metis.services.graph import register_emails_at_ugent
from metis.services.mailer.contacts import schedule_welcome_email

from ..permissions import IsEducationOfficeMember
from ..serializers import ContactSerializer, PlaceSerializer
from .base import BaseModelViewSet
from .educations import EducationNestedModelViewSet


if TYPE_CHECKING:
    from metis.models.educations import Education


def schedule_contact_welcome_email(contact: Contact, project_id: int | None) -> None:
    """Schedule an invitation email for a contact, adding the project info to the email logs (if set)."""
    project = None

    if project_id:
        try:
            project = Project.objects.get(id=project_id, education=contact.place.education)
        except Project.DoesNotExist:
            project = None

    schedule_welcome_email(contact, project=project)


class PlaceViewSet(EducationNestedModelViewSet):
    """API endpoint for managing places."""

    queryset = Place.objects.select_related("updated_by").prefetch_related(
        "education", "contacts__user", "contacts__updated_by", "addresses", "phone_numbers"
    )
    pagination_class = None
    permission_classes = (IsEducationOfficeMember,)
    serializer_class = PlaceSerializer

    filter_backends = (SearchFilter,)
    search_fields = ("name", "code")

    @action(detail=True, methods=["post"])
    def invite(self, request, *args, **kwargs):
        """Invite contacts to place."""
        emails = request.data.get("emails")
        data = request.data.get("data", {})

        if not emails:
            raise ValidationError({"emails": ["Must provide emails"]})

        user = User.create_from_name_emails(name=request.data.get("name"), emails=emails)
        contact = Contact.objects.create(place=self.get_object(), user=user, created_by=self.request.user, **data)
        self.get_object().contacts.add(contact)

        if contact.education.configuration["place_contact_welcome_email"]:
            schedule_contact_welcome_email(contact, request.data.get("project_id", None))

        return Response(ContactSerializer(contact, context={"request": request}).data, status=status.CREATED)


class PlaceNestedModelViewSet(BaseModelViewSet):
    """Base viewset for place child models."""

    _place = None

    def get_queryset(self):
        """Get queryset for place child models."""
        return super().get_queryset().filter(place=self.get_place())

    def get_education(self) -> "Education":
        """Get education from place object."""
        return self.get_place().education

    def get_place(self) -> "Place":
        """Get place object."""
        if not self._place:
            self._place = Place.objects.select_related("education").get(id=self.kwargs["parent_lookup_place_id"])
        return self._place

    def perform_create(self, serializer) -> None:
        """Create model instance."""
        self.validate(serializer)
        serializer.save(place=self.get_place(), created_by=self.request.user)

    def perform_update(self, serializer) -> None:
        """Update model instance."""
        self.validate(serializer)
        serializer.save(place=self.get_place(), updated_by=self.request.user)

    def validate(self, serializer) -> None:
        """Validate model instance."""
        try:
            Model = serializer.Meta.model
            Model(place=self.get_place(), **serializer.validated_data).clean()
        except Exception as exc:
            raise ValidationError(str(exc)) from exc


class ContactViewSet(PlaceNestedModelViewSet):
    """API endpoint for managing contacts."""

    queryset = Contact.objects.prefetch_related("user__emailaddress_set").select_related("user")
    pagination_class = None
    permission_classes = (IsEducationOfficeMember,)
    serializer_class = ContactSerializer

    def _get_request_email(self, request, field: str = "email") -> str:
        """Get email from request data and validate it."""
        try:
            email = request.data.get(field)
            validate_email(email)
            return email.lower()
        except DjangoValidationError as exc:
            raise ValidationError({field: ["Invalid email address."]}) from exc

    def _check_email_exists(self, email) -> None:
        existing_user = find_user_by_email(email)

        if existing_user and existing_user != self.get_object().user:
            raise ValidationError({"email": [f"Email is already in use by: {existing_user}."]})

        if existing_user:
            raise ValidationError({"email": ["Email already exists for this contact."]})

    def _save_contact_email(self, email: str) -> None:
        register_emails_at_ugent([email])
        EmailAddress.objects.create(user=self.get_object().user, email=email, verified=True, primary=False)

    def _make_email_primary(self, email: str) -> None:
        user = self.get_object().user
        user.email = email
        user.save()
        EmailAddress.objects.filter(user=user).update(primary=False)
        EmailAddress.objects.filter(user=user, email=email).update(primary=True)

    @action(detail=True, methods=["post"])
    def invite(self, request, *args, **kwargs):
        """Invite contact to place."""
        schedule_contact_welcome_email(self.get_object(), request.data.get("project_id", None))
        return Response(status=status.NO_CONTENT)

    @action(detail=True, methods=["post"])
    def add_email(self, request, *args, **kwargs):
        """Add an email to a contact."""
        email = self._get_request_email(request)
        self._check_email_exists(email)
        self._save_contact_email(email)

        if request.data.get("primary", False):
            self._make_email_primary(email)

        return Response(ContactSerializer(self.get_object(), context={"request": request}).data)

    @action(detail=True, methods=["post"])
    def delete_email(self, request, *args, **kwargs):
        """Delete an email from a contact, only if it is not the primary one."""
        email = self._get_request_email(request)
        user = self.get_object().user

        if user.email == email:
            raise ValidationError({"email": ["Cannot delete primary email address."]})

        EmailAddress.objects.filter(user=user, email=email).delete()
        return Response(status=status.NO_CONTENT)

    @action(detail=True, methods=["post"])
    def change_primary_email(self, request, *args, **kwargs):
        """Change the primary email for a contact."""
        email = self._get_request_email(request)

        if not EmailAddress.objects.filter(user=self.get_object().user, email=email).exists():
            raise ValidationError({"email": ["Email does not exist for this contact."]})

        self._make_email_primary(email)
        return Response(ContactSerializer(self.get_object(), context={"request": request}).data)
