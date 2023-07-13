from pydantic import BaseModel
from typing import List


class TaskSchema(BaseModel):
    name: str
    task_id: str
    current_job: str
    api_gateway_id: str
    status: str


class TasksSchema(BaseModel):
    jobs: List[str]
