from rest_framework.permissions import IsAuthenticated
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..views.rel import RelModelViewSet


class IsOfficeMember(IsAuthenticated):
    """
    Only office members can see things like the full list of Metis users (for search purposes).
    """

    def has_permission(self, request, view) -> bool:
        return (
            request.user and request.user.is_authenticated and (request.user.is_office_member or request.user.is_staff)
        )


class IsManager(IsAuthenticated):
    """
    Only managers can update an object.
    """

    def has_object_permission(self, request, view, obj) -> bool:
        return obj.can_be_managed_by(request.user)


class IsRelManager(IsAuthenticated):
    """
    When dealing with a rel object (ContentType) we check if the content object can be managed by the user.
    When it is shared, anybody can update or delete the object.
    Not shared objects can only be updated or deleted by the user who created it.
    """
    shared = False

    def has_permission(self, request, view: "RelModelViewSet") -> bool:
        return view.get_content_object().can_be_managed_by(request.user)

    def has_object_permission(self, request, view: "RelModelViewSet", obj) -> bool:
        """Only real owner can UPDATE or DELETE a related object."""
        if request.method in ("PUT", "PATCH", "DELETE"):
            return self.shared or obj.created_by_id == request.user.pk
        return view.get_content_object().can_be_managed_by(request.user)


class IsSharedRelManager(IsRelManager):
    shared = True
