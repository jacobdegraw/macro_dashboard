from __future__ import annotations

from dataclasses import dataclass
from typing import List

from sqlalchemy.orm import Session

from macro_dashboard.core.models.series_release import SeriesRelease


@dataclass(frozen=True)
class SeriesReleaseRepository:
    """
    Repository for reads/writes against series_releases_current and series_releases_history.
    """

    session: Session

    @staticmethod
    def _row_to_series_release(row) -> SeriesRelease:
        raise NotImplementedError

    def upsert_current(self, series_release: SeriesRelease) -> None:
        raise NotImplementedError

    def upsert_current_many(self, series_releases: List[SeriesRelease]) -> None:
        raise NotImplementedError

    def insert_history(self, series_release: SeriesRelease) -> None:
        raise NotImplementedError

    def insert_history_many(self, series_releases: List[SeriesRelease]) -> None:
        raise NotImplementedError

    def get_series_releases_current(self, series_id: str) -> List[SeriesRelease]:
        raise NotImplementedError

    def get_series_releases_history(self, series_id: str) -> List[SeriesRelease]:
        raise NotImplementedError

    def get_release_series_current(self, release_id: int) -> List[SeriesRelease]:
        raise NotImplementedError

    def get_release_series_history(self, release_id: int) -> List[SeriesRelease]:
        raise NotImplementedError