from typing import Optional

from pydantic import BaseModel


class JobSchema(BaseModel):
    name: str
    job_id: str
    task_id: str
    previous_job_id: str
    content: str
    status: str


class JobsSchema(BaseModel):
    name: str
    type: str
    exchange: Optional[str] = None
    routing_key: Optional[str] = None


class JobRequest(BaseModel):
    job_id: str


class JobResponse(BaseModel):
    job_id: str
