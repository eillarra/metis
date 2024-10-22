from http import HTTPStatus as status

import pytest
from django.urls import reverse


@pytest.mark.api
@pytest.mark.django_db
class TestForAnonymous:
    """Tests for anonymous users."""

    expected_status_codes: dict[str, status] = {
        "place_invite": status.FORBIDDEN,
        "existing_contact_invite": status.FORBIDDEN,
    }

    def _get_contact_invite_data(self, place):
        return {}

    def test_invite_contact(self, api_client, t_education, t_place):  # noqa: D102
        url = reverse("v1:education-place-invite", args=[t_education.id, t_place.id])
        data = self._get_contact_invite_data(t_place)
        response = api_client.post(url, data)
        assert response.status_code == self.expected_status_codes["place_invite"]

    def test_invite_existing_contact(self, api_client, t_education, t_place):  # noqa: D102
        contact = t_place.contacts.first()
        url = reverse("v1:education-place-contact-invite", args=[t_education.id, t_place.id, contact.id])
        response = api_client.post(url)
        assert response.status_code == self.expected_status_codes["existing_contact_invite"]


class TestForAuthenticated(TestForAnonymous):
    """Tests for authenticated users."""

    @pytest.fixture(autouse=True)
    def setup(self, api_client, t_random_user):  # noqa: D102
        api_client.force_authenticate(user=t_random_user)


class TestForOtherEducationOfficeMember(TestForAuthenticated):
    """Tests for an office member in another education."""

    @pytest.fixture(autouse=True)
    def setup(self, api_client, t_random_office_member):  # noqa: D102
        api_client.force_authenticate(user=t_random_office_member)


class TestForOfficeMember(TestForAuthenticated):
    """Tests for an office member in t_education."""

    expected_status_codes = {
        "place_invite": status.CREATED,
        "existing_contact_invite": status.NO_CONTENT,
    }

    @pytest.fixture(autouse=True)
    def setup(self, api_client, t_office_member):  # noqa: D102
        api_client.force_authenticate(user=t_office_member)

    def _get_contact_invite_data(self, place):
        return {
            "name": "Test Contact",
            "emails": ["contact@uzgent.be"],
            "data": {
                "is_mentor": False,
                "is_staff": False,
            },
        }

    def test_invite_contact_bad_request(self, api_client, t_education, t_place):  # noqa: D102
        url = reverse("v1:education-place-invite", args=[t_education.id, t_place.id])
        response = api_client.post(url, {"name": "Test Contact"})
        assert response.status_code == status.BAD_REQUEST
