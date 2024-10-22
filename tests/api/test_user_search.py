from http import HTTPStatus as status

import pytest
from django.urls import reverse


@pytest.mark.api
class TestForAnonymous:
    """Tests for anonymous users."""

    expected_status_codes: dict[str, status] = {
        "user_list": status.FORBIDDEN,
    }

    def test_list_users(self, api_client):  # noqa: D102
        url = reverse("v1:user-list")
        response = api_client.get(url)
        assert response.status_code == self.expected_status_codes["user_list"]


class TestForAuthenticated(TestForAnonymous):
    """Tests for authenticated users."""

    @pytest.fixture(autouse=True)
    def setup(self, api_client, t_random_user):  # noqa: D102
        api_client.force_authenticate(user=t_random_user)


class TestForOfficeMember(TestForAuthenticated):
    """Tests for office members.

    Office members can list Metis users for search purposes.
    Only basic information is returned.
    """

    expected_status_codes = {
        "user_list": status.OK,
    }

    @pytest.fixture(autouse=True)
    def setup(self, api_client, t_office_member):  # noqa: D102
        api_client.force_authenticate(user=t_office_member)


class TestForOtherEducationOfficeMember(TestForOfficeMember):
    """Tests for an office member in another education."""

    @pytest.fixture(autouse=True)
    def setup(self, api_client, t_random_office_member):  # noqa: D102
        api_client.force_authenticate(user=t_random_office_member)
