from http import HTTPStatus as status

import pytest
from django.urls import reverse

from metis.utils.factories import EmailLogFactory


@pytest.fixture
def email(t_project):  # noqa: D103
    return EmailLogFactory(project=t_project)


@pytest.mark.api
class TestForAnonymous:
    """Tests for anonymous users."""

    expected_status_codes: dict[str, status] = {
        "email_list": status.FORBIDDEN,
        "email_detail": status.FORBIDDEN,
    }

    def _get_text_create_data(self):
        return {}

    def _get_text_update_data(self):
        return {}

    def test_list_emails(self, api_client, t_project):  # noqa: D102
        url = reverse("v1:project-email-list", args=[t_project.education_id, t_project.id])
        response = api_client.get(url)
        assert response.status_code == self.expected_status_codes["email_list"]

    def test_retrieve_email(self, api_client, t_project, email):  # noqa: D102
        url = reverse("v1:project-email-detail", args=[t_project.education_id, t_project.id, email.id])
        response = api_client.get(url)
        assert response.status_code == self.expected_status_codes["email_detail"]


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
        "email_list": status.OK,
        "email_detail": status.OK,
    }

    @pytest.fixture(autouse=True)
    def setup(self, api_client, t_office_member):  # noqa: D102
        api_client.force_authenticate(user=t_office_member)
