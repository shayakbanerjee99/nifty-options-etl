"""Database engine and session factory."""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_engine_and_session(database_url: str):
    engine = create_engine(database_url, future=True)
    return engine, sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
