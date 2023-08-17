from typing import List

from pydantic import BaseModel


class EmbedStoreRequest(BaseModel):
    document_id: str
    text: List[str]
    uuid: List[str]


class EmbedStoreResponse(BaseModel):
    uuid: List[str]
