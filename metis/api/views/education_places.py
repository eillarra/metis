from typing import TYPE_CHECKING

from metis.models import EducationPlace, Contact
from ..permissions import IsEducationOfficeMember
from ..serializers import EducationPlaceSerializer, ContactSerializer
from .base import BaseModelViewSet
from .educations import EducationNestedModelViewSet

if TYPE_CHECKING:
    from metis.models.educations import Education


class EducationPlaceViewSet(EducationNestedModelViewSet):
    queryset = EducationPlace.objects.select_related(
        "place__region", "place__updated_by", "updated_by"
    ).prefetch_related("contacts__user")
    pagination_class = None
    permission_classes = (IsEducationOfficeMember,)
    serializer_class = EducationPlaceSerializer


class EducationPlaceNestedModelViewSet(BaseModelViewSet):
    _education_place = None

    def get_queryset(self):
        return super().get_queryset().filter(education_place=self.get_education_place())

    def get_education(self) -> "Education":
        return self.get_education_place().education

    def get_education_place(self) -> "EducationPlace":
        if self._education_place:
            return self._education_place
        self._education_place = EducationPlace.objects.select_related("education").get(
            id=self.kwargs["parent_lookup_education_place_id"]
        )
        return self._education_place

    def perform_create(self, serializer):
        serializer.save(education_place=self.get_education_place())


class ContactViewSet(EducationPlaceNestedModelViewSet):
    queryset = Contact.objects.select_related("user")
    pagination_class = None
    permission_classes = (IsEducationOfficeMember,)
    serializer_class = ContactSerializer
