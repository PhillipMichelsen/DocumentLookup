import json

from app.config import settings
from app.schemas.task_schemas import TaskResponse
from app.utils.pika_utils import pika_utils
from app.utils.response_hold_utils import response_hold


def send_handler_messages(task_id, job_data, response):
    job_data.update(response.model_dump())
    response_hold.stash_job_data(task_id, job_data)

    task_response = TaskResponse(
        task_id=task_id,
        service_id=pika_utils.service_id,
        status='COMPLETED'
    )

    message = json.dumps(task_response.model_dump())
    pika_utils.publish_message(
        exchange_name=settings.task_orchestrator_exchange,
        routing_key=settings.task_orchestrator_task_response_routing_key,
        message=message.encode('utf-8')
    )
