from http import HTTPStatus as status

import pytest
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from metis.models.rel import Address
from metis.utils.factories import ContactFactory


@pytest.fixture
def admin_contact(db, t_place):  # noqa: D103
    return ContactFactory(place=t_place, is_admin=True)


@pytest.mark.api
class TestForAnonymous:
    """Tests for anonymous users."""

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

    def test_list_addresses(self, api_client, t_place):  # noqa: D102
        ct = ContentType.objects.get_for_model(t_place)
        url = reverse("v1:address-list", args=[ct.id, t_place.id])
        response = api_client.get(url)
        assert response.status_code == self.expected_status_codes["address_list"]

    def test_create_address_place(self, api_client, t_place):  # noqa: D102
        ct = ContentType.objects.get_for_model(t_place)
        url = reverse("v1:address-list", args=[ct.id, t_place.id])
        data = self._get_address_data()
        response = api_client.post(url, data)
        assert response.status_code == self.expected_status_codes["address_create"]

        if response.status_code == status.CREATED:
            assert response.data["address"] == data["address"]
            assert t_place.addresses.count() == 1

    def test_update_address_place(self, api_client, t_place):  # noqa: D102
        address = self._create_address(t_place)
        ct = ContentType.objects.get_for_model(t_place)
        url = reverse("v1:address-detail", args=[ct.id, t_place.id, address.id])
        data = self._get_address_data()
        response = api_client.put(url, data)
        assert response.status_code == self.expected_status_codes["address_update"]

    def test_partial_update_address_place(self, api_client, t_place):  # noqa: D102
        address = self._create_address(t_place)
        ct = ContentType.objects.get_for_model(t_place)
        url = reverse("v1:address-detail", args=[ct.id, t_place.id, address.id])
        response = api_client.patch(url, {"address": "updated address"})
        assert response.status_code == self.expected_status_codes["address_update"]

    def test_delete_address_place(self, api_client, t_place):  # noqa: D102
        address = self._create_address(t_place)
        ct = ContentType.objects.get_for_model(t_place)
        url = reverse("v1:address-detail", args=[ct.id, t_place.id, address.id])
        response = api_client.delete(url)
        assert response.status_code == self.expected_status_codes["address_delete"]


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
    def setup(self, api_client, t_office_member):  # noqa: D102
        self.created_by = t_office_member
        api_client.force_authenticate(user=t_office_member)


class TestForOfficeMemberTwo(TestForOfficeMember):
    """Tests for a second office member in t_education."""

    @pytest.fixture(autouse=True)
    def setup(self, api_client, t_office_member, t_second_office_member):  # noqa: D102
        self.created_by = t_office_member
        api_client.force_authenticate(user=t_second_office_member)


class TestForAdminContact(TestForOfficeMember):
    """Tests for an admin contact in t_place."""

    @pytest.fixture(autouse=True)
    def setup(self, api_client, admin_contact):  # noqa: D102
        self.created_by = admin_contact.user
        api_client.force_authenticate(user=admin_contact.user)
