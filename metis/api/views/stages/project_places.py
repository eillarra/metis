from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter

from metis.models import ProjectPlace, ProjectPlaceAvailability

from ...permissions import IsEducationOfficeMember
from ...serializers import ProjectPlaceAvailabilitySerializer, ProjectPlaceSerializer
from .projects import ProjectNestedModelViewSet


class ProjectPlaceViewSet(ProjectNestedModelViewSet):
    """API endpoint for managing project places."""

    queryset = ProjectPlace.objects.select_related("place").prefetch_related(
        "availability_set",
        "disciplines",
        "place__contacts__user",
        "place__contacts__updated_by",
        "place__education__updated_by",
        "place__updated_by",
        "place__addresses",
        "place__phone_numbers",
        "updated_by",
    )
    pagination_class = None
    permission_classes = (IsEducationOfficeMember,)
    serializer_class = ProjectPlaceSerializer

    filter_backends = (SearchFilter,)
    search_fields = ("place__name", "place__code")

    def perform_create(self, serializer):  # noqa: D102
        # TODO: activate validation
        # self.validate(serializer)
        serializer.save(project=self.get_project(), created_by=self.request.user)

    def perform_update(self, serializer):  # noqa: D102
        # TODO: activate validation
        # self.validate(serializer)
        serializer.save(project=self.get_project(), updated_by=self.request.user)

    @action(detail=True, methods=["put"])
    def availability(self, request, *args, **kwargs):
        """Update availability for a project place."""
        project_place = self.get_object()

        try:
            serializer = ProjectPlaceAvailabilitySerializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            ModelClass = ProjectPlaceAvailabilitySerializer.Meta.model
            for data in serializer.validated_data:  # type: ignore
                ModelClass(project_place=project_place, **data).clean()
        except Exception as exc:
            raise ValidationError(str(exc)) from exc

        for availability in request.data:
            try:
                pc = ProjectPlaceAvailability.objects.get(project_place=project_place, period_id=availability["period"])
                pc.min = availability["min"]
                pc.max = availability["max"]
                pc.updated_by = request.user
                pc.save()
            except ProjectPlaceAvailability.DoesNotExist:
                ProjectPlaceAvailability.objects.create(
                    project_place=project_place,
                    period_id=availability["period"],
                    min=availability["min"],
                    max=availability["max"],
                    created_by=request.user,
                )

        return self.retrieve(request, *args, **kwargs)
