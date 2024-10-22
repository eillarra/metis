from http import HTTPStatus as status

import pytest
from django.urls import reverse

from metis.utils.factories import EducationFactory, PlaceFactory, ProjectFactory, ProjectPlaceFactory, StudentFactory


@pytest.mark.api
class TestForAnonymous:
    """Tests for anonymous users."""

    expected_status_codes: dict[str, status] = {
        "retrieve": status.FORBIDDEN,
        "programs": status.FORBIDDEN,
        "student_users": status.FORBIDDEN,
    }

    def _get_project_create_data(self):
        return {}

    def _get_project_update_data(self):
        return {}

    def test_retrieve(self, api_client, t_education):  # noqa: D102
        url = reverse("v1:education-detail", args=[t_education.id])
        response = api_client.get(url)
        assert response.status_code == self.expected_status_codes["retrieve"]

    def test_programs(self, api_client, t_education):  # noqa: D102
        url = reverse("v1:education-programs", args=[t_education.id])
        response = api_client.get(url)
        assert response.status_code == self.expected_status_codes["programs"]

    def test_students(self, api_client, t_education):  # noqa: D102
        url = reverse("v1:education-student-users", args=[t_education.id])
        response = api_client.get(url)
        assert response.status_code == self.expected_status_codes["student_users"]


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
    """Tests for an office member in t_education.

    Office members can manage their projects and places.

    Exceptions:
    - projects with students cannot be deleted anymore, all students must be removed first
    - students with internships cannot be deleted anymore, all internships must be removed first
    """

    expected_status_codes = {
        "retrieve": status.OK,
        "programs": status.OK,
        "student_users": status.OK,
    }

    @pytest.fixture(autouse=True)
    def setup(self, api_client, t_office_member):  # noqa: D102
        api_client.force_authenticate(user=t_office_member)

    def _get_project_create_data(self):
        return {
            "name": "Updated project name",
        }

    def _get_project_update_data(self):
        return {
            "name": "Updated project name",
        }

    def test_create_project_for_other_education(self, api_client):  # noqa: D102
        other_education = EducationFactory()
        url = reverse("v1:project-list", args=[other_education.id])  # type: ignore
        response = api_client.post(url, self._get_project_create_data())
        assert response.status_code == status.FORBIDDEN

    def test_delete_project(self, api_client, t_education):  # noqa: D102
        project = ProjectFactory(education=t_education)
        url = reverse("v1:project-detail", args=[t_education.id, project.id])  # type: ignore
        response = api_client.delete(url)
        assert response.status_code == status.NO_CONTENT

    def test_delete_project_with_place(self, api_client, t_education):  # noqa: D102
        project = t_education.projects.first()
        place = PlaceFactory(education=t_education)
        project.place_set.add(ProjectPlaceFactory(place=place))
        assert project.project_places.filter(place=place).count() == 1

        url = reverse("v1:project-detail", args=[t_education.id, project.id])
        response = api_client.delete(url)
        assert response.status_code == status.FORBIDDEN
        assert project.project_places.filter(place=place).count() == 1

    def test_delete_project_with_student(self, api_client, t_education):  # noqa: D102
        project = t_education.projects.first()
        student_count = project.students.count()
        StudentFactory(project=project)
        assert project.students.count() == student_count + 1

        url = reverse("v1:project-detail", args=[t_education.id, project.id])
        response = api_client.delete(url)
        assert response.status_code == status.FORBIDDEN
        assert project.students.count() == student_count + 1
