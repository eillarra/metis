from http import HTTPStatus as status

import pytest
from django.urls import reverse

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
        "existing_contact_invite": status.FORBIDDEN,
    }

    def _get_contact_invite_data(self, place):
        return {}

    def test_invite_contact(self, api_client, education, place):
        url = reverse("v1:education-place-invite", args=[education.id, place.id])
        data = self._get_contact_invite_data(place)
        response = api_client.post(url, data)
        assert response.status_code == self.expected_status_codes["place_invite"]

    def test_invite_existing_contact(self, api_client, education, place):
        contact = place.contacts.first()
        url = reverse("v1:education-place-contact-invite", args=[education.id, place.id, contact.id])
        response = api_client.post(url)
        assert response.status_code == self.expected_status_codes["existing_contact_invite"]


class TestForAuthenticated(TestForAnonymous):
    @pytest.fixture(autouse=True)
    def setup(self, api_client, user):
        api_client.force_authenticate(user=user)


class TestForOfficeMember(TestForAuthenticated):
    expected_status_codes = {
        "place_invite": status.CREATED,
        "existing_contact_invite": status.NO_CONTENT,
    }

    @pytest.fixture(autouse=True)
    def setup(self, api_client, office_member):
        api_client.force_authenticate(user=office_member)

    def _get_contact_invite_data(self, place):
        return {
            "name": "Test Contact",
            "emails": ["contact@uzgent.be"],
            "data": {
                "is_mentor": False,
                "is_staff": False,
            },
        }

    def test_invite_contact_bad_request(self, api_client, education, place):
        url = reverse("v1:education-place-invite", args=[education.id, place.id])
        response = api_client.post(url, {"name": "Test Contact"})
        assert response.status_code == status.BAD_REQUEST
