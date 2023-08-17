from typing import List

from pydantic import BaseModel


class RetrieveQueryContextRequest(BaseModel):
    text: List[str]
    query: str
    top_n: int = 20
    type_filter: str = "div"
    document_id: str = None


class RetrieveQueryContextResponse(BaseModel):
    ranked_entries: List[str]


class GetFilesRequest(BaseModel):
    document_id: List[str]


class GetFilesResponse(BaseModel):
    document_id: List[str]
    filename: List[str]
    file_status: List[str]
