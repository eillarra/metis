from datetime import datetime
from http import HTTPStatus as status

from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from metis.models.places import Contact, Place, find_place_by_name
from metis.models.rel.addresses import Address
from metis.models.rel.phone_numbers import PhoneNumber
from metis.models.rel.signatures import Signature
from metis.models.stages import Internship, Mentor, ProjectPlace, Student
from metis.models.users import User, find_user_by_email

from ...permissions import IsAuthenticated
from ...serializers import (
    AuthSignatureSerializer,
    AuthStudentSerializer,
    InternshipFullInertiaSerializer,
    PreplanningInternshipSerializer,
)


class AuthStudentViewSet(ListModelMixin, GenericViewSet):
    queryset = Student.objects.all()
    pagination_class = None
    permission_classes = (IsAuthenticated,)
    serializer_class = AuthStudentSerializer

    @method_decorator(never_cache)
    def list(self, request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class AuthStudentSignatureViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    queryset = Signature.objects.all()
    pagination_class = None
    permission_classes = (IsAuthenticated,)
    serializer_class = AuthSignatureSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        user_id = self.request.data["user"]

        if user_id != self.request.user.id:
            raise PermissionDenied("This student does not belong to this user")

        serializer.save(
            user=self.request.user,
            content_type_id=self.request.data["content_type"],
            object_id=self.request.data["object_id"],
        )

    @method_decorator(never_cache)
    def list(self, request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)


class AuthStudentInternshipViewSet(UpdateModelMixin, ListModelMixin, GenericViewSet):
    queryset = Internship.objects.prefetch_related("project__education", "mentors__user", "updated_by")
    pagination_class = None
    permission_classes = (IsAuthenticated,)
    serializer_class = InternshipFullInertiaSerializer

    def get_queryset(self):
        """Internships for the current student."""
        return super().get_queryset().filter(student__user=self.request.user)

    def update(self, request, *args, **kwargs):
        """Update the start and end dates of the internship."""
        instance = self.get_object()
        data = request.data

        if not instance.education.configuration["student_update_dates"]:
            raise PermissionDenied("This education does not allow students to update dates")

        try:
            start_date = data["start_date"]
            end_date = data["end_date"]
        except KeyError as exc:
            raise ValidationError(f"Missing required fields: {exc}") from exc

        instance.start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        instance.end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        instance.save()

        return Response(self.serializer_class(instance, context={"request": request}).data, status=status.OK)

    @method_decorator(never_cache)
    def list(self, request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)


class AuthStudentProposeInternshipPlaceViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    """Endpoint so a user can manage or propose an internship place (when status is PREPLANNING)."""

    pagination_class = None
    permission_classes = (IsAuthenticated,)
    serializer_class = PreplanningInternshipSerializer

    def get_queryset(self):
        """Internships for the current user."""
        return (
            Internship.objects.filter(student__user=self.request.user, status=Internship.PREPLANNING, is_approved=False)
            .select_related("project__education")
            .prefetch_related("project__periods")
        )

    def create(self, request, *args, **kwargs):
        """Create an internship place and new contacts."""
        data = request.data

        try:
            internship_id = data["internship_id"]
            place_name = data["place_name"]
            place_address = data["place_address"]
            place_contact_name = data["place_contact_name"]
            place_contact_email = data["place_contact_email"]
            place_contact_phone_number = data["place_contact_phone_number"]
        except KeyError as exc:
            raise ValidationError(f"Missing required fields: {exc}") from exc

        try:
            internship = self.get_queryset().select_related("student__user").get(id=internship_id)
        except Internship.DoesNotExist as exc:
            raise PermissionDenied("This internship does not belong to this user") from exc

        user = find_user_by_email(place_contact_email) or User.create_from_name_emails(
            place_contact_name, [place_contact_email]
        )
        place = find_place_by_name(place_name, internship.project.education) or Place.objects.create(
            name=place_name, code=place_name, education=internship.project.education, created_by=request.user
        )
        mentor, _ = Mentor.objects.get_or_create(
            internship=internship,
            user=user,
            is_primary=True,
            defaults={
                "created_by": request.user,
            },
        )

        Contact.objects.get_or_create(
            place=place,
            user=user,
            is_admin=True,
            defaults={
                "created_by": request.user,
            },
        )

        if place_contact_phone_number:
            PhoneNumber.objects.create(content_object=user, number=place_contact_phone_number, type=PhoneNumber.MOBILE)

        if place_address:
            Address.objects.create(content_object=place, address=place_address, city="-", postcode="-", country="BE")

        internship.project_place, _ = ProjectPlace.objects.get_or_create(  # type: ignore
            project=internship.project,
            place=place,
            defaults={
                "created_by": request.user,
            },
        )
        internship.mentors.add(mentor)  # type: ignore
        internship.save()

        return Response(self.serializer_class(internship, context={"request": request}).data, status=status.CREATED)

    @method_decorator(never_cache)
    def list(self, request, *args, **kwargs) -> Response:
        """List internships for the current user."""
        return super().list(request, *args, **kwargs)
