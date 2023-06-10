import pytest

from metis.models.rel.invitations import Invitation
from metis.services.inviter import process_student_invitation
from metis.utils.factories import ProjectFactory, UserFactory


@pytest.fixture
def project(db):
    return ProjectFactory()


@pytest.fixture
def user(db):
    return UserFactory()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "data",
    [
        None,
        {"unknown_key": "unknown_value"},
        {"block_id": "a string, but it should be a number"},
    ],
)
def test_invitation_data_is_invalid(data, project, user):
    invitation = Invitation.objects.create(content_object=project, name=user.name, email=user.email, data=data)
    with pytest.raises(ValueError):
        process_student_invitation(invitation, user)
