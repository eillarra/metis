from typing import TYPE_CHECKING

from .base import IsManager

if TYPE_CHECKING:
    from ..views.educations import EducationNestedModelViewSet


class IsEducationOfficeMember(IsManager):
    """
    Only members of the education office can update an object.
    """

    def has_permission(self, request, view: "EducationNestedModelViewSet"):
        return view.get_education().can_be_managed_by(request.user)

    def has_object_permission(self, request, view: "EducationNestedModelViewSet", obj):
        return view.get_education().can_be_managed_by(request.user)
