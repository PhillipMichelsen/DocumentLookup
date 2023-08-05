from app.schemas.task_schemas import TaskRouteResponse
from app.utils.redis_utils import job_redis, task_redis
from app.utils.task_utils import task_utils


def handle_task_route_response(decoded_message_body):
    task_route_response = TaskRouteResponse.model_validate(decoded_message_body)

    next_task = task_redis.get_stored_task(task_route_response.new_task_id)
    new_task_attributes = task_utils.tasks[next_task.task_name]

    if new_task_attributes.task_type == 'return':
        job = job_redis.get_stored_job(next_task.job_id)

        job_chain = job.task_chain.split(',')
        for task in job_chain:
            task_redis.delete_stored_task(task)

        job_redis.delete_stored_job(job.job_id)
