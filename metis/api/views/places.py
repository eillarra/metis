from http import HTTPStatus as status
from typing import TYPE_CHECKING

from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from metis.models import Contact, Place, User
from metis.services.mailer import schedule_invitation_email

from ..permissions import IsEducationOfficeMember
from ..serializers import ContactSerializer, PlaceSerializer
from .base import BaseModelViewSet
from .educations import EducationNestedModelViewSet


if TYPE_CHECKING:
    from metis.models.educations import Education


class PlaceViewSet(EducationNestedModelViewSet):
    queryset = Place.objects.select_related("updated_by").prefetch_related(
        "education", "contacts__user", "contacts__updated_by"
    )
    pagination_class = None
    permission_classes = (IsEducationOfficeMember,)
    serializer_class = PlaceSerializer

    filter_backends = (SearchFilter,)
    search_fields = ("name", "code")

    @action(detail=True, methods=["post"])
    def invite(self, request, *args, **kwargs):
        emails = request.data.get("emails")
        data = request.data.get("data", {})

        if not emails:
            return Response({"emails": ["Must provide emails"]}, status=status.BAD_REQUEST)

        user = User.create_from_invitation(name=request.data.get("name"), emails=emails)
        contact = Contact.objects.create(place=self.get_object(), user=user, created_by=self.request.user, **data)
        self.get_object().contacts.add(contact)
        schedule_invitation_email("contact", contact)

        return Response(ContactSerializer(contact, context={"request": request}).data, status=status.CREATED)


class PlaceNestedModelViewSet(BaseModelViewSet):
    _place = None

    def get_queryset(self):
        return super().get_queryset().filter(place=self.get_place())

    def get_education(self) -> "Education":
        return self.get_place().education

    def get_place(self) -> "Place":
        if not self._place:
            self._place = Place.objects.select_related("education").get(id=self.kwargs["parent_lookup_place_id"])
        return self._place

    def perform_create(self, serializer):
        self.validate(serializer)
        serializer.save(place=self.get_place(), created_by=self.request.user)

    def perform_update(self, serializer):
        self.validate(serializer)
        serializer.save(place=self.get_place(), updated_by=self.request.user)

    def validate(self, serializer) -> None:
        try:
            ModelClass = serializer.Meta.model
            ModelClass(place=self.get_place(), **serializer.validated_data).clean()
        except Exception as exc:
            raise ValidationError(str(exc)) from exc


class ContactViewSet(PlaceNestedModelViewSet):
    queryset = Contact.objects.select_related("user")
    pagination_class = None
    permission_classes = (IsEducationOfficeMember,)
    serializer_class = ContactSerializer

    @action(detail=True, methods=["post"])
    def invite(self, request, *args, **kwargs):
        schedule_invitation_email("contact", self.get_object())
        return Response(status=status.NO_CONTENT)
