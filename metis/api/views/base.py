from http import HTTPStatus as status

from django.db.models.deletion import ProtectedError
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class ProtectedMixin:
    """Mixin to handle protected objects."""

    def destroy(self, request, *args, **kwargs):
        """Try destroying a model instance.

        If `PROTECT` has been set as `on_delete` for a foreign key,return a `403 Forbidden` response.
        """
        try:
            return super().destroy(request, *args, **kwargs)  # type: ignore
        except ProtectedError as e:
            message, _ = e.args
            return Response({"protected": [message]}, status=status.FORBIDDEN)


class BaseModelViewSet(ProtectedMixin, ModelViewSet):
    """Base viewset for all model viewsets."""

    def perform_create(self, serializer):
        """Create model instance."""
        self.validate(serializer)
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        """Update model instance."""
        self.validate(serializer)
        serializer.save(updated_by=self.request.user)

    def validate(self, serializer) -> None:
        """Validate model instance."""
        try:
            Model = serializer.Meta.model
            Model(**serializer.validated_data).clean()
        except Exception as exc:
            raise ValidationError(str(exc)) from exc

    @method_decorator(never_cache)
    def list(self, request, *args, **kwargs):
        """List model instances."""
        return super().list(request, *args, **kwargs)
