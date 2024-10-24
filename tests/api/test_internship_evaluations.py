from http import HTTPStatus as status

import pytest
from django.urls import reverse

from metis.utils.factories import ContactFactory, InternshipFactory, MentorFactory, StudentFactory
from metis.utils.fixtures.forms.evaluations import get_audio_internship_evaluation_form_klinisch


@pytest.fixture
def internship(db, t_project):  # noqa: D103
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
def place_admin(db, internship):  # noqa: D103
    admin = ContactFactory.create(place=internship.place, is_admin=True)
    return admin.user


@pytest.mark.api
class TestForAnonymous:
    """Tests for anonymous users."""

    expected_status_codes: dict[str, status] = {
        "evaluation_list": status.FORBIDDEN,
        "evaluation_create": status.FORBIDDEN,
        "evaluation_create_self": status.FORBIDDEN,
        "evaluation_update": status.FORBIDDEN,
        "evaluation_update_self": status.FORBIDDEN,
        "evaluation_delete": status.FORBIDDEN,
        "evaluation_approve": status.FORBIDDEN,
        "evaluation_approve_self": status.FORBIDDEN,
    }

    def _get_evaluation_create_data(self, internship, is_self_evaluation):
        return {}

    def test_list_evaluations(self, api_client, t_education, internship):  # noqa: D102
        url = reverse(
            "v1:project-internship-evaluation-list", args=[t_education.id, internship.project_id, internship.id]
        )
        response = api_client.get(url)
        assert response.status_code == self.expected_status_codes["evaluation_list"]

    def test_create_evaluation(self, api_client, t_education, internship, is_self_evaluation=False):  # noqa: D102
        url = reverse(
            "v1:project-internship-evaluation-list", args=[t_education.id, internship.project_id, internship.id]
        )
        response = api_client.post(url, self._get_evaluation_create_data(internship, is_self_evaluation))

        if response.status_code == status.BAD_REQUEST:
            assert response.data is True

        assert (
            response.status_code == self.expected_status_codes["evaluation_create_self"]
            if is_self_evaluation
            else self.expected_status_codes["evaluation_create"]
        )

        if response.status_code == status.CREATED:
            assert response.data["internship"] == internship.id  # type: ignore

    def test_create_self_evaluation(self, api_client, t_education, internship):  # noqa: D102
        self.test_create_evaluation(api_client, t_education, internship, is_self_evaluation=True)

    def test_approve_evaluation(self, api_client, t_education, internship):  # noqa: D102
        url = reverse(
            "v1:project-internship-evaluation-approve",
            args=[t_education.id, internship.project_id, internship.id, 1],
        )
        response = api_client.post(url, {"signed_text": "signature"})
        assert response.status_code == self.expected_status_codes["evaluation_approve"]


class TestForAuthenticated(TestForAnonymous):
    """Tests for authenticated users."""

    @pytest.fixture(autouse=True)
    def setup(self, api_client, t_random_user):  # noqa: D102
        api_client.force_authenticate(user=t_random_user)


class TestForMentorOrStudent(TestForAuthenticated):
    """Tests for internship mentors or students."""

    def _get_evaluation_create_data(self, internship, is_self_evaluation):
        form = get_audio_internship_evaluation_form_klinisch()
        data = {
            "global_score": "zg",
            "global_remarks": "global remarks",
            "sections": {},
        }

        for section in form["sections"]:
            data["sections"][section["code"]] = {
                "score": "zg",
                "scores": {},
                "remarks": "test",
            }

            for item in section["items"]:
                data["sections"][section["code"]]["scores"][item["value"]] = ("zg", None)

        return {
            "internship_id": internship.id,
            "form": 1,  # TODO: fix this using form_id?
            "data": data,
            "intermediate": 1,
            "is_self_evaluation": is_self_evaluation,
        }

    def _approve_evaluation(self, api_client, t_education, internship, is_self_evaluation=False):  # noqa: D102
        self.test_create_evaluation(api_client, t_education, internship, is_self_evaluation)
        evaluation = internship.evaluations.first()
        url = reverse(
            "v1:project-internship-evaluation-approve", args=[t_education.id, internship.project_id, internship.id, 1]
        )
        response = api_client.post(url, {"signed_text": "signature"})

        assert (
            response.status_code == self.expected_status_codes["evaluation_approve_self"]
            if is_self_evaluation
            else self.expected_status_codes["evaluation_approve"]
        )

        if response.status_code == status.NO_CONTENT:
            assert evaluation.signatures.first().signed_text == "signature"


class TestForMentor(TestForMentorOrStudent):
    """Tests for internship mentors."""

    expected_status_codes = {
        "evaluation_list": status.OK,
        "evaluation_create": status.CREATED,
        "evaluation_create_self": status.FORBIDDEN,
        "evaluation_update": status.OK,
        "evaluation_update_self": status.FORBIDDEN,
        "evaluation_delete": status.NO_CONTENT,
        "evaluation_approve": status.NO_CONTENT,
        "evaluation_approve_self": status.FORBIDDEN,
    }

    @pytest.fixture(autouse=True)
    def setup(self, api_client, internship):  # noqa: D102
        api_client.force_authenticate(user=internship.mentors.first().user)

    def test_approve_evaluation(self, api_client, t_education, internship):  # noqa: D102
        return super()._approve_evaluation(api_client, t_education, internship)

    def test_update_approved_evaluation(self, api_client, t_education, internship):  # noqa: D102
        self.test_create_evaluation(api_client, t_education, internship)
        evaluation = internship.evaluations.first()
        evaluation.is_approved = True
        evaluation.save()

        url = reverse(
            "v1:project-internship-evaluation-detail",
            args=[t_education.id, internship.project_id, internship.id, evaluation.id],
        )
        response = api_client.put(url, self._get_evaluation_create_data(internship, is_self_evaluation=False))
        assert response.status_code == status.BAD_REQUEST


class TestForPlaceAdmin(TestForMentor):
    """Tests for internship place admins."""

    @pytest.fixture(autouse=True)
    def setup(self, api_client, place_admin):  # noqa: D102
        api_client.force_authenticate(user=place_admin)


class TestForStudent(TestForMentorOrStudent):
    """Tests for internship students."""

    expected_status_codes = {
        "evaluation_list": status.OK,
        "evaluation_create": status.FORBIDDEN,
        "evaluation_create_self": status.CREATED,
        "evaluation_update": status.FORBIDDEN,
        "evaluation_update_self": status.OK,
        "evaluation_delete": status.FORBIDDEN,
        "evaluation_approve": status.FORBIDDEN,
        "evaluation_approve_self": status.NO_CONTENT,
    }

    @pytest.fixture(autouse=True)
    def setup(self, api_client, internship):  # noqa: D102
        api_client.force_authenticate(user=internship.student.user)

    def test_approve_evaluation(self, api_client, t_education, internship):  # noqa: D102
        self._approve_evaluation(api_client, t_education, internship, is_self_evaluation=True)


class TestForOtherEducationOfficeMember(TestForAuthenticated):
    """Tests for office members of other educations."""

    @pytest.fixture(autouse=True)
    def setup(self, api_client, t_random_office_member):  # noqa: D102
        api_client.force_authenticate(user=t_random_office_member)


class TestForOfficeMember(TestForAuthenticated):
    """Tests for office members of the internship's education."""

    expected_status_codes = {
        "evaluation_list": status.OK,
        "evaluation_create": status.FORBIDDEN,
        "evaluation_create_self": status.FORBIDDEN,
        "evaluation_update": status.FORBIDDEN,
        "evaluation_update_self": status.FORBIDDEN,
        "evaluation_delete": status.FORBIDDEN,
        "evaluation_approve": status.FORBIDDEN,
        "evaluation_approve_self": status.FORBIDDEN,
    }

    @pytest.fixture(autouse=True)
    def setup(self, api_client, t_office_member):  # noqa: D102
        api_client.force_authenticate(user=t_office_member)
