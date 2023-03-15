import factory


class ProgramFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "sparta.Program"
