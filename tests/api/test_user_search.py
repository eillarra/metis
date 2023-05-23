import pytest

from django.urls import reverse
from http import HTTPStatus as status
from typing import Dict

from metis.utils.factories import (
    EducationFactory,
    UserFactory,
)


@pytest.fixture
def education(db):
    education = EducationFactory()
    return education


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
    expected_status_codes: Dict[str, status] = {
        "user_list": status.FORBIDDEN,
    }

    def test_list_users(self, api_client):
        url = reverse("v1:user-list")
        response = api_client.get(url)
        assert response.status_code == self.expected_status_codes["user_list"]


class TestForAuthenticated(TestForAnonymous):
    @pytest.fixture(autouse=True)
    def setup(self, api_client, user):
        api_client.force_authenticate(user=user)


class TestForOfficeMember(TestForAuthenticated):
    """
    Office members can list Metis users for search purposes.
    Only basic information is returned.
    """

    expected_status_codes = {
        "user_list": status.OK,
    }

    @pytest.fixture(autouse=True)
    def setup(self, api_client, office_member):
        api_client.force_authenticate(user=office_member)
