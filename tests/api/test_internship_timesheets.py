from http import HTTPStatus as status

import pytest
from django.urls import reverse

from metis.utils.factories import ContactFactory, InternshipFactory, MentorFactory, StudentFactory, TimesheetFactory


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
        "timesheet_list": status.FORBIDDEN,
        "timesheet_create": status.FORBIDDEN,
        "timesheet_update": status.FORBIDDEN,
        "timesheet_delete": status.FORBIDDEN,
        "timesheet_approve": status.FORBIDDEN,
    }

    def test_list_timesheets(self, api_client, t_education, internship):  # noqa: D102
        url = reverse(
            "v1:project-internship-timesheet-list", args=[t_education.id, internship.project_id, internship.id]
        )
        response = api_client.get(url)
        assert response.status_code == self.expected_status_codes["timesheet_list"]

    def test_create_timesheet(self, api_client, t_education, internship):  # noqa: D102
        url = reverse(
            "v1:project-internship-timesheet-list", args=[t_education.id, internship.project_id, internship.id]
        )
        response = api_client.post(
            url,
            {
                "date": str(internship.start_date),
                "start_time_am": "8:00",
                "end_time_am": "12:00",
            },
        )
        assert response.status_code == self.expected_status_codes["timesheet_create"]

        if response.status_code == status.CREATED:
            assert response.data["internship"] == internship.id
            assert response.data["date"] == str(internship.start_date)

    def test_approve_timesheets(self, api_client, t_education, internship):  # noqa: D102
        timesheet = TimesheetFactory.create(
            internship=internship, date=internship.start_date, start_time_am="8:00", end_time_am="12:00"
        )
        url = reverse(
            "v1:project-internship-timesheet-approve", args=[t_education.id, internship.project_id, internship.id]
        )
        response = api_client.post(url, {"ids": [timesheet.id], "signed_text": "signature"})
        assert response.status_code == self.expected_status_codes["timesheet_approve"]

        if response.status_code == status.NO_CONTENT:
            assert internship.timesheets.first().signatures.first().signed_text == "signature"


class TestForAuthenticated(TestForAnonymous):
    """Tests for authenticated users."""

    @pytest.fixture(autouse=True)
    def setup(self, api_client, t_random_user):  # noqa: D102
        api_client.force_authenticate(user=t_random_user)


class TestForMentor(TestForAuthenticated):
    """Tests for mentors."""

    expected_status_codes = {
        "timesheet_list": status.OK,
        "timesheet_create": status.FORBIDDEN,
        "timesheet_update": status.FORBIDDEN,
        "timesheet_delete": status.FORBIDDEN,
        "timesheet_approve": status.NO_CONTENT,
    }

    @pytest.fixture(autouse=True)
    def setup(self, api_client, internship):  # noqa: D102
        api_client.force_authenticate(user=internship.mentors.first().user)


class TestForPlaceAdmin(TestForMentor):
    """Tests for place admins."""

    @pytest.fixture(autouse=True)
    def setup(self, api_client, place_admin):  # noqa: D102
        api_client.force_authenticate(user=place_admin)


class TestForStudent(TestForAuthenticated):
    """Tests for students."""

    expected_status_codes = {
        "timesheet_list": status.OK,
        "timesheet_create": status.CREATED,
        "timesheet_update": status.FORBIDDEN,
        "timesheet_update_with_reapproval": status.OK,
        "timesheet_delete": status.NO_CONTENT,
        "timesheet_approve": status.FORBIDDEN,
    }

    @pytest.fixture(autouse=True)
    def setup(self, api_client, internship):  # noqa: D102
        api_client.force_authenticate(user=internship.student.user)

    def _update_approved_timesheet(self, api_client, t_education, internship, data, status_code):
        self.test_create_timesheet(api_client, t_education, internship)
        timesheet = internship.timesheets.first()
        timesheet.is_approved = True
        timesheet.save()

        url = reverse(
            "v1:project-internship-timesheet-detail",
            args=[t_education.id, internship.project_id, internship.id, timesheet.id],
        )
        response = api_client.put(
            url,
            data,
        )
        assert response.status_code == status_code

    def test_update_approved_timesheet(self, api_client, t_education, internship):  # noqa: D102
        self._update_approved_timesheet(
            api_client,
            t_education,
            internship,
            {
                "date": str(internship.start_date),
                "start_time_am": "8:00",
                "end_time_am": "12:00",
                "is_approved": False,
            },
            self.expected_status_codes["timesheet_update"],
        )

    def test_update_approved_timesheet_with_reapproval(self, api_client, t_education, internship):  # noqa: D102
        self._update_approved_timesheet(
            api_client,
            t_education,
            internship,
            {
                "__reapprove": True,
                "date": str(internship.start_date),
                "start_time_am": "8:00",
                "end_time_am": "12:00",
            },
            self.expected_status_codes["timesheet_update_with_reapproval"],
        )


class TestForOtherEducationOfficeMember(TestForAuthenticated):
    """Tests for office members of other educations."""

    @pytest.fixture(autouse=True)
    def setup(self, api_client, t_random_office_member):  # noqa: D102
        api_client.force_authenticate(user=t_random_office_member)


class TestForOfficeMember(TestForAuthenticated):
    """Tests for office members of the internship's education."""

    expected_status_codes = {
        "timesheet_list": status.OK,
        "timesheet_create": status.FORBIDDEN,
        "timesheet_update": status.FORBIDDEN,
        "timesheet_delete": status.FORBIDDEN,
        "timesheet_approve": status.FORBIDDEN,
    }

    @pytest.fixture(autouse=True)
    def setup(self, api_client, t_office_member):  # noqa: D102
        api_client.force_authenticate(user=t_office_member)
