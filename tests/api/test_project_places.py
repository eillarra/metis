from http import HTTPStatus as status

import pytest
from django.urls import reverse

from metis.utils.factories import PlaceFactory, ProjectPlaceFactory


@pytest.mark.api
class TestForAnonymous:
    """Tests for anonymous users."""

    expected_status_codes: dict[str, status] = {
        "project_place_list": status.FORBIDDEN,
        "project_place_create": status.FORBIDDEN,
        "project_place_update": status.FORBIDDEN,
        "project_place_delete": status.FORBIDDEN,
    }

    def _get_project_place_create_data(self, education):
        return {}

    def _get_project_place_update_data(self, education):
        return {}

    def _get_project_place_partial_update_data(self, education):
        return {}

    def test_list_places(self, api_client, t_education, t_project_place):  # noqa: D102
        url = reverse("v1:project-place-list", args=[t_education.id, t_project_place.project_id])
        response = api_client.get(url)
        assert response.status_code == self.expected_status_codes["project_place_list"]

    def test_create_place(self, api_client, t_education, t_project_place):  # noqa: D102
        url = reverse("v1:project-place-list", args=[t_education.id, t_project_place.project_id])
        data = self._get_project_place_create_data(t_education)
        response = api_client.post(url, data)
        assert response.status_code == self.expected_status_codes["project_place_create"]

        if response.status_code == status.CREATED:
            assert response.data["place"]["id"] == data["place_id"]

    def test_update_place(self, api_client, t_education, t_project_place):  # noqa: D102
        url = reverse("v1:project-place-detail", args=[t_education.id, t_project_place.project_id, t_project_place.id])
        data = self._get_project_place_update_data(t_education) | {"place_id": t_project_place.place_id}
        response = api_client.put(url, data)
        assert response.status_code == self.expected_status_codes["project_place_update"]

    def test_partial_update_place(self, api_client, t_education, t_project_place):  # noqa: D102
        url = reverse("v1:project-place-detail", args=[t_education.id, t_project_place.project_id, t_project_place.id])
        response = api_client.patch(url, self._get_project_place_partial_update_data(t_education))
        assert response.status_code == self.expected_status_codes["project_place_update"]

    def test_delete_place(self, api_client, t_education, t_project_place):  # noqa: D102
        new_project_place = ProjectPlaceFactory(
            project=t_project_place.project, place=PlaceFactory(education=t_education)
        )
        url = reverse(
            "v1:project-place-detail", args=[t_education.id, t_project_place.project_id, new_project_place.id]
        )
        response = api_client.delete(url)
        assert response.status_code == self.expected_status_codes["project_place_delete"]


class TestForAuthenticated(TestForAnonymous):
    """Tests for authenticated users."""

    @pytest.fixture(autouse=True)
    def setup(self, api_client, t_random_user):  # noqa: D102
        api_client.force_authenticate(user=t_random_user)


class TestForOtherEducationOfficeMember(TestForAuthenticated):
    """Tests for office members of other educations."""

    @pytest.fixture(autouse=True)
    def setup(self, api_client, t_random_office_member):  # noqa: D102
        api_client.force_authenticate(user=t_random_office_member)


class TestForOfficeMember(TestForAuthenticated):
    """Tests for office members of the education.

    Exceptions:
    - education places added to a project (ProjectPlace) cannot be deleted anymore
    """

    expected_status_codes = {
        "project_place_list": status.OK,
        "project_place_create": status.CREATED,
        "project_place_update": status.OK,
        "project_place_delete": status.NO_CONTENT,
    }

    @pytest.fixture(autouse=True)
    def setup(self, api_client, t_office_member):  # noqa: D102
        api_client.force_authenticate(user=t_office_member)

    def _get_project_place_create_data(self, t_education):
        return {
            "project_id": t_education.projects.first().id,
            "place_id": PlaceFactory(education=t_education).id,  # type: ignore
            "disciplines": list(t_education.disciplines.values_list("id", flat=True)),
        }

    def _get_project_place_update_data(self, t_education):
        return {
            "project_id": t_education.projects.first().id,
            "place_id": PlaceFactory(education=t_education).id,  # type: ignore
            "disciplines": list(t_education.disciplines.values_list("id", flat=True)),
        }

    def _get_project_place_partial_update_data(self, t_education):
        return {
            "disciplines": [list(t_education.disciplines.values_list("id", flat=True))[0]],
        }

    def test_delete_with_no_internships(self, api_client, t_education, t_project):  # noqa: D102
        initial_count = t_project.places.count()
        new_project_place = ProjectPlaceFactory(project=t_project, place=PlaceFactory(education=t_education))
        assert t_project.places.count() == initial_count + 1

        url = reverse("v1:project-place-detail", args=[t_education.id, t_project.id, new_project_place.id])
        response = api_client.delete(url)
        assert response.status_code == status.NO_CONTENT
        with pytest.raises(new_project_place.DoesNotExist):
            new_project_place.refresh_from_db()

        t_project.refresh_from_db()
        assert t_project.places.count() == initial_count
