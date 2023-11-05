import factory

from metis.models.stages.projects import Period, Project

from ..educations import EducationFactory
from .programs import ProgramInternshipFactory


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    education = factory.SubFactory(EducationFactory)
    program = factory.SubFactory("metis.utils.factories.ProgramFactory")


class PeriodFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Period

    project = factory.SubFactory(ProjectFactory)
    program_internship = factory.SubFactory(ProgramInternshipFactory)
    start_date = factory.Faker("date_between", start_date="-1y", end_date="today")
    end_date = factory.Faker("date_between", start_date="today", end_date="+1y")
