import json
import uuid

import yaml

from app.config import settings
from app.schemas.job_schemas import JobSchema
from app.schemas.task_schemas import TasksSchema, TaskSchema, TaskRouteRequest
from app.utils.pika_utils import pika_utils
from app.utils.redis_utils import task_redis


class TaskUtils:
    """Task utilities class"""

    def __init__(self):
        self.tasks = {}

    def load_tasks(self) -> None:
        """Load jobs from a YAML file

        :return: None
        """
        with open('app/tasks.yaml', "r") as stream:
            config = yaml.safe_load(stream)

            for task_name, task_config in config['tasks'].items():
                self.tasks[task_name] = TasksSchema.model_validate(task_config)

    @staticmethod
    def create_task(task_name: str, job_id: str) -> str:
        """Creates a task

        :param task_name: Name of task
        :param job_id: ID of job
        :return: ID of task
        """
        task_id = str(uuid.uuid4())
        task = TaskSchema(task_name=task_name, task_id=task_id, job_id=job_id, handled_by='WAITING', status='CREATED')
        task_redis.store_task(task)

        return task_id

    def determine_task_type(self, task: TaskSchema) -> str:
        """Determines the type of task

        :param task: Task
        :return: Type of task
        """
        task_attributes = self.tasks[task.task_name]
        return task_attributes.task_type

    def route_process_task(self, completed_task: TaskSchema, next_task: TaskSchema, job: JobSchema,
                           requesting_service_id: str) -> None:
        completed_task_attributes = self.tasks[completed_task.task_name]
        next_task_attributes = self.tasks[next_task.task_name]

        task_route_request = TaskRouteRequest(
            task_id=completed_task.task_id,
            next_task_id=next_task.task_id,
            job_id=job.job_id,
            exchange=next_task_attributes.exchange,
            routing_key=next_task_attributes.routing_key,
        )

        message = json.dumps(task_route_request.model_dump())
        pika_utils.publish_message(
            exchange_name=completed_task_attributes.exchange,
            routing_key=f'{requesting_service_id}_{settings.route_request_queue_routing_key}',
            message=message.encode('utf-8'),
        )

    @staticmethod
    def route_return_task(completed_task: TaskSchema, next_task: TaskSchema, job: JobSchema,
                          requesting_service_id: str) -> None:
        completed_task_attributes = task_utils.tasks[completed_task.task_name]

        task_route_request = TaskRouteRequest(
            task_id=completed_task.task_id,
            next_task_id=next_task.task_id,
            job_id=job.job_id,
            exchange=job.requesting_service_exchange,
            routing_key=f'{job.requesting_service_id}_{job.requesting_service_return_queue_routing_key}',
        )

        message = json.dumps(task_route_request.model_dump())
        pika_utils.publish_message(
            exchange_name=completed_task_attributes.exchange,
            routing_key=f'{requesting_service_id}_{settings.route_request_queue_routing_key}',
            message=message.encode('utf-8')
        )


task_utils = TaskUtils()
