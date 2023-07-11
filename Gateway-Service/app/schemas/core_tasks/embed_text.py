from typing import List

from pydantic import BaseModel


class TaskEmbedTextRequest(BaseModel):
    sentences: List[str]


class TaskEmbedTextResponse(BaseModel):
    embedding: List[List[float]] = None
    error: str = None
