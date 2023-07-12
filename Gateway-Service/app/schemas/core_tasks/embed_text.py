from typing import List, Optional

from pydantic import BaseModel


class TaskEmbedTextRequest(BaseModel):
    sentences: List[str]


class TaskEmbedTextResponse(BaseModel):
    embedding: Optional[List[List[float]]]
    error: Optional[str]
