import pytest

from django.urls import reverse
from http import HTTPStatus as status

from metis.utils.factories import (
    EducationFactory,
    ProjectFactory,
    PlaceFactory,
    ContactFactory,
    StudentFactory,
    UserFactory,
)


@pytest.fixture
def education(db):
    education = EducationFactory()
    ProjectFactory(education=education)
    return education


@pytest.fixture
def office_member(db, education):
    user = UserFactory()
    education.office_members.add(user)
    return user


@pytest.fixture
def contact(db, education):
    place = PlaceFactory(education=education)
    return ContactFactory(place=place)


@pytest.fixture
def student(db, education):
    return StudentFactory(project=education.projects.first())


@pytest.fixture
def user(db):
    return UserFactory()


@pytest.mark.site
class TestForAnonymous:
    expected_status_codes: dict[str, status] = {
        "homepage": status.OK,
        "dashboard": status.FOUND,
        "education_office": status.FOUND,
    }

    def test_homepage_access(self, client):
        response = client.get(reverse("homepage"))
        assert response.status_code == self.expected_status_codes["homepage"]

    def test_dashboard_access(self, client):
        response = client.get(reverse("dashboard"))
        assert response.status_code == self.expected_status_codes["dashboard"]

    def test_office_access(self, client, education):
        response = client.get(education.get_office_url())
        assert response.status_code == self.expected_status_codes["education_office"]


class TestForAuthenticated(TestForAnonymous):
    expected_status_codes: dict[str, status] = {
        "homepage": status.OK,
        "dashboard": status.OK,
        "education_office": status.FORBIDDEN,
    }

    @pytest.fixture(autouse=True)
    def setup(self, client, user):
        client.force_login(user=user)


class TestForOfficeMember(TestForAuthenticated):
    expected_status_codes: dict[str, status] = {
        "homepage": status.OK,
        "dashboard": status.OK,
        "education_office": status.OK,
    }

    @pytest.fixture(autouse=True)
    def setup(self, client, office_member):
        client.force_login(user=office_member)


class TestForContact(TestForAuthenticated):
    @pytest.fixture(autouse=True)
    def setup(self, client, contact):
        client.force_login(user=contact.user)


class TestForStudent(TestForAuthenticated):
    @pytest.fixture(autouse=True)
    def setup(self, client, student):
        client.force_login(user=student.user)
