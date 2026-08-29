from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config.settings import get_settings


class Base(DeclarativeBase):
    pass


class DatabaseConnection:
    _instance: "DatabaseConnection | None" = None

    def __new__(cls) -> "DatabaseConnection":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            settings = get_settings()
            cls._instance.engine = create_engine(settings.database_url, pool_pre_ping=True)
            cls._instance.session_factory = sessionmaker(
                bind=cls._instance.engine,
                autoflush=False,
                autocommit=False,
                expire_on_commit=False,
            )
        return cls._instance


def get_db() -> Generator[Session, None, None]:
    db = DatabaseConnection().session_factory()
    try:
        yield db
    finally:
        db.close()

