from typing import List

from pydantic import BaseModel


class StoreEmbeddingRequest(BaseModel):
    embedding: List[List[float]]
    uuid: List[str]
