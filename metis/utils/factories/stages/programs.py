import factory
from django.utils import timezone

from metis.models.stages.programs import Program, ProgramBlock, ProgramInternship, Track, TrackInternship

from ..educations import EducationFactory


class ProgramFactory(factory.django.DjangoModelFactory):
    """ºFactory for Program model."""

    class Meta:  # noqa: D106
        model = Program

    education = factory.SubFactory(EducationFactory)
    name = factory.Sequence(lambda n: f"Program {n}")
    valid_from = factory.LazyFunction(lambda: timezone.now().date())
    valid_until = factory.LazyAttribute(lambda o: o.valid_from + timezone.timedelta(days=365))


class ProgramBlockFactory(factory.django.DjangoModelFactory):
    """Factory for ProgramBlock model."""

    class Meta:  # noqa: D106
        model = ProgramBlock

    program = factory.SubFactory(ProgramFactory)
    name = factory.Sequence(lambda n: f"Block {n + 1}")
    position = factory.Sequence(lambda n: n + 1)


class ProgramInternshipFactory(factory.django.DjangoModelFactory):
    """Factory for ProgramInternship model."""

    class Meta:  # noqa: D106
        model = ProgramInternship

    block = factory.SubFactory(ProgramBlockFactory)
    name = factory.Sequence(lambda n: f"Internship {n}")
    position = factory.Sequence(lambda n: n)
    start_week = factory.Sequence(lambda n: n * 4)
    duration = factory.LazyFunction(lambda: timezone.timedelta(weeks=12))


class TrackFactory(factory.django.DjangoModelFactory):
    """Factory for Track model."""

    class Meta:  # noqa: D106
        model = Track

    program = factory.SubFactory(ProgramFactory)
    name = factory.Sequence(lambda n: f"Track {n}")


class TrackInternshipFactory(factory.django.DjangoModelFactory):
    """Factory for TrackInternship model."""

    class Meta:  # noqa: D106
        model = TrackInternship

    track = factory.SubFactory(TrackFactory)
    internship = factory.SubFactory(ProgramInternshipFactory)
    position = factory.Sequence(lambda n: n)
