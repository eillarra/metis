import factory


class EvaluationFormFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "metis.EvaluationForm"

    email_subject = factory.Faker("sentence")
    email_body = factory.Faker("text")


class EvaluationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "metis.Evaluation"
