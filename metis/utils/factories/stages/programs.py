import factory

from django.utils import timezone

from metis.models.stages.programs import Program, ProgramBlock, ProgramInternship, Track, TrackInternship
from ..educations import EducationFactory


class DisciplineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "metis.Discipline"

    education = factory.SubFactory(EducationFactory)
    name = factory.Sequence(lambda n: f"Discipline {n}")


class ProgramFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Program

    education = factory.SubFactory(EducationFactory)
    name = factory.Sequence(lambda n: f"Program {n}")
    valid_from = factory.LazyFunction(lambda: timezone.now().date())
    valid_until = factory.LazyAttribute(lambda o: o.valid_from + timezone.timedelta(days=365))


class ProgramBlockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProgramBlock

    program = factory.SubFactory(ProgramFactory)
    name = factory.Sequence(lambda n: f"Block {n}")
    position = factory.Sequence(lambda n: n)


class ProgramInternshipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProgramInternship

    block = factory.SubFactory(ProgramBlockFactory)
    name = factory.Sequence(lambda n: f"Internship {n}")
    position = factory.Sequence(lambda n: n)
    start_week = factory.Sequence(lambda n: n * 4)
    duration = factory.LazyFunction(lambda: timezone.timedelta(weeks=12))
    required_discipline = factory.SubFactory(DisciplineFactory)


class TrackFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Track

    program = factory.SubFactory(ProgramFactory)
    name = factory.Sequence(lambda n: f"Track {n}")


class TrackInternshipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TrackInternship

    track = factory.SubFactory(TrackFactory)
    internship = factory.SubFactory(ProgramInternshipFactory)
    position = factory.Sequence(lambda n: n)
