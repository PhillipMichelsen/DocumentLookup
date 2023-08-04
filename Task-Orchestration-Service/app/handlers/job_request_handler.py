import json

from app.schemas.job_schemas import JobRequest
from app.schemas.task_schemas import TaskRequest
from app.utils.job_utils import job_utils
from app.utils.redis_utils import task_redis
from app.utils.pika_utils import pika_utils
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
    task_attributes = task_utils.tasks[task.task_name]

    task_request = TaskRequest(
        task_id=task.task_id,
        job_id=job.job_id,
        request_content=job.initial_request_content
    )

    message = json.dumps(task_request.model_dump())
    pika_utils.publish_message(
        exchange_name=task_attributes.exchange,
        routing_key=task_attributes.routing_key,
        message=message.encode()
    )


