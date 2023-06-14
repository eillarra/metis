import pytest

from django.urls import reverse
from http import HTTPStatus as status

from metis.utils.factories import (
    ContactFactory,
    EducationFactory,
    PeriodFactory,
    PlaceFactory,
    ProjectFactory,
    ProjectPlaceFactory,
    InternshipFactory,
    StudentFactory,
    UserFactory,
)
from metis.utils.fixtures.programs import create_audiology_program


@pytest.fixture
def education(db):
    program = create_audiology_program()
    place = PlaceFactory(education=program.education)
    ContactFactory(place=place)
    project = ProjectFactory(education=program.education)
    ProjectPlaceFactory(place=place, project=project)
    for block in program.blocks.all():
        for program_internship in block.internships.all():
            PeriodFactory(project=project, program_internship=program_internship)
    return program.education


@pytest.fixture
def project_place(db, education):
    return education.projects.first().place_set.first()


@pytest.fixture
def internship(db, education, project_place):
    student = StudentFactory(project=project_place.project)
    period = project_place.project.periods.first()
    available_disciplines = period.program_internship.get_available_disciplines()
    return InternshipFactory(
        project=project_place.project,
        period=period,
        project_place=project_place,
        student=student,
        discipline=available_disciplines.first(),
    )


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
def user(db):
    return UserFactory()


@pytest.mark.api
class TestForAnonymous:
    expected_status_codes: dict[str, status] = {
        "internship_list": status.FORBIDDEN,
        "internship_create": status.FORBIDDEN,
        "internship_update": status.FORBIDDEN,
        "internship_delete": status.FORBIDDEN,
    }

    def _get_internship_create_data(self, internship):
        return {}

    def _get_internship_update_data(self, internship):
        return {}

    def test_list_internships(self, api_client, education, internship):
        url = reverse("v1:project-internship-list", args=[education.id, internship.project_id])
        response = api_client.get(url)
        assert response.status_code == self.expected_status_codes["internship_list"]

    def test_create_internship(self, api_client, education, internship):
        url = reverse("v1:project-internship-list", args=[education.id, internship.project_id])
        data = self._get_internship_create_data(internship)
        response = api_client.post(url, data)
        assert response.status_code == self.expected_status_codes["internship_create"]

        if data:
            assert response.data["student"] == data["student"]

    def test_update_internship(self, api_client, education, internship):
        url = reverse("v1:project-internship-detail", args=[education.id, internship.project_id, internship.id])
        data = self._get_internship_update_data(internship) | {"student_id": internship.student_id}
        response = api_client.put(url, data)
        assert response.status_code == self.expected_status_codes["internship_update"]

    def test_partial_update_internship(self, api_client, education, internship):
        url = reverse("v1:project-internship-detail", args=[education.id, internship.project_id, internship.id])
        response = api_client.patch(url, self._get_internship_update_data(internship))
        assert response.status_code == self.expected_status_codes["internship_update"]

    def test_delete_internship(self, api_client, education, internship):
        url = reverse("v1:project-internship-detail", args=[education.id, internship.project_id, internship.id])
        response = api_client.delete(url)
        assert response.status_code == self.expected_status_codes["internship_delete"]


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
    Office members can manage the EducationPlace and ProjectPlaces.
    Exceptions:
    - education places added to a project (ProjectPlace) cannot be deleted anymore
    """

    expected_status_codes = {
        "internship_list": status.OK,
        "internship_create": status.CREATED,
        "internship_update": status.OK,
        "internship_delete": status.NO_CONTENT,
    }

    @pytest.fixture(autouse=True)
    def setup(self, api_client, office_member):
        api_client.force_authenticate(user=office_member)

    def _get_internship_create_data(self, internship):
        return {
            "student": StudentFactory(project=internship.project).id,  # type: ignore
            "project_place": internship.project_place.id,
            "discipline_id": internship.discipline.id,
        }

    def _get_internship_update_data(self, internship):
        return {
            "student": StudentFactory(project=internship.project).id,  # type: ignore
            "project_place": internship.project_place.id,
            "discipline_id": internship.discipline.id,
        }

    def test_delete_related_place(self, api_client, education, internship):
        """When the place has been used in an internshiop, it cannot be deleted anymore."""
        url = reverse(
            "v1:project-place-detail", args=[education.id, internship.project_id, internship.project_place_id]
        )
        response = api_client.delete(url)
        assert response.status_code == status.FORBIDDEN
