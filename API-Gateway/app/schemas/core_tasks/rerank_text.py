from typing import List, Optional

from pydantic import BaseModel


class TaskRerankTextRequest(BaseModel):
    query: str
    sentences: List[str]


class TaskRerankTextResponse(BaseModel):
    sentences: List[str]
    scores: List[float]
