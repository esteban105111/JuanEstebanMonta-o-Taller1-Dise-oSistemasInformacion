from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "NOTASYA API"
    app_env: str = "development"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/notasya"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @field_validator("app_name", mode="before")
    @classmethod
    def default_app_name_when_empty(cls, value: str | None) -> str:
        if value is None or str(value).strip() == "":
            return "NOTASYA API"
        return str(value)

    @field_validator("app_env", mode="before")
    @classmethod
    def default_app_env_when_empty(cls, value: str | None) -> str:
        if value is None or str(value).strip() == "":
            return "development"
        return str(value)


@lru_cache
def get_settings() -> Settings:
    return Settings()
