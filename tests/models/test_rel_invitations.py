import pytest

from metis.models.rel import Invitation
from metis.utils.factories import (
    EducationFactory,
    PlaceFactory,
    UserFactory,
)


@pytest.fixture(autouse=True)
def education(db):
    education = EducationFactory()
    PlaceFactory(education=education)
    return education


@pytest.fixture
def place(db, education):
    return education.places.first()


@pytest.mark.django_db
def test_invited_contact_makes_acount(place):
    contact_email = "contact@uzgent.be"
    Invitation.objects.create(
        content_object=place,
        type="contact",
        name="UZ Contact",
        email=contact_email,
        data={
            "is_mentor": True,
            "is_staff": False,
        },
    )
    assert Invitation.objects.count() == 1

    user = UserFactory(email=contact_email)
    assert place.contacts.count() == 1
    assert place.contacts.first().user == user

    assert Invitation.objects.count() == 0
