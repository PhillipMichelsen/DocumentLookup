from typing import List

from pydantic import BaseModel


class StoreEmbeddingRequest(BaseModel):
    document_id: str
    embedding: List[List[float]]
    uuid: List[str]


class StoreEmbeddingResponse(BaseModel):
    uuid: List[str]
