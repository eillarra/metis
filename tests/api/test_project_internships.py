from http import HTTPStatus as status

import pytest
from django.urls import reverse

from metis.utils.factories import ContactFactory, InternshipFactory, MentorFactory, StudentFactory


@pytest.fixture
def internship(db, t_project):
    """Return an Internship instance."""
    student = StudentFactory.create(project=t_project)
    period = t_project.periods.first()
    project_place = t_project.place_set.first()
    available_disciplines = period.program_internship.get_available_disciplines()
    internship = InternshipFactory.create(
        project=t_project,
        period=period,
        project_place=project_place,
        student=student,
        discipline=available_disciplines.first(),
    )
    MentorFactory.create(internship=internship)
    return internship


@pytest.fixture
def place_admin(db, internship):
    """Return a User instance that is a place admin."""
    admin = ContactFactory.create(place=internship.place, is_admin=True)
    return admin.user


@pytest.mark.api
class TestForAnonymous:
    """Tests for anonymous users."""

    expected_status_codes: dict[str, status] = {
        "internship_list": status.FORBIDDEN,
        "internship_create": status.FORBIDDEN,
        "internship_update": status.FORBIDDEN,
        "internship_delete": status.FORBIDDEN,
        "internship_create_mentor": status.FORBIDDEN,
        "internship_delete_mentor": status.FORBIDDEN,
    }

    def _get_internship_create_data(self, internship):
        return {}

    def _get_internship_update_data(self, internship):
        return {}

    def _get_mentor_create_data(self, internship):
        return {
            "user_id": internship.place.contacts.filter(is_mentor=True).first().user_id,
        }

    def test_list_internships(self, api_client, t_education, internship):  # noqa: D102
        url = reverse("v1:project-internship-list", args=[t_education.id, internship.project_id])
        response = api_client.get(url)
        assert response.status_code == self.expected_status_codes["internship_list"]

    def test_create_internship(self, api_client, t_education, internship):  # noqa: D102
        url = reverse("v1:project-internship-list", args=[t_education.id, internship.project_id])
        data = self._get_internship_create_data(internship)
        response = api_client.post(url, data)
        assert response.status_code == self.expected_status_codes["internship_create"]

        if response.status_code == status.CREATED:
            assert response.data["student"] == data["student"]

    def test_update_internship(self, api_client, t_education, internship):  # noqa: D102
        url = reverse("v1:project-internship-detail", args=[t_education.id, internship.project_id, internship.id])
        data = self._get_internship_update_data(internship) | {"student_id": internship.student_id}
        response = api_client.put(url, data)
        assert response.status_code == self.expected_status_codes["internship_update"]

    def test_partial_update_internship(self, api_client, t_education, internship):  # noqa: D102
        url = reverse("v1:project-internship-detail", args=[t_education.id, internship.project_id, internship.id])
        response = api_client.patch(url, self._get_internship_update_data(internship))
        assert response.status_code == self.expected_status_codes["internship_update"]

    def test_delete_internship(self, api_client, t_education, internship):  # noqa: D102
        url = reverse("v1:project-internship-detail", args=[t_education.id, internship.project_id, internship.id])
        response = api_client.delete(url)
        assert response.status_code == self.expected_status_codes["internship_delete"]

    def test_create_mentor(self, api_client, t_education, internship):  # noqa: D102
        url = reverse("v1:project-internship-add-mentor", args=[t_education.id, internship.project_id, internship.id])
        data = self._get_mentor_create_data(internship)
        response = api_client.post(url, data)
        assert response.status_code == self.expected_status_codes["internship_create_mentor"]

        if response.status_code == status.CREATED:
            assert response.data["user"]["id"] == data["user_id"]

    def test_delete_mentor(self, api_client, t_education, internship):  # noqa: D102
        url = reverse(
            "v1:project-internship-remove-mentor", args=[t_education.id, internship.project_id, internship.id]
        )
        response = api_client.post(url, {"user_id": internship.mentors.first().user_id})
        assert response.status_code == self.expected_status_codes["internship_delete_mentor"]


class TestForAuthenticated(TestForAnonymous):
    """Tests for authenticated users."""

    @pytest.fixture(autouse=True)
    def setup(self, api_client, t_random_user):  # noqa: D102
        api_client.force_authenticate(user=t_random_user)


class TestForStudent(TestForAuthenticated):
    """Tests for students."""

    @pytest.fixture(autouse=True)
    def setup(self, api_client, internship):  # noqa: D102
        api_client.force_authenticate(user=internship.student.user)


class TestForOtherEducationOfficeMember(TestForAuthenticated):
    """Tests for an office member in another education."""

    @pytest.fixture(autouse=True)
    def setup(self, api_client, t_random_office_member):  # noqa: D102
        api_client.force_authenticate(user=t_random_office_member)


class TestForOfficeMember(TestForAuthenticated):
    """Tests for an office member in t_education."""

    expected_status_codes = {
        "internship_list": status.OK,
        "internship_create": status.CREATED,
        "internship_update": status.OK,
        "internship_delete": status.NO_CONTENT,
        "internship_create_mentor": status.CREATED,
        "internship_delete_mentor": status.NO_CONTENT,
    }

    @pytest.fixture(autouse=True)
    def setup(self, api_client, t_office_member):  # noqa: D102
        api_client.force_authenticate(user=t_office_member)

    def _get_internship_create_data(self, internship):
        period = internship.project.periods.first()

        return {
            "student": StudentFactory.create(project=internship.project).id,
            "project_place": internship.project_place.id,
            "period": period.id,
            "discipline": internship.discipline.id,
            "start_date": period.start_date,
            "end_date": period.end_date,
        }

    def _get_internship_update_data(self, internship):
        period = internship.project.periods.first()

        return {
            "student": StudentFactory.create(project=internship.project).id,
            "project_place": internship.project_place.id,
            "period": period.id,
            "discipline": internship.discipline.id,
            "start_date": period.start_date,
            "end_date": period.end_date,
        }

    def test_delete_related_place(self, api_client, t_education, internship):
        """When the place has been used in an internship, it cannot be deleted anymore."""
        url = reverse(
            "v1:project-place-detail", args=[t_education.id, internship.project_id, internship.project_place_id]
        )
        response = api_client.delete(url)
        assert response.status_code == status.FORBIDDEN


class TestForPlaceAdmin(TestForAuthenticated):
    """Tests for a place admin."""

    expected_status_codes: dict[str, status] = {
        "internship_list": status.FORBIDDEN,
        "internship_create": status.FORBIDDEN,
        "internship_update": status.FORBIDDEN,
        "internship_delete": status.FORBIDDEN,
        "internship_create_mentor": status.CREATED,
        "internship_delete_mentor": status.NO_CONTENT,
    }

    @pytest.fixture(autouse=True)
    def setup(self, api_client, place_admin):  # noqa: D102
        api_client.force_authenticate(user=place_admin)
