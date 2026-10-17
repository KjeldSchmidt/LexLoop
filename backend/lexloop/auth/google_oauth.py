"""Google OAuth client that uses OpenID userinfo (no People API required)."""

from collections.abc import Mapping

from httpx_oauth.clients.google import GoogleOAuth2
from httpx_oauth.exceptions import GetIdEmailError

USERINFO_ENDPOINT = "https://openidconnect.googleapis.com/v1/userinfo"


class GoogleOAuth2UserInfo(GoogleOAuth2):
    """Same as GoogleOAuth2, but resolve id/email via userinfo instead of People API.

    httpx-oauth's default ``get_profile`` calls people.googleapis.com, which
    requires enabling the People API on the GCP project. The OpenID userinfo
    endpoint works with the standard userinfo.email / userinfo.profile scopes.
    """

    async def get_id_email(self, token: str) -> tuple[str, str | None]:
        async with self.get_httpx_client() as client:
            response = await client.get(
                USERINFO_ENDPOINT,
                headers={
                    **self.request_headers,
                    "Authorization": f"Bearer {token}",
                },
            )
            if response.status_code >= 400:
                raise GetIdEmailError(response=response)

            payload: object = response.json()
            if not isinstance(payload, Mapping):
                raise GetIdEmailError(response=response)
            sub = payload.get("sub")
            if not isinstance(sub, str) or not sub:
                raise GetIdEmailError(response=response)
            email = payload.get("email")
            return sub, email if isinstance(email, str) else None
