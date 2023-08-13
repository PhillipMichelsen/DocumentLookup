import json

from app.config import settings
from app.modules.embed_module import generate_embeddings
from app.schemas.task_schemas import TaskRequest, TaskResponse
from app.schemas.tasks.embed_schemas import EmbedRequest, EmbedResponse
from app.utils.pika_utils import pika_utils
from app.utils.response_hold_utils import response_hold


def handle_embed(decoded_message_body):
    task_request = TaskRequest.model_validate(decoded_message_body)
    print(f'Embed request received: {task_request.request_content}', flush=True)
    embed_request = EmbedRequest.model_validate(json.loads(task_request.request_content))

    embeddings = generate_embeddings(embed_request.sentences)

    embed_response = EmbedResponse(embedding=embeddings)

    response_hold.stash_response(task_request.task_id, embed_response)

    task_response = TaskResponse(
        task_id=task_request.task_id,
        service_id=pika_utils.service_id,
        status='COMPLETED'
    )

    message = json.dumps(task_response.model_dump())

    pika_utils.publish_message(
        exchange_name=settings.task_orchestrator_exchange,
        routing_key=settings.task_orchestrator_task_response_routing_key,
        message=message.encode('utf-8')
    )
