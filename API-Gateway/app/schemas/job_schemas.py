from pydantic import BaseModel


class JobRequest(BaseModel):
    job_name: str
    requesting_service_exchange: str
    requesting_service_return_queue_routing_key: str
    requesting_service_id: str
    job_id: str
    job_data: str


class JobResponse(BaseModel):
    job_name: str
    job_id: str
    return_task_id: str
    status: str
