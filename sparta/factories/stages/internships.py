import factory

from django.utils import timezone

from sparta.models.stages.internships import Internship
from ..places import PlaceFactory
from ..users import UserFactory


class InternshipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Internship

    user = factory.SubFactory(UserFactory)
    place = factory.SubFactory(PlaceFactory)
