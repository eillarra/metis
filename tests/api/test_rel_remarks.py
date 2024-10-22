from http import HTTPStatus as status

import pytest
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from metis.models.rel import Remark


@pytest.mark.api
class TestForAnonymous:
    """Tests for anonymous users."""

    expected_status_codes: dict[str, status] = {
        "remark_list": status.FORBIDDEN,
        "remark_detail": status.FORBIDDEN,
        "remark_create": status.FORBIDDEN,
        "remark_update": status.FORBIDDEN,
        "remark_delete": status.FORBIDDEN,
    }

    def _get_remark_create_data(self):
        return {}

    def _get_remark_update_data(self):
        return {}

    def test_list_remarks(self, api_client, t_place):  # noqa: D102
        ct = ContentType.objects.get_for_model(t_place)
        url = reverse("v1:remark-list", args=[ct.id, t_place.id])
        response = api_client.get(url)
        assert response.status_code == self.expected_status_codes["remark_list"]

    def test_create_remark_place(self, api_client, t_place):  # noqa: D102
        ct = ContentType.objects.get_for_model(t_place)
        url = reverse("v1:remark-list", args=[ct.id, t_place.id])
        data = self._get_remark_create_data()
        response = api_client.post(url, data)
        assert response.status_code == self.expected_status_codes["remark_create"]

        if response.status_code == status.CREATED:
            assert response.data["text"] == data["text"]
            assert t_place.remarks.count() == 1

    def test_create_remark_project_place(self, api_client, t_education):  # noqa: D102
        project_place = t_education.projects.first().place_set.first()
        ct = ContentType.objects.get_for_model(project_place)
        url = reverse("v1:remark-list", args=[ct.id, project_place.id])
        data = self._get_remark_create_data()
        response = api_client.post(url, data)
        assert response.status_code == self.expected_status_codes["remark_create"]

        if response.status_code == status.CREATED:
            assert response.data["text"] == data["text"]
            assert project_place.remarks.count() == 1


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

    Office members can add remarks to places, places, project_places, students, contacts...

    - users can only uopdate or delete their own remarks.
    """

    created_by = None
    expected_status_codes = {
        "remark_list": status.OK,
        "remark_detail": status.OK,
        "remark_create": status.CREATED,
        "remark_update": status.OK,
        "remark_delete": status.NO_CONTENT,
    }

    @pytest.fixture(autouse=True)
    def setup(self, api_client, t_office_member):  # noqa: D102
        self.created_by = t_office_member
        api_client.force_authenticate(user=t_office_member)

    def _get_remark_create_data(self):
        return {
            "text": "remark text",
        }

    def _get_remark_update_data(self):
        return {
            "text": "updated remark text",
        }

    def test_update_remark(self, api_client, t_place):  # noqa: D102
        ct = ContentType.objects.get_for_model(t_place)
        remark = Remark.objects.create(content_object=t_place, text="remark text", created_by=self.created_by)
        url = reverse("v1:remark-detail", args=[ct.id, t_place.id, remark.pk])
        data = self._get_remark_update_data()
        response = api_client.patch(url, data)
        assert response.status_code == self.expected_status_codes["remark_update"]

    def test_delete_remark(self, api_client, t_place):  # noqa: D102
        ct = ContentType.objects.get_for_model(t_place)
        remark = Remark.objects.create(content_object=t_place, text="remark text", created_by=self.created_by)
        url = reverse("v1:remark-detail", args=[ct.id, t_place.id, remark.pk])
        data = self._get_remark_update_data()
        response = api_client.delete(url, data)
        assert response.status_code == self.expected_status_codes["remark_delete"]


class TestForOfficeMemberTwo(TestForOfficeMember):
    """Tests for a second office member in t_education."""

    expected_status_codes = {
        "remark_list": status.OK,
        "remark_detail": status.OK,
        "remark_create": status.CREATED,
        "remark_update": status.FORBIDDEN,
        "remark_delete": status.FORBIDDEN,
    }

    @pytest.fixture(autouse=True)
    def setup(self, api_client, t_office_member, t_second_office_member):  # noqa: D102
        self.created_by = t_office_member
        api_client.force_authenticate(user=t_second_office_member)
