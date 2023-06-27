from pydantic import BaseModel


class UploadFileRequest(BaseModel):
    filename: str


class UploadFileResponse(BaseModel):
    presigned_url: str = None
    error: str = None
