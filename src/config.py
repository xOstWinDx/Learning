from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str

    DEBUG_MODE: bool = False

    @property
    def get_database_url(self) -> str:
        return (f"asyncpg://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}"
                f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}")

    model_config = SettingsConfigDict(env_file=".env", extra='ignore')


CONFIG = Config()
