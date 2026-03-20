from __future__ import annotations

from dataclasses import dataclass
from typing import List

from sqlalchemy.orm import Session

from macro_dashboard.core.models.release import Release


@dataclass(frozen=True)
class ReleaseRepository:
    """
    Repository for reads/writes against releases_current and releases_history.
    """

    session: Session

    @staticmethod
    def _row_to_release(row) -> Release:
        raise NotImplementedError

    def upsert_current(self, release: Release) -> None:
        raise NotImplementedError

    def insert_history(self, release: Release) -> None:
        raise NotImplementedError

    def get_release_current(self, release_id: int) -> Release | None:
        raise NotImplementedError

    def get_release_history(self, release_id: int) -> List[Release]:
        raise NotImplementedError

    def get_all_current(self) -> List[Release]:
        raise NotImplementedError