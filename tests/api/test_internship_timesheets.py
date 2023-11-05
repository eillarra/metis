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
    UserFactory,
)
from metis.utils.fixtures.programs import create_audiology_program


@pytest.fixture
def education(db):
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
def project_place(db, education):
    return education.projects.first().place_set.first()


@pytest.fixture
def internship(db, education, project_place):
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
def office_member(db, education):
    user = UserFactory.create()
    education.office_members.add(user)
    return user


@pytest.fixture
def office_member_of_other_education(db):
    user = UserFactory.create()
    education2 = EducationFactory.create()
    education2.office_members.add(user)  # type: ignore
    return user


@pytest.fixture
def place_admin(db, internship):
    admin = ContactFactory.create(place=internship.place, is_admin=True)
    return admin.user


@pytest.fixture
def user(db):
    return UserFactory.create()


@pytest.mark.api
class TestForAnonymous:
    expected_status_codes: dict[str, status] = {
        "timesheet_list": status.FORBIDDEN,
        "timesheet_create": status.FORBIDDEN,
        "timesheet_update": status.FORBIDDEN,
        "timesheet_delete": status.FORBIDDEN,
    }

    def test_list_timesheets(self, api_client, education, internship):
        url = reverse("v1:project-internship-timesheet-list", args=[education.id, internship.project_id, internship.id])
        response = api_client.get(url)
        assert response.status_code == self.expected_status_codes["timesheet_list"]

    def test_create_timesheet(self, api_client, education, internship):
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


class TestForAuthenticated(TestForAnonymous):
    @pytest.fixture(autouse=True)
    def setup(self, api_client, user):
        api_client.force_authenticate(user=user)


class TestForMentor(TestForAuthenticated):
    expected_status_codes = {
        "timesheet_list": status.OK,
        "timesheet_create": status.FORBIDDEN,
        "timesheet_update": status.FORBIDDEN,
        "timesheet_delete": status.FORBIDDEN,
    }

    @pytest.fixture(autouse=True)
    def setup(self, api_client, internship):
        api_client.force_authenticate(user=internship.mentors.first().user)


class TestForPlaceAdmin(TestForMentor):
    @pytest.fixture(autouse=True)
    def setup(self, api_client, place_admin):
        api_client.force_authenticate(user=place_admin)


class TestForStudent(TestForAuthenticated):
    expected_status_codes = {
        "timesheet_list": status.OK,
        "timesheet_create": status.CREATED,
        "timesheet_update": status.OK,
        "timesheet_delete": status.NO_CONTENT,
    }

    @pytest.fixture(autouse=True)
    def setup(self, api_client, internship):
        api_client.force_authenticate(user=internship.student.user)


class TestForOtherEducationOfficeMember(TestForAuthenticated):
    @pytest.fixture(autouse=True)
    def setup(self, api_client, office_member_of_other_education):
        api_client.force_authenticate(user=office_member_of_other_education)


class TestForOfficeMember(TestForAuthenticated):
    expected_status_codes = {
        "timesheet_list": status.OK,
        "timesheet_create": status.FORBIDDEN,
        "timesheet_update": status.FORBIDDEN,
        "timesheet_delete": status.FORBIDDEN,
    }

    @pytest.fixture(autouse=True)
    def setup(self, api_client, office_member):
        api_client.force_authenticate(user=office_member)
