from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import List

from sqlalchemy.orm import Session

from macro_dashboard.core.models.release_date import ReleaseDate


@dataclass(frozen=True)
class ReleaseDateRepository:
    """
    Repository for reads/writes against release_dates_current and release_dates_history.
    """

    session: Session

    @staticmethod
    def _row_to_release_date(row) -> ReleaseDate:
        raise NotImplementedError

    def upsert_current(self, release_date: ReleaseDate) -> None:
        raise NotImplementedError

    def insert_history(self, release_date: ReleaseDate) -> None:
        raise NotImplementedError

    def get_release_date_current(self, release_id: int) -> ReleaseDate | None:
        raise NotImplementedError

    def get_release_date_history(self, release_id: int) -> List[ReleaseDate]:
        raise NotImplementedError

    def get_release_dates_current_range(
        self,
        start_date: date,
        end_date: date,
    ) -> List[ReleaseDate]:
        raise NotImplementedError