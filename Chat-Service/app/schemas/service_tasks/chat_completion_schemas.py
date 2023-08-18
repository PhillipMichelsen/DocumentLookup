from pydantic import BaseModel
from typing import List


class ChatCompletionRequest(BaseModel):
    ranked_entries: List[str]
    query: str


class ChatCompletionResponse(BaseModel):
    chat_completion: str
