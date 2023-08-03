from typing import List

from pydantic import BaseModel


class JobSchema(BaseModel):
    job_name: str
    job_id: str
    requesting_service_id: str
    task_chain: str
    current_task_index: int
    initial_request_content: str
    status: str


class JobsSchema(BaseModel):
    tasks: List[str]


class JobRequest(BaseModel):
    job_name: str
    requesting_service_id: str
    job_id: str
    initial_request_content: str


class JobResponse(BaseModel):
    job_id: str
    return_content: str
