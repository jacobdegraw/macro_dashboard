# TODO: add updateddate or smth
from datetime import datetime, date
from pydantic import BaseModel, Field
from typing import List, Optional
import pandas as pd

class Release(BaseModel):
    release_id: int = Field(alias = "id")
    name: str
    press_release: bool
    
    # TODO: make sure this is robust
    link: Optional[str] = None
    note: Optional[str] = None

    realtime_start: date
    realtime_end: date
    


class ReleaseCollection(BaseModel):
    release_list: List[Release]
    ingested_at: datetime = Field(default_factory=datetime.now)

    # @classmethod
    # def from_fred_payload(cls, *, payload: dict, ingested_at: Optional[datetime] = None) -> "ReleaseCollection":
    #     """
    #     Convert a FRED 'releases' JSON payload into a ReleaseCollection
    #     """
        

    #     releases = []

    #     for r in payload.get("releases", []):
    #         releases.append(
    #             Release(
    #                 release_id = r["id"],
    #                 name = r["name"],
    #                 press_release= r["press_release"],
    #                 ingested_at= ingested_at,
    #                 link = r.get("link", None),
    #                 note = r.get("note", None)
    #             )
    #         )

    #     return cls(release_list=releases)


    def to_dataframe(self) -> pd.DataFrame:
        """
        Convert to pandas DataFrame
        """
        df = pd.DataFrame(
            {
                "release_id": [r.release_id for r in self.release_list],
                "name": [r.name for r in self.release_list],
                "press_release": [r.press_release for r in self.release_list],
                "link": [r.link for r in self.release_list],
                "note": [r.note for r in self.release_list],
                "realtime_start": [r.realtime_start for r in self.release_list],
                "realtime_end": [r.realtime_end for r in self.release_list],
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