from http import HTTPStatus as status

import pytest
from django.urls import reverse


@pytest.mark.api
class TestForAnonymous:
    """Tests for anonymous users."""

    expected_status_codes: dict[str, status] = {
        "project_place_availability": status.FORBIDDEN,
    }

    def _update_place_availability_data(self, education, project_place):
        return []

    def test_availability_place(self, api_client, t_education, t_project_place):  # noqa: D102
        url = reverse(
            "v1:project-place-availability", args=[t_education.id, t_project_place.project_id, t_project_place.id]
        )
        data = self._update_place_availability_data(t_education, t_project_place)
        response = api_client.put(url, data)
        assert response.status_code == self.expected_status_codes["project_place_availability"]

        if response.status_code == status.CREATED:
            assert len(response.data["availability_set"]) == 1


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
    """Office members can manage the EducationPlace and ProjectPlaces.
    Exceptions:
    - education places added to a project (ProjectPlace) cannot be deleted anymore
    """

    expected_status_codes = {
        "project_place_availability": status.OK,
    }

    @pytest.fixture(autouse=True)
    def setup(self, api_client, t_office_member):  # noqa: D102
        api_client.force_authenticate(user=t_office_member)

    def _update_place_availability_data(self, education, project_place):
        return [
            {
                "period": education.projects.first().periods.first().id,
                "min": 1,
                "max": 5,
            }
        ]

    @pytest.mark.parametrize(
        "data",
        [
            {"period": 1, "min": 1, "max": 2},
            [{"period": 1, "min": 2, "max": 1}],
        ],
    )
    def test_invalid_data(self, api_client, t_education, t_project_place, data):  # noqa: D102
        url = reverse(
            "v1:project-place-availability", args=[t_education.id, t_project_place.project_id, t_project_place.id]
        )
        response = api_client.put(url, data)
        assert response.status_code == status.BAD_REQUEST
