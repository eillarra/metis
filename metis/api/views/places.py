from http import HTTPStatus as status
from typing import TYPE_CHECKING

from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from metis.models import Contact, Place, User
from metis.services.mailer.contacts import schedule_invitation_email

from ..permissions import IsEducationOfficeMember
from ..serializers import ContactSerializer, PlaceSerializer
from .base import BaseModelViewSet
from .educations import EducationNestedModelViewSet


if TYPE_CHECKING:
    from metis.models.educations import Education


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
            return Response({"emails": ["Must provide emails"]}, status=status.BAD_REQUEST)

        user = User.create_from_name_emails(name=request.data.get("name"), emails=emails)
        contact = Contact.objects.create(place=self.get_object(), user=user, created_by=self.request.user, **data)
        self.get_object().contacts.add(contact)
        schedule_invitation_email(contact)

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

    queryset = Contact.objects.select_related("user")
    pagination_class = None
    permission_classes = (IsEducationOfficeMember,)
    serializer_class = ContactSerializer

    @action(detail=True, methods=["post"])
    def invite(self, request, *args, **kwargs):
        """Invite contact to place."""
        schedule_invitation_email(self.get_object())
        return Response(status=status.NO_CONTENT)
