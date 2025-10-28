from pydantic_settings import BaseSettings


class Environment(BaseSettings):  # type: ignore
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str  # For RLS-enabled requests
    SUPABASE_SERVICE_ROLE_KEY: str  # For admin/test operations (bypasses RLS)


environment = Environment()
