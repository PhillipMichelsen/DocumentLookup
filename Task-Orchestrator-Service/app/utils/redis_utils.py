import aioredis

from app.schemas.task_schemas import TaskSchema


class TaskRedis:
    def __init__(self):
        self.redis = None

    async def init_connection(self):
        self.redis = await aioredis.from_url("redis://redis-service", db=0, decode_responses=True)

    async def create_task(self, task_id: str, task: TaskSchema) -> None:
        await self.redis.hset(task_id, mapping=task.model_dump)

    async def update_task_detail(self, task_id: str, attribute: str, value: str) -> None:
        await self.redis.hset(task_id, attribute, value)

    async def get_task_detail(self, task_id: str, attribute: str) -> str:
        return await self.redis.hget(task_id, attribute)

    async def get_task(self, task_id: str) -> TaskSchema:
        task = await self.redis.hgetall(task_id)
        return TaskSchema(**task)

    async def delete_task(self, task_id: str) -> None:
        await self.redis.delete(task_id)


class JobRedis:
    def __init__(self):
        self.redis = None

    async def init_connection(self):
        self.redis = await aioredis.from_url("redis://redis-service", db=1, decode_responses=True)

    async def create_job(self, job_id: str) -> None:
        await self.redis.set(job_id, "PENDING")

    async def update_content(self, job_id: str, result: str) -> None:
        await self.redis.set(job_id, result)

    async def get_content(self, job_id: str) -> str:
        return await self.redis.get(job_id)

    async def delete_job(self, job_id: str) -> None:
        await self.redis.delete(job_id)


# Singleton instances
task_redis = TaskRedis()
job_redis = JobRedis()
