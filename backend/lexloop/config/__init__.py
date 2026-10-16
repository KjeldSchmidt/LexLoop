from dotenv import load_dotenv
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

load_dotenv()


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
