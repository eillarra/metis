import pytest

from django.urls import reverse
from http import HTTPStatus as status

from metis.models.rel.invitations import Invitation
from metis.utils.factories import (
    ContactFactory,
    EducationFactory,
    PlaceFactory,
    ProjectFactory,
    UserFactory,
)


@pytest.fixture
def education(db):
    education = EducationFactory()
    place = PlaceFactory(education=education)
    ContactFactory(place=place)
    ProjectFactory(education=education)
    return education


@pytest.fixture
def place(db, education):
    return education.places.first()


@pytest.fixture
def office_member(db, education):
    user = UserFactory()
    education.office_members.add(user)
    return user


@pytest.fixture
def user(db):
    return UserFactory()


@pytest.mark.api
class TestForAnonymous:
    expected_status_codes: dict[str, status] = {
        "place_invite": status.FORBIDDEN,
    }

    def _get_contact_invite_data(self, place):
        return {}

    def test_invite_contact(self, api_client, education, place):
        url = reverse("v1:education-place-invite", args=[education.id, place.id])
        data = self._get_contact_invite_data(place)
        response = api_client.post(url, data)
        assert response.status_code == self.expected_status_codes["place_invite"]
        assert Invitation.objects.count() == int(bool(data))


class TestForAuthenticated(TestForAnonymous):
    @pytest.fixture(autouse=True)
    def setup(self, api_client, user):
        api_client.force_authenticate(user=user)


class TestForOfficeMember(TestForAuthenticated):
    expected_status_codes = {
        "place_invite": status.CREATED,
    }

    @pytest.fixture(autouse=True)
    def setup(self, api_client, office_member):
        api_client.force_authenticate(user=office_member)

    def _get_contact_invite_data(self, place):
        return {
            "type": "contact",
            "name": "Test Contact",
            "email": "contact@uzgent.be",
            "data": {
                "is_mentor": False,
                "is_staff": False,
            },
        }

    def test_invite_contact_bad_request(self, api_client, education, place):
        url = reverse("v1:education-place-invite", args=[education.id, place.id])
        response = api_client.post(url, {"name": "Test Contact"})
        assert response.status_code == status.BAD_REQUEST
