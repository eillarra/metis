import factory

from epione.models.stages.projects import Project
from ..faculties import EducationFactory


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    education = factory.SubFactory(EducationFactory)