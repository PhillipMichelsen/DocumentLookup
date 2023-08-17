from typing import List

from pydantic import BaseModel


class RetrieveClosestEntriesRequest(BaseModel):
    embedding: List[List[float]]
    top_n: int = 20
    type_filter: str = "div"
    document_id: str = None


class RetrieveClosestEntriesResponse(BaseModel):
    entries: List[str]
