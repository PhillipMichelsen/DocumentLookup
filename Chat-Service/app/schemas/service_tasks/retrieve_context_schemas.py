from pydantic import BaseModel
from typing import List


class RetrieveContextRequest(BaseModel):
    query: str
    top_n: int
    text_type: str
    document_id: str


class RetrieveContextResponse(BaseModel):
    context: List[str]
