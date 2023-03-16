import pytest

from datetime import date, timedelta

from sparta.factories import TrackFactory, ProgramFactory


@pytest.mark.django_db
@pytest.mark.parametrize(
    "valid_from,valid_until,expected_availability",
    [
        (date.today() - timedelta(days=10), date.today() + timedelta(days=10), True),
        (date.today() - timedelta(days=30), date.today() - timedelta(days=10), False),
    ],
)
def test_track_is_available(valid_from, valid_until, expected_availability):
    program = ProgramFactory(valid_from=valid_from, valid_until=valid_until)
    track = TrackFactory(program=program)

    assert track.is_available == expected_availability
