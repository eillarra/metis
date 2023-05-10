import pytest

from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from http import HTTPStatus as status
from typing import Dict

from metis.models.rel import Remark
from metis.utils.factories import (
    EducationFactory,
    EducationPlaceFactory,
    ProjectFactory,
    ProjectPlaceFactory,
    UserFactory,
)


@pytest.fixture(autouse=True)
def education(db):
    education = EducationFactory()
    education_place = EducationPlaceFactory(education=education)
    project = ProjectFactory(education=education)
    ProjectPlaceFactory(education_place=education_place, project=project)
    return education


@pytest.fixture
def education_place(db, education):
    return education.place_set.first()


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
    expected_status_codes: Dict[str, status] = {
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

    def test_list_remarks(self, api_client, education_place):
        ct = ContentType.objects.get_for_model(education_place)
        url = reverse("v1:remark-list", args=[ct.id, education_place.id])
        response = api_client.get(url)
        assert response.status_code == self.expected_status_codes["remark_list"]

    def test_create_remark_place(self, api_client, education_place):
        ct = ContentType.objects.get_for_model(education_place.place)
        url = reverse("v1:remark-list", args=[ct.id, education_place.place.id])
        data = self._get_remark_create_data()
        response = api_client.post(url, data)
        assert response.status_code == self.expected_status_codes["remark_create"]

        if data:
            assert response.data["text"] == data["text"]
            assert education_place.place.remarks.count() == 1

    def test_create_remark_education_place(self, api_client, education_place):
        ct = ContentType.objects.get_for_model(education_place)
        url = reverse("v1:remark-list", args=[ct.id, education_place.id])
        data = self._get_remark_create_data()
        response = api_client.post(url, data)
        assert response.status_code == self.expected_status_codes["remark_create"]

        if data:
            assert response.data["text"] == data["text"]
            assert education_place.remarks.count() == 1

    def test_create_remark_project_place(self, api_client, education):
        project_place = education.projects.first().place_set.first()
        ct = ContentType.objects.get_for_model(project_place)
        url = reverse("v1:remark-list", args=[ct.id, project_place.id])
        data = self._get_remark_create_data()
        response = api_client.post(url, data)
        assert response.status_code == self.expected_status_codes["remark_create"]

        if data:
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
    Office members can add remarks to places, education_places, project_places, students, contacts...
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

    def test_update_remark(self, api_client, education_place):
        ct = ContentType.objects.get_for_model(education_place)
        remark = Remark.objects.create(content_object=education_place, text="remark text", created_by=self.created_by)
        url = reverse("v1:remark-detail", args=[ct.id, education_place.id, remark.pk])
        data = self._get_remark_update_data()
        response = api_client.patch(url, data)
        assert response.status_code == self.expected_status_codes["remark_update"]

    def test_delete_remark(self, api_client, education_place):
        ct = ContentType.objects.get_for_model(education_place)
        remark = Remark.objects.create(content_object=education_place, text="remark text", created_by=self.created_by)
        url = reverse("v1:remark-detail", args=[ct.id, education_place.id, remark.pk])
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
