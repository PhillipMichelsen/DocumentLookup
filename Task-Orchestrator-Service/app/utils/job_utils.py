import uuid
import yaml

from app.schemas.job_schemas import JobsSchema, JobSchema
from app.utils.pika_utils import pika_helper
from app.utils.redis_utils import task_redis, job_redis

from app.config import settings


class JobUtils:
    def __init__(self):
        self.jobs = {}

    def load_jobs(self, job_file: str = "app/jobs.yaml") -> None:
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
            self._execute_process_job(job_id, job, job_info)
        elif job_info.type == "return":
            self._execute_return_job(job_id, job)
        elif job_info.type == "wait":
            self._execute_wait_job()
        elif job_info.type == "end":
            self._execute_end_job(job_id, job)

    @staticmethod
    def _execute_process_job(job_id: str, job: JobSchema, job_info: JobsSchema) -> None:
        pika_helper.publish_message(
            exchange_name=job_info.exchange,
            routing_key=job_info.routing_key,
            message=job_id
        )
        job_redis.update_job_attribute(job_id, "status", "SENT")
        task_redis.update_task_attribute(job.task_id, "status", "PROCESSING")

    @staticmethod
    def _execute_return_job(job_id: str, job: JobSchema) -> None:
        pika_helper.publish_message(
            exchange=settings.service_exchange,
            routing_key=task_redis.get_task_attribute(job.task_id, "api_gateway_id"),
            message=job.content
        )
        job_redis.update_job_attribute(job_id, "status", "SENT")
        task_redis.update_task_attribute(job.task_id, "status", "RETURNED")

    def _execute_wait_job(self):
        pass

    @staticmethod
    def _execute_end_job(job_id: str, job: JobSchema) -> None:
        task = task_redis.get_task(job.task_id)

        for job_id in task.job_chain.join(','):
            job_redis.delete_job(job_id)

        task_redis.delete_task(job.task_id)


job_utils = JobUtils()
