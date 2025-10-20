"""Application configuration settings."""
from __future__ import annotations

from pathlib import Path
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Attributes
    ----------
    database_url:
        SQLAlchemy database URL used to create engine and sessions. Defaults to
        a local SQLite database that lives next to the source tree.
    alembic_ini:
        Path to the Alembic configuration file used by migration commands.
    """

    database_url: str = f"sqlite:///{Path(__file__).resolve().parent.parent / 'app.db'}"
    alembic_ini: str = str(Path(__file__).resolve().parent.parent / "alembic.ini")


settings = Settings()
