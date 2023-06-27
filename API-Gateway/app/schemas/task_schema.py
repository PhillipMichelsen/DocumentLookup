from pydantic import BaseModel
from typing import Optional


class Task(BaseModel):
    task_name: str
    current_job: str
    original_gateway_id: str
    status: str


class Job(BaseModel):
    job_name: str
    type: str
    exchange: Optional[str]
    routing_key: Optional[str]

