import datetime
import os
from typing import NamedTuple

import requests
from allauth.socialaccount.models import SocialApp


class GraphToken(NamedTuple):
    """Represents an access token for the Microsoft Graph API.

    Attributes:
        token_type: The type of the access token.
        access_token: The access token string.
        expires_at: The datetime at which the token expires.
    """

    token_type: str
    access_token: str
    expires_at: datetime.datetime

    def has_expired(self) -> bool:
        """Checks if the token has expired.

        Returns:
            A boolean indicating whether the token has expired.
        """
        return self.expires_at < datetime.datetime.now()


class GraphAPI:
    """A class for interacting with the Microsoft Graph API."""

    def __init__(self) -> None:
        try:
            app = SocialApp.objects.get(provider="ugent")
        except SocialApp.DoesNotExist as exc:
            raise RuntimeError("UGent Azure app not configured") from exc

        self.tenant_id: str = os.environ["UGENT_TENANT_ID"]
        self.client_id: str = app.client_id
        self.client_secret: str = app.secret
        self._token: GraphToken | None = None

    def __enter__(self):
        self.session = requests.Session()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()

    def _get_token(self) -> GraphToken:
        """Gets an access token for the Microsoft Graph API.

        Returns:
            A GraphToken object containing the access token and token type.
        """
        if self._token and not self._token.has_expired():
            return self._token

        response = self.session.post(
            f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token",
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "scope": "https://graph.microsoft.com/.default",
            },
        )
        response.raise_for_status()
        response_data = response.json()

        self._token = GraphToken(
            token_type=response_data["token_type"],
            access_token=response_data["access_token"],
            expires_at=datetime.datetime.now() + datetime.timedelta(seconds=response_data["expires_in"] - 60),
        )

        return self._token

    def _get_delegated_token(self):
        raise NotImplementedError

    def find_user_by_email(self, email: str) -> tuple[str | None, bool]:
        """Finds a user in Azure AD by their email address.

        Args:
            email: The email address of the user to find.

        Returns:
            A tuple containing the user's id and status (enabled), or (None, False) if the user was not found.
        """
        token = self._get_token()
        response = self.session.get(
            "https://graph.microsoft.com/v1.0/users",
            headers={"Authorization": f"{token.token_type} {token.access_token}"},
            params={"$filter": f"mail eq '{email}'", "$select": "id,accountEnabled"},
        )
        response.raise_for_status()
        response_data = response.json()

        return (
            (response_data["value"][0]["id"], response_data["value"][0]["accountEnabled"])
            if response_data["value"]
            else (None, False)
        )

    def register_email(self, email: str, *, send_invitation: bool = False) -> tuple[bool, str, bool]:
        """Registers a new email address and (optionally) sends an invitation to join the Metis platform.

        Args:
            email: The email address to register.
            send_invitation: Whether or not to send an invitation email. Defaults to False.

        Returns:
            A tuple containing a bool indicating success or failure, a user id, and account enabled status.
        """
        existing_user_id, enabled = self.find_user_by_email(email)
        if existing_user_id:
            return False, existing_user_id, enabled

        token = self._get_token()
        res = self.session.post(
            "https://graph.microsoft.com/v1.0/invitations",
            headers={"Authorization": f"{token.token_type} {token.access_token}"},
            json={
                "invitedUserEmailAddress": email,
                "inviteRedirectUrl": "https://metis.ugent.be/",
                "sendInvitationMessage": send_invitation,
            },
        )
        res.raise_for_status()

        return True, res.json()["invitedUser"]["id"], True
