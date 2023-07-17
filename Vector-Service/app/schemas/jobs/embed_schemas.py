from typing import List

from pydantic import BaseModel


class EmbedRequest(BaseModel):
    sentences: List[str]


class EmbedResponse(BaseModel):
    embedding: List[List[float]]
