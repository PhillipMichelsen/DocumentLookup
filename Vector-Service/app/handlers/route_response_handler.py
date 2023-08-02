import json

from app.schemas.task_schemas import TaskRequest, TaskRouteResponse
from app.utils.pika_utils import pika_utils
from app.utils.response_hold_utils import response_hold


def handle_route_response(decoded_message_body):
    request = TaskRouteResponse.model_validate(decoded_message_body)

    stashed_response = response_hold.get_response(request.task_id)

    task_request = TaskRequest(
        task_id=request.next_task_id,
        request_content=stashed_response.model_dump()
    )

    message = json.dumps(task_request.model_dump())

    pika_utils.publish_message(
        exchange_name=request.exchange,
        routing_key=request.routing_key,
        message=message.encode()
    )
