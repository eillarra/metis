import pytest

from epione.models import Link, Place
from epione.utils.factories import PlaceFactory


@pytest.fixture
def uz():
    return PlaceFactory(name="UZ", type=Place.HOSPITAL)


@pytest.mark.django_db
def test_place_is_hospital(uz):
    assert uz.is_hospital is True
    assert uz.is_ward is False
    assert uz.is_private is False


@pytest.mark.django_db
def test_place_website(uz):
    assert uz.website is None
    Link.objects.create(url="https://www.uzgent.be/", type=Link.WEBSITE, content_object=uz)
    assert uz.website == "https://www.uzgent.be/"


@pytest.mark.django_db
def test_place_children(uz):
    PlaceFactory(name="Ward 1", parent=uz, type=Place.WARD)
    PlaceFactory(name="Ward 2", parent=uz, type=Place.WARD)
    assert uz.children.count() == 2
