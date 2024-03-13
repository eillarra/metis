from http import HTTPStatus as status

from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from metis.models import Education, EmailTemplate, Internship, Mentor, Project, Signature, User
from metis.services.mailer import schedule_template_email

from ...permissions import IsEducationOfficeMember
from ...serializers import InternshipSerializer, MentorTinySerializer
from ..base import BaseModelViewSet
from .projects import ProjectNestedModelViewSet


class CanManageInternshipPlace(IsAuthenticated):
    """Permission class for managing a place."""

    def has_object_permission(self, request, view, obj):
        """Checks if the user has permission to manipulate the Internship object."""
        return obj.place.can_be_managed_by(request.user)


class InternshipViewSet(ProjectNestedModelViewSet):
    """API endpoint for managing internships."""

    queryset = Internship.objects.prefetch_related("project__education", "mentors__user", "updated_by")
    pagination_class = None
    permission_classes = (IsEducationOfficeMember,)
    serializer_class = InternshipSerializer

    def _check_user_id(self, request) -> int:
        user_id = request.data.get("user_id", None)

        if not user_id or not User.objects.filter(id=user_id).exists():
            raise ValidationError({"user_id": "No valid user id provided."})

        return user_id

    @action(detail=True, methods=["post"], permission_classes=(CanManageInternshipPlace,))
    def add_mentor(self, request, *args, **kwargs):
        """Add mentor to internship."""
        user_id = self._check_user_id(request)
        mentor = Mentor.objects.create(internship=self.get_object(), user_id=user_id, created_by=request.user)
        serializer = MentorTinySerializer(mentor)
        return Response(serializer.data, status=status.CREATED, headers=self.get_success_headers(serializer.data))

    @action(detail=True, methods=["post"], permission_classes=(CanManageInternshipPlace,))
    def remove_mentor(self, request, *args, **kwargs):
        """Remove mentor from internship."""
        user_id = self._check_user_id(request)
        mentor = Mentor.objects.get(internship=self.get_object(), user_id=user_id)
        mentor.delete()
        return Response(status=status.NO_CONTENT)

    @action(detail=True, methods=["post"], permission_classes=(CanManageInternshipPlace,))
    def approve(self, request, *args, **kwargs):
        """Approve internship."""
        internship = self.get_object()
        signed_text = request.data.get("signed_text", "")

        signature = Signature.objects.create(content_object=internship, user=request.user, signed_text=signed_text)
        Internship.approve(internship, signature)

        return Response(status=status.NO_CONTENT)

    @action(detail=True, methods=["post"], permission_classes=(IsEducationOfficeMember,))
    def send_email(self, request, *args, **kwargs):
        """Send template email to internship."""
        internship = self.get_object()
        email_code = request.data.get("code", None)

        if email_code != "internship.approve":
            # TODO: tmp check, this should be moved to a separate service, to support different emails per status
            raise ValidationError({"code": "No valid email template code provided."})

        try:
            email_template = EmailTemplate.objects.get(education=internship.project.education, code=email_code)
        except EmailTemplate.DoesNotExist as exc:
            raise ValidationError({"code": "No valid email template code provided."}) from exc

        user = internship.place.contacts.filter(is_admin=True)[0].user  # TODO: service should decide

        schedule_template_email(
            template=email_template,
            to=[user.email],
            context={"internship": internship, "user": user},
            log_user=user,
            tags=[
                f"internship.id:{internship.id}",
                f"place.id:{internship.place.id}",
                f"user.id:{user.id}",
                "type:internship.approve",  # TODO: in the future, we will have different types
            ],
        )

        return Response(status=status.NO_CONTENT)


class InternshipNestedModelViewSet(BaseModelViewSet):
    """Base viewset for internship child models."""

    _internship = None

    def get_queryset(self):
        """Get queryset for internship child models."""
        return super().get_queryset().filter(internship=self.get_internship())

    def get_education(self) -> "Education":
        """Get education from internship object."""
        return self.get_project().education

    def get_project(self) -> "Project":
        """Get project from internship object."""
        return self.get_internship().project

    def get_internship(self) -> "Internship":
        """Get internship object."""
        if not self._internship:
            self._internship = Internship.objects.select_related("project__education").get(
                id=self.kwargs["parent_lookup_internship_id"]
            )
        return self._internship

    def perform_create(self, serializer) -> None:
        """Create model instance."""
        self.validate(serializer)
        serializer.save(internship=self.get_internship(), created_by=self.request.user)

    def perform_update(self, serializer) -> None:
        """Update model instance."""
        self.validate(serializer)
        serializer.save(internship=self.get_internship(), updated_by=self.request.user)

    def validate(self, serializer, *, check_is_approved: bool = False) -> None:
        """Validate model instance.

        :param serializer: Serializer instance.
        :param check_is_approved: If True, extra checks for is_approved are performed, as this cannot be updated
        """
        try:
            data = serializer.validated_data
            if check_is_approved:
                data["is_approved"] = self.get_object().is_approved
            Model = serializer.Meta.model
            Model(internship=self.get_internship(), **data).clean()
        except Exception as exc:
            raise ValidationError(str(exc)) from exc
