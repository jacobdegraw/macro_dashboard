# TODO: add updateddate or smth
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd

class Release(BaseModel):
    id: int
    name: str
    press_release: bool
    ingested_at: datetime
    # TODO: make sure this is robust
    link: Optional[str]
    note: Optional[str]


class ReleaseCollection(BaseModel):
    release_list: List[Release]

    @classmethod
    def from_fred_payload(cls, *, payload: dict, ingested_at: Optional[datetime] = None) -> "ReleaseCollection":
        """
        Convert a FRED 'releases' JSON payload into a ReleaseCollection
        """
        if ingested_at is None:
            ingested_at = datetime.now()

        releases = []

        for r in payload.get("releases", []):
            releases.append(
                Release(
                    id = r["id"],
                    name = r["name"],
                    press_release= r["press_release"],
                    ingested_at= ingested_at,
                    link = r.get("link", None),
                    note = r.get("note", None)
                )
            )

        return cls(release_list=releases)


    def to_dataframe(self) -> pd.DataFrame:
        """
        Convert to pandas DataFrame
        """
        df = pd.DataFrame(
            {
                "id": [r.id for r in self.release_list],
                "name": [r.name for r in self.release_list],
                "press_release": [r.press_release for r in self.release_list],
                "link": [r.link for r in self.release_list]
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