import pytest

from django.db.utils import IntegrityError

from metis.models import File
from metis.utils.factories import EducationPlaceFactory


@pytest.fixture
def uz():
    return EducationPlaceFactory(code="UZ")


@pytest.mark.django_db
def test_add_multiple_files_without_code(uz):
    File.objects.create(content_object=uz, description="file1")
    File.objects.create(content_object=uz, description="file2")
    assert uz.files.count() == 2


@pytest.mark.django_db
def test_add_file_with_code(uz):
    """An object can have multiple NULL codes."""
    File.objects.create(content_object=uz, description="file1")
    File.objects.create(content_object=uz, description="file2")
    File.objects.create(content_object=uz, code="agreement", description="agreement1")
    assert uz.files.count() == 3


@pytest.mark.django_db
def test_duplicated_code(uz):
    """Codes cannot be repeated by object."""
    with pytest.raises(IntegrityError):
        File.objects.create(content_object=uz, code="agreement", description="agreement1")
        File.objects.create(content_object=uz, code="agreement", description="agreement2")


@pytest.mark.django_db
def test_education_place_agreement(uz):
    File.objects.create(content_object=uz, code="agreement", description="agreement1")
    assert uz.agreement.id == uz.get_file("agreement").id
