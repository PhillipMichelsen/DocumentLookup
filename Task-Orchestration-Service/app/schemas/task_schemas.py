from typing import Optional

from pydantic import BaseModel


class TaskSchema(BaseModel):
    task_name: str
    task_id: str
    job_id: str
    status: str


class TasksSchema(BaseModel):
    name: str
    type: str
    exchange: Optional[str] = None
    routing_key: Optional[str] = None


class TaskRequest(BaseModel):
    task_id: str


class TaskResponse(BaseModel):
    task_id: str
