from dotenv import load_dotenv
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

load_dotenv()


class EnvSettings(BaseSettings):  # type: ignore[explicit-any]
    DB_URL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


env_settings = EnvSettings.model_validate({})
