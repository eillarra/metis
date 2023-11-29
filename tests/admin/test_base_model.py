import pytest
from django.contrib.admin.sites import AdminSite
from django.http import HttpRequest

from metis.admin.educations import FacultyAdmin
from metis.models.educations import Faculty
from metis.utils.factories import AdminFactory, FacultyFactory


@pytest.fixture
def admin_user(db):
    """Create a superuser."""
    return AdminFactory()


@pytest.fixture
def faculty_admin():
    """Create a model admin."""
    return FacultyAdmin(model=Faculty, admin_site=AdminSite())


def test_updated_by_user(admin_user, faculty_admin):
    """Test that the updating a model adds the request user."""
    request = HttpRequest()
    request.user = admin_user

    faculty_to_update: Faculty = FacultyFactory.create()
    faculty_admin.save_model(obj=faculty_to_update, request=request, form=None, change=None)
    faculty_to_update.refresh_from_db()
    assert faculty_to_update.updated_by == admin_user


def test_created_by_user(admin_user, faculty_admin):
    """Test that the creating a model adds the request user."""
    request = HttpRequest()
    request.user = admin_user

    faculty_to_create = FacultyFactory.build()
    faculty_admin.save_model(obj=faculty_to_create, request=request, form=None, change=None)
    faculty_to_create.refresh_from_db()
    assert faculty_to_create.created_by == admin_user
    assert faculty_to_create.updated_by == admin_user
