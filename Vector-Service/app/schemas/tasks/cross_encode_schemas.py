from typing import List

from pydantic import BaseModel


class CrossEncodeRequest(BaseModel):
    query: str
    sentences: List[str]


class CrossEncodeResponse(BaseModel):
    sentences: List[str]
    scores: List[float]
