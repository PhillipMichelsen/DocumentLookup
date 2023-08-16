from typing import List

from pydantic import BaseModel


class EmbedStoreRequest(BaseModel):
    text: List[str]
    uuid: List[str]
