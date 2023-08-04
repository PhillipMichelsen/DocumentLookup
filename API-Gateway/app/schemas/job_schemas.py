from typing import List

from pydantic import BaseModel


class JobRequest(BaseModel):
    job_name: str
    requesting_service_id: str
    job_id: str
    initial_request_content: str


class JobResponse(BaseModel):
    job_id: str
    return_content: str
