from http import HTTPStatus as status

from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.response import Response

from metis.models import Evaluation, Signature

from ...serializers import EvaluationSerializer
from .internships import InternshipNestedModelViewSet


class EvaluationPermissions(BasePermission):
    """Permissions for evaluations."""

    def has_permission(self, request, view):
        """Check if the user has permission to access the view."""
        if not bool(request.user and request.user.is_authenticated):
            return False

        internship = view.get_internship()
        user_is_student = internship.student.user == request.user
        user_is_office = internship.education.can_be_managed_by(request.user)
        user_is_contact = (
            internship.place and internship.place.user_is_admin(request.user)
        ) or internship.mentors.filter(user=request.user).exists()

        if request.method in SAFE_METHODS:
            return user_is_student or user_is_office or user_is_contact

        if request.method == "POST" and request.resolver_match.url_name == "project-internship-evaluation-approve":
            return user_is_student or user_is_contact

        if request.method in ["POST", "PUT"] and request.data.get("is_self_evaluation"):
            return user_is_student

        return user_is_contact

    def has_object_permission(self, request, view, obj):
        """Check if the user has permission to manipulate the Evaluation object."""
        if request.method in SAFE_METHODS:
            return True

        if obj.is_self_evaluation:
            return obj.internship.student.user == request.user

        return (
            obj.internship.place and obj.internship.place.user_is_admin(request.user)
        ) or obj.internship.mentors.filter(user=request.user).exists()


class EvaluationViewSet(InternshipNestedModelViewSet):
    """API endpoint for evaluations."""

    queryset = Evaluation.objects.prefetch_related("internship__project__education")
    pagination_class = None
    permission_classes = (EvaluationPermissions,)
    serializer_class = EvaluationSerializer

    def get_queryset(self):
        """Get queryset making sure that students can only see approved evaluations or their own."""
        qs = super().get_queryset()
        internship = self.get_internship()

        if self.request.user == internship.student.user and not internship.can_be_managed_by(self.request.user):
            return qs.filter(Q(is_approved=True) | Q(is_self_evaluation=True, updated_by=self.request.user))

        return qs

    def perform_update(self, serializer) -> None:
        """Update model instance, performing extra `is_approved` check."""
        self.validate(serializer, check_is_approved=True)
        serializer.save(internship=self.get_internship(), updated_by=self.request.user)

    @action(detail=True, methods=["post"])
    def approve(self, request, *args, **kwargs):
        """Approves an evaluation."""
        evaluation = self.get_object()
        signed_text = request.data.get("signed_text", "")

        signature = Signature.objects.create(content_object=evaluation, user=request.user, signed_text=signed_text)
        Evaluation.approve(evaluation, signature)

        return Response(status=status.NO_CONTENT)
