import pytest

from django.urls import reverse
from http import HTTPStatus as status
from typing import Dict

from metis.utils.factories import (
    ContactFactory,
    EducationFactory,
    EducationPlaceFactory,
    PlaceFactory,
    ProjectFactory,
    ProjectPlaceFactory,
    UserFactory,
)


@pytest.fixture
def education(db):
    education = EducationFactory()
    education_place = EducationPlaceFactory(education=education)
    ContactFactory(education_place=education_place)
    ProjectFactory(education=education)
    return education


@pytest.fixture
def education_place(db, education):
    return education.place_set.first()


@pytest.fixture
def contact(db, education_place):
    return education_place.contacts.first()


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
        "places": status.FORBIDDEN,
        "place_create": status.FORBIDDEN,
        "place_update": status.FORBIDDEN,
        "place_delete": status.FORBIDDEN,
        "contacts": status.FORBIDDEN,
        "contact_create": status.FORBIDDEN,
        "contact_update": status.FORBIDDEN,
        "contact_delete": status.FORBIDDEN,
    }

    def _get_place_create_data(self):
        return {}

    def _get_place_update_data(self):
        return {}

    def _get_contact_create_data(self, education_place):
        return {}

    def _get_contact_update_data(self):
        return {}

    def test_places(self, api_client, education):
        url = reverse("v1:education-place-list", args=[education.id])
        response = api_client.get(url)
        assert response.status_code == self.expected_status_codes["places"]

    def test_create_place(self, api_client, education):
        url = reverse("v1:education-place-list", args=[education.id])
        data = self._get_place_create_data()
        response = api_client.post(url, data)
        assert response.status_code == self.expected_status_codes["place_create"]

        if data:
            assert response.data["place"]["id"] == data["place_id"]

    def test_update_place(self, api_client, education, education_place):
        url = reverse("v1:education-place-detail", args=[education.id, education_place.id])
        data = self._get_place_update_data() | {"place_id": education_place.place_id}
        response = api_client.put(url, data)
        assert response.status_code == self.expected_status_codes["place_update"]

    def test_partial_update_place(self, api_client, education, education_place):
        url = reverse("v1:education-place-detail", args=[education.id, education_place.id])
        response = api_client.patch(url, self._get_place_update_data())
        assert response.status_code == self.expected_status_codes["place_update"]

    def test_delete_place(self, api_client, education, education_place):
        url = reverse("v1:education-place-detail", args=[education.id, education_place.id])
        response = api_client.delete(url)
        assert response.status_code == self.expected_status_codes["place_delete"]

    def test_contacts(self, api_client, education, education_place):
        url = reverse("v1:education-place-contact-list", args=[education.id, education_place.id])
        response = api_client.get(url)
        assert response.status_code == self.expected_status_codes["contacts"]

    def test_create_contact(self, api_client, education, education_place):
        url = reverse("v1:education-place-contact-list", args=[education.id, education_place.id])
        data = self._get_contact_create_data(education_place)
        response = api_client.post(url, data)
        assert response.status_code == self.expected_status_codes["contact_create"]

        if data:
            assert response.data["education_place"]["id"] == data["education_place_id"]

    def test_update_contact(self, api_client, education, education_place, contact):
        url = reverse("v1:education-place-contact-detail", args=[education.id, education_place.id, contact.id])
        data = self._get_contact_update_data() | {
            "education_place_id": contact.education_place_id,
            "user_id": contact.user_id,
        }
        response = api_client.put(url, data)
        assert response.status_code == self.expected_status_codes["contact_update"]

    def test_partial_update_contact(self, api_client, education, education_place, contact):
        url = reverse("v1:education-place-contact-detail", args=[education.id, education_place.id, contact.id])
        response = api_client.patch(url, self._get_contact_update_data())
        assert response.status_code == self.expected_status_codes["contact_update"]

    def test_delete_contact(self, api_client, education, education_place, contact):
        url = reverse("v1:education-place-contact-detail", args=[education.id, education_place.id, contact.id])
        response = api_client.delete(url)
        assert response.status_code == self.expected_status_codes["contact_delete"]


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
    Office members can manage the EducationPlace and ProjectPlaces.
    Exceptions:
    - education places added to a project (ProjectPlace) cannot be deleted anymore
    """

    expected_status_codes = {
        "places": status.OK,
        "place_create": status.CREATED,
        "place_update": status.OK,
        "place_delete": status.NO_CONTENT,
        "contacts": status.OK,
        "contact_create": status.CREATED,
        "contact_update": status.OK,
        "contact_delete": status.NO_CONTENT,
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

    def _get_contact_create_data(self, education_place):
        return {
            "education_place_id": education_place.id,
            "user_id": UserFactory().id,  # type: ignore
            "is_staff": True,
        }

    def _get_contact_update_data(self):
        return {
            "is_staff": False,
            "is_mentor": True,
        }

    def test_delete_used_education_place(self, api_client, education, education_place):
        project = education.projects.first()
        project.place_set.add(ProjectPlaceFactory(education_place=education_place))
        assert project.places.count() == 1

        url = reverse("v1:education-place-detail", args=[education_place.id, project.id])
        response = api_client.delete(url)
        assert response.status_code == status.FORBIDDEN
        assert project.places.count() == 1
