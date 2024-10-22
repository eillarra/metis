from http import HTTPStatus as status

import pytest
from django.urls import reverse

from metis.utils.factories import ProjectFactory


@pytest.mark.api
class TestForAnonymous:
    """Tests for anonymous users."""

    expected_status_codes: dict[str, status] = {
        "project_list": status.FORBIDDEN,
        "project_create": status.FORBIDDEN,
        "project_update": status.FORBIDDEN,
        "project_delete": status.FORBIDDEN,
    }

    def _get_project_create_data(self, project):
        return {}

    def _get_project_update_data(self, project):
        return {}

    def test_list_projects(self, api_client, t_project):  # noqa: D102
        url = reverse("v1:project-list", args=[t_project.education_id])
        response = api_client.get(url)
        assert response.status_code == self.expected_status_codes["project_list"]

    def test_create_project(self, api_client, t_project):  # noqa: D102
        url = reverse("v1:project-list", args=[t_project.education_id])
        data = self._get_project_create_data(t_project)
        response = api_client.post(url, data)
        assert response.status_code == self.expected_status_codes["project_create"]

        if response.status_code == status.CREATED:
            assert response.data["name"] == data["name"]

    def test_update_project(self, api_client, t_project):  # noqa: D102
        url = reverse("v1:project-detail", args=[t_project.education_id, t_project.id])
        data = self._get_project_update_data(t_project)
        response = api_client.put(url, data)
        assert response.status_code == self.expected_status_codes["project_update"]

    def test_partial_update_project(self, api_client, t_project):  # noqa: D102
        url = reverse("v1:project-detail", args=[t_project.education_id, t_project.id])
        response = api_client.patch(url, self._get_project_update_data(t_project))
        assert response.status_code == self.expected_status_codes["project_update"]

    def test_delete_project(self, api_client, t_education):  # noqa: D102
        new_project = ProjectFactory(education=t_education)
        url = reverse("v1:project-detail", args=[t_education.id, new_project.id])
        response = api_client.delete(url)
        assert response.status_code == self.expected_status_codes["project_delete"]

        if response.status_code == status.NO_CONTENT:
            with pytest.raises(new_project.DoesNotExist):
                new_project.refresh_from_db()


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

    Office members can manage the EducationPlace and ProjectPlaces.

    Exceptions:
    - education places added to a project (ProjectPlace) cannot be deleted anymore
    """

    expected_status_codes = {
        "project_list": status.OK,
        "project_create": status.CREATED,
        "project_update": status.OK,
        "project_delete": status.NO_CONTENT,
    }

    @pytest.fixture(autouse=True)
    def setup(self, api_client, t_office_member):  # noqa: D102
        api_client.force_authenticate(user=t_office_member)

    def _get_project_create_data(self, project):
        return {
            "name": "project name",
            "program": project.program_id,
        }

    def _get_project_update_data(self, project):
        return {
            "name": "updated project name",
            "program": project.program_id,
        }

    def test_delete_project_when_project_place_exists(self, api_client, t_project):  # noqa: D102
        url = reverse("v1:project-detail", args=[t_project.education_id, t_project.id])
        response = api_client.delete(url)
        assert response.status_code == status.FORBIDDEN
