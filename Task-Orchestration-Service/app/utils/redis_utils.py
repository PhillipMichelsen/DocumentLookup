import redis

from app.schemas.task_schemas import TaskSchema
from app.schemas.job_schemas import JobSchema


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

    def store_job(self, job: JobSchema) -> None:
        """Creates a job

        :param job: The job to create
        :return: None
        """
        self.redis.hset(job.job_id, job.model_dump())

    def update_task_index(self, job_id: str, task_index: int) -> None:
        """Updates the task index of a job

        :param job_id: The ID of the job to update
        :param task_index: The new task index
        :return: None
        """
        self.redis.hset(job_id, 'current_task_index', task_index)

    def update_job_status(self, job_id: str, status: str) -> None:
        """Updates the status of a job

        :param job_id: The ID of the job to update
        :param status: The new status
        :return: None
        """
        self.redis.hset(job_id, 'status', status)

    def get_stored_job(self, job_id: str) -> JobSchema:
        """Gets a job

        :param job_id: The ID of the job to get
        :return: The job
        """
        job = self.redis.hgetall(job_id)
        return JobSchema.model_validate(job)

    def delete_stored_job(self, job_id: str) -> None:
        """Deletes a job

        :param job_id: The ID of the job to delete
        :return: None
        """
        self.redis.delete(job_id)


class TaskRedis:
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

    def store_task(self, task: TaskSchema) -> None:
        """Creates a task

        :param task: The task to create
        :return: None
        """
        self.redis.hset(task.task_id, task.model_dump())

    def update_task_status(self, task_id: str, status: str) -> None:
        """Updates the status of a task

        :param task_id: The ID of the task to update
        :param status: The new status
        :return: None
        """
        self.redis.hset(task_id, 'status', status)

    def get_stored_task(self, task_id: str) -> TaskSchema:
        """Gets a task

        :param task_id: The ID of the task to get
        :return: The task
        """
        task = self.redis.hgetall(task_id)
        return TaskSchema.model_validate(task)

    def delete_stored_task(self, task_id: str) -> None:
        """Deletes a task

        :param task_id: The ID of the task to delete
        :return: None
        """
        self.redis.delete(task_id)


# Singleton instances
job_redis = JobRedis()
task_redis = TaskRedis()
