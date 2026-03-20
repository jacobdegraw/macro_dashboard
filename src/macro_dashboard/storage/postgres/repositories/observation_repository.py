from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime
from typing import List

from sqlalchemy import Row, text
from sqlalchemy.orm import Session

from macro_dashboard.core.models.observations import Observation, TimeSeries


@dataclass(frozen=True)
class ObservationRepository:
    """
    Repository for reads/writes against observations_current and observations_history.
    """

    session: Session

    @staticmethod
    def _row_to_observation(row: Row) -> Observation:
        return Observation(
                        date = row.date, 
                        value = row.value
                    )

    @staticmethod
    def _rows_to_time_series(rows: List[Row]) -> TimeSeries:
        if not rows:
            raise ValueError("rows must not be empty")
        

        observations = [ObservationRepository._row_to_observation(row) for row in rows]

        return TimeSeries(
            series_id = rows[0].series_id,
            realtime_start = rows[0].realtime_start,
            realtime_end = rows[0].realtime_end,
            observations = observations,
            ingested_at = rows[0].ingested_at,
        )
    
    @staticmethod
    def _rows_to_time_series_history(rows: List[Row]) -> List[TimeSeries]:
        grouped = defaultdict(list)

        for row in rows:
            key = (row.realtime_start, row.realtime_end)
            grouped[key].append(row)
        
        return [
            ObservationRepository._rows_to_time_series(group_rows)
            for _, group_rows in grouped.items()
        ]
    
    @staticmethod
    def _time_series_to_rows(time_series: TimeSeries) -> List[dict]:
        return [
            {
                "series_id": time_series.series_id,
                "realtime_start": time_series.realtime_start,
                "realtime_end": time_series.realtime_end,
                "date": obs.date,
                "value": obs.value,
                "ingested_at": time_series.ingested_at,
            }
            for obs in time_series.observations
        ]

    def _execute_upsert_current(self, params: List[dict]) -> None:
        stmt = text("""
            INSERT INTO observations_current (
                series_id, realtime_start, realtime_end, date, value, ingested_at
             )
             VALUES (
                :series_id, :realtime_start, :realtime_end, :date, :value, :ingested_at
             )
             ON CONFLICT (series_id, date)
             DO UPDATE SET
                realtime_end = EXCLUDED.realtime_end, 
                realtime_start = EXCLUDED.realtime_start,
                value = EXCLUDED.value, 
                ingested_at = EXCLUDED.ingested_at
        """)

        self.session.execute(
            stmt,
            params
        )

    def _execute_insert_history(self, params: List[dict]) -> None:
        stmt = text("""
            INSERT INTO observations_history (
                series_id, realtime_start, realtime_end, date, value, ingested_at
             )
             VALUES (
                :series_id, :realtime_start, :realtime_end, :date, :value, :ingested_at
             )
             ON CONFLICT (series_id, date, realtime_start) DO NOTHING
        """)

        self.session.execute(
            stmt,
            params
        )

    def upsert_time_series_current(self, time_series: TimeSeries) -> None:
        self._execute_upsert_current(ObservationRepository._time_series_to_rows(time_series))

    def upsert_time_series_current_many(self, time_series_list: List[TimeSeries]) -> None:
        params = [
            row for time_series in time_series_list 
                    for row in ObservationRepository._time_series_to_rows(time_series)
        ]

        self._execute_upsert_current(params)

    def insert_time_series_history(self, time_series: TimeSeries) -> None:
        self._execute_insert_history(ObservationRepository._time_series_to_rows(time_series))

    def insert_time_series_history_many(self, time_series_list: List[TimeSeries]) -> None:
        params = [
            row for time_series in time_series_list 
                    for row in ObservationRepository._time_series_to_rows(time_series)
        ]

        self._execute_insert_history(params)

    def get_observation_current(
        self,
        series_id: str,
        observation_date: date,
    ) -> Observation | None:
        stmt = text("""
            SELECT date, value
            FROM observations_current
            WHERE series_id = :series_id
                AND date = :observation_date
        """)

        result = self.session.execute(
            stmt,
            {
                "series_id": series_id,
                "observation_date": observation_date
            }
        )
        
        row = result.fetchone()
        if row is None:
            return None
        return self._row_to_observation(row)

    def get_time_series_range_current(
        self,
        series_id: str,
        start_date: date,
        end_date: date,
    ) -> TimeSeries | None:
        if start_date > end_date:
            raise ValueError("start_date must be on or before end_date")
        

        stmt = text("""
            SELECT series_id, date, value, realtime_start, realtime_end, ingested_at
            FROM observations_current
            WHERE series_id = :series_id
                AND date >= :start_date
                AND date <= :end_date
            ORDER BY date
        """)

        result = self.session.execute(
            stmt,
            {
                "series_id": series_id,
                "start_date": start_date,
                "end_date": end_date
            }
        )

        rows_list = result.fetchall()
        if not rows_list:
            return None
        return self._rows_to_time_series(rows_list)

    def get_time_series_current(self, series_id: str) -> TimeSeries | None:
        stmt = text("""
            SELECT series_id, date, value, realtime_start, realtime_end, ingested_at
            FROM observations_current
            WHERE series_id = :series_id
            ORDER BY date
        """)

        result = self.session.execute(
            stmt,
            {"series_id": series_id}
        )

        rows_list = result.fetchall()
        if not rows_list:
            return None
        return self._rows_to_time_series(rows_list)
    

    def get_time_series_history(self, series_id: str) -> List[TimeSeries]:
        stmt = text("""
            SELECT series_id, date, value, realtime_start, realtime_end, ingested_at
            FROM observations_history
            WHERE series_id = :series_id
            ORDER BY realtime_start DESC, date
        """)

        result = self.session.execute(
            stmt,
            {"series_id": series_id}
        )

        return self._rows_to_time_series_history(result.fetchall())

    def get_observation_history_for_date(
        self,
        series_id: str,
        observation_date: date,
    ) -> List[TimeSeries]:
        stmt = text("""
            SELECT series_id, date, value, realtime_start, realtime_end, ingested_at
            FROM observations_history
            WHERE series_id = :series_id
                AND date = :observation_date
            ORDER BY realtime_start DESC
        """)

        result = self.session.execute(
            stmt,
            {
                "series_id": series_id,
                "observation_date": observation_date
            }
        )

        return self._rows_to_time_series_history(result.fetchall())