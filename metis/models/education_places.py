from django.db import models
from typing import TYPE_CHECKING

from .base import BaseModel
from .rel.contents import ContentsMixin
from .rel.files import FilesMixin
from .rel.phone_numbers import PhoneNumbersMixin
from .rel.remarks import RemarksMixin

if TYPE_CHECKING:
    from .rel.files import File


class EducationPlace(ContentsMixin, FilesMixin, RemarksMixin, BaseModel):
    """
    The stagebureau works with a subset of all the places available.
    Contacts or remarks are specific to each Education.
    """

    education = models.ForeignKey("metis.Education", related_name="place_set", on_delete=models.PROTECT)
    place = models.ForeignKey("metis.Place", related_name="education_place_set", on_delete=models.PROTECT)
    code = models.CharField(max_length=160)

    class Meta:
        db_table = "metis_education_places"
        unique_together = (("education", "place"), ("education", "code"))

    def __str__(self) -> str:
        return f"{self.code} ({self.education.code})"

    def can_be_managed_by(self, user) -> bool:
        return self.education.can_be_managed_by(user)

    @property
    def agreement(self) -> "File":
        return self.get_file("agreement")


class Contact(PhoneNumbersMixin, RemarksMixin, BaseModel):
    """
    Contact information for a place.
    Contacts can have administrative rights for a place for a education (`is_staff`).
    Contacts can also be designed as mentors. These mentors can be then assigned to specific internships.
    Contacts that are no staff or mentor have limited read-only access to the place information.
    """

    education_place = models.ForeignKey(EducationPlace, related_name="contacts", on_delete=models.CASCADE)
    user = models.ForeignKey("metis.User", related_name="contact_set", on_delete=models.CASCADE)
    is_staff = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=True)

    class Meta:
        db_table = "metis_education_contacts"
        unique_together = ("education_place", "user")

    def __str__(self) -> str:
        return f"{self.user} ({self.education_place.code})"
