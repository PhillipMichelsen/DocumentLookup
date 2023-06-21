from pydantic import BaseModel


class ProcessFileRequest(BaseModel):
    presigned_url: str = None
