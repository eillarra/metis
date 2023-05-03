import pytest

from metis.models import Link, Institution
from metis.utils.factories import InstitutionFactory


@pytest.fixture
def uz():
    return InstitutionFactory(name="UZ", type=Institution.HOSPITAL)


@pytest.mark.django_db
def test_institution_is_hospital(uz):
    assert uz.is_hospital is True
    assert uz.is_ward is False
    assert uz.is_private is False


@pytest.mark.django_db
def test_institution_website(uz):
    assert uz.website is None
    Link.objects.create(url="https://www.uzgent.be/", type=Link.WEBSITE, content_object=uz)
    assert uz.website == "https://www.uzgent.be/"


@pytest.mark.django_db
def test_institution_children(uz):
    InstitutionFactory(name="Ward 1", parent=uz, type=Institution.WARD)
    InstitutionFactory(name="Ward 2", parent=uz, type=Institution.WARD)
    assert uz.children.count() == 2
