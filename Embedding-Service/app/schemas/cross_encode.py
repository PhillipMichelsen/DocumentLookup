from pydantic import BaseModel
from typing import List


class CrossEncodeRequest(BaseModel):
    query: str
    sentences: List[str]


class CrossEncodeResponse(BaseModel):
    sentences: List[str] = None
    scores: List[float] = None
    error: str = None
