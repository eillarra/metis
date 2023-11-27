from allauth.socialaccount.providers.microsoft.provider import MicrosoftGraphProvider


class UgentMicrosoftProvider(MicrosoftGraphProvider):
    """UGent Microsoft provider."""

    id = "ugent"
    name = "UGent"


provider_classes = [UgentMicrosoftProvider]
