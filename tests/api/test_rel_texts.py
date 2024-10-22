from http import HTTPStatus as status

import pytest
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from metis.models.rel import TextEntry


@pytest.mark.api
class TestForAnonymous:
    """Tests for anonymous users."""

    expected_status_codes: dict[str, status] = {
        "text_list": status.FORBIDDEN,
        "text_detail": status.FORBIDDEN,
        "text_create": status.FORBIDDEN,
        "text_update": status.FORBIDDEN,
        "text_delete": status.FORBIDDEN,
    }

    def _get_text_create_data(self):
        return {}

    def _get_text_update_data(self):
        return {}

    def test_list_texts(self, api_client, t_place):  # noqa: D102
        ct = ContentType.objects.get_for_model(t_place)
        url = reverse("v1:text-list", args=[ct.id, t_place.id])
        response = api_client.get(url)
        assert response.status_code == self.expected_status_codes["text_list"]

    def test_create_text_place(self, api_client, t_place):  # noqa: D102
        ct = ContentType.objects.get_for_model(t_place)
        url = reverse("v1:text-list", args=[ct.id, t_place.id])
        data = self._get_text_create_data()
        response = api_client.post(url, data)
        assert response.status_code == self.expected_status_codes["text_create"]

        if response.status_code == status.CREATED:
            assert response.data["text_nl"] == data["text_nl"]
            assert t_place.texts.count() == 1

    def test_create_text_project(self, api_client, t_project):  # noqa: D102
        ct = ContentType.objects.get_for_model(t_project)
        url = reverse("v1:text-list", args=[ct.id, t_project.id])
        data = self._get_text_create_data()
        response = api_client.post(url, data)
        assert response.status_code == self.expected_status_codes["text_create"]

        if response.status_code == status.CREATED:
            assert response.data["text_nl"] == data["text_nl"]
            assert t_project.texts.count() == 1


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
    """Office members can add texts to places, places, project_places, students, contacts..."""

    created_by = None
    expected_status_codes = {
        "text_list": status.OK,
        "text_detail": status.OK,
        "text_create": status.CREATED,
        "text_update": status.OK,
        "text_delete": status.NO_CONTENT,
    }

    @pytest.fixture(autouse=True)
    def setup(self, api_client, t_office_member):  # noqa: D102
        self.created_by = t_office_member
        api_client.force_authenticate(user=t_office_member)

    def _create_text(self, project):
        return TextEntry.objects.create(
            content_object=project, **self._get_text_create_data(), created_by=self.created_by
        )

    def _get_text_create_data(self):
        return {
            "code": "a.code",
            "title_nl": "NL text title",
            "text_nl": "NL text",
            "title_en": "EN text title",
            "text_en": "EN text",
        }

    def _get_text_update_data(self):
        return {
            "code": "a.code",
            "title_nl": "NL updated title",
            "text_nl": "NL updated",
            "title_en": "EN updated title",
            "text_en": "EN updated",
        }

    def test_update_text(self, api_client, t_project):  # noqa: D102
        ct = ContentType.objects.get_for_model(t_project)
        text = self._create_text(t_project)
        url = reverse("v1:text-detail", args=[ct.id, t_project.id, text.pk])
        data = self._get_text_update_data()
        response = api_client.patch(url, data)
        assert response.status_code == self.expected_status_codes["text_update"]

    def test_delete_text(self, api_client, t_project):  # noqa: D102
        ct = ContentType.objects.get_for_model(t_project)
        text = self._create_text(t_project)
        url = reverse("v1:text-detail", args=[ct.id, t_project.id, text.pk])
        data = self._get_text_update_data()
        response = api_client.delete(url, data)
        assert response.status_code == self.expected_status_codes["text_delete"]


class TestForOfficeMemberTwo(TestForOfficeMember):
    """Tests for a second office member in t_education."""

    @pytest.fixture(autouse=True)
    def setup(self, api_client, t_office_member, t_second_office_member):  # noqa: D102
        self.created_by = t_office_member
        api_client.force_authenticate(user=t_second_office_member)
