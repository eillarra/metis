from rest_framework.permissions import IsAuthenticated


class IsManager(IsAuthenticated):
    """
    Only managers can update an object.
    """

    def has_object_permission(self, request, view, obj):
        return obj.can_be_managed_by(request.user)
