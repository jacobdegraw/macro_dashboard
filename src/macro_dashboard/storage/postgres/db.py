"""
macro_dashboard.storage.db

SQL-first Postgres connectivity using SQLAlchemy.

This module is intentionally small and boring:
- It creates ONE SQLAlchemy Engine (connection pool) for the whole process.
- It exposes a Session factory (SessionLocal) for transaction-scoped work.
- It does NOT run queries, manage commits/rollbacks, or define repositories.
Those concerns live in session/unit-of-work helpers and repository classes.
"""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from macro_dashboard.core.settings import get_settings


def make_engine() -> Engine:
    """
    Create the SQLAlchemy Engine (connection pool).
    Notes:
    - pool_pre_ping=True helps avoid failures from stale TCP connections.
    - future=True opts into modern SQLAlchemy 2.x behaviors.
    """
    settings = get_settings()

    if not getattr(settings, "postgres_dsn", None):
        raise RuntimeError(
            "Settings.postgres_dsn is missing. "
            "Set it via ENV (e.g. POSTGRES_DSN) or your settings mechanism."
        )

    return create_engine(
        settings.postgres_dsn(),
        pool_pre_ping=True,
        future=True,
        # You can tune pooling later if/when you have concurrency:
        # pool_size=5,
        # max_overflow=10,
        # pool_timeout=30,
    )


# Create one Engine for the entire process (jobs, API, etc.).
engine: Engine = make_engine()

# Session factory for transaction-scoped work (used by session.py / unit-of-work).
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)