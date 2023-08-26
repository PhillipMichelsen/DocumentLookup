from pydantic import BaseModel
from typing import List, Optional, Tuple


class RetrieveContextRequest(BaseModel):
    context_query: str
    top_n: int
    text_type: Optional[str] = 'paragraph'
    document_ids: Optional[List[str]] = None


class RetrieveContextResponse(BaseModel):
    context: List[str]
