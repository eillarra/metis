import json
from http import HTTPStatus as status

import pytest
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse


@pytest.mark.api
class TestForAnonymous:
    """Tests for anonymous users."""

    expected_status_codes: dict[str, status] = {
        "upload": status.FORBIDDEN,
    }

    def test_file_upload(self, api_client, t_project) -> None:  # noqa: D102
        ct = ContentType.objects.get_for_model(t_project)
        url = reverse("v1:file-list", args=[ct.id, t_project.id])
        response = api_client.post(
            url,
            {
                "file": SimpleUploadedFile("test.txt", b"file content"),
                "json": json.dumps(
                    {
                        "description": "test description",
                        "tags": ["_visible:place", "_visible:student"],
                    }
                ),
            },
            format="multipart",
        )
        assert response.status_code == self.expected_status_codes["upload"]

        if response.status_code == status.CREATED:
            assert response.data["description"] == "test description"
            assert response.data["tags"] == ["_visible:place", "_visible:student"]


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
        "upload": status.CREATED,
    }

    @pytest.fixture(autouse=True)
    def setup(self, api_client, t_office_member):  # noqa: D102
        api_client.force_authenticate(user=t_office_member)
