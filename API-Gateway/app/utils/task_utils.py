import yaml
import uuid
import json
import aioredis
import asyncio

from app.utils.pika_utils import pika_helper
from app.schemas.tasks_schema import Task, Job


class TaskRedis:
    def __init__(self):
        self.redis_tasks = None
        self.redis_job_data = None

    def connect_redis(self):
        self.redis_tasks = aioredis.from_url("redis://localhost", db=0, charset="utf-8", decode_responses=True)
        self.redis_job_data = aioredis.from_url("redis://localhost", db=1, charset="utf-8", decode_responses=True)

    async def initialize_task(self, task_id: str, task: dict, initial_data: dict) -> None:
        await self.redis_tasks.hset(task_id, mapping=task)
        await self.redis_job_data.set(task_id, json.dumps(initial_data))

    async def remove_task(self, task_id: str) -> None:
        await self.redis_tasks.delete(task_id)
        await self.redis_job_data.delete(task_id)

    async def get_full_task_details(self, task_id: str) -> Task:
        task = await self.redis_tasks.hgetall(task_id)
        return Task.parse_obj(task)

    async def get_single_task_detail(self, task_id: str, attribute: str) -> str:
        return await self.redis_tasks.hget(task_id, attribute)

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

        await task_redis.initialize_task(task_id, task.dict(), initial_data)

        return task_id

    async def remove_task(self, task_id: str) -> None:
        await task_redis.remove_task(task_id)

        if task_id in self.endpoint_returns:
            del self.endpoint_returns[task_id]

    async def create_future(self, task_id: str) -> asyncio.Future:
        future = asyncio.Future()
        self.endpoint_returns[task_id] = future
        return future

    async def update_future(self, task_id: str, result: any) -> None:
        future = self.endpoint_returns[task_id]
        future.set_result(result)

    async def fetch_next_job(self, task_name: str, current_job: str) -> str:
        current_job_index = self.tasks[task_name]['jobs'].index(current_job)
        return self.tasks[task_name]['jobs'][current_job_index + 1]


class JobExecutor:
    async def execute_job(self, task_id: str) -> None:
        current_job = await task_redis.get_single_task_detail(task_id, "current_job")
        job_details = Job.parse_obj(task_helper.jobs[current_job])

        if job_details.type == "process":
            await self._execute_job_process(task_id, job_details)

        elif job_details.type == "return":
            await self._execute_job_return(task_id)

        elif job_details.type == "wait":
            await self._execute_job_wait(task_id)

        elif job_details.type == "end":
            await self._execute_job_end(task_id)

    @staticmethod
    async def _execute_job_process(task_id: str, job_details: Job) -> None:
        exchange = job_details.exchange
        routing_key = job_details.routing_key
        job_data = await task_redis.get_job_data(task_id)

        pika_helper.publish_message(exchange, routing_key, job_data)

    @staticmethod
    async def _execute_job_return(task_id: str) -> None:
        job_data = await task_redis.get_job_data(task_id)
        await task_helper.update_future(task_id, job_data)

    @staticmethod
    async def _execute_job_wait(task_id: str) -> None:
        # TODO: Implement, waits for a message from the exchange and routing key in job_details
        raise NotImplementedError

    @staticmethod
    async def _execute_job_end(task_id: str) -> None:
        await asyncio.sleep(10)
        await task_helper.remove_task(task_id)


# Create singletons
task_redis = TaskRedis()
task_helper = TaskHelper()
job_executor = JobExecutor()

