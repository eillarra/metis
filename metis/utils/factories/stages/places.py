import factory

from metis.models.stages.project_places import ProjectPlace

from ..places import PlaceFactory
from .projects import ProjectFactory


class ProjectPlaceFactory(factory.django.DjangoModelFactory):
    """Factory for ProjectPlace model."""

    class Meta:  # noqa: D106
        model = ProjectPlace

    project = factory.SubFactory(ProjectFactory)
    place = factory.SubFactory(PlaceFactory)
