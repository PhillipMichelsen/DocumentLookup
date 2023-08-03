from app.schemas.task_schemas import TaskRouteRequest
from app.utils.job_utils import job_utils
from app.utils.redis_utils import job_redis, task_redis
from app.utils.task_utils import task_utils


def handle_task_response(decoded_message_body):
    task_response = TaskRouteRequest.model_validate(decoded_message_body)

    completed_task = task_redis.get_stored_task(task_response.task_id)
    job = job_redis.get_stored_job(completed_task.job_id)

    job_utils.step_up_task_index(job.job_id)
    new_task = task_redis.get_stored_task(job.task_chain.split(',')[job.current_task_index])

    task_utils.send_task_routing_instructions(completed_task, new_task, task_response.service_id)
