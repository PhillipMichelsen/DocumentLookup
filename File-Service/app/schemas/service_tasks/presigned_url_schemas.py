from pydantic import BaseModel


class PresignedURLUploadRequest(BaseModel):
    filename: str


class PresignedURLUploadResponse(BaseModel):
    presigned_url_upload: str
