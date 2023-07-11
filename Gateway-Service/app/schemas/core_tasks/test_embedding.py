from typing import List

from pydantic import BaseModel


class TaskTestEmbedRequest(BaseModel):
    sentences: List[str]


class TaskTestEmbedResponse(BaseModel):
    embedding: List[List[float]] = None
    error: str = None
