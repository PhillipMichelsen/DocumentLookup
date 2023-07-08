from typing import Optional

from pydantic import BaseModel


class Task(BaseModel):
    name: str
    current_job: str
    original_gateway_id: str
    status: str


class Job(BaseModel):
    name: str
    type: str
    exchange: Optional[str] = None
    routing_key: Optional[str] = None
