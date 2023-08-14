import json
import uuid
from app.config import settings
from app.schemas.job_schemas import JobRequest, JobResponse
from app.schemas.task_schemas import TaskRequest
from app.utils.job_utils import job_utils
from app.utils.pika_utils import pika_utils
from app.utils.redis_utils import task_redis
from app.utils.task_utils import task_utils


def handle_minio_message(decoded_message_body):
    print(f'Minio messaged received: {decoded_message_body}', flush=True)

    job = job_utils.create_job(
        job_name='process_file',
        job_id=str(uuid.uuid4()),
        initial_request_content=json.dumps(decoded_message_body),
        requesting_service_exchange=settings.service_exchange,
        requesting_service_return_queue_routing_key='None',
        requesting_service_id=pika_utils.service_id
    )

    current_task_id = job.task_chain.split(',')[job.current_task_index]

    task = task_redis.get_stored_task(current_task_id)
    task_attributes = task_utils.tasks[task.task_name]

    return_task = job_utils.get_return_task(job)

    task_request = TaskRequest(
        task_id=task.task_id,
        job_id=job.job_id,
        request_content=job.initial_request_content
    )

    job_response = JobResponse(
        job_name=job.job_name,
        job_id=job.job_id,
        return_task_id=return_task.task_id,
        status='CREATED'
    )

    message = json.dumps(task_request.model_dump())
    pika_utils.publish_message(
        exchange_name=task_attributes.exchange,
        routing_key=task_attributes.routing_key,
        message=message.encode('utf-8')
    )
