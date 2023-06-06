import pytest

from django.urls import reverse
from http import HTTPStatus as status
from typing import Dict

from metis.utils.factories import UserFactory


@pytest.fixture
def admin(db):
    return UserFactory(is_staff=True)


@pytest.fixture
def superuser(db):
    return UserFactory(is_staff=True, is_superuser=True)


@pytest.fixture
def user(db):
    return UserFactory()


@pytest.mark.site
class TestForAnonymous:
    expected_status_codes: Dict[str, status] = {
        "admin_index": status.FOUND,
    }

    def test_admin_index(self, client):
        response = client.get(reverse("admin:index"))
        assert response.status_code == self.expected_status_codes["admin_index"]


class TestAuthenticated(TestForAnonymous):
    expected_status_codes: Dict[str, status] = {
        "admin_index": status.FOUND,
    }

    @pytest.fixture(autouse=True)
    def setup(self, client, user):
        client.force_login(user=user)


class TestAdmin(TestAuthenticated):
    expected_status_codes: Dict[str, status] = {
        "admin_index": status.OK,
        "admin_pages": status.FORBIDDEN,
    }

    @pytest.fixture(autouse=True)
    def setup(self, client, admin):
        client.force_login(user=admin)

    @pytest.mark.parametrize(
        "route",
        [
            "admin:metis_faculty",
            "admin:metis_education",
            "admin:metis_program",
            "admin:metis_discipline",
            "admin:metis_project",
            "admin:metis_internship",
            "admin:metis_user",
        ],
    )
    def test_admin_pages(self, client, route):
        response = client.get(reverse(f"{route}_changelist"))
        assert response.status_code == self.expected_status_codes["admin_pages"]
        response = client.get(reverse(f"{route}_add"))
        assert response.status_code == self.expected_status_codes["admin_pages"]


class TestSuperuser(TestAdmin):
    expected_status_codes: Dict[str, status] = {
        "admin_index": status.OK,
        "admin_pages": status.OK,
    }

    @pytest.fixture(autouse=True)
    def setup(self, client, superuser):
        client.force_login(user=superuser)
