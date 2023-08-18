from pydantic import BaseModel
from typing import List


class GetFilesRequest(BaseModel):
    document_id: List[str]


class GetFilesResponse(BaseModel):
    document_id: List[str]
    filename: List[str]
    file_status: List[str]
