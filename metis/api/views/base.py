from django.db.models.deletion import ProtectedError
from django.db.utils import IntegrityError
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from http import HTTPStatus as status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from metis.models.users import User


class ProtectedMixin:
    def destroy(self, request, *args, **kwargs):
        """
        Try destroying a model instance.
        If `PROTECT` has been set as `on_delete` for a foreign key,
        return a `403 Forbidden` response.
        """
        try:
            return super().destroy(request, *args, **kwargs)  # type: ignore
        except ProtectedError as e:
            message, _ = e.args
            return Response({"protected": [message]}, status=status.FORBIDDEN)


class BaseModelViewSet(ProtectedMixin, ModelViewSet):
    """Prefetching happens automatically, even for generic relations."""

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    @method_decorator(never_cache)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
