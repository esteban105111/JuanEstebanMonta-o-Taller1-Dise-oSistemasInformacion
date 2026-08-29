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

    @field_validator("database_url", mode="before")
    @classmethod
    def normalize_database_url(cls, value: str | None) -> str:
        if value is None or str(value).strip() == "":
            return "postgresql+psycopg://postgres:postgres@localhost:5432/notasya"

        database_url = str(value).strip()
        if database_url.startswith("postgresql://"):
            return database_url.replace("postgresql://", "postgresql+psycopg://", 1)
        return database_url


@lru_cache
def get_settings() -> Settings:
    return Settings()
