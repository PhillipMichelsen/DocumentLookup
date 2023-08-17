import json
import uuid

from app.config import settings
from app.schemas.job_schemas import JobRequest
from app.utils.pika_utils import pika_utils
from app.utils.response_utils import response_utils


async def job_request_response(request, job_name: str) -> str:
    """Handles all the logic for a job request and waiting for a response

    :param request: The request object
    :param job_name: The name of the job to be requested
    :return: The response from the job
    """
    job_id = str(uuid.uuid4())

    job = JobRequest(
        job_name=job_name,
        requesting_service_exchange=settings.service_exchange,
        requesting_service_return_queue_routing_key=settings.update_result_queue_routing_key,
        requesting_service_id=pika_utils.service_id,
        job_id=job_id,
        job_data=json.dumps(request.model_dump())
    )

    task_result_response_future = await response_utils.create_response(job_id)

    message = json.dumps(job.model_dump())
    await pika_utils.publish_message(
        exchange_name=settings.task_orchestrator_exchange,
        routing_key=settings.task_orchestrator_job_request_routing_key,
        message=message.encode('utf-8')
    )

    return_task_id = await task_result_response_future

    job_response_future = await response_utils.create_response(return_task_id)

    return await job_response_future
