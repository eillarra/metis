import pytest

from django.urls import reverse
from http import HTTPStatus as status
from typing import Dict

from metis.utils.factories import (
    EducationFactory,
    EducationPlaceFactory,
    PlaceFactory,
    ProjectFactory,
    ProjectPlaceFactory,
    StudentFactory,
    UserFactory,
)


@pytest.fixture
def education(db):
    education = EducationFactory()
    EducationPlaceFactory(education=education)
    ProjectFactory(education=education)
    return education


@pytest.fixture
def office_member(db, education):
    user = UserFactory()
    education.office_members.add(user)
    return user


@pytest.fixture
def office_member2(db):
    user = UserFactory()
    education2 = EducationFactory()
    education2.office_members.add(user)  # type: ignore
    return user


@pytest.fixture
def user(db):
    return UserFactory()


@pytest.mark.api
class TestForAnonymous:
    expected_status_codes: Dict[str, status] = {
        "retrieve": status.FORBIDDEN,
        "places": status.FORBIDDEN,
        "place_create": status.FORBIDDEN,
        "place_update": status.FORBIDDEN,
        "place_delete": status.FORBIDDEN,
        "projects": status.FORBIDDEN,
        "project_create": status.FORBIDDEN,
        "project_update": status.FORBIDDEN,
        "project_delete": status.FORBIDDEN,
        "programs": status.FORBIDDEN,
        "students": status.FORBIDDEN,
    }

    def _get_place_create_data(self):
        return {}

    def _get_place_update_data(self):
        return {}

    def _get_project_create_data(self):
        return {}

    def _get_project_update_data(self):
        return {}

    def test_retrieve(self, api_client, education):
        url = reverse("v1:education-detail", args=[education.id])
        response = api_client.get(url)
        assert response.status_code == self.expected_status_codes["retrieve"]

    def test_places(self, api_client, education):
        url = reverse("v1:education-place-list", args=[education.id])
        response = api_client.get(url)
        assert response.status_code == self.expected_status_codes["places"]

    def test_programs(self, api_client, education):
        url = reverse("v1:education-programs", args=[education.id])
        response = api_client.get(url)
        assert response.status_code == self.expected_status_codes["programs"]

    def test_projects(self, api_client, education):
        url = reverse("v1:education-project-list", args=[education.id])
        response = api_client.get(url)
        assert response.status_code == self.expected_status_codes["projects"]

    def test_students(self, api_client, education):
        url = reverse("v1:education-students", args=[education.id])
        response = api_client.get(url)
        assert response.status_code == self.expected_status_codes["students"]

    def test_create_place(self, api_client, education):
        url = reverse("v1:education-place-list", args=[education.id])
        data = self._get_place_create_data()
        response = api_client.post(url, data)
        assert response.status_code == self.expected_status_codes["place_create"]

        if data:
            assert response.data["place"]["id"] == data["place_id"]

    def test_update_place(self, api_client, education):
        education_place = education.place_set.first()
        url = reverse("v1:education-place-detail", args=[education.id, education_place.id])
        data = self._get_place_update_data() | {"place_id": education_place.place_id}
        response = api_client.put(url, data)
        assert response.status_code == self.expected_status_codes["place_update"]

    def test_partial_update_place(self, api_client, education):
        place_id = education.place_set.first().id
        url = reverse("v1:education-place-detail", args=[education.id, place_id])
        response = api_client.patch(url, self._get_place_update_data())
        assert response.status_code == self.expected_status_codes["place_update"]

    def test_delete_place(self, api_client, education):
        place_id = education.place_set.first().id
        url = reverse("v1:education-place-detail", args=[education.id, place_id])
        response = api_client.delete(url)
        assert response.status_code == self.expected_status_codes["place_delete"]

    def test_create_project(self, api_client, education):
        url = reverse("v1:education-project-list", args=[education.id])
        data = self._get_project_create_data()
        response = api_client.post(url, data)
        assert response.status_code == self.expected_status_codes["project_create"]

        if data:
            assert response.data["name"] == data["name"]
            assert reverse("v1:education-detail", args=[education.id]) in response.data["education"]

    def test_update_project(self, api_client, education):
        project_id = education.projects.first().id
        url = reverse("v1:education-project-detail", args=[education.id, project_id])
        response = api_client.put(url, self._get_project_update_data())
        assert response.status_code == self.expected_status_codes["project_update"]

    def test_partial_update_project(self, api_client, education):
        project_id = education.projects.first().id
        url = reverse("v1:education-project-detail", args=[education.id, project_id])
        response = api_client.patch(url, self._get_project_update_data())
        assert response.status_code == self.expected_status_codes["project_update"]

    def test_delete_project(self, api_client, education):
        project_id = education.projects.first().id
        url = reverse("v1:education-project-detail", args=[education.id, project_id])
        response = api_client.delete(url)
        assert response.status_code == self.expected_status_codes["project_delete"]


class TestForAuthenticated(TestForAnonymous):
    @pytest.fixture(autouse=True)
    def setup(self, api_client, user):
        api_client.force_authenticate(user=user)


class TestForOtherOfficeMember(TestForAuthenticated):
    @pytest.fixture(autouse=True)
    def setup(self, api_client, office_member2):
        api_client.force_authenticate(user=office_member2)


class TestForOfficeMember(TestForAnonymous):
    """
    Office members can manage their projects and places.
    Exceptions:
    - projects with students cannot be deleted anymore, all students must be removed first
    - students with internships cannot be deleted anymore, all internships must be removed first
    """

    expected_status_codes = {
        "retrieve": status.OK,
        "places": status.OK,
        "place_create": status.CREATED,
        "place_update": status.OK,
        "place_delete": status.NO_CONTENT,
        "projects": status.OK,
        "project_create": status.CREATED,
        "project_update": status.OK,
        "project_delete": status.NO_CONTENT,
        "programs": status.OK,
        "students": status.OK,
    }

    @pytest.fixture(autouse=True)
    def setup(self, api_client, office_member):
        api_client.force_authenticate(user=office_member)

    def _get_place_create_data(self):
        return {
            "place_id": PlaceFactory().id,  # type: ignore
            "code": "New place code",
        }

    def _get_place_update_data(self):
        return {
            "code": "Updated place code",
        }

    def _get_project_create_data(self):
        return {
            "name": "Updated project name",
        }

    def _get_project_update_data(self):
        return {
            "name": "Updated project name",
        }

    def test_create_project_for_other_education(self, api_client):
        other_education = EducationFactory()
        url = reverse("v1:education-project-list", args=[other_education.id])  # type: ignore
        response = api_client.post(url, self._get_project_create_data())
        assert response.status_code == status.FORBIDDEN

    def test_delete_project_with_place(self, api_client, education):
        project = education.projects.first()
        place = education.places.first()
        project.place_set.add(ProjectPlaceFactory(place=place))
        assert project.places.count() == 1

        url = reverse("v1:education-project-detail", args=[education.id, project.id])
        response = api_client.delete(url)
        assert response.status_code == status.NO_CONTENT
        assert project.places.count() == 0

    def test_delete_project_with_student(self, api_client, education):
        project = education.projects.first()
        StudentFactory(project=project)
        assert project.students.count() == 1

        url = reverse("v1:education-project-detail", args=[education.id, project.id])
        response = api_client.delete(url)
        assert response.status_code == status.FORBIDDEN
        assert project.students.count() == 1
