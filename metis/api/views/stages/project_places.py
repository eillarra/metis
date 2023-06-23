from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter

from metis.models import ProjectPlace, ProjectPlaceAvailability
from ...permissions import IsEducationOfficeMember
from ...serializers import ProjectPlaceSerializer, ProjectPlaceAvailabilitySerializer
from .projects import ProjectNestedModelViewSet


class ProjectPlaceViewSet(ProjectNestedModelViewSet):
    queryset = ProjectPlace.objects.select_related("place").prefetch_related(
        "availability_set",
        "disciplines",
        "place__contacts__user",
        "place__contacts__updated_by",
        "place__education__updated_by",
        "place__updated_by",
        "updated_by",
    )
    pagination_class = None
    permission_classes = (IsEducationOfficeMember,)
    serializer_class = ProjectPlaceSerializer

    filter_backends = (SearchFilter,)
    search_fields = ("place__name", "place__code")

    @action(detail=True, methods=["put"])
    def availability(self, request, *args, **kwargs):
        """
        This endpoint is a bit special, because it is an endpoint for a nested field.
        TODO: We repeat the validations from Model.clean() here, it could be refactored in the future.
        """

        project_place = self.get_object()
        period_ids = set(project_place.project.periods.values_list("id", flat=True))

        # validate

        ProjectPlaceAvailabilitySerializer(data=request.data, many=True).is_valid(raise_exception=True)

        for availability in request.data:
            if availability["period"] not in period_ids:
                raise ValidationError({"period": "Period does not belong to project"})
            if availability["min"] > availability["max"]:
                raise ValidationError({"min": "Min availability cannot be greater than max availability"})

        # update

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
