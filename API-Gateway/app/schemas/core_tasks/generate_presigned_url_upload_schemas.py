from pydantic import BaseModel
from typing import List


class GeneratePresignedURLUploadRequest(BaseModel):
    filename: str


class GeneratePresignedURLUploadResponse(BaseModel):
    presigned_url_upload: str
