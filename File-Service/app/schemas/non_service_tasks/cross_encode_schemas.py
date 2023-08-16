from typing import List

from pydantic import BaseModel


class CrossEncodeRequest(BaseModel):
    query: str
    entries: List[str]


class CrossEncodeResponse(BaseModel):
    ranked_entries: List[str]
    ranked_scores: List[float]
