import redis

from app.schemas.job_schemas import JobSchema


class JobRedisUtils:
    def __init__(self):
        self.redis = None

    def init_connection(self, host: str, port: int, db: int) -> None:
        """Initialize connection to Redis

        :param host: The host of the Redis server
        :param port: The port of the Redis server
        :param db: The database of the Redis server to use
        """
        try:
            self.redis = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        except redis.exceptions.ConnectionError as error:
            raise error

    def create_job(self, job_id: str, job: JobSchema) -> None:
        """Creates a new job in Redis

        :param job_id: The ID of the job
        :param job: The job to create
        """
        self.redis.hset(job_id, mapping=job.model_dump())

    def update_job_attribute(self, job_id: str, attribute: str, value: str) -> None:
        """Updates a job attribute in Redis

        :param job_id: The ID of the job
        :param attribute: The attribute to update
        :param value: The new value of the attribute
        """
        self.redis.hset(job_id, attribute, value)

    def get_job_attribute(self, job_id: str, attribute: str) -> str:
        """Gets a job attribute from Redis

        :param job_id: The ID of the job
        :param attribute: The attribute to get
        """
        return self.redis.hget(job_id, attribute)

    def get_job(self, job_id: str) -> JobSchema:
        """Gets a job from Redis, and returns it as a JobSchema object

        :param job_id: The ID of the job
        """
        job = self.redis.hgetall(job_id)
        return JobSchema(**job)

    def delete_job(self, job_id: str) -> None:
        """Deletes a job from Redis

        :param job_id: The ID of the job
        """
        self.redis.delete(job_id)


job_redis_utils = JobRedisUtils()
