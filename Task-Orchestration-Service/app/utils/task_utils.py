import yaml

from app.schemas.task_schemas import TaskSchema, TasksSchema
from app.utils.job_utils import job_utils
from app.utils.redis_utils import task_redis


class TaskUtils:
    def __init__(self):
        self.tasks = {}

    def load_tasks(self, task_file) -> None:
        with open(task_file, "r") as stream:
            config = yaml.safe_load(stream)

            for task_name, task_config in config['tasks'].items():
                self.tasks[task_name] = TasksSchema(**task_config)

    def create_task(self, task_name: str, task_id: str, api_gateway_id: str, initial_request: str) -> TaskSchema:
        jobs = list()
        for job_index, job_name in enumerate(self.tasks[task_name].jobs):
            if job_index == 0:
                job_id = job_utils.create_job(
                    job_name=job_name,
                    task_id=task_id,
                    previous_job_id="START",
                    initial_request=initial_request
                )
            else:
                job_id = job_utils.create_job(
                    job_name=job_name,
                    task_id=task_id,
                    previous_job_id=jobs[job_index - 1],
                    initial_request="WAITING"
                )

            jobs.append(job_id)

        task = TaskSchema(
            name=task_name,
            task_id=task_id,
            job_chain=','.join(jobs),
            current_job_index=0,
            api_gateway_id=api_gateway_id,
            status="INITIALIZED"
        )

        task_redis.create_task(task_id, task)

        return task

    @staticmethod
    def step_job_chain(task_id: str) -> str:
        task = task_redis.get_task(task_id)
        task_redis.update_task_attribute(task_id, "current_job_index", task.current_job_index + 1)

        return task.job_chain.split(',')[task.current_job_index + 1]


# Singleton instance
task_utils = TaskUtils()
