from pydantic import BaseModel
from typing import List


class ChatCompletionRequest(BaseModel):
    context: List[str]
    query: str


class ChatCompletionResponse(BaseModel):
    chat_completion: str
