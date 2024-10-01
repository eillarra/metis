import arrow
import pytest
from rest_framework.test import APIClient


@pytest.fixture()
def api_client():
    """Provide a Django REST framework test client instance."""
    return APIClient(enforce_csrf_checks=True)


@pytest.fixture()
def now():
    """Return an Arrow UTC instance."""
    return arrow.utcnow()
