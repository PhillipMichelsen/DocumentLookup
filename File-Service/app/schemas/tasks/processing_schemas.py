from pydantic import BaseModel
from typing import List


class ProcessFileRequest(BaseModel):
    EventName: str
    Key: str
    Records: List[dict]


class ProcessFileResponse(BaseModel):
    paragraphs: List[str]
    sentences: List[str]
