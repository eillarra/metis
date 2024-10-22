from http import HTTPStatus as status

import pytest
from django.urls import reverse

from metis.utils.factories import ContactFactory, StudentFactory


@pytest.fixture
def contact(db, t_place):  # noqa: D103
    return ContactFactory(place=t_place)


@pytest.fixture
def student(db, t_project):  # noqa: D103
    return StudentFactory(project=t_project)


@pytest.mark.site
class TestForAnonymous:
    """Tests for anonymous users."""

    expected_status_codes: dict[str, status] = {
        "homepage": status.OK,
        "dashboard": status.FOUND,
        "education_office": status.FOUND,
    }

    def test_homepage_access(self, client):  # noqa: D102
        response = client.get(reverse("homepage"))
        assert response.status_code == self.expected_status_codes["homepage"]

    def test_dashboard_access(self, client):  # noqa: D102
        response = client.get(reverse("dashboard"))
        assert response.status_code == self.expected_status_codes["dashboard"]

    def test_office_access(self, client, t_education):  # noqa: D102
        response = client.get(t_education.get_office_url())
        assert response.status_code == self.expected_status_codes["education_office"]


class TestForAuthenticated(TestForAnonymous):
    """Tests for authenticated users."""

    expected_status_codes: dict[str, status] = {
        "homepage": status.OK,
        "dashboard": status.OK,
        "education_office": status.FORBIDDEN,
    }

    @pytest.fixture(autouse=True)
    def setup(self, client, t_random_user):  # noqa: D102
        client.force_login(user=t_random_user)


class TestForOfficeMember(TestForAuthenticated):
    """Tests for office members."""

    expected_status_codes: dict[str, status] = {
        "homepage": status.OK,
        "dashboard": status.OK,
        "education_office": status.OK,
    }

    @pytest.fixture(autouse=True)
    def setup(self, client, t_office_member):  # noqa: D102
        client.force_login(user=t_office_member)


class TestForContact(TestForAuthenticated):
    """Tests for contacts."""

    @pytest.fixture(autouse=True)
    def setup(self, client, contact):  # noqa: D102
        client.force_login(user=contact.user)


class TestForStudent(TestForAuthenticated):
    """Tests for students."""

    @pytest.fixture(autouse=True)
    def setup(self, client, student):  # noqa: D102
        client.force_login(user=student.user)
