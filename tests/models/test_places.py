import pytest

from metis.models import Link
from metis.utils.factories import PlaceFactory, PlaceTypeFactory


@pytest.fixture
def place_type():
    return PlaceTypeFactory(name="Hospital")


@pytest.fixture
def uz(place_type):
    return PlaceFactory(name="UZ", type=place_type, education=place_type.education)


@pytest.mark.django_db
def test_institution_website(uz):
    assert uz.website is None
    Link.objects.create(url="https://www.uzgent.be/", type=Link.WEBSITE, content_object=uz)
    assert uz.website == "https://www.uzgent.be/"


@pytest.mark.django_db
def test_institution_children(uz, place_type):
    PlaceFactory(name="Ward 1", parent=uz, type=place_type, education=place_type.education)
    PlaceFactory(name="Ward 2", parent=uz, type=place_type, education=place_type.education)
    assert uz.children.count() == 2
