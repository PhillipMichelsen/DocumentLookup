import yaml
import uuid
import json
import aioredis
import asyncio

from app.utils.pika_utils import pika_helper
from app.schemas.task_schema import Task, Job


class TaskRedis:
    def __init__(self):
        self.redis_tasks = None
        self.redis_job_data = None

    def connect_redis(self):
        self.redis_tasks = aioredis.from_url("redis://localhost", db=0, charset="utf-8", decode_responses=True)
        self.redis_job_data = aioredis.from_url("redis://localhost", db=1, charset="utf-8", decode_responses=True)

    async def initialize_task(self, task_id: str, task: Task, initial_data: dict) -> None:
        await self.redis_tasks.hset(task_id, mapping=task.dict())
        await self.redis_job_data.set(task_id, json.dumps(initial_data))

    async def remove_task(self, task_id: str) -> None:
        await self.redis_tasks.delete(task_id)
        await self.redis_job_data.delete(task_id)

    async def get_full_task_details(self, task_id: str) -> Task:
        task = await self.redis_tasks.hgetall(task_id)
        return Task.parse_obj(task)

    async def update_full_task_details(self, task_id: str, task: Task) -> None:
        await self.redis_tasks.hset(task_id, mapping=task.dict())

    async def update_single_task_detail(self, task_id: str, attribute: str, new_value: str) -> None:
        await self.redis_tasks.hset(task_id, attribute, new_value)

    async def get_job_data(self, task_id: str) -> dict:
        response = await self.redis_job_data.get(task_id)
        return json.loads(response)

    async def update_job_data(self, task_id: str, response: dict) -> None:
        await self.redis_job_data.set(task_id, json.dumps(response))


class TaskHelper:
    def __init__(self):
        self.tasks = {}
        self.jobs = {}
        self.endpoint_returns = {}

    def load_tasks_yaml(self, task_file: str = "app/tasks.yaml"):
        with open(task_file, "r") as stream:
            config = yaml.safe_load(stream)

            for task_name, task_config in config['tasks'].items():
                self.tasks[task_name] = task_config

            for job_name, job_config in config['jobs'].items():
                self.jobs[job_name] = Job(**job_config)

    async def create_task(self, task_name: str, initial_data: dict) -> str:
        task_id = str(uuid.uuid4())
        task = Task(
            task_name=task_name,
            current_job=self.tasks[task_name]['jobs'][0],
            original_api_gateway_id=initial_data['api_gateway_id'],
            status="initialized"
        )

        await task_redis.initialize_task(task_id, task, initial_data)

        return task_id

    async def remove_task(self, task_id: str) -> None:
        # TODO: Implement, calls task_redis.remove_task, deletes task from endpoint_returns if it exists
        raise NotImplementedError

    async def create_future(self, task_id: str) -> asyncio.Future:
        future = asyncio.Future()
        self.endpoint_returns[task_id] = future
        return future

    async def update_future(self, task_id: str) -> None:
        future = self.endpoint_returns[task_id]
        future.set_result(True)

    async def start_task(self, task_id: str) -> None:
        await pika_helper.publish_job(task_id)
        await task_redis.update_single_task_detail(task_id, "status", "started")

    async def handle_job_response(self, task_id: str, response: dict) -> None:
        await task_redis.update_job_data(task_id, response)
        await pika_helper.publish_job(task_id)

    async def _fetch_job_details(self, job_name: str) -> dict:
        # TODO: Implement, fetch details of a job from self.jobs
        raise NotImplementedError

    async def _fetch_next_job(self, task_id: str) -> str:
        # TODO: Implement, determines the next job in the task given task_id
        raise NotImplementedError


class JobExecutor:
    async def execute_job(self, task_id: str) -> None:
        # TODO: Implement, calls the correct job function based on the job type
        raise NotImplementedError

    async def _execute_job_process(self, task_id: str, job_details: dict) -> None:
        # TODO: Implement, fetches job data of task_id and sends to exchange and routing key in job_details
        raise NotImplementedError

    async def _execute_job_return(self, task_id: str) -> None:
        # TODO: Implement, updates the future of task_id with the job data of task_id
        raise NotImplementedError

    async def _execute_job_wait(self, task_id: str) -> None:
        # TODO: Implement, waits for a message from the exchange and routing key in job_details
        raise NotImplementedError

    async def _execute_job_end(self, task_id: str) -> None:
        # TODO: Implement, updates the status of task_id to "completed". Deletes task after 10 seconds.
        raise NotImplementedError


# Create singletons
task_redis = TaskRedis()
task_helper = TaskHelper()
job_executor = JobExecutor()

