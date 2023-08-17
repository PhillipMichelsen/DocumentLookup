import json

import yaml

from app.config import settings
from app.schemas.job_schemas import JobSchema, JobsSchema
from app.schemas.task_schemas import TaskSchema, TaskClearDataRequest
from app.utils.pika_utils import pika_utils
from app.utils.redis_utils import job_redis, task_redis
from app.utils.task_utils import task_utils


class JobUtils:
    """Job utilities class

    Handles job-related tasks and functions

    This class should be instantiated as a singleton instance
    """

    def __init__(self):
        self.jobs = {}

    def load_jobs(self) -> None:
        """Load jobs from YAML file

        :return: None
        """
        with open('app/jobs.yaml', "r") as stream:
            config = yaml.safe_load(stream)

            for job_name, job_config in config['jobs'].items():
                self.jobs[job_name] = JobsSchema.model_validate(job_config)

    def create_job(self, job_name: str, job_id: str, job_data: str,
                   requesting_service_exchange: str, requesting_service_return_queue_routing_key: str,
                   requesting_service_id: str) -> JobSchema:
        """Creates a job

        :param job_name: Name of job
        :param job_id: ID of job
        :param job_data: Data of job
        :param requesting_service_exchange: Exchange of requesting service
        :param requesting_service_return_queue_routing_key: Routing key of requesting service's return queue
        :param requesting_service_id: ID of requesting service
        :return: None
        """
        task_chain_ids = []

        for task in self.jobs[job_name].tasks:
            task_chain_ids.append(task_utils.create_task(task, job_id))

        job = JobSchema(
            job_name=job_name,
            job_id=job_id,
            requesting_service_exchange=requesting_service_exchange,
            requesting_service_return_queue_routing_key=requesting_service_return_queue_routing_key,
            requesting_service_id=requesting_service_id,
            task_chain=','.join(task_chain_ids),
            current_task_index=0,
            job_data=job_data,
            status='CREATED'
        )

        job_redis.store_job(job)

        return job

    @staticmethod
    def delete_job(job: JobSchema) -> None:
        """Deletes a job and all of its tasks

        :param job: Job
        :return: None
        """
        task_chain = job.task_chain.split(',')

        for task_id in task_chain:
            task = task_redis.get_stored_task(task_id)
            task_attributes = task_utils.tasks[task.task_name]

            if task_attributes.task_type == 'process':
                task_clear_data_request = TaskClearDataRequest(
                    task_id=task_id
                )

                message = json.dumps(task_clear_data_request.model_dump())
                pika_utils.publish_message(
                    exchange_name=task_attributes.exchange,
                    routing_key=f'{task.handled_by}_{settings.clear_job_data_queue_routing_key}',
                    message=message.encode('utf-8')
                )

            task_redis.delete_stored_task(task_id)

        job_redis.delete_stored_job(job.job_id)

    @staticmethod
    def get_return_task(job: JobSchema) -> TaskSchema:
        """Gets the return task of a job

        :param job: Job
        :return: Return task
        """
        task_chain = job.task_chain.split(',')
        task_chain.reverse()

        for task_id in task_chain:
            task = task_redis.get_stored_task(task_id)
            if task_utils.determine_task_type(task) == 'return':
                return task

        return task_redis.get_stored_task(task_chain[0])

    @staticmethod
    def step_up_task_index(job_id: str) -> None:
        """Steps the task index of a job

        :param job_id: ID of job
        :return: None
        """
        job = job_redis.get_stored_job(job_id)
        job_redis.update_task_index(job_id, job.current_task_index + 1)

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
