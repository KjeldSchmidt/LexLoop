from pydantic_settings import BaseSettings


class Environment(BaseSettings):  # type: ignore
    SUPABASE_URL: str
    SUPABASE_KEY: str


environment = Environment()
