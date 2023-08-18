from pydantic import BaseModel
from typing import List


class GeneratePresignedURLUploadRequest(BaseModel):
    filename: str


class GeneratePresignedURLUploadResponse(BaseModel):
    presigned_url_upload: str


class AnswerQuestionRequest(BaseModel):
    query: str
    top_n: int
    text_type: str
    document_id: str


class AnswerQuestionResponse(BaseModel):
    chat_completion: str
    context: List[str]


class GetFilesRequest(BaseModel):
    document_id: List[str]


class GetFilesResponse(BaseModel):
    document_id: List[str]
    filename: List[str]
    file_status: List[str]
