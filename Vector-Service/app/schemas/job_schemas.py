from pydantic import BaseModel


class JobSchema(BaseModel):
    name: str
    job_id: str
    task_id: str
    previous_job_id: str
    content: str
    status: str


class JobRequest(BaseModel):
    job_id: str


class JobResponse(BaseModel):
    job_id: str
