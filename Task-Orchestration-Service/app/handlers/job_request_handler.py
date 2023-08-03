import json

from app.schemas.job_schemas import JobRequest
from app.schemas.task_schemas import TaskRequest
from app.utils.job_utils import job_utils
from app.utils.redis_utils import task_redis
from app.utils.task_utils import task_utils


def handle_job_request(decoded_message_body):
    job_request = JobRequest.model_validate(decoded_message_body)

    job = job_utils.create_job(
        job_name=job_request.job_name,
        job_id=job_request.job_id,
        initial_request_content=job_request.initial_request_content,
        requesting_service_id=job_request.requesting_service_id
    )

    current_task_id = job.task_chain.split(',')[job.current_task_index]
    task = task_redis.get_stored_task(current_task_id)

    task_request = TaskRequest(
        task_id=task.task_id,
        request_content=job.initial_request_content
    )
    task_utils.send_task(task, json.dumps(task_request.model_dump()))
