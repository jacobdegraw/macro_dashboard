from datetime import date, datetime
from typing import Any, List, Optional
from pydantic import BaseModel, Field, field_validator
import pandas as pd

class Observation(BaseModel):
    date: date
    value: Optional[float] = Field(
        None,
        description="Missing values allowed (e.g. '.', None)"
    )

    model_config = {
        "frozen": True
    }

    @field_validator("value", mode="before")
    @classmethod
    def coerce_value(cls, v: Any):
        """
        Convert non-numeric values ('.', '', None, etc.) to None.
        """
        if v in (None, "", ".", "NA", "N/A"):
            return None

        try:
            return float(v)
        except (TypeError, ValueError):
            return None

class TimeSeries(BaseModel):
    series_id: str
    realtime_start: date
    realtime_end: date
    observations: List[Observation]
    ingested_at: datetime = Field(default_factory=datetime.now)

    @classmethod
    def from_fred_payload(cls, *, series_id: str, payload: dict, ingested_at: Optional[date] = None) -> "TimeSeries":
        """
        Convert a FRED 'series/observations' JSON payload into a TimeSeries.

        - Ignores extra fields in each observation (realtime_start/end, etc.)
        """
        # if ingested_at is None:
        #     ingested_at = datetime.now()

        obs = []
        for o in payload.get("observations", []):

            obs.append(
                Observation(
                    date=o["date"],
                    value=o["value"]
                )
            )

        return cls(series_id=series_id, observations=obs, 
                   realtime_start=payload.get("realtime_start"), 
                   realtime_end=payload.get("realtime_end"))

    def to_dataframe(self) -> pd.DataFrame:
        """
        Convert to pandas DataFrame
        """
        df = pd.DataFrame(
            {
                "series_id": self.series_id,
                "date": [o.date for o in self.observations],
                "value": [o.value for o in self.observations],
                "realtime_start": self.realtime_start,
                "realtime_end": self.realtime_end,
                "ingested_at": self.ingested_at
            }
        )

        return df.sort_values("date")

    def to_json(self, *, indent: int = 2) -> str:
        """
        Serialize to JSON string.
        """
        return self.model_dump_json(indent = indent)
    
    def to_dict(self) -> dict:
        """
        Python-native dict
        """
        return self.model_dump()
