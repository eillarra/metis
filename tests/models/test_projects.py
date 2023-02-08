import pytest

from model_bakery import baker


@pytest.mark.django_db
class TestProject:
    @pytest.fixture(autouse=True)
    def setup_data(self) -> None:
        self.open = baker.make_recipe("sparta.project_1")
        baker.make_recipe("sparta.period_1", project=self.open)
        self.inactive = baker.make_recipe("sparta.project_1_inactive")
        baker.make_recipe("sparta.period_1", project=self.inactive)

    def test_str(self):
        assert str(self.open) == self.open.name

    def test_is_open(self):
        assert self.open.is_open is True
        assert self.inactive.is_open is False
