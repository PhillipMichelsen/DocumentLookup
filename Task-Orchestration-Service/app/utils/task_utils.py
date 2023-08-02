import json
import uuid
from typing import Optional, Any, Tuple
import yaml

from app.config import settings
from app.schemas.task_schemas import TasksSchema, TaskSchema, TaskRouteResponse, TaskRouteRequest
from app.schemas.job_schemas import JobResponse
from app.utils.job_utils import job_utils
from app.utils.pika_utils import pika_utils
from app.utils.redis_utils import task_redis, job_redis


class TaskUtils:
    def __init__(self):
        self.tasks = {}

    def load_tasks(self, task_file: str) -> None:
        """Load jobs from a YAML file

        :param task_file: Path to the YAML file
        :return: None
        """
        with open(task_file, "r") as stream:
            config = yaml.safe_load(stream)

            for task_name, task_config in config['tasks'].items():
                self.tasks[task_name] = TasksSchema(**task_config)

    @staticmethod
    def create_task(task_name: str, job_id: str) -> str:
        """Creates a task

        :param task_name: Name of task
        :param job_id: ID of job
        :return: ID of task
        """
        task_id = str(uuid.uuid4())
        task = TaskSchema(task_name=task_name, task_id=task_id, job_id=job_id, status='CREATED')
        task_redis.store_task(task)

        return task_id

    @staticmethod
    def return_task(task: TaskSchema) -> None:
        job = job_redis.get_job(task.job_id)

        route_request = TaskRouteResponse(
            task_id=task.task_id,
            exchange=task.return_exchange,
            routing_key=task.return_routing_key
        )

        message = json.dumps(route_request.model_dump())

        pika_utils.publish_message(
            exchange_name=settings.gateway_exchange,
            routing_key=job.return_routing_key,
            message=message.encode()
        )

    @staticmethod
    def end_task(task: TaskSchema) -> None:
        job = job_redis.get_job(task.job_id)

        for task in job.task_chain.split(','):
            task_redis.delete_task(task)

        job_redis.delete_job(job.job_id)

    def send_task(self, task: TaskSchema, message_content: str) -> None:
        task_attributes = self.tasks[task.task_name]

        pika_utils.publish_message(
            exchange_name=task_attributes.exchange,
            routing_key=task_attributes.routing_key,
            message=message_content.encode()
        )

    @staticmethod
    def send_task_routing_instructions(completed_task: TaskSchema, new_task: TaskSchema, completed_task_service_id: str) -> None:
        completed_task_attributes = task_utils.tasks[completed_task.task_name]
        new_task_attributes = task_utils.tasks[new_task.task_name]

        route_instructions = TaskRouteResponse(
            task_id=completed_task.task_id,
            next_task_id=new_task.task_id,
            exchange=new_task_attributes.exchange,
            routing_key=new_task_attributes.routing_key
        )

        message = json.dumps(route_instructions.model_dump())

        pika_utils.publish_message(
            exchange_name='task_routing',
            routing_key=completed_task_service_id,
            message=message.encode()
        )


task_utils = TaskUtils()
