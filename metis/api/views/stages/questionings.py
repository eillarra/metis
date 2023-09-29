from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from metis.models import Questioning
from ...permissions import IsEducationOfficeMember
from ...serializers import QuestioningSerializer, FormResponseSerializer
from .projects import ProjectNestedModelViewSet

from metis.tasks.emails import schedule_project_place_information_email, schedule_student_tops_email


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

        if questioning.type == Questioning.PROJECT_PLACE_INFORMATION:
            schedule_project_place_information_email(questioning, ids)
        if questioning.type == Questioning.STUDENT_TOPS:
            schedule_student_tops_email(questioning, ids)

        return Response({"status": "ok", "message": "Emails scheduled."})
