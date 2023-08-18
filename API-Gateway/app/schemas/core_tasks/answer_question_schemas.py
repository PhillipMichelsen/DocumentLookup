from pydantic import BaseModel
from typing import List


class AnswerQuestionRequest(BaseModel):
    query: str
    top_n: int
    text_type: str
    document_id: str


class AnswerQuestionResponse(BaseModel):
    chat_completion: str
    context: List[str]

