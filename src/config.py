from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str

    TEST_DATABASE_USER: str
    TEST_DATABASE_PASSWORD: str
    TEST_DATABASE_HOST: str
    TEST_DATABASE_PORT: int
    TEST_DATABASE_NAME: str

    DEBUG_MODE: bool = False

    MODE: Literal["TEST", "PROD"] = "PROD"

    @property
    def database_url(self) -> str:
        return (f"postgresql+asyncpg://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}"
                f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}")

    @property
    def test_database_url(self) -> str:
        return (f"postgresql+asyncpg://{self.TEST_DATABASE_USER}:{self.TEST_DATABASE_PASSWORD}"
                f"@{self.TEST_DATABASE_HOST}:{self.TEST_DATABASE_PORT}/{self.TEST_DATABASE_NAME}")

    model_config = SettingsConfigDict(env_file=".env", extra='ignore')


CONFIG = Config()  # type: ignore
