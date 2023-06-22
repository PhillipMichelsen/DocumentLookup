from typing import List

from pydantic import BaseModel


class EmbedRequest(BaseModel):
    sentences: List[str]


class EmbedResponse(BaseModel):
    embedding: List[List[float]] = None
    error: str = None


class CrossEncodeRequest(BaseModel):
    query: str
    sentences: List[str]


class CrossEncodeResponse(BaseModel):
    sentences: List[str] = None
    scores: List[float] = None
    error: str = None
