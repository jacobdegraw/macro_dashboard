"""
Session management for Postgres.

Defines a transaction-scoped session helper used by repositories,
jobs, and API endpoints.

Design rules:
- One `with` block = one transaction
- Repositories NEVER commit or rollback
- Always close the session to return the connection to the pool
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from sqlalchemy.orm import Session

from macro_dashboard.storage.postgres.db import SessionLocal


@contextmanager
def session_scope(*, commit: bool = True) -> Iterator[Session]:
    """
    Provide a transactional scope around a set of database operations.

    Typical usage:

        from macro_dashboard.storage.postgres.session import session_scope

        with session_scope() as session:
            repo = SeriesRepository(session)
            repo.insert_series(...)

    Behavior:
        - Opens a new session
        - Yields it to the caller
        - On success:
            commit (if commit=True)
        - On failure:
            rollback
        - Always closes the session
    """

    session: Session = SessionLocal()

    try:
        yield session
        

    except Exception:
        session.rollback()
        raise

    else:
        if commit:
            session.commit()

    finally:
        session.close()