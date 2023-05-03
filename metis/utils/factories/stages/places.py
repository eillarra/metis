import factory

from metis.models.stages.places import Place
from ..institutions import InstitutionFactory
from .projects import ProjectFactory


class PlaceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Place

    project = factory.SubFactory(ProjectFactory)
    institution = factory.SubFactory(InstitutionFactory)
