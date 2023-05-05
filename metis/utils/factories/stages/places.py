import factory

from metis.models.stages.places import ProjectPlace
from ..places import PlaceFactory
from .projects import ProjectFactory


class ProjectPlaceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProjectPlace

    project = factory.SubFactory(ProjectFactory)
    place = factory.SubFactory(PlaceFactory)
