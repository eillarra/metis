import pytest

from django.utils import timezone

from metis.utils.factories import ProgramFactory


@pytest.mark.django_db
@pytest.mark.parametrize(
    "days_from_now,expected_validity",
    [
        (0, True),  # today
        (-365, True),  # one year ago
        (365, False),  # one year in the future
    ],
)
def test_program_is_valid(days_from_now, expected_validity):
    program = ProgramFactory(valid_from=timezone.now().date() + timezone.timedelta(days=days_from_now))

    assert program.is_valid == expected_validity
