from rest_framework.permissions import IsAuthenticated
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..views.rel import RelViewSet


class IsManager(IsAuthenticated):
    """
    Only managers can update an object.
    """

    def has_object_permission(self, request, view, obj) -> bool:
        return obj.can_be_managed_by(request.user)


class IsRelManager(IsAuthenticated):
    """
    When dealing with a rel object (ContentType) we check if the content object can be managed by the user.
    """

    def has_permission(self, request, view: "RelViewSet") -> bool:
        return view.get_content_object().can_be_managed_by(request.user)

    def has_object_permission(self, request, view: "RelViewSet", obj) -> bool:
        """Only real owner can UPDATE or DELETE a related object."""
        if request.method in ("PUT", "PATCH", "DELETE"):
            return obj.created_by_id == request.user.pk
        return view.get_content_object().can_be_managed_by(request.user)
