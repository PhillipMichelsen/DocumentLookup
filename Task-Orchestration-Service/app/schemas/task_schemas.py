from typing import List

from pydantic import BaseModel


class TaskSchema(BaseModel):
    name: str
    task_id: str
    job_chain: str
    current_job_index: int
    api_gateway_id: str
    status: str


class TasksSchema(BaseModel):
    jobs: List[str]


class TaskRequest(BaseModel):
    task_name: str
    api_gateway_id: str
    task_id: str
    initial_request: str


class TaskResponse(BaseModel):
    task_id: str
    content: str
