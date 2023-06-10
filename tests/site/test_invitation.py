import pytest

from django.urls import reverse
from hashlib import sha256
from http import HTTPStatus as status
from uuid import uuid4

from metis.models.rel.invitations import Invitation
from metis.utils.factories import ContactFactory


@pytest.fixture
def contact(db):
    return ContactFactory()


@pytest.fixture
def invitation(db, contact):
    return Invitation.from_existing_contact(contact)


class TestForAuthenticated:
    @pytest.fixture(autouse=True)
    def setup(self, client, contact):
        client.force_login(user=contact.user)

    def test_non_existing_invitation(self, client):
        uuid = uuid4()
        secret = sha256(uuid.bytes).hexdigest()
        response = client.get(reverse("invitation", kwargs={"uuid": uuid, "secret": secret}))
        assert response.status_code == status.NOT_FOUND

    def test_wrong_secret(self, client, invitation):
        secret = sha256(invitation.uuid.bytes).hexdigest()
        response = client.get(reverse("invitation", kwargs={"uuid": invitation.uuid, "secret": secret}))
        assert response.status_code == status.NOT_FOUND
