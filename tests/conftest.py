import arrow
import pytest
from rest_framework.test import APIClient

from metis.models import Education, Place, Project, ProjectPlace, User
from metis.utils.factories import (
    ContactFactory,
    EducationFactory,
    EvaluationFormFactory,
    InternshipFactory,
    PeriodFactory,
    PlaceFactory,
    ProjectFactory,
    ProjectPlaceFactory,
    StudentFactory,
    UserFactory,
)
from metis.utils.fixtures.forms.evaluations import get_audio_internship_evaluation_form_klinisch
from metis.utils.fixtures.programs import create_audiology_program


@pytest.fixture()
def api_client():
    """Provide a Django REST framework test client instance."""
    return APIClient(enforce_csrf_checks=True)


@pytest.fixture()
def now():
    """Return an Arrow UTC instance."""
    return arrow.utcnow()


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """Create a sample Education instance, with a Project, some Places and Students and office_members."""
    with django_db_blocker.unblock():
        program = create_audiology_program()
        block = program.blocks.first()  # type: ignore
        project = ProjectFactory(education=program.education, program=program)

        EvaluationFormFactory.create(
            project=project,
            has_self_evaluations=True,
            form_definition=get_audio_internship_evaluation_form_klinisch(),
        )

        for block in program.blocks.all():  # type: ignore
            for program_internship in block.internships.all():
                PeriodFactory(project=project, program_internship=program_internship)

        for _ in range(3):
            program.education.office_members.add(UserFactory())  # type: ignore

        for _ in range(3):
            place = PlaceFactory(education=program.education)
            ProjectPlaceFactory(project=project, place=place)
            ContactFactory(place=place)

        for _ in range(10):
            student = StudentFactory(project=project)
            for _ in range(2):
                InternshipFactory(student=student, project=project)

        # create a random user and another education office_member
        UserFactory(id=9999)
        education2 = EducationFactory(id=2000, name="Another education")
        education2.office_members.add(UserFactory(id=999))  # type: ignore


@pytest.fixture(scope="session")
def django_db_modify_db_settings():
    """Modify the database settings. Don't do anything, so xdist reuses database between tests."""
    pass


@pytest.fixture()
def t_education(db) -> Education:
    """Return a sample Education instance, with a Project, some Places and Students and office_members."""
    return Education.objects.get(code="audio")


@pytest.fixture()
def t_second_education(db) -> Education:
    """Return a second sample Education instance."""
    return Education.objects.get(id=2000)


@pytest.fixture()
def t_project(t_education) -> Project:
    """Return a sample Project instance."""
    return t_education.projects.first()


@pytest.fixture()
def t_place(t_education) -> Place:
    """Return a sample Place instance."""
    return t_education.places.first()


@pytest.fixture()
def t_project_place(t_project) -> ProjectPlace:
    """Return a sample ProjectPlace instance."""
    return t_project.place_set.first()


@pytest.fixture()
def t_office_member(t_education) -> User:
    """Return a sample User instance that is an office member for t_education."""
    return t_education.office_members.first()


@pytest.fixture()
def t_second_office_member(t_education) -> User:
    """Return a second sample User instance that is an office member for t_education."""
    return t_education.office_members.last()


@pytest.fixture()
def t_random_user(db) -> User:
    """Return a sample User instance."""
    return User.objects.get(id=9999)


@pytest.fixture()
def t_random_office_member(db) -> User:
    """Return a second sample User instance that is an office member, from another Education."""
    return User.objects.get(id=999)


@pytest.fixture()
def t_contact(t_place) -> User:
    """Return a sample Contact instance."""
    return t_place.contacts.first()
