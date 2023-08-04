from pydantic import BaseModel


class TaskRouteResponse(BaseModel):
    task_id: str
    next_task_id: str
    job_id: str
    exchange: str
    routing_key: str


class TaskRouteRequest(BaseModel):
    task_id: str
    service_id: str
    status: str


class TaskRequest(BaseModel):
    task_id: str
    job_id: str
    request_content: str
