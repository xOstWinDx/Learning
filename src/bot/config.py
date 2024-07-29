from pydantic_settings import BaseSettings, SettingsConfigDict


class BotConfig(BaseSettings):
    TOKEN: str
    PREFIX: str = "/"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


BOT_CONFIG = BotConfig()
