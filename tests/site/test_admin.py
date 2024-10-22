from http import HTTPStatus as status

import pytest
from django.urls import reverse

from metis.utils.factories import UserFactory


@pytest.fixture
def admin(db):  # noqa: D103
    return UserFactory(is_staff=True)


@pytest.fixture
def superuser(db):  # noqa: D103
    return UserFactory(is_staff=True, is_superuser=True)


@pytest.mark.site
class TestForAnonymous:
    """Tests for anonymous users."""

    expected_status_codes: dict[str, status] = {
        "admin_index": status.FOUND,
    }

    def test_admin_index(self, client):  # noqa: D102
        response = client.get(reverse("admin:index"))
        assert response.status_code == self.expected_status_codes["admin_index"]


class TestForAuthenticated(TestForAnonymous):
    """Tests for authenticated users."""

    expected_status_codes: dict[str, status] = {
        "admin_index": status.FOUND,
    }

    @pytest.fixture(autouse=True)
    def setup(self, client, t_random_user):  # noqa: D102
        client.force_login(user=t_random_user)


class TestForAdmin(TestForAuthenticated):
    expected_status_codes: dict[str, status] = {
        "admin_index": status.OK,
        "admin_pages": status.FORBIDDEN,
    }

    @pytest.fixture(autouse=True)
    def setup(self, client, admin):  # noqa: D102
        client.force_login(user=admin)

    @pytest.mark.parametrize(
        "route",
        [
            "admin:metis_faculty",
            "admin:metis_education",
            "admin:metis_program",
            "admin:metis_discipline",
            "admin:metis_project",
            "admin:metis_place",
            "admin:metis_internship",
            "admin:metis_user",
        ],
    )
    def test_admin_pages(self, client, route):  # noqa: D102
        response = client.get(reverse(f"{route}_changelist"))
        assert response.status_code == self.expected_status_codes["admin_pages"]
        response = client.get(reverse(f"{route}_add"))
        assert response.status_code == self.expected_status_codes["admin_pages"]


class TestForSuperuser(TestForAdmin):
    """Tests for superusers."""

    expected_status_codes: dict[str, status] = {
        "admin_index": status.OK,
        "admin_pages": status.OK,
    }

    @pytest.fixture(autouse=True)
    def setup(self, client, superuser):  # noqa: D102
        client.force_login(user=superuser)
