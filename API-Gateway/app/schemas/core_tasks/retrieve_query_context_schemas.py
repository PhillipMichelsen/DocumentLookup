from pydantic import BaseModel
from typing import List


class RetrieveQueryContextRequest(BaseModel):
    text: List[str]
    query: str
    top_n: int = 20
    type_filter: str = "div"
    document_id: str = None


class RetrieveQueryContextResponse(BaseModel):
    ranked_entries: List[str]
