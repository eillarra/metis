import pytest

from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from http import HTTPStatus as status

from metis.models.rel import Address
from metis.utils.factories import (
    ContactFactory,
    EducationFactory,
    PlaceFactory,
    ProjectFactory,
    ProjectPlaceFactory,
    UserFactory,
)


@pytest.fixture(autouse=True)
def education(db):
    education = EducationFactory()
    place = PlaceFactory(education=education)
    project = ProjectFactory(education=education)
    ProjectPlaceFactory(place=place, project=project)
    return education


@pytest.fixture
def place(db, education):
    return education.places.first()


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
def office_member2(db, education):
    user = UserFactory()
    education.office_members.add(user)
    return user


@pytest.fixture
def admin_contact(db, place):
    user = UserFactory()
    return ContactFactory(user=user, place=place, is_admin=True)


@pytest.fixture
def user(db):
    return UserFactory()


@pytest.mark.api
class TestForAnonymous:
    expected_status_codes: dict[str, status] = {
        "address_list": status.FORBIDDEN,
        "address_detail": status.FORBIDDEN,
        "address_create": status.FORBIDDEN,
        "address_update": status.FORBIDDEN,
        "address_delete": status.FORBIDDEN,
    }

    def _create_address(self, place):
        return Address.objects.create(content_object=place, **self._get_address_data())

    def _get_address_data(self):
        return {
            "address": "updated address",
            "postcode": "postcode",
            "city": "city",
            "country": "BE",
            "mapbox_feature": {},
        }

    def test_list_addresses(self, api_client, place):
        ct = ContentType.objects.get_for_model(place)
        url = reverse("v1:address-list", args=[ct.id, place.id])
        response = api_client.get(url)
        assert response.status_code == self.expected_status_codes["address_list"]

    def test_create_address_place(self, api_client, place):
        ct = ContentType.objects.get_for_model(place)
        url = reverse("v1:address-list", args=[ct.id, place.id])
        data = self._get_address_data()
        response = api_client.post(url, data)
        assert response.status_code == self.expected_status_codes["address_create"]

        if response.status_code == status.CREATED:
            assert response.data["address"] == data["address"]
            assert place.addresses.count() == 1

    def test_update_address_place(self, api_client, place):
        address = self._create_address(place)
        ct = ContentType.objects.get_for_model(place)
        url = reverse("v1:address-detail", args=[ct.id, place.id, address.id])
        data = self._get_address_data()
        response = api_client.put(url, data)
        assert response.status_code == self.expected_status_codes["address_update"]

    def test_partial_update_address_place(self, api_client, place):
        address = self._create_address(place)
        ct = ContentType.objects.get_for_model(place)
        url = reverse("v1:address-detail", args=[ct.id, place.id, address.id])
        response = api_client.patch(url, {"address": "updated address"})
        assert response.status_code == self.expected_status_codes["address_update"]

    def test_delete_address_place(self, api_client, place):
        address = self._create_address(place)
        ct = ContentType.objects.get_for_model(place)
        url = reverse("v1:address-detail", args=[ct.id, place.id, address.id])
        response = api_client.delete(url)
        assert response.status_code == self.expected_status_codes["address_delete"]


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
    Office members can add addresses to places, places, project_places, students, contacts...
    - users can only uopdate or delete their own addresses.
    """

    created_by = None
    expected_status_codes = {
        "address_list": status.OK,
        "address_detail": status.OK,
        "address_create": status.CREATED,
        "address_update": status.OK,
        "address_delete": status.NO_CONTENT,
    }

    @pytest.fixture(autouse=True)
    def setup(self, api_client, office_member):
        self.created_by = office_member
        api_client.force_authenticate(user=office_member)


class TestForOfficeMemberTwo(TestForOfficeMember):
    @pytest.fixture(autouse=True)
    def setup(self, api_client, office_member, office_member2):
        self.created_by = office_member
        api_client.force_authenticate(user=office_member2)


class TestForAdminContact(TestForOfficeMember):
    @pytest.fixture(autouse=True)
    def setup(self, api_client, admin_contact):
        self.created_by = admin_contact.user
        api_client.force_authenticate(user=admin_contact.user)
