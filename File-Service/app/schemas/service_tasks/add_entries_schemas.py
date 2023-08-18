from typing import List, Tuple

from pydantic import BaseModel


class AddEntriesRequest(BaseModel):
    entries: List[Tuple[List[str], str, str]]


class AddEntriesResponse(BaseModel):
    entries_added: int
