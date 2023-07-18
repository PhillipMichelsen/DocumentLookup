from typing import List, Optional

from pydantic import BaseModel


class TaskEmbedTextRequest(BaseModel):
    sentences: List[str]


class TaskEmbedTextResponse(BaseModel):
    embedding: List[List[float]]
