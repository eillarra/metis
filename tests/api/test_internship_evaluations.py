import pytest

from django.urls import reverse
from http import HTTPStatus as status

from metis.utils.factories import (
    ContactFactory,
    EducationFactory,
    EvaluationFormFactory,
    MentorFactory,
    PeriodFactory,
    PlaceFactory,
    ProjectFactory,
    ProjectPlaceFactory,
    InternshipFactory,
    StudentFactory,
    UserFactory,
)
from metis.utils.fixtures.programs import create_audiology_program
from metis.utils.fixtures.forms.evaluations import get_audio_internship_evaluation_form_klinisch


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
    EvaluationFormFactory.create(
        project=project,
        form_definition=get_audio_internship_evaluation_form_klinisch(),
    )
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
        "evaluation_list": status.FORBIDDEN,
        "evaluation_create": status.FORBIDDEN,
        "evaluation_update": status.FORBIDDEN,
        "evaluation_delete": status.FORBIDDEN,
    }

    def _get_evaluation_create_data(self, internship):
        return {}

    def test_list_evaluations(self, api_client, education, internship):
        url = reverse(
            "v1:project-internship-evaluation-list", args=[education.id, internship.project_id, internship.id]
        )
        response = api_client.get(url)
        assert response.status_code == self.expected_status_codes["evaluation_list"]

    def test_create_evaluation(self, api_client, education, internship):
        url = reverse(
            "v1:project-internship-evaluation-list", args=[education.id, internship.project_id, internship.id]
        )
        response = api_client.post(url, self._get_evaluation_create_data(internship))

        if response.status_code == status.BAD_REQUEST:
            assert response.data is True

        assert response.status_code == self.expected_status_codes["evaluation_create"]

        if response.status_code == status.CREATED:
            assert response.data["internship"] == internship.id


class TestForAuthenticated(TestForAnonymous):
    @pytest.fixture(autouse=True)
    def setup(self, api_client, user):
        api_client.force_authenticate(user=user)


class TestForMentor(TestForAuthenticated):
    expected_status_codes = {
        "evaluation_list": status.OK,
        "evaluation_create": status.CREATED,
        "evaluation_update": status.OK,
        "evaluation_delete": status.NO_CONTENT,
    }

    def _get_evaluation_create_data(self, internship):
        form = get_audio_internship_evaluation_form_klinisch()
        data = {
            "grade": 3,
            "sections": {},
        }

        for section in form["sections"]:
            data["sections"][section["code"]] = {
                "grade": 3,
                "grades": {},
                "remarks": "test",
            }

            for item in section["items"]:
                data["sections"][section["code"]]["grades"][item["value"]] = (3, None)

        return {
            "internship_id": internship.id,
            "form": 1,  # TODO: fix this using form_id?
            "data": data,
            "intermediate": 1,
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
        "evaluation_list": status.FORBIDDEN,
        "evaluation_create": status.FORBIDDEN,
        "evaluation_update": status.FORBIDDEN,
        "evaluation_delete": status.FORBIDDEN,
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
        "evaluation_list": status.OK,
        "evaluation_create": status.FORBIDDEN,
        "evaluation_update": status.FORBIDDEN,
        "evaluation_delete": status.FORBIDDEN,
    }

    @pytest.fixture(autouse=True)
    def setup(self, api_client, office_member):
        api_client.force_authenticate(user=office_member)
