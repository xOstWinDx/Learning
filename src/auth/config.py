from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthConfig(BaseSettings):
    JWT_ALGORITHM: str
    JWT_SECRET_KEY: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


AUTH_CONFIG = AuthConfig()  # type: ignore
