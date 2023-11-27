from allauth.socialaccount.providers.microsoft.views import MicrosoftGraphOAuth2Adapter
from allauth.socialaccount.providers.oauth2.views import OAuth2CallbackView, OAuth2LoginView

from .provider import UgentMicrosoftProvider


class UgentMicrosoftOAuth2Adapter(MicrosoftGraphOAuth2Adapter):
    """UGent Microsoft OAuth2 adapter."""

    provider_id = UgentMicrosoftProvider.id


oauth2_login = OAuth2LoginView.adapter_view(UgentMicrosoftOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(UgentMicrosoftOAuth2Adapter)
