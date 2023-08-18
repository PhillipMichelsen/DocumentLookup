from typing import List, Tuple

from pydantic import BaseModel


class ProcessFileRequest(BaseModel):
    EventName: str
    Key: str
    Records: List[dict]


class ProcessFileResponse(BaseModel):
    entries: List[Tuple[List[str], str, str]]
