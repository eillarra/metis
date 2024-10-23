from http import HTTPStatus as status

import pytest
from django.urls import reverse

from metis.utils.factories import ContactFactory, UserFactory


@pytest.fixture
def contact(t_place):  # noqa: D103
    return ContactFactory(place=t_place, user=UserFactory(email="initial.email@place.com"))


@pytest.mark.api
@pytest.mark.django_db
class TestForAnonymous:
    """Tests for anonymous users."""

    expected_status_codes: dict[str, status] = {
        "contact_add_email": status.FORBIDDEN,
        "contact_delete_email": status.FORBIDDEN,
        "contact_change_primary_email": status.FORBIDDEN,
    }

    @pytest.mark.parametrize(
        "email,primary",
        [
            ("new.email@place.com", False),
            ("another.new.email@place.com", True),
        ],
    )
    def test_add_email_to_contact(self, api_client, t_education, t_place, contact, email, primary):  # noqa: D102
        url = reverse("v1:education-place-contact-add-email", args=[t_education.id, t_place.id, contact.id])
        response = api_client.post(url, {"email": email, "primary": primary})
        assert response.status_code == self.expected_status_codes["contact_add_email"]

        if response.status_code == status.OK:
            assert len(response.data["email_addresses"]) == 2

            emaildict = {e["email"]: e["primary"] for e in response.data["email_addresses"]}
            assert emaildict["initial.email@place.com"] is not primary
            assert emaildict[email] is primary

    @pytest.mark.parametrize(
        "email",
        [
            "new.email@place.com",
            "another.new.email@place.com",
        ],
    )
    def test_delete_email_from_contact(self, api_client, t_education, t_place, contact, email):  # noqa: D102
        if self.expected_status_codes["contact_delete_email"] == status.NO_CONTENT:
            url = reverse("v1:education-place-contact-add-email", args=[t_education.id, t_place.id, contact.id])
            api_client.post(url, {"email": email, "primary": False})

        url = reverse("v1:education-place-contact-delete-email", args=[t_education.id, t_place.id, contact.id])
        response = api_client.post(url, {"email": email})
        assert response.status_code == self.expected_status_codes["contact_delete_email"]

    @pytest.mark.parametrize(
        "email",
        [
            "new.email@place.com",
            "another.new.email@place.com",
        ],
    )
    def test_change_primary_email(self, api_client, t_education, t_place, contact, email):  # noqa: D102
        if self.expected_status_codes["contact_change_primary_email"] == status.OK:
            url = reverse("v1:education-place-contact-add-email", args=[t_education.id, t_place.id, contact.id])
            api_client.post(url, {"email": email, "primary": False})

        url = reverse("v1:education-place-contact-change-primary-email", args=[t_education.id, t_place.id, contact.id])
        response = api_client.post(url, {"email": email})
        assert response.status_code == self.expected_status_codes["contact_change_primary_email"]

        if response.status_code == status.OK:
            emaildict = {e["email"]: e["primary"] for e in response.data["email_addresses"]}
            assert emaildict[email] is True


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
    """Tests for an office member in t_education."""

    expected_status_codes = {
        "contact_add_email": status.OK,
        "contact_delete_email": status.NO_CONTENT,
        "contact_change_primary_email": status.OK,
    }

    @pytest.fixture(autouse=True)
    def setup(self, api_client, t_office_member):  # noqa: D102
        api_client.force_authenticate(user=t_office_member)

    def test_add_email_from_another_user(self, api_client, t_education, t_place, contact, t_random_user):  # noqa: D102
        url = reverse("v1:education-place-contact-add-email", args=[t_education.id, t_place.id, contact.id])
        response = api_client.post(url, {"email": t_random_user.email})
        assert response.status_code == status.BAD_REQUEST

    @pytest.mark.parametrize("email", ["", "initial.email@place.com"])
    def test_add_email_to_contact_bad_request(self, api_client, t_education, t_place, contact, email):  # noqa: D102
        url = reverse("v1:education-place-contact-add-email", args=[t_education.id, t_place.id, contact.id])
        response = api_client.post(url, {"email": email})
        assert response.status_code == status.BAD_REQUEST

    def test_delete_primary_email(self, api_client, t_education, t_place, contact):  # noqa: D102
        url = reverse("v1:education-place-contact-delete-email", args=[t_education.id, t_place.id, contact.id])
        response = api_client.post(url, {"email": contact.user.email})
        assert response.status_code == status.BAD_REQUEST

    def test_change_inexistent_primary_email(self, api_client, t_education, t_place, contact):  # noqa: D102
        url = reverse("v1:education-place-contact-change-primary-email", args=[t_education.id, t_place.id, contact.id])
        response = api_client.post(url, {"email": "inexistent.email@place.com"})
        assert response.status_code == status.BAD_REQUEST
