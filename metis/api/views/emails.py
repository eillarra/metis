from rest_framework.filters import SearchFilter

from metis.models import EmailLog

from ..permissions import IsEducationOfficeMember
from ..serializers.emails import EmailSerializer, EmailTinySerializer
from .stages.projects import ProjectNestedModelViewSet


class ProjectEmailViewSet(ProjectNestedModelViewSet):
    """API endpoint for managing project places."""

    queryset = EmailLog.objects.prefetch_related("project__education").defer("body")
    pagination_class = None
    permission_classes = (IsEducationOfficeMember,)
    serializer_class = EmailTinySerializer

    filter_backends = (SearchFilter,)
    search_fields = ("subject",)

    def retrieve(self, request, *args, **kwargs):
        """Retrieve a single email."""
        self.queryset = self.queryset.defer(None)
        self.serializer_class = EmailSerializer
        return super().retrieve(request, *args, **kwargs)
