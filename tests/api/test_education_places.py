from http import HTTPStatus as status

import pytest
from django.urls import reverse

from metis.utils.factories import PlaceFactory, PlaceLocationFactory, PlaceTypeFactory, ProjectPlaceFactory, UserFactory


@pytest.fixture
def wrong_place_location(t_second_education):
    """Return a PlaceLocation instance for a different education."""
    return PlaceLocationFactory(education=t_second_education)


@pytest.fixture
def wrong_place_type(t_second_education):
    """Return a PlaceType instance for a different education."""
    return PlaceTypeFactory(education=t_second_education)


@pytest.mark.api
class TestForAnonymous:
    """Tests for anonymous users."""

    expected_status_codes: dict[str, status] = {
        "place_list": status.FORBIDDEN,
        "place_create": status.FORBIDDEN,
        "place_update": status.FORBIDDEN,
        "place_delete": status.FORBIDDEN,
        "contact_list": status.FORBIDDEN,
        "contact_create": status.FORBIDDEN,
        "contact_update": status.FORBIDDEN,
        "contact_delete": status.FORBIDDEN,
    }

    def _get_place_create_data(self, education):
        return {}

    def _get_place_update_data(self, education):
        return {}

    def _get_place_partial_update_data(self):
        return {}

    def _get_contact_create_data(self, place):
        return {}

    def _get_contact_update_data(self, place):
        return {}

    def _get_contact_partial_update_data(self):
        return {}

    def test_list_places(self, api_client, t_education):  # noqa: D102
        url = reverse("v1:education-place-list", args=[t_education.id])
        response = api_client.get(url)
        assert response.status_code == self.expected_status_codes["place_list"]

    def test_create_place(self, api_client, t_education):  # noqa: D102
        url = reverse("v1:education-place-list", args=[t_education.id])
        data = self._get_place_create_data(t_education)
        response = api_client.post(url, data)
        assert response.status_code == self.expected_status_codes["place_create"]

        if response.status_code == status.CREATED:
            assert response.data["code"] == data["code"]

    def test_update_place(self, api_client, t_education, t_place):  # noqa: D102
        url = reverse("v1:education-place-detail", args=[t_education.id, t_place.id])
        data = self._get_place_update_data(t_education) | {"education_id": t_place.education_id}
        response = api_client.put(url, data)
        assert response.status_code == self.expected_status_codes["place_update"]

    def test_partial_update_place(self, api_client, t_education, t_place):  # noqa: D102
        url = reverse("v1:education-place-detail", args=[t_education.id, t_place.id])
        response = api_client.patch(url, self._get_place_partial_update_data())
        assert response.status_code == self.expected_status_codes["place_update"]

    def test_delete_place(self, api_client, t_education):  # noqa: D102
        place = PlaceFactory(education=t_education)
        url = reverse("v1:education-place-detail", args=[t_education.id, place.id])
        response = api_client.delete(url)
        assert response.status_code == self.expected_status_codes["place_delete"]

    def test_list_contacts(self, api_client, t_education, t_place):  # noqa: D102
        url = reverse("v1:education-place-contact-list", args=[t_education.id, t_place.id])
        response = api_client.get(url)
        assert response.status_code == self.expected_status_codes["contact_list"]

    def test_create_contact(self, api_client, t_education, t_place):  # noqa: D102
        url = reverse("v1:education-place-contact-list", args=[t_education.id, t_place.id])
        data = self._get_contact_create_data(t_place)
        response = api_client.post(url, data)
        assert response.status_code == self.expected_status_codes["contact_create"]

        if response.status_code == status.CREATED:
            assert response.data["user"]["id"] == data["user_id"]

    def test_update_contact(self, api_client, t_education, t_place, t_contact):  # noqa: D102
        url = reverse("v1:education-place-contact-detail", args=[t_education.id, t_place.id, t_contact.id])
        data = self._get_contact_update_data(t_place) | {"place_id": t_place.id}
        response = api_client.put(url, data)
        assert response.status_code == self.expected_status_codes["contact_update"]

    def test_partial_update_contact(self, api_client, t_education, t_place, t_contact):  # noqa: D102
        url = reverse("v1:education-place-contact-detail", args=[t_education.id, t_place.id, t_contact.id])
        response = api_client.patch(url, self._get_contact_partial_update_data())
        assert response.status_code == self.expected_status_codes["contact_update"]

    def test_delete_contact(self, api_client, t_education, t_place, t_contact):  # noqa: D102
        url = reverse("v1:education-place-contact-detail", args=[t_education.id, t_place.id, t_contact.id])
        response = api_client.delete(url)
        assert response.status_code == self.expected_status_codes["contact_delete"]


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
        "place_list": status.OK,
        "place_create": status.CREATED,
        "place_update": status.OK,
        "place_delete": status.NO_CONTENT,
        "contact_list": status.OK,
        "contact_create": status.CREATED,
        "contact_update": status.OK,
        "contact_delete": status.NO_CONTENT,
    }

    @pytest.fixture(autouse=True)
    def setup(self, api_client, t_office_member):  # noqa: D102
        api_client.force_authenticate(user=t_office_member)

    def _get_place_create_data(self, education):
        return {
            "education_id": education.id,
            "name": "New place name",
            "code": "New place code",
            "disciplines": list(education.disciplines.values_list("id", flat=True)),
        }

    def _get_place_update_data(self, education):
        return {
            "education_id": education.id,
            "name": "Updated place name",
            "code": "Updated place code",
            "disciplines": [list(education.disciplines.values_list("id", flat=True))[0]],
        }

    def _get_place_partial_update_data(self):
        return {
            "name": "Updated place name",
        }

    def _get_contact_create_data(self, place):
        return {
            "place_id": place.id,
            "user_id": UserFactory().id,  # type: ignore
            "is_staff": True,
        }

    def _get_contact_update_data(self, place):
        return {
            "place_id": place.id,
            "user_id": UserFactory().id,  # type: ignore
            "is_staff": False,
            "is_mentor": True,
        }

    def _get_contact_partial_update_data(self):
        return {
            "is_staff": True,
            "is_mentor": False,
        }

    def test_partial_update_wrong_data(self, api_client, t_education, t_place, wrong_place_location, wrong_place_type):  # noqa: D102
        url = reverse("v1:education-place-detail", args=[t_education.id, t_place.id])
        response = api_client.patch(url, {"location": wrong_place_location.id})
        assert response.status_code == status.BAD_REQUEST

        response = api_client.patch(url, {"type": wrong_place_type.id})
        assert response.status_code == status.BAD_REQUEST

    def test_delete_used_place(self, api_client, t_education):  # noqa: D102
        place = PlaceFactory(education=t_education)
        project = t_education.projects.first()
        project.place_set.add(ProjectPlaceFactory(place=place))
        assert project.places.filter(id=place.id).count() == 1

        url = reverse("v1:education-place-detail", args=[t_education.id, place.id])
        response = api_client.delete(url)
        assert response.status_code == status.FORBIDDEN
        assert project.places.filter(id=place.id).count() == 1
