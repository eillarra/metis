import pytest

from metis.models.rel.invitations import Invitation
from metis.services.inviter import process_contact_invitation
from metis.utils.factories import PlaceFactory, UserFactory


@pytest.fixture
def place(db):
    return PlaceFactory()


@pytest.fixture
def user(db):
    return UserFactory()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "data",
    [
        None,
        {"unknown_key": "unknown_value"},
        {"is_staff": True},
        {"is_staff": "a string, but it should be a boolean", "is_mentor": True},
    ],
)
def test_invitation_data_is_invalid(data, place, user):
    invitation = Invitation.objects.create(content_object=place, data=data)
    with pytest.raises(ValueError):
        process_contact_invitation(invitation, user)
