from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from metis.models import Questioning
from metis.tasks.emails import schedule_questioning_email

from ...permissions import IsEducationOfficeMember
from ...serializers import FormResponseSerializer, QuestioningSerializer
from .projects import ProjectNestedModelViewSet


class QuestioningViewSet(ProjectNestedModelViewSet):
    queryset = Questioning.objects.prefetch_related("project__education", "period", "updated_by")
    pagination_class = None
    permission_classes = (IsEducationOfficeMember,)
    serializer_class = QuestioningSerializer

    @action(detail=True, methods=["get"])
    def responses(self, request, *args, **kwargs):
        serializer = FormResponseSerializer(self.get_object().responses.all(), many=True, context={"request": request})
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def send_emails(self, request, *args, **kwargs):
        ids = request.data.get("ids", [])

        if not ids:
            raise ValidationError({"ids": "No ids provided."})

        questioning = self.get_object()

        if not questioning.is_active:
            raise PermissionDenied("Questioning is not active.")

        schedule_questioning_email(questioning, filtered_ids=ids)

        return Response({"status": "ok", "message": "Emails scheduled."})
