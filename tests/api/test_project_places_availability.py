import pytest

from django.urls import reverse
from http import HTTPStatus as status

from metis.utils.factories import (
    ContactFactory,
    DisciplineFactory,
    EducationFactory,
    PeriodFactory,
    PlaceFactory,
    ProjectFactory,
    ProjectPlaceFactory,
    UserFactory,
)


@pytest.fixture
def education(db):
    education = EducationFactory()
    DisciplineFactory(education=education)
    place = PlaceFactory(education=education)
    ContactFactory(place=place)
    project = ProjectFactory(education=education)
    PeriodFactory(project=project)
    ProjectPlaceFactory(place=place, project=project)
    return education


@pytest.fixture
def project_place(db, education):
    return education.projects.first().place_set.first()


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
        "project_place_availability": status.FORBIDDEN,
    }

    def _update_place_availability_data(self, education, project_place):
        return []

    def test_availability_place(self, api_client, education, project_place):
        url = reverse("v1:project-place-availability", args=[education.id, project_place.project_id, project_place.id])
        data = self._update_place_availability_data(education, project_place)
        response = api_client.put(url, data)
        assert response.status_code == self.expected_status_codes["project_place_availability"]

        if response.status_code == status.CREATED:
            assert len(response.data["availability_set"]) == 1


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
        "project_place_availability": status.OK,
    }

    @pytest.fixture(autouse=True)
    def setup(self, api_client, office_member):
        api_client.force_authenticate(user=office_member)

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
    def test_invalid_data(self, api_client, education, project_place, data):
        url = reverse("v1:project-place-availability", args=[education.id, project_place.project_id, project_place.id])
        response = api_client.put(url, data)
        assert response.status_code == status.BAD_REQUEST
