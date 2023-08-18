from typing import List

from pydantic import BaseModel


class AnswerQuestionRequest(BaseModel):
    text: List[str]
    query: str
    top_n: int = 20
    type_filter: str = "div"
    document_id: str = None


class AnswerQuestionResponse(BaseModel):
    chat_completion: str
