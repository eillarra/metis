import factory

from .stages.projects import ProjectFactory


class EmailLogFactory(factory.django.DjangoModelFactory):
    """Factory for EmailLog model."""

    class Meta:  # noqa: D106
        model = "metis.EmailLog"

    project = factory.SubFactory(ProjectFactory)
