import factory

from metis.models.stages.projects import Project
from ..educations import EducationFactory


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    education = factory.SubFactory(EducationFactory)
