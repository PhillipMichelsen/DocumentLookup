import json
from typing import List

from app.config import settings
from app.schemas.job_schemas import AddTasksToJobRequest
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


def send_add_task_to_job_message(job_id: str, requesting_task_id: str, task_names: List[str]) -> None:
    add_tasks_to_job_request = AddTasksToJobRequest(
        job_id=job_id,
        requesting_task_id=requesting_task_id,
        task_names=task_names
    )

    message = json.dumps(add_tasks_to_job_request.model_dump())
    pika_utils.publish_message(
        exchange_name=settings.task_orchestrator_exchange,
        routing_key=settings.task_orchestrator_add_tasks_to_job_routing_key,
        message=message.encode('utf-8')
    )
