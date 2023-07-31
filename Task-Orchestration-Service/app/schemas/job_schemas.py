from typing import List, Optional

from pydantic import BaseModel


class JobSchema(BaseModel):
    job_name: str
    job_id: str
    return_service_id: Optional[str] = None
    task_chain: str
    current_task_index: int
    initial_request_content: str
    status: str


class JobsSchema(BaseModel):
    tasks: List[str]


class JobRequest(BaseModel):
    job_name: str
    return_service_id: Optional[str] = None
    job_id: str
    initial_request_content: str


class JobResponse(BaseModel):
    job_id: str
    return_content: str
