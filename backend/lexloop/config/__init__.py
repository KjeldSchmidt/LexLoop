import json
import os
from collections.abc import Mapping

from dotenv import load_dotenv
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

load_dotenv()

# Credentials + public URLs (CloudFront) kept together so deploy can refresh URLs
# without a Terraform cycle on the Lambda env.
_AUTH_SECRET_KEYS = (
    "JWT_SIGNING_SECRET",
    "GOOGLE_OAUTH_CLIENT_ID",
    "GOOGLE_OAUTH_CLIENT_SECRET",
    "FRONTEND_URL",
    "GOOGLE_OAUTH_REDIRECT_URL",
)


def _apply_auth_secrets_from_aws() -> None:
    """Load JWT/OAuth secrets from Secrets Manager when AUTH_SECRETS_ARN is set."""
    arn = os.environ.get("AUTH_SECRETS_ARN")
    if not arn:
        return

    # boto3 is provided by the Lambda runtime; listed under dependency-groups.dev.
    import boto3

    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId=arn)
    raw = response.get("SecretString")
    if not isinstance(raw, str) or not raw:
        raise RuntimeError(f"Auth secret {arn} has no SecretString")

    payload: object = json.loads(raw)
    if not isinstance(payload, Mapping):
        raise RuntimeError(f"Auth secret {arn} must be a JSON object")

    for key in _AUTH_SECRET_KEYS:
        value = payload.get(key)
        if isinstance(value, str) and value:
            os.environ[key] = value


_apply_auth_secrets_from_aws()


class EnvSettings(BaseSettings):  # type: ignore[explicit-any]
    DB_URL: str
    JWT_SIGNING_SECRET: str = "dev-insecure-jwt-secret-change-me"
    RESET_PASSWORD_TOKEN_SECRET: str = "dev-insecure-reset-secret"
    VERIFICATION_TOKEN_SECRET: str = "dev-insecure-verify-secret"
    GOOGLE_OAUTH_CLIENT_ID: str = ""
    GOOGLE_OAUTH_CLIENT_SECRET: str = ""
    # Optional absolute callback URL override (else fastapi-users generates it).
    GOOGLE_OAUTH_REDIRECT_URL: str | None = None
    FRONTEND_URL: str = "http://localhost:5173"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


env_settings = EnvSettings.model_validate({})
