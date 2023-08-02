import yaml
from typing import List, Optional

from app.schemas.job_schemas import JobSchema, JobsSchema
from app.utils.task_utils import task_utils
from app.utils.redis_utils import job_redis


class JobUtils:
    def __init__(self):
        self.jobs = {}

    def load_jobs(self, job_file: str) -> None:
        """Load jobs from YAML file

        :param job_file: Path to YAML file
        :return: None
        """
        with open(job_file, "r") as stream:
            config = yaml.safe_load(stream)

            for job_name, job_config in config['jobs'].items():
                self.jobs[job_name] = JobsSchema.model_validate(job_config)

    def create_job(self, job_name: str, job_id: str, initial_request_content: str, requesting_service_id: str) -> JobSchema:
        """Creates a job

        :param job_name: Name of job
        :param job_id: ID of job
        :param initial_request_content: Initial request content
        :param requesting_service_id: ID of requesting service
        :return: None
        """
        task_chain_ids = []

        for task in self.jobs[job_name].tasks:
            task_chain_ids.append(task_utils.create_task(task, job_id))

        job = JobSchema(
            job_name=job_name,
            job_id=job_id,
            requesting_service_id=requesting_service_id,
            task_chain=','.join(task_chain_ids),
            current_task_index=0,
            initial_request_content=initial_request_content,
            status='CREATED'
        )

        job_redis.store_job(job)

        return job

    @staticmethod
    def step_up_task_index(job_id: str) -> None:
        """Steps the task index of a job

        :param job_id: ID of job
        :return: None
        """
        job = job_redis.get_job(job_id)
        job.current_task_index += 1
        job_redis.store_job(job)

    @staticmethod
    def step_down_task_index(job_id: str) -> None:
        """Steps the task index of a job

        :param job_id: ID of job
        :return: None
        """
        job = job_redis.get_job(job_id)
        job.current_task_index -= 1
        job_redis.store_job(job)


# Singleton instance
job_utils = JobUtils()
