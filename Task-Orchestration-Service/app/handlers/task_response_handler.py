import json

from app.schemas.task_schemas import TaskResponse, TaskRouteRequest
from app.utils.job_utils import job_utils
from app.utils.pika_utils import pika_utils
from app.utils.redis_utils import job_redis, task_redis
from app.utils.task_utils import task_utils


def handle_task_response(decoded_message_body):
    task_response = TaskResponse.model_validate(decoded_message_body)

    completed_task = task_redis.get_stored_task(task_response.task_id)

    job_utils.step_up_task_index(completed_task.job_id)
    job = job_redis.get_stored_job(completed_task.job_id)

    next_task = task_redis.get_stored_task(job.task_chain.split(',')[job.current_task_index])

    next_task_type = task_utils.determine_task_type(next_task)
    if next_task_type == "process":
        task_utils.route_process_task(completed_task, next_task, job, task_response.service_id)
    elif next_task_type == "return":
        task_utils.route_return_task(completed_task, next_task, job, task_response.service_id)
    elif next_task_type == "end":
        job_utils.delete_job(job)
