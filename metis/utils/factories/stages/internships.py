import factory

from metis.models.stages.internships import Internship
from .places import ProjectPlaceFactory
from .programs import ProgramInternshipFactory
from .students import StudentFactory


class InternshipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Internship

    program_internship = factory.SubFactory(ProgramInternshipFactory)
    student = factory.SubFactory(StudentFactory)
    project_place = factory.SubFactory(ProjectPlaceFactory)
    custom_start_date = factory.Faker("date_between", start_date="-1y", end_date="today")
    custom_end_date = factory.Faker("date_between", start_date="today", end_date="+1y")

    @factory.post_generation
    def validate_and_save(self, create, extracted, **kwargs):
        self.clean()
        self.save()
