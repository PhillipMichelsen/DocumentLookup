from typing import List, Optional

from pydantic import BaseModel


class TaskRerankTextRequest(BaseModel):
    query: str
    sentences: List[str]


class TaskRerankTextResponse(BaseModel):
    sentences: Optional[List[str]]
    scores: Optional[List[float]]
    error: Optional[str]
