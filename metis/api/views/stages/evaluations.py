from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS

from metis.models import Evaluation
from ...serializers import EvaluationSerializer
from .internships import InternshipNestedModelViewSet


class EvaluationPermissions(IsAuthenticated):
    def has_permission(self, request, view):
        internship = view.get_internship()

        if not bool(request.user and request.user.is_authenticated):
            return False

        if request.method in SAFE_METHODS:
            return (
                internship.place.can_be_managed_by(request.user)
                or internship.mentors.filter(user=request.user).exists()
            )

        if request.method == "POST":
            return (
                internship.mentors.filter(user=request.user).exists()
                or internship.place.contacts.filter(user=request.user, is_admin=True).exists()
            )

        return internship.mentors.filter(user=request.user).exists()

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.internship.mentors.filter(user=request.user).exists()


class EvaluationViewSet(InternshipNestedModelViewSet):
    queryset = Evaluation.objects.prefetch_related("internship__project__education")
    pagination_class = None
    permission_classes = (EvaluationPermissions,)
    serializer_class = EvaluationSerializer

    @action(detail=False, methods=["post"])
    def approve(self, request, *args, **kwargs):
        raise NotImplementedError
