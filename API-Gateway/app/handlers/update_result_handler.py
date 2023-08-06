from app.schemas.task_schemas import TaskRequest, TaskResponse
from app.utils.response_utils import response_utils
from app.utils.pika_utils import pika_utils
from app.config import settings
import json


async def handle_update_result(decoded_message_body):
    request = TaskRequest.model_validate(decoded_message_body)
    await response_utils.update_response(request.task_id, request.request_content)

    task_response = TaskResponse(
        task_id=request.task_id,
        service_id=pika_utils.service_id,
        status='COMPLETED'
    )

    message = json.dumps(task_response.model_dump())
    await pika_utils.publish_message(
        exchange_name=settings.task_orchestrator_exchange,
        routing_key=settings.task_orchestrator_task_response_routing_key,
        message=message.encode('utf-8')
    )
