from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from metis.models import Place

from ...permissions import IsAuthenticated
from ...serializers import PlaceSerializer


class ContactPlaceViewSet(GenericViewSet):
    queryset = Place.objects.select_related("updated_by").prefetch_related(
        "education", "contacts__user", "contacts__updated_by"
    )
    pagination_class = None
    permission_classes = (IsAuthenticated,)
    serializer_class = PlaceSerializer

    def get_queryset(self):
        return self.queryset.filter(contacts__user=self.request.user)

    @action(detail=True, methods=["post"])
    def email(self, request, *args, **kwargs):
        """Send an email to the place's office email."""
        from rest_framework import status
        from rest_framework.response import Response

        from metis.services.mailer import schedule_email

        place = self.get_object()

        text = f"from: {request.user.first_name} {request.user.last_name}  \n"
        text += f"email: <{request.user.email}>\n---\n\n"
        text += request.data["text"]

        schedule_email(
            to=[place.education.office_email] if place.education.office_email else ["helpdesk.metis@ugent.be"],
            subject=f"[METIS] update for {place.name}",
            text_content=text,
            reply_to=[request.user.email],
            tags=[f"place.id:{place.id}", f"from.id:{request.user.id}"],
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
