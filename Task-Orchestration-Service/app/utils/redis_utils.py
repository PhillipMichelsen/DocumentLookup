import redis

from app.schemas.job_schemas import JobSchema
from app.schemas.task_schemas import TaskSchema


class TaskRedis:
    # TODO: Add docstrings to all methods
    def __init__(self):
        self.redis = None

    def init_connection(self, host: str, port: int, db: int) -> None:
        """Initializes a connection to the Redis database

        :param host: The host of the Redis database
        :param port: The port of the Redis database
        :param db: The database number to use
        :return: None
        """
        self.redis = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def create_task(self, task_id: str, task: TaskSchema) -> None:
        """Creates a task in the Redis database

        :param task_id: The ID of the task to create
        :param task: The task to create
        :return: None
        """
        self.redis.hset(task_id, mapping=task.model_dump())

    def update_task_attribute(self, task_id: str, attribute: str, value: str) -> None:
        """Updates a task attribute in the Redis database

        :param task_id: The ID of the task to update
        :param attribute: The attribute to update
        :param value: The value to set the attribute to
        :return: None
        """
        self.redis.hset(task_id, attribute, value)

    def get_task_attribute(self, task_id: str, attribute: str) -> str:
        """Gets a task attribute from the Redis database

        :param task_id: The ID of the task to get the attribute from
        :param attribute: The attribute to get
        :return: The value of the attribute
        """
        return self.redis.hget(task_id, attribute)

    def get_task(self, task_id: str) -> TaskSchema:
        """Gets a task from the Redis database, returns a TaskSchema object

        :param task_id: The ID of the task to get
        :return: The task as a TaskSchema object
        """
        task = self.redis.hgetall(task_id)
        return TaskSchema(**task)

    def update_task(self, task: TaskSchema) -> None:
        """Updates a task in the Redis database

        :param task: The task to update
        :return: None
        """
        self.redis.hset(task.task_id, mapping=task.model_dump())

    def delete_task(self, task_id: str) -> None:
        """Deletes a task from the Redis database

        :param task_id: The ID of the task to delete
        :return: None
        """
        self.redis.delete(task_id)


class JobRedis:
    def __init__(self):
        self.redis = None

    def init_connection(self, host: str, port: int, db: int) -> None:
        """Initializes a connection to the Redis database

        :param host: The host of the Redis database
        :param port: The port of the Redis database
        :param db: The database number to use
        :return: None
        """
        self.redis = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def create_job(self, job_id: str, job: JobSchema) -> None:
        """Creates a job in the Redis database

        :param job_id: The ID of the job to create
        :param job: The job to create
        :return: None
        """
        self.redis.hset(job_id, mapping=job.model_dump())

    def update_job_attribute(self, job_id: str, attribute: str, value: str) -> None:
        """Updates a job attribute in the Redis database

        :param job_id: The ID of the job to update
        :param attribute: The attribute to update
        :param value: The value to set the attribute to
        :return: None
        """
        self.redis.hset(job_id, attribute, value)

    def get_job_attribute(self, job_id: str, attribute: str) -> str:
        """Gets a job attribute from the Redis database

        :param job_id: The ID of the job to get the attribute from
        :param attribute: The attribute to get
        :return: The value of the attribute
        """
        return self.redis.hget(job_id, attribute)

    def get_job(self, job_id: str) -> JobSchema:
        """Gets a job from the Redis database, returns a JobSchema object

        :param job_id: The ID of the job to get
        :return: The job as a JobSchema object
        """
        job = self.redis.hgetall(job_id)
        return JobSchema(**job)

    def delete_job(self, job_id: str) -> None:
        """Deletes a job from the Redis database

        :param job_id: The ID of the job to delete
        :return: None
        """
        self.redis.delete(job_id)


# Singleton instances
task_redis = TaskRedis()
job_redis = JobRedis()
