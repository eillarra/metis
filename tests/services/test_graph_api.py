import os
from unittest import mock

import responses

from metis.services.graph import GraphAPI


@mock.patch.dict(os.environ, {"UGENT_TENANT_ID": "tenant_id"})
@responses.activate
def test_get_token():
    """Test getting an access token for the Microsoft Graph API."""
    responses.add(
        responses.POST,
        "https://login.microsoftonline.com/tenant_id/oauth2/v2.0/token",
        json={
            "token_type": "Bearer",
            "access_token": "mock_access_token",
            "expires_in": 3600,
        },
        status=200,
    )

    with GraphAPI(client_id="client_id", secret="secret") as api:
        token = api._get_token()

    assert token.token_type == "Bearer"
    assert token.access_token == "mock_access_token"
    assert token.has_expired() is False

    responses.add(
        responses.GET,
        "https://graph.microsoft.com/v1.0/users",
        json={
            "value": [
                {
                    "id": "mock_id",
                    "accountEnabled": True,
                }
            ]
        },
        status=200,
    )

    with GraphAPI(client_id="client_id", secret="secret") as api:
        user_id, status = api.find_user_by_email("mock@emai.l")

    assert user_id == "mock_id"
    assert status is True
