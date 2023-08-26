from pydantic import BaseModel
from typing import Optional, List, Tuple


class ChatCompletionRequest(BaseModel):
    context: Optional[List[str]] = None
    messages: Optional[List[dict]] = None
    user_query: str


class ChatCompletionResponse(BaseModel):
    chat_completion: Optional[str] = None
    context_query: Optional[str] = None
    messages: List[dict]
