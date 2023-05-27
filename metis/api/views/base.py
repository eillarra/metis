from django.db.models.deletion import ProtectedError
from django.db.utils import IntegrityError
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from http import HTTPStatus as status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from metis.models.rel.invitations import Invitation


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
            return Response({"ProtectedError": [message]}, status=status.FORBIDDEN)


class BaseModelViewSet(ProtectedMixin, ModelViewSet):
    """Prefetching happens automatically, even for generic relations."""

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    @method_decorator(never_cache)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class InvitationMixin:
    def get_object(self):
        raise NotImplementedError

    @action(detail=True, methods=["post"])
    def invite(self, request, *args, **kwargs):
        try:
            Invitation.objects.create(
                content_object=self.get_object(),
                type=request.data.get("type"),
                name=request.data.get("name"),
                email=request.data.get("email"),
                data=request.data.get("data"),
            )
            return Response(status=status.CREATED)
        except IntegrityError as e:
            return Response({"ValueError": [str(e)]}, status=status.BAD_REQUEST)
