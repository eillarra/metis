import pytest

from metis.services.file_guard import check_file_access
from metis.utils.factories import ContactFactory, StudentFactory
from metis.utils.factories.rel import FileFactory


@pytest.fixture
def file_for_all(t_project):  # noqa: D103
    return FileFactory(content_object=t_project, tags=["_visible:place", "_visible:student"])


@pytest.fixture
def file_for_place(t_project):  # noqa: D103
    return FileFactory(content_object=t_project, tags=["_visible:place"])


@pytest.fixture
def file_for_student(t_project):  # noqa: D103
    return FileFactory(content_object=t_project, tags=["_visible:student"])


@pytest.fixture
def place_contact(t_place):  # noqa: D103
    return ContactFactory(place=t_place)


@pytest.fixture
def student(t_project):  # noqa: D103
    return StudentFactory(project=t_project)


@pytest.mark.unit
def test_file_guard_all(file_for_all, t_office_member, place_contact, student):  # noqa: D103
    assert file_for_all.is_visible_for_target_group("place")
    assert file_for_all.is_visible_for_target_group("student")
    assert check_file_access(file_for_all, t_office_member) is True
    assert check_file_access(file_for_all, place_contact.user) is True
    assert check_file_access(file_for_all, student.user) is True


@pytest.mark.unit
def test_file_guard_place(file_for_place, t_office_member, place_contact, student):  # noqa: D103
    assert file_for_place.is_visible_for_target_group("place")
    assert not file_for_place.is_visible_for_target_group("student")
    assert check_file_access(file_for_place, t_office_member) is True
    assert check_file_access(file_for_place, place_contact.user) is True
    assert check_file_access(file_for_place, student.user) is False


@pytest.mark.unit
def test_file_guard_student(file_for_student, t_office_member, place_contact, student):  # noqa: D103
    assert not file_for_student.is_visible_for_target_group("place")
    assert file_for_student.is_visible_for_target_group("student")
    assert check_file_access(file_for_student, t_office_member) is True
    assert check_file_access(file_for_student, place_contact.user) is False
    assert check_file_access(file_for_student, student.user) is True
