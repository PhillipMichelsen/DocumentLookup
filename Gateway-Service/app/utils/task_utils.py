import asyncio
import json
import uuid
import logging

import aioredis
import yaml

from app.schemas.tasks_schema import Task, Job
from app.utils.pika_async_utils import pika_helper


class TaskRedis:
    def __init__(self):
        self.redis_tasks = None
        self.redis_job_data = None

    def connect_redis(self):
        self.redis_tasks = aioredis.from_url("redis://redis", db=0, decode_responses=True)
        self.redis_job_data = aioredis.from_url("redis://redis", db=1, decode_responses=True)
        logging.info("Connected to Redis")

    async def initialize_task(self, task_id: str, task: dict, initial_data: str) -> None:
        await self.redis_tasks.hset(task_id, mapping=task)
        await self.redis_job_data.set(task_id, initial_data)

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

    async def get_job_data(self, task_id: str) -> str:
        response = await self.redis_job_data.get(task_id)
        return response

    async def update_job_data(self, task_id: str, response: str) -> None:
        await self.redis_job_data.set(task_id, response)


class TaskHelper:
    def __init__(self):
        self.tasks = {}
        self.jobs = {}
        self.endpoint_returns = {}

    def load_tasks_yaml(self, task_file: str = "app/tasks.yml"):
        with open(task_file, "r") as stream:
            config = yaml.safe_load(stream)

            for task_name, task_config in config['tasks'].items():
                self.tasks[task_name] = task_config

            for job_name, job_config in config['jobs'].items():
                self.jobs[job_name] = Job(**job_config)

        logging.info("Loaded tasks.yml!")

    async def create_task(self, task_name: str, initial_data: str) -> tuple[dict, asyncio.Future]:
        task_id = str(uuid.uuid4())
        task = Task(
            name=task_name,
            current_job=self.tasks[task_name]['jobs'][0],
            original_gateway_id=pika_helper.service_id,
            status="initialized"
        )

        await task_redis.initialize_task(task_id, task.dict(), initial_data)
        return_future = self.create_future(task_id)

        headers = {
            "task_id": task_id,
            "original_gateway_id": pika_helper.service_id,
        }

        logging.info(f"[+] Created new task, {task_name}. Task ID: {task_id}")

        return headers, return_future

    async def remove_task(self, task_id: str) -> None:
        await task_redis.remove_task(task_id)

        if task_id in self.endpoint_returns:
            del self.endpoint_returns[task_id]

    def create_future(self, task_id: str) -> asyncio.Future:
        future = asyncio.Future()
        self.endpoint_returns[task_id] = future
        return future

    async def update_future(self, task_id: str, result: any) -> None:
        future = self.endpoint_returns[task_id]
        future.set_result(result)

    async def fetch_next_job(self, task_name: str, current_job: str) -> str:
        current_job_index = self.tasks[task_name]['jobs'].index(current_job)
        return self.tasks[task_name]['jobs'][current_job_index + 1]

    async def step_next_job(self, task_id: str) -> None:
        task_name = await task_redis.get_single_task_detail(task_id, "name")
        current_job = await task_redis.get_single_task_detail(task_id, "current_job")

        if current_job == "end":
            pass
        else:
            next_job = await self.fetch_next_job(task_name, current_job)
            await task_redis.update_single_task_detail(task_id, "current_job", next_job)


class JobExecutor:
    async def execute_job(self, task_id: str, headers: dict) -> None:
        current_job = await task_redis.get_single_task_detail(task_id, "current_job")
        job_details = task_helper.jobs[current_job]

        if job_details.type == "process":
            await self._execute_job_process(task_id, job_details, headers)

        elif job_details.type == "return":
            await self._execute_job_return(task_id, job_details, headers)

        elif job_details.type == "wait":
            await self._execute_job_wait(task_id, job_details)

        elif job_details.type == "end":
            await self._execute_job_end(task_id)

    @staticmethod
    async def _execute_job_process(task_id: str, job_details: Job, headers: dict) -> None:
        logging.info(f"[+] Executing process job, {job_details.name} for task {task_id}")
        job_data = await task_redis.get_job_data(task_id)

        await pika_helper.publish_message(
            exchange_name=job_details.exchange,
            routing_key=job_details.routing_key,
            headers=headers,
            message=job_data.encode('utf-8')
        )

        await task_redis.update_single_task_detail(task_id, "status", "processing")

    @staticmethod
    async def _execute_job_return(task_id: str, job_details: Job, headers: dict) -> None:
        logging.info(f"[+] Executing return job, {job_details.name} for task {task_id}")

        job_data = await task_redis.get_job_data(task_id)
        await task_helper.update_future(task_id, job_data)

        await task_helper.step_next_job(task_id)

        message = json.dumps({"task_id": task_id})

        await pika_helper.publish_message(
            exchange_name="gateway_exchange",
            routing_key=".job",
            headers=headers,
            message=message.encode('utf-8')
        )

        await task_redis.update_single_task_detail(task_id, "status", "processing_background")

    @staticmethod
    async def _execute_job_wait(task_id: str, job_details: Job) -> None:
        logging.info(f"[+] Executing wait job, {job_details.name} for task {task_id}")
        await task_redis.update_single_task_detail(task_id, "status", "waiting")
        await task_redis.update_single_task_detail(task_id, "current_job", job_details.name)

    @staticmethod
    async def _execute_job_end(task_id: str) -> None:
        logging.info(f"[+] Executing end job for task {task_id}")
        await task_redis.update_single_task_detail(task_id, "status", "completed")
        await asyncio.sleep(10)
        await task_helper.remove_task(task_id)


# Create singletons
task_redis = TaskRedis()
task_helper = TaskHelper()
job_executor = JobExecutor()
