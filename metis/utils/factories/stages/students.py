import factory

from metis.models.stages.students import Student
from ..users import UserFactory
from .programs import ProgramBlockFactory
from .projects import ProjectFactory


class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Student

    project = factory.SubFactory(ProjectFactory)
    user = factory.SubFactory(UserFactory)
    block = factory.SubFactory(ProgramBlockFactory)
