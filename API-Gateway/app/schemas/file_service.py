from pydantic import BaseModel


class GetPresignedURLRequest(BaseModel):
    filename: str


class GetPresignedURLResponse(BaseModel):
    presigned_url: str = None
    error: str = None
