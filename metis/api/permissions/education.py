from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..views.educations import EducationNestedModelViewSet

from .base import IsManager


class IsEducationOfficeMember(IsManager):
    """
    Only members of the education office can update an object.
    """

    def has_permission(self, request, view: "EducationNestedModelViewSet"):
        return view.get_education().can_be_managed_by(request.user)

    def has_object_permission(self, request, view: "EducationNestedModelViewSet", obj):
        return view.get_education().can_be_managed_by(request.user)
