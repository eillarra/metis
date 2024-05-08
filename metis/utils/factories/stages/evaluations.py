import factory


class EvaluationFormFactory(factory.django.DjangoModelFactory):
    """Factory for EvaluationForm."""

    class Meta:  # noqa: D106
        model = "metis.EvaluationForm"


class EvaluationFactory(factory.django.DjangoModelFactory):
    """Factory for Evaluation."""

    class Meta:  # noqa: D106
        model = "metis.Evaluation"
