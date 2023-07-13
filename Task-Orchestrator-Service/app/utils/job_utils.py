import json

from app.schemas.job_schemas import JobsSchema
from app.utils.pika_utils import pika_helper
from app.utils.redis_utils import task_redis, job_redis

class JobUtils:
    def __init__(self):
        self.tasks = None

    async def load_tasks(self, task_file: str = "app/tasks.yaml") -> None:
        with open(task_file, "r") as stream:
            config = yaml.safe_load(stream)

            for task_name, task_config in config['tasks'].items():
                self.tasks[task_name] = JobsSchema(**task_config)

    async def get_job_details(self, job_name: str) -> JobsSchema:
        return self.tasks[job_name]

    async def execute_process_job(self, task_id: str) -> None:
        current_job = await task_redis.get_task_detail(task_id, "current_job")
        job_details = await self.get_job_details(current_job)

        message = json.dumps({"task_id": task_id})

        await pika_helper.publish_job(
            exchange_name=job_details.exchange,
            routing_key=job_details.routing_key,
            message=message.encode('utf-8')
        )

        await task_redis.update_task_detail(task_id, "status", "PROCESSING")

    async def execute_return_job(self, task_id: str) -> None:
        api_gateway_id = await task_redis.get_task_detail(task_id, "api_gateway_id")
        job_content = await job_redis.get_content(task_id)

        message = json.dumps()

        await pika_helper.publish_reply(
            api_gateway_id=api_gateway_id,
            task_id=task_id,
            message=message.encode('utf-8')
        )

        await task_redis.update_task_detail(task_id, "status", "RETURNED")
