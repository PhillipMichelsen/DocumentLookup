from pydantic import BaseModel
from typing import List


class EmbedStoreRequest(BaseModel):
    text: List[str]
    uuid: List[str]


class EmbedStoreResponse(BaseModel):
    embedding: List[List[float]]
    uuid: List[str]
