from typing import Optional

from pydantic import BaseModel


class TaskSchema(BaseModel):
    task_name: str
    task_id: str
    job_id: str
    status: str


class TasksSchema(BaseModel):
    task_name: str
    task_type: str
    exchange: Optional[str] = None
    routing_key: Optional[str] = None


class TaskRouteRequest(BaseModel):
    task_id: str
    next_task_id: str
    job_id: str
    exchange: str
    routing_key: str


class TaskRouteResponse(BaseModel):
    task_id: str
    next_task_id: str
    service_id: str
    status: str


class TaskResponse(BaseModel):
    task_id: str
    service_id: str
    status: str


class TaskRequest(BaseModel):
    task_id: str
    job_id: str
    request_content: str
