import factory

from metis.models.stages.students import Student

from ..users import UserFactory
from .programs import ProgramBlockFactory
from .projects import ProjectFactory


class StudentFactory(factory.django.DjangoModelFactory):
    """Factory for Student model."""

    class Meta:  # noqa: D106
        model = Student

    project = factory.SubFactory(ProjectFactory)
    user = factory.SubFactory(UserFactory)
    block = factory.SubFactory(ProgramBlockFactory)
