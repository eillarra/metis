import pytest

from model_bakery import baker

from sparta.models import Link


@pytest.mark.django_db
class TestInstitution:
    @pytest.fixture(autouse=True)
    def setup_data(self) -> None:
        self.uz = baker.make_recipe("sparta.uz")

    def test_website(self):
        assert self.uz.website is None
        Link.objects.create(url="https://www.uzgent.be/", type=Link.WEBSITE, content_object=self.uz)
        assert self.uz.website == "https://www.uzgent.be/"
