import factory

from metis.models.stages.internships import Internship
from .places import ProjectPlaceFactory
from .projects import ProjectFactory, PeriodFactory
from .students import StudentFactory


class InternshipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Internship

    project = factory.SubFactory(ProjectFactory)
    period = factory.SubFactory(PeriodFactory)
    student = factory.SubFactory(StudentFactory)
    project_place = factory.SubFactory(ProjectPlaceFactory)

    @factory.post_generation
    def validate_and_save(self, create, extracted, **kwargs):
        self.clean()
        self.save()
