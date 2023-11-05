from http import HTTPStatus as status

import pytest
from django.urls import reverse

from metis.utils.factories import (
    ContactFactory,
    DisciplineFactory,
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
    DisciplineFactory(education=education)
    DisciplineFactory(education=education)
    ContactFactory(place=place)
    ProjectFactory(education=education)
    return education


@pytest.fixture
def place(db, education):
    return education.places.first()


@pytest.fixture
def contact(db, place):
    return place.contacts.first()


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

    def test_list_places(self, api_client, education):
        url = reverse("v1:education-place-list", args=[education.id])
        response = api_client.get(url)
        assert response.status_code == self.expected_status_codes["place_list"]

    def test_create_place(self, api_client, education):
        url = reverse("v1:education-place-list", args=[education.id])
        data = self._get_place_create_data(education)
        response = api_client.post(url, data)
        assert response.status_code == self.expected_status_codes["place_create"]

        if response.status_code == status.CREATED:
            assert response.data["code"] == data["code"]

    def test_update_place(self, api_client, education, place):
        url = reverse("v1:education-place-detail", args=[education.id, place.id])
        data = self._get_place_update_data(education) | {"education_id": place.education_id}
        response = api_client.put(url, data)
        assert response.status_code == self.expected_status_codes["place_update"]

    def test_partial_update_place(self, api_client, education, place):
        url = reverse("v1:education-place-detail", args=[education.id, place.id])
        response = api_client.patch(url, self._get_place_partial_update_data())
        assert response.status_code == self.expected_status_codes["place_update"]

    def test_delete_place(self, api_client, education, place):
        url = reverse("v1:education-place-detail", args=[education.id, place.id])
        response = api_client.delete(url)
        assert response.status_code == self.expected_status_codes["place_delete"]

    def test_list_contacts(self, api_client, education, place):
        url = reverse("v1:education-place-contact-list", args=[education.id, place.id])
        response = api_client.get(url)
        assert response.status_code == self.expected_status_codes["contact_list"]

    def test_create_contact(self, api_client, education, place):
        url = reverse("v1:education-place-contact-list", args=[education.id, place.id])
        data = self._get_contact_create_data(place)
        response = api_client.post(url, data)
        assert response.status_code == self.expected_status_codes["contact_create"]

        if response.status_code == status.CREATED:
            assert response.data["user"]["id"] == data["user_id"]

    def test_update_contact(self, api_client, education, place, contact):
        url = reverse("v1:education-place-contact-detail", args=[education.id, place.id, contact.id])
        data = self._get_contact_update_data(place) | {"place_id": place.id}
        response = api_client.put(url, data)
        assert response.status_code == self.expected_status_codes["contact_update"]

    def test_partial_update_contact(self, api_client, education, place, contact):
        url = reverse("v1:education-place-contact-detail", args=[education.id, place.id, contact.id])
        response = api_client.patch(url, self._get_contact_partial_update_data())
        assert response.status_code == self.expected_status_codes["contact_update"]

    def test_delete_contact(self, api_client, education, place, contact):
        url = reverse("v1:education-place-contact-detail", args=[education.id, place.id, contact.id])
        response = api_client.delete(url)
        assert response.status_code == self.expected_status_codes["contact_delete"]


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
        "contact_list": status.OK,
        "contact_create": status.CREATED,
        "contact_update": status.OK,
        "contact_delete": status.NO_CONTENT,
    }

    @pytest.fixture(autouse=True)
    def setup(self, api_client, office_member):
        api_client.force_authenticate(user=office_member)

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

    def test_delete_used_place(self, api_client, education, place):
        project = education.projects.first()
        project.place_set.add(ProjectPlaceFactory(place=place))
        assert project.places.count() == 1

        url = reverse("v1:education-place-detail", args=[place.id, project.id])
        response = api_client.delete(url)
        assert response.status_code == status.FORBIDDEN
        assert project.places.count() == 1
