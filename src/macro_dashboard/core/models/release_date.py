from datetime import date, datetime
from pydantic import BaseModel, Field, StringConstraints
from typing_extensions import Annotated
from typing import List
import pandas as pd

class ReleaseDate(BaseModel):
    release_id: int
    release_name: str
    release_date: date = Field(alias = "date")


class ReleaseDateCollection(BaseModel):
    release_dates: List[ReleaseDate]
    realtime_start: date
    realtime_end: date
    ingested_at: datetime = Field(default_factory=datetime.now)

    def to_dataframe(self) -> pd.DataFrame:
        """
        Convert to pandas DataFrame
        """
        df = pd.DataFrame(
            {
                "release_id": [r.release_id for r in self.release_dates],
                "release_name": [r.release_name for r in self.release_dates],
                "release_date": [r.release_date for r in self.release_dates],
                "realtime_start": self.realtime_start,
                "realtime_end": self.realtime_end,
                "ingested_at": self.ingested_at
            }
        )
        return df
    
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