from app.schemas.job_schemas import JobRequest
from app.utils.task_utils import task_utils
from app.utils.job_utils import job_utils
from app.utils.pika_utils import pika_utils
from app.utils.redis_utils import task_redis


def handle_job_request(decoded_message_body):
    job_request = JobRequest.model_validate(decoded_message_body)

    job = job_utils.create_job(
        job_name=job_request.job_name,
        job_id=job_request.job_id,
        initial_request=job_request.initial_request_content,
        requesting_service_id=job_request.requesting_service_id
    )

    current_task_id = job.task_chain.split(',')[job.current_task_index]
    task = task_redis.get_stored_task(current_task_id)

    task_utils.send_task(task, job.initial_request_content)
