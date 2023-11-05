from http import HTTPStatus as status

import pytest
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from metis.models.rel import Remark
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

    def test_list_remarks(self, api_client, place):
        ct = ContentType.objects.get_for_model(place)
        url = reverse("v1:remark-list", args=[ct.id, place.id])
        response = api_client.get(url)
        assert response.status_code == self.expected_status_codes["remark_list"]

    def test_create_remark_place(self, api_client, place):
        ct = ContentType.objects.get_for_model(place)
        url = reverse("v1:remark-list", args=[ct.id, place.id])
        data = self._get_remark_create_data()
        response = api_client.post(url, data)
        assert response.status_code == self.expected_status_codes["remark_create"]

        if response.status_code == status.CREATED:
            assert response.data["text"] == data["text"]
            assert place.remarks.count() == 1

    def test_create_remark_project_place(self, api_client, education):
        project_place = education.projects.first().place_set.first()
        ct = ContentType.objects.get_for_model(project_place)
        url = reverse("v1:remark-list", args=[ct.id, project_place.id])
        data = self._get_remark_create_data()
        response = api_client.post(url, data)
        assert response.status_code == self.expected_status_codes["remark_create"]

        if response.status_code == status.CREATED:
            assert response.data["text"] == data["text"]
            assert project_place.remarks.count() == 1


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
    def setup(self, api_client, office_member):
        self.created_by = office_member
        api_client.force_authenticate(user=office_member)

    def _get_remark_create_data(self):
        return {
            "text": "remark text",
        }

    def _get_remark_update_data(self):
        return {
            "text": "updated remark text",
        }

    def test_update_remark(self, api_client, place):
        ct = ContentType.objects.get_for_model(place)
        remark = Remark.objects.create(content_object=place, text="remark text", created_by=self.created_by)
        url = reverse("v1:remark-detail", args=[ct.id, place.id, remark.pk])
        data = self._get_remark_update_data()
        response = api_client.patch(url, data)
        assert response.status_code == self.expected_status_codes["remark_update"]

    def test_delete_remark(self, api_client, place):
        ct = ContentType.objects.get_for_model(place)
        remark = Remark.objects.create(content_object=place, text="remark text", created_by=self.created_by)
        url = reverse("v1:remark-detail", args=[ct.id, place.id, remark.pk])
        data = self._get_remark_update_data()
        response = api_client.delete(url, data)
        assert response.status_code == self.expected_status_codes["remark_delete"]


class TestForOfficeMemberTwo(TestForOfficeMember):
    expected_status_codes = {
        "remark_list": status.OK,
        "remark_detail": status.OK,
        "remark_create": status.CREATED,
        "remark_update": status.FORBIDDEN,
        "remark_delete": status.FORBIDDEN,
    }

    @pytest.fixture(autouse=True)
    def setup(self, api_client, office_member, office_member2):
        self.created_by = office_member
        api_client.force_authenticate(user=office_member2)
