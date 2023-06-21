from pydantic import BaseModel
from typing import List


class EmbedRequest(BaseModel):
    sentences: List[str]


class EmbedResponse(BaseModel):
    embedding: List[List[float]] = None
    error: str = None
