from django.db.models.deletion import ProtectedError
from http import HTTPStatus as status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class BaseModelViewSet(ModelViewSet):
    """Prefetching happens automatically, even for generic relations."""

    def destroy(self, request, *args, **kwargs):
        """
        Try destroying a model instance.
        If `PROTECT` has been set as `on_delete` for a foreign key,
        return a `403 Forbidden` response.
        """
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError as e:
            return Response({"detail": str(e)}, status=status.FORBIDDEN)
