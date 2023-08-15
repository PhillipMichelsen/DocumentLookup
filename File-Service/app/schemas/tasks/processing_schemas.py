from typing import List

from pydantic import BaseModel


class ProcessFileRequest(BaseModel):
    EventName: str
    Key: str
    Records: List[dict]
