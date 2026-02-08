from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    APP_ENV: str = "dev"
    LOG_LEVEL: str = "INFO"
    DATABASE_URL: str


settings = Settings()
