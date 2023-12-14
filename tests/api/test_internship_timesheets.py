from http import HTTPStatus as status

import pytest
from django.urls import reverse

from metis.utils.factories import (
    ContactFactory,
    EducationFactory,
    InternshipFactory,
    MentorFactory,
    PeriodFactory,
    PlaceFactory,
    ProjectFactory,
    ProjectPlaceFactory,
    StudentFactory,
    TimesheetFactory,
    UserFactory,
)
from metis.utils.fixtures.programs import create_audiology_program


@pytest.fixture
def education(db):  # noqa: D103
    program = create_audiology_program()
    place = PlaceFactory.create(education=program.education)
    ContactFactory.create(place=place, is_mentor=True)
    project = ProjectFactory.create(education=program.education)
    ProjectPlaceFactory.create(place=place, project=project)
    for block in program.blocks.all():
        for program_internship in block.internships.all():
            PeriodFactory.create(project=project, program_internship=program_internship)
    return program.education


@pytest.fixture
def project_place(db, education):  # noqa: D103
    return education.projects.first().place_set.first()


@pytest.fixture
def internship(db, project_place):  # noqa: D103
    student = StudentFactory.create(project=project_place.project)
    period = project_place.project.periods.first()
    available_disciplines = period.program_internship.get_available_disciplines()
    internship = InternshipFactory.create(
        project=project_place.project,
        period=period,
        project_place=project_place,
        student=student,
        discipline=available_disciplines.first(),
    )
    MentorFactory.create(internship=internship)
    return internship


@pytest.fixture
def office_member(db, education):  # noqa: D103
    user = UserFactory.create()
    education.office_members.add(user)
    return user


@pytest.fixture
def office_member_of_other_education(db):  # noqa: D103
    user = UserFactory.create()
    education2 = EducationFactory.create()
    education2.office_members.add(user)  # type: ignore
    return user


@pytest.fixture
def place_admin(db, internship):  # noqa: D103
    admin = ContactFactory.create(place=internship.place, is_admin=True)
    return admin.user


@pytest.fixture
def user(db):  # noqa: D103
    return UserFactory.create()


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

    def test_list_timesheets(self, api_client, education, internship):
        """Test listing timesheets for an internship."""
        url = reverse("v1:project-internship-timesheet-list", args=[education.id, internship.project_id, internship.id])
        response = api_client.get(url)
        assert response.status_code == self.expected_status_codes["timesheet_list"]

    def test_create_timesheet(self, api_client, education, internship):
        """Test creating a timesheet for an internship."""
        url = reverse("v1:project-internship-timesheet-list", args=[education.id, internship.project_id, internship.id])
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

    def test_approve_timesheets(self, api_client, education, internship):
        """Test approving timesheets for an internship."""
        timesheet = TimesheetFactory.create(
            internship=internship, date=internship.start_date, start_time_am="8:00", end_time_am="12:00"
        )
        url = reverse(
            "v1:project-internship-timesheet-approve", args=[education.id, internship.project_id, internship.id]
        )
        response = api_client.post(url, {"ids": [timesheet.id], "signed_text": "signature"})
        assert response.status_code == self.expected_status_codes["timesheet_approve"]

        if response.status_code == status.NO_CONTENT:
            assert internship.timesheets.first().signatures.first().signed_text == "signature"


class TestForAuthenticated(TestForAnonymous):
    """Tests for authenticated users."""

    @pytest.fixture(autouse=True)
    def setup(self, api_client, user):
        """Log in as user."""
        api_client.force_authenticate(user=user)


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
    def setup(self, api_client, internship):
        """Log in as mentor."""
        api_client.force_authenticate(user=internship.mentors.first().user)


class TestForPlaceAdmin(TestForMentor):
    """Tests for place admins."""

    @pytest.fixture(autouse=True)
    def setup(self, api_client, place_admin):
        """Log in as place admin."""
        api_client.force_authenticate(user=place_admin)


class TestForStudent(TestForAuthenticated):
    """Tests for students."""

    expected_status_codes = {
        "timesheet_list": status.OK,
        "timesheet_create": status.CREATED,
        "timesheet_update": status.OK,
        "timesheet_delete": status.NO_CONTENT,
        "timesheet_approve": status.FORBIDDEN,
    }

    @pytest.fixture(autouse=True)
    def setup(self, api_client, internship):
        """Log in as student."""
        api_client.force_authenticate(user=internship.student.user)

    def test_update_approved_timesheet(self, api_client, education, internship):
        """Test updating an approved timesheet."""
        self.test_create_timesheet(api_client, education, internship)
        timesheet = internship.timesheets.first()
        timesheet.is_approved = True
        timesheet.save()

        url = reverse(
            "v1:project-internship-timesheet-detail",
            args=[education.id, internship.project_id, internship.id, timesheet.id],
        )
        response = api_client.put(
            url,
            {
                "date": str(internship.start_date),
                "start_time_am": "8:00",
                "end_time_am": "12:00",
                "is_approved": False,
            },
        )
        assert response.status_code == status.BAD_REQUEST


class TestForOtherEducationOfficeMember(TestForAuthenticated):
    """Tests for office members of other educations."""

    @pytest.fixture(autouse=True)
    def setup(self, api_client, office_member_of_other_education):
        api_client.force_authenticate(user=office_member_of_other_education)


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
    def setup(self, api_client, office_member):
        """Log in as office member."""
        api_client.force_authenticate(user=office_member)
