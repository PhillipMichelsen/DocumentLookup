from pydantic import BaseModel
from typing import List


class GetPresignedURLUploadRequest(BaseModel):
    filename: str


class GetPresignedURLUploadResponse(BaseModel):
    presigned_url: str = None
    error: str = None


class FileUploadedRequest(BaseModel):
    EventName: str
    Key: str
    Records: List[dict]


class FileUploadedResponse(BaseModel):
    presigned_url: str = None
