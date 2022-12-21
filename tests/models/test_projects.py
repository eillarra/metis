import pytest

from model_bakery import baker


@pytest.mark.django_db
class TestProject:
    @pytest.fixture(autouse=True)
    def setup_data(self) -> None:
        self.open = baker.make_recipe("sparta.project")
        self.closed = baker.make_recipe("sparta.project_closed")
        self.inactive = baker.make_recipe("sparta.project_open_but_inactive")

    def test_str(self):
        assert str(self.open) == self.open.name

    def test_is_open(self):
        assert self.open.is_open is True
        assert self.closed.is_open is False
        assert self.inactive.is_open is False
