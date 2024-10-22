import factory


class FileFactory(factory.django.DjangoModelFactory):
    """Factory for File model."""

    class Meta:  # noqa: D106
        model = "metis.File"
