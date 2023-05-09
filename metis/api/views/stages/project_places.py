from rest_framework_extensions.mixins import NestedViewSetMixin

from metis.models import EducationPlace, Contact
from ...permissions import IsEducationOfficeMember
from ...serializers import EducationPlaceSerializer
from ..educations import EducationNestedModelViewSet
from ..base import BaseModelViewSet


class EducationPlaceViewSet(EducationNestedModelViewSet):
    queryset = EducationPlace.objects.prefetch_related("contacts__user", "place__region", "updated_by")
    pagination_class = None
    permission_classes = (IsEducationOfficeMember,)
    serializer_class = EducationPlaceSerializer


class EducationPlaceNestedModelViewSet(NestedViewSetMixin, BaseModelViewSet):
    _education_place = None

    def get_education(self):
        return self.get_education_place().education

    def get_education_place(self):
        if self._education_place:
            return self._education_place
        self._education_place = EducationPlace.objects.get(id=self.kwargs["parent_lookup_education_place"])
        return self._education_place

    def perform_create(self, serializer):
        serializer.save(education_place=self.get_education_place())


class ProjectPlaceViewSet(EducationPlaceNestedModelViewSet):
    queryset = Contact.objects.select_related("user")
    pagination_class = None
    permission_classes = (IsEducationOfficeMember,)
    serializer_class = EducationPlaceSerializer
