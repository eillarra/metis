import pytest

from django.urls import reverse
from http import HTTPStatus as status
from typing import Dict

from metis.utils.factories import (
    ContactFactory,
    EducationFactory,
    PlaceFactory,
    ProjectFactory,
    ProjectPlaceFactory,
    UserFactory,
)


@pytest.fixture
def education(db):
    education = EducationFactory()
    place = PlaceFactory(education=education)
    ContactFactory(place=place)
    project = ProjectFactory(education=education)
    ProjectPlaceFactory(place=place, project=project)
    return education


@pytest.fixture
def project_place(db, education):
    return education.projects.first().place_set.first()


@pytest.fixture
def contact(db, project_place):
    return project_place.contacts.first()


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
    expected_status_codes: Dict[str, status] = {
        "place_list": status.FORBIDDEN,
        "place_create": status.FORBIDDEN,
        "place_update": status.FORBIDDEN,
        "place_delete": status.FORBIDDEN,
    }

    def _get_place_create_data(self, education):
        return {}

    def _get_place_update_data(self, education):
        return {}

    def test_list_places(self, api_client, education, project_place):
        url = reverse("v1:project-place-list", args=[education.id, project_place.project_id])
        response = api_client.get(url)
        assert response.status_code == self.expected_status_codes["place_list"]

    def test_create_place(self, api_client, education, project_place):
        url = reverse("v1:project-place-list", args=[education.id, project_place.project_id])
        data = self._get_place_create_data(education)
        response = api_client.post(url, data)
        assert response.status_code == self.expected_status_codes["place_create"]

        if data:
            assert response.data["place"]["id"] == data["place_id"]

    def test_update_place(self, api_client, education, project_place):
        url = reverse("v1:project-place-detail", args=[education.id, project_place.project_id, project_place.id])
        data = self._get_place_update_data(education) | {"place_id": project_place.place_id}
        response = api_client.put(url, data)
        assert response.status_code == self.expected_status_codes["place_update"]

    def test_partial_update_place(self, api_client, education, project_place):
        url = reverse("v1:project-place-detail", args=[education.id, project_place.project_id, project_place.id])
        response = api_client.patch(url, self._get_place_update_data(education))
        assert response.status_code == self.expected_status_codes["place_update"]

    def test_delete_place(self, api_client, education, project_place):
        url = reverse("v1:project-place-detail", args=[education.id, project_place.project_id, project_place.id])
        response = api_client.delete(url)
        assert response.status_code == self.expected_status_codes["place_delete"]


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
        "place_list": status.OK,
        "place_create": status.CREATED,
        "place_update": status.OK,
        "place_delete": status.NO_CONTENT,
    }

    @pytest.fixture(autouse=True)
    def setup(self, api_client, office_member):
        api_client.force_authenticate(user=office_member)

    def _get_place_create_data(self, education):
        return {
            "place_id": PlaceFactory(education=education).id,  # type: ignore
        }

    def _get_place_update_data(self, education):
        return {
            "place_id": PlaceFactory(education=education).id,  # type: ignore
        }

    def test_delete_with_no_internships(self, api_client, education, project_place):
        project = project_place.project
        assert project.places.count() == 1

        url = reverse("v1:project-place-detail", args=[education.id, project_place.project_id, project_place.id])
        response = api_client.delete(url)
        assert response.status_code == status.NO_CONTENT
        with pytest.raises(project_place.DoesNotExist):
            project_place.refresh_from_db()

        project.refresh_from_db()
        assert project.places.count() == 0

    @pytest.mark.skip(reason="TODO")
    def test_delete_with_internships(self, api_client, education, project_place):
        """When the place has been used in an internshiop, it cannot be deleted anymore."""
        # assert response.status_code == status.FORBIDDEN
        pass
