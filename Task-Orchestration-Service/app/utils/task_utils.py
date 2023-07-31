import json
import uuid
from typing import Optional
import yaml

from app.config import settings
from app.schemas.task_schemas import TasksSchema, TaskSchema, TaskRequest, TaskResponse
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

    def execute_task(self, task_id: str, request_content: Optional[str] = None) -> None:
        task = task_redis.get_task(task_id)

        if self.tasks[task.task_name].type == 'process':
            self._execute_process_task(task_id, task, self.tasks[task.task_name], request_content)
        elif self.tasks[task.task_name].type == 'return':
            self._execute_return_task(task_id, task)
        elif self.tasks[task.task_name].type == 'end':
            self._execute_end_task(task_id, task)

    @staticmethod
    def _execute_process_task(task_id: str, task: TaskSchema, task_attributes: TasksSchema, request_content: str) -> None:
        message = json.dumps(request_content)

        pika_utils.publish_message(
            exchange_name=task_attributes.exchange,
            routing_key=task_attributes.routing_key,
            message=message.encode('utf-8')
        )

        task_redis.update_task_status(task_id, 'PUBLISHED')

    @staticmethod
    def _execute_return_task(task_id: str, task) -> None:
        raise NotImplementedError

    @staticmethod
    def _execute_end_task(task_id: str, task) -> None:
        job = job_redis.get_job(task.job_id)

        for task in job.task_chain.split(','):
            task_redis.delete_task(task)

        job_redis.delete_job(job.job_id)


task_utils = TaskUtils()
