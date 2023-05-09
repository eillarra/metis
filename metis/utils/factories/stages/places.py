import factory

from metis.models.stages.project_places import ProjectPlace
from ..education_places import EducationPlaceFactory
from .projects import ProjectFactory


class ProjectPlaceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProjectPlace

    project = factory.SubFactory(ProjectFactory)
    education_place = factory.SubFactory(EducationPlaceFactory)
