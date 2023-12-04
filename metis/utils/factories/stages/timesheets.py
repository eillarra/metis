import factory


class TimesheetFactory(factory.django.DjangoModelFactory):
    """Factory for Timesheet."""

    class Meta:  # noqa: D106
        model = "metis.Timesheet"
