import json
import uuid

import yaml

from app.config import settings
from app.schemas.job_schemas import JobsSchema, JobSchema, JobRequest, JobResponse
from app.schemas.task_schemas import TaskResponse
from app.utils.pika_utils import pika_utils
from app.utils.redis_utils import task_redis, job_redis


class JobUtils:
    def __init__(self):
        self.jobs = {}

    def load_jobs(self, job_file) -> None:
        with open(job_file, "r") as stream:
            config = yaml.safe_load(stream)

            for job_name, job_config in config['jobs'].items():
                self.jobs[job_name] = JobsSchema(**job_config)

    @staticmethod
    def create_job(job_name: str, task_id: str, previous_job_id: str, initial_request: str) -> str:
        job_id = str(uuid.uuid4())

        job = JobSchema(
            name=job_name,
            task_id=task_id,
            job_id=job_id,
            previous_job_id=previous_job_id,
            content=initial_request,
            status="INITIALIZED"
        )

        job_redis.create_job(job_id, job)

        return job_id

    def execute_job(self, job_id: str) -> None:
        job = job_redis.get_job(job_id)
        job_info = self.jobs[job.name]

        if job_info.type == "process":
            self._execute_process_job(job, job_info)
        elif job_info.type == "return":
            self._execute_return_job(job)
        elif job_info.type == "wait":
            self._execute_wait_job()
        elif job_info.type == "end":
            self._execute_end_job(job)

    @staticmethod
    def _execute_process_job(job: JobSchema, job_info: JobsSchema) -> None:
        job_request = JobRequest(
            job_id=job.job_id
        )

        job_request = json.dumps(job_request.model_dump())

        pika_utils.publish_message(
            exchange_name=job_info.exchange,
            routing_key=job_info.routing_key,
            message=job_request.encode('utf-8')
        )
        job_redis.update_job_attribute(job.job_id, "status", "SENT")
        task_redis.update_task_attribute(job.task_id, "status", "PROCESSING")

    @staticmethod
    def _execute_return_job(job: JobSchema) -> None:
        task_response = TaskResponse(
            task_id=job.task_id,
            content=job_redis.get_job_attribute(job.previous_job_id, "content")
        )
        task_response = json.dumps(task_response.model_dump())

        pika_utils.publish_message(
            exchange_name=settings.gateway_exchange,
            routing_key=task_redis.get_task_attribute(job.task_id, "api_gateway_id"),
            message=task_response.encode('utf-8')
        )
        job_redis.update_job_attribute(job.job_id, "status", "SENT")
        task_redis.update_task_attribute(job.task_id, "status", "RETURNED")

        job_response = JobResponse(
            job_id=job.job_id
        )
        job_response = json.dumps(job_response.model_dump())

        pika_utils.publish_message(
            exchange_name=settings.service_exchange,
            routing_key='job_response',
            message=job_response.encode('utf-8')
        )

    def _execute_wait_job(self):
        pass

    @staticmethod
    def _execute_end_job(job: JobSchema) -> None:
        task = task_redis.get_task(job.task_id)

        for job_id in task.job_chain.split(','):
            job_redis.delete_job(job_id)

        task_redis.delete_task(job.task_id)


job_utils = JobUtils()
