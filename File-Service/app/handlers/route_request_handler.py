import json

from app.config import settings
from app.schemas.task_schemas import TaskRequest, TaskRouteRequest, TaskRouteResponse
from app.utils.pika_utils import pika_utils
from app.utils.response_hold_utils import response_hold


def handle_route_request(decoded_message_body):
    task_route_request = TaskRouteRequest.model_validate(decoded_message_body)
    stashed_response = response_hold.get_job_data(task_route_request.task_id)

    task_request = TaskRequest(
        task_id=task_route_request.next_task_id,
        job_id=task_route_request.job_id,
        job_data=json.dumps(stashed_response)
    )

    task_route_response = TaskRouteResponse(
        task_id=task_route_request.task_id,
        next_task_id=task_route_request.next_task_id,
        service_id=pika_utils.service_id,
        status='COMPLETED'
    )

    message = json.dumps(task_request.model_dump())
    pika_utils.publish_message(
        exchange_name=task_route_request.exchange,
        routing_key=task_route_request.routing_key,
        message=message.encode('utf-8')
    )

    message = json.dumps(task_route_response.model_dump())
    pika_utils.publish_message(
        exchange_name=settings.task_orchestrator_exchange,
        routing_key=settings.task_orchestrator_task_route_response_routing_key,
        message=message.encode('utf-8')
    )
