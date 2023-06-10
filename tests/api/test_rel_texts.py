import pytest

from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from http import HTTPStatus as status

from metis.models.rel import TextEntry
from metis.utils.factories import (
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
def project(db, education):
    return education.projects.first()


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
def user(db):
    return UserFactory()


@pytest.mark.api
class TestForAnonymous:
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

    def test_list_texts(self, api_client, place):
        ct = ContentType.objects.get_for_model(place)
        url = reverse("v1:text-list", args=[ct.id, place.id])
        response = api_client.get(url)
        assert response.status_code == self.expected_status_codes["text_list"]

    def test_create_text_place(self, api_client, place):
        ct = ContentType.objects.get_for_model(place)
        url = reverse("v1:text-list", args=[ct.id, place.id])
        data = self._get_text_create_data()
        response = api_client.post(url, data)
        assert response.status_code == self.expected_status_codes["text_create"]

        if data:
            assert response.data["text_nl"] == data["text_nl"]
            assert place.texts.count() == 1

    def test_create_text_project(self, api_client, project):
        ct = ContentType.objects.get_for_model(project)
        url = reverse("v1:text-list", args=[ct.id, project.id])
        data = self._get_text_create_data()
        response = api_client.post(url, data)
        assert response.status_code == self.expected_status_codes["text_create"]

        if data:
            assert response.data["text_nl"] == data["text_nl"]
            assert project.texts.count() == 1


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
    Office members can add texts to places, places, project_places, students, contacts...
    """

    created_by = None
    expected_status_codes = {
        "text_list": status.OK,
        "text_detail": status.OK,
        "text_create": status.CREATED,
        "text_update": status.OK,
        "text_delete": status.NO_CONTENT,
    }

    @pytest.fixture(autouse=True)
    def setup(self, api_client, office_member):
        self.created_by = office_member
        api_client.force_authenticate(user=office_member)

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

    def test_update_text(self, api_client, project):
        ct = ContentType.objects.get_for_model(project)
        text = self._create_text(project)
        url = reverse("v1:text-detail", args=[ct.id, project.id, text.pk])
        data = self._get_text_update_data()
        response = api_client.patch(url, data)
        assert response.status_code == self.expected_status_codes["text_update"]

    def test_delete_text(self, api_client, project):
        ct = ContentType.objects.get_for_model(project)
        text = self._create_text(project)
        url = reverse("v1:text-detail", args=[ct.id, project.id, text.pk])
        data = self._get_text_update_data()
        response = api_client.delete(url, data)
        assert response.status_code == self.expected_status_codes["text_delete"]


class TestForOfficeMemberTwo(TestForOfficeMember):
    """
    Second office member can also update and delete texts, even if they are not the creator.
    """

    @pytest.fixture(autouse=True)
    def setup(self, api_client, office_member, office_member2):
        self.created_by = office_member
        api_client.force_authenticate(user=office_member2)
