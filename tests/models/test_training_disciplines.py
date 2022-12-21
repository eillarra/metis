import pytest

from model_bakery import baker


@pytest.mark.django_db
class TestTrainingDiscipline:
    @pytest.fixture(autouse=True)
    def setup_data(self) -> None:
        self.td = baker.make_recipe("sparta.training_discipline1")

    def test_str(self):
        assert str(self.td.discipline) == self.td.discipline.name
        assert str(self.td.group) == self.td.group.name
