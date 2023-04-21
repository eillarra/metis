import factory

from metis.models.stages.internships import Internship
from ..places import PlaceFactory
from ..users import UserFactory
from .projects import ProjectFactory


class InternshipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Internship

    project = factory.SubFactory(ProjectFactory)
    student = factory.SubFactory(UserFactory)
    place = factory.SubFactory(PlaceFactory)
    custom_start_date = factory.Faker("date_between", start_date="-1y", end_date="today")
    custom_end_date = factory.Faker("date_between", start_date="today", end_date="+1y")

    @factory.post_generation
    def validate_and_save(self, create, extracted, **kwargs):
        self.clean()
        self.save()
