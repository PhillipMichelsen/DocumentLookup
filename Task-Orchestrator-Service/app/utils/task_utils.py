import asyncio
import uuid

from app.utils.redis_utils import task_redis, job_redis
from app.schemas.task_schemas import TaskSchema, TasksSchema


class TaskUtils:
    def __init__(self):
        self.tasks = None

    async def load_tasks(self, task_file: str = "app/tasks.yaml") -> None:
        with open(task_file, "r") as stream:
            config = yaml.safe_load(stream)

            for task_name, task_config in config['tasks'].items():
                self.tasks[task_name] = TasksSchema(**task_config)

    async def create_task(self, task_name: str, api_gateway_id: str) -> str:
        task_id = str(uuid.uuid4())

        task = TaskSchema(
            name=task_name,
            task_id=task_id,
            current_job=self.tasks[task_name]['jobs'][0],
            api_gateway_id=api_gateway_id,
            status="CREATED"
        )

        await task_redis.create_task(task_id, task)

        return task_id

    async def get_next_job(self, task_name: str, current_job: str) -> str:
        current_job_index = self.tasks[task_name]['jobs'].index(current_job)
        return self.tasks[task_name]['jobs'][current_job_index + 1]

    async def step_task_job(self, task_id: str) -> None:
        task = await task_redis.get_task(task_id)

        if task.current_job == "END":
            pass
        else:
            next_job = await self.get_next_job(task.name, task.current_job)
            await task_redis.update_task_detail(task_id, "current_job", next_job)


# Singleton instance
task_utils = TaskUtils()
