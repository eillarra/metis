from rest_framework.filters import SearchFilter
from typing import TYPE_CHECKING

from metis.models import Place, Contact
from ..permissions import IsEducationOfficeMember
from ..serializers import PlaceSerializer, ContactSerializer
from .base import BaseModelViewSet
from .educations import EducationNestedModelViewSet

if TYPE_CHECKING:
    from metis.models.educations import Education


class PlaceViewSet(EducationNestedModelViewSet):
    queryset = Place.objects.select_related("updated_by").prefetch_related(
        "education", "contacts__user", "contacts__updated_by", "region"
    )
    pagination_class = None
    permission_classes = (IsEducationOfficeMember,)
    serializer_class = PlaceSerializer

    filter_backends = (SearchFilter,)
    search_fields = ("name", "code")


class PlaceNestedModelViewSet(BaseModelViewSet):
    _place = None

    def get_queryset(self):
        return super().get_queryset().filter(place=self.get_place())

    def get_education(self) -> "Education":
        return self.get_place().education

    def get_place(self) -> "Place":
        if self._place:
            return self._place
        self._place = Place.objects.select_related("education").get(id=self.kwargs["parent_lookup_place_id"])
        return self._place

    def perform_create(self, serializer):
        serializer.save(place=self.get_place(), created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(place=self.get_place(), updated_by=self.request.user)


class ContactViewSet(PlaceNestedModelViewSet):
    queryset = Contact.objects.select_related("user")
    pagination_class = None
    permission_classes = (IsEducationOfficeMember,)
    serializer_class = ContactSerializer
