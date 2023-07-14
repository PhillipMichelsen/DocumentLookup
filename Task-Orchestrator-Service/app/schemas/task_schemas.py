from pydantic import BaseModel
from typing import List


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
    task_id: str
    initial_request: str
