import pytest

from http import HTTPStatus as status

from metis.models.rel.invitations import Invitation
from metis.utils.factories import PlaceFactory, ContactFactory, UserFactory


@pytest.fixture
def place(db):
    return PlaceFactory()


@pytest.fixture
def contact(db, place):
    return ContactFactory(place=place)


@pytest.fixture
def user(db):
    return UserFactory()


@pytest.mark.site
class TestForAnonymous:
    def test_invitation_access(self, client, contact):
        invitation = Invitation.from_existing_contact(contact)
        response = client.get(invitation.get_absolute_url())
        assert response.status_code == status.FOUND


class TestForExistingContact(TestForAnonymous):
    @pytest.fixture(autouse=True)
    def setup(self, client, contact):
        client.force_login(user=contact.user)

    def test_invitation_processed(self, client, contact):
        invitation = Invitation.from_existing_contact(contact)
        client.get(invitation.get_absolute_url())
        with pytest.raises(Invitation.DoesNotExist):
            invitation.refresh_from_db()


class TestForNewUser(TestForAnonymous):
    @pytest.fixture(autouse=True)
    def setup(self, client, user):
        client.force_login(user=user)

    def test_invitation_access(self, client, contact, user):
        invitation = Invitation.from_existing_contact(contact)
        assert Invitation.objects.count() == 1
        client.get(invitation.get_absolute_url())
        contact.refresh_from_db()
        assert contact.user == user
