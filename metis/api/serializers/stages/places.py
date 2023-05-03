from metis.models.stages.places import Place, Contact
from ..base import BaseModelSerializer
from ..disciplines import DisciplineTinySerializer
from ..institutions import InstitutionSerializer
from ..users import UserTinySerializer


class ContactSerializer(BaseModelSerializer):
    user = UserTinySerializer(read_only=True)

    class Meta:
        model = Contact
        fields = ("id", "user", "is_staff", "is_mentor")


class PlaceSerializer(BaseModelSerializer):
    institution = InstitutionSerializer()
    contacts = ContactSerializer(many=True)
    disciplines = DisciplineTinySerializer(many=True)

    class Meta:
        model = Place
        exclude = ("created_at", "created_by")
