import pytest

from django.urls import reverse
from http import HTTPStatus as status

from metis.utils.factories import (
    ContactFactory,
    EducationFactory,
    PlaceFactory,
    ProgramFactory,
    ProjectFactory,
    UserFactory,
)


@pytest.fixture
def education(db):
    education = EducationFactory()
    place = PlaceFactory(education=education)
    program = ProgramFactory(education=education)
    ContactFactory(place=place)
    ProjectFactory(education=education, program=program)
    return education


@pytest.fixture
def project(db, education):
    return education.projects.first()


@pytest.fixture
def office_member(db, education):
    user = UserFactory()
    education.office_members.add(user)
    return user


@pytest.fixture
def office_member_of_other_education(db):
    user = UserFactory()
    education2 = EducationFactory()
    education2.office_members.add(user)  # type: ignore
    return user


@pytest.fixture
def user(db):
    return UserFactory()


@pytest.mark.api
class TestForAnonymous:
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

    def test_list_projects(self, api_client, project):
        url = reverse("v1:project-list", args=[project.education_id])
        response = api_client.get(url)
        assert response.status_code == self.expected_status_codes["project_list"]

    def test_create_project(self, api_client, project):
        url = reverse("v1:project-list", args=[project.education_id])
        data = self._get_project_create_data(project)
        response = api_client.post(url, data)
        assert response.status_code == self.expected_status_codes["project_create"]

        if response.status_code == status.CREATED:
            assert response.data["name"] == data["name"]

    def test_update_project(self, api_client, project):
        url = reverse("v1:project-detail", args=[project.education_id, project.id])
        data = self._get_project_update_data(project)
        response = api_client.put(url, data)
        assert response.status_code == self.expected_status_codes["project_update"]

    def test_partial_update_project(self, api_client, project):
        url = reverse("v1:project-detail", args=[project.education_id, project.id])
        response = api_client.patch(url, self._get_project_update_data(project))
        assert response.status_code == self.expected_status_codes["project_update"]

    def test_delete_project(self, api_client, project):
        url = reverse("v1:project-detail", args=[project.education_id, project.id])
        response = api_client.delete(url)
        assert response.status_code == self.expected_status_codes["project_delete"]


class TestForAuthenticated(TestForAnonymous):
    @pytest.fixture(autouse=True)
    def setup(self, api_client, user):
        api_client.force_authenticate(user=user)


class TestForOtherEducationOfficeMember(TestForAuthenticated):
    @pytest.fixture(autouse=True)
    def setup(self, api_client, office_member_of_other_education):
        api_client.force_authenticate(user=office_member_of_other_education)


class TestForOfficeMember(TestForAuthenticated):
    """
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
    def setup(self, api_client, office_member):
        api_client.force_authenticate(user=office_member)

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

    def test_delete_project_when_place_exists(self, api_client, project):
        url = reverse("v1:project-detail", args=[project.education_id, project.id])
        response = api_client.delete(url)
        assert response.status_code == status.NO_CONTENT
        with pytest.raises(project.DoesNotExist):
            project.refresh_from_db()
