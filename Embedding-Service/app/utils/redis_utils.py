import redis

from app.schemas.job_schemas import JobSchema


class JobRedisUtils:
    def __init__(self):
        self.redis = None

    def init_connection(self, host: str, port: int, db: int) -> None:
        self.redis = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def create_job(self, job_id: str, job: JobSchema) -> None:
        self.redis.hset(job_id, mapping=job.model_dump())

    def update_job_attribute(self, job_id: str, attribute: str, value: str) -> None:
        self.redis.hset(job_id, attribute, value)

    def get_job_attribute(self, job_id: str, attribute: str) -> str:
        return self.redis.hget(job_id, attribute)

    def get_job(self, job_id: str) -> JobSchema:
        job = self.redis.hgetall(job_id)
        return JobSchema(**job)

    def delete_job(self, job_id: str) -> None:
        self.redis.delete(job_id)


job_redis_utils = JobRedisUtils()
