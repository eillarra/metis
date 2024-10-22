from datetime import timedelta

import factory

from metis.models.stages.internships import Internship

from ..users import UserFactory
from .project_places import ProjectPlaceFactory
from .projects import PeriodFactory, ProjectFactory
from .students import StudentFactory


class InternshipFactory(factory.django.DjangoModelFactory):
    """Factory for Internship model."""

    class Meta:  # noqa: D106
        model = Internship

    project = factory.SubFactory(ProjectFactory)
    period = factory.SubFactory(PeriodFactory)
    student = factory.SubFactory(StudentFactory)
    project_place = factory.SubFactory(ProjectPlaceFactory)
    start_date = factory.Faker("date_object")
    end_date = factory.LazyAttribute(lambda o: o.start_date + timedelta(days=20))


class MentorFactory(factory.django.DjangoModelFactory):
    """Factory for Mentor model."""

    class Meta:  # noqa: D106
        model = "metis.Mentor"

    internship = factory.SubFactory(InternshipFactory)
    user = factory.SubFactory(UserFactory)
