from pydantic import BaseModel


class TaskRequest(BaseModel):
    task_name: str
    api_gateway_id: str
    task_id: str
    initial_request: str


class TaskResponse(BaseModel):
    task_id: str
    content: str