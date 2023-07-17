from pydantic import BaseModel


class TaskRequest(BaseModel):
    """Schema for a task request"""
    task_name: str
    api_gateway_id: str
    task_id: str
    initial_request: str


class TaskResponse(BaseModel):
    """Schema for a task response"""
    task_id: str
    content: str
