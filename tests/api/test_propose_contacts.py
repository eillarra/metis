from http import HTTPStatus as status

import pytest
from django.urls import reverse

from metis.models import Internship
from metis.utils.factories import InternshipFactory, StudentFactory


@pytest.fixture
def internship(db, t_project):  # noqa: D103
    student = StudentFactory.create(project=t_project)
    period = t_project.periods.first()
    available_disciplines = period.program_internship.get_available_disciplines()
    internship = InternshipFactory.create(
        project=t_project,
        period=period,
        project_place=None,
        status=Internship.PREPLANNING,
        student=student,
        discipline=available_disciplines.first(),
    )
    return internship


@pytest.fixture
def internship2(db, t_project):  # noqa: D103
    student = StudentFactory.create(project=t_project)
    period = t_project.periods.first()
    available_disciplines = period.program_internship.get_available_disciplines()
    internship = InternshipFactory.create(
        project=t_project,
        period=period,
        project_place=None,
        status=Internship.PREPLANNING,
        student=student,
        discipline=available_disciplines.first(),
    )
    return internship


@pytest.fixture
def other_student(db, t_project):  # noqa: D103
    student = StudentFactory.create(project=t_project)
    return student.user


@pytest.mark.api
class TestForAnonymous:
    """Tests for anonymous users."""

    expected_status_codes: dict[str, status] = {
        "preplanned_internship_list": status.FORBIDDEN,
        "preplanned_internship_create": status.FORBIDDEN,
        "preplanned_internship_create_invalid": status.FORBIDDEN,
    }

    def _get_propose_data(self, internship):
        return {
            "internship_id": internship.id,
            "place_name": "Test place",
            "place_address": "Test address",
            "place_contact_name": "Test contact",
            "place_contact_email": "contact@place.com",
            "place_contact_phone_number": "+32123456789",
        }

    def _get_invalid_data(self, internship):
        return {
            "internship_id": internship.id,
            "place_contact_name": "Test contact",
            "place_contact_email": "contact@place.com",
        }

    def test_preplanned_internship_list(self, api_client):
        """Test proposing an internship place."""
        url = reverse("v1:student-preplanned-internship-list")
        response = api_client.get(url)
        assert response.status_code == self.expected_status_codes["preplanned_internship_list"]

    def test_preplanned_internship_create(self, api_client, internship):
        """Test proposing an internship place."""
        url = reverse("v1:student-preplanned-internship-list")
        data = self._get_propose_data(internship)
        response = api_client.post(url, data)
        assert response.status_code == self.expected_status_codes["preplanned_internship_create"]

        if response.status_code == status.CREATED:
            mentor = internship.mentors.first()
            assert mentor.user.email in data["place_contact_email"]
            assert mentor.user.phone_numbers.first().number in data["place_contact_phone_number"]

    def test_preplanned_internship_create_invalid(self, api_client, internship):
        """Test proposing an internship place."""
        url = reverse("v1:student-preplanned-internship-list")
        response = api_client.post(url, self._get_invalid_data(internship))
        assert response.status_code == self.expected_status_codes["preplanned_internship_create_invalid"]


class TestForAuthenticated(TestForAnonymous):
    """Tests for authenticated users."""

    expected_status_codes: dict[str, status] = {
        "preplanned_internship_list": status.OK,
        "preplanned_internship_create": status.FORBIDDEN,
        "preplanned_internship_create_invalid": status.BAD_REQUEST,
    }

    @pytest.fixture(autouse=True)
    def setup(self, api_client, t_random_user):
        """Log in as user."""
        api_client.force_authenticate(user=t_random_user)


class TestForStudent(TestForAuthenticated):
    """Tests for internship mentors."""

    expected_status_codes = {
        "preplanned_internship_list": status.OK,
        "preplanned_internship_create": status.CREATED,
        "preplanned_internship_create_invalid": status.BAD_REQUEST,
    }

    @pytest.fixture(autouse=True)
    def setup(self, api_client, internship):
        """Log in as student."""
        api_client.force_authenticate(user=internship.student.user)


class TestForOtherStudent(TestForAuthenticated):
    """Tests for internship mentors."""

    @pytest.fixture(autouse=True)
    def setup(self, api_client, internship2):
        """Log in as another student."""
        api_client.force_authenticate(user=internship2.student.user)
