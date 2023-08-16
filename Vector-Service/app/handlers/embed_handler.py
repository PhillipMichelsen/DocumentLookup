import json

from app.config import settings
from app.modules.embed_module import generate_embeddings
from app.schemas.task_schemas import TaskRequest, TaskResponse
from app.schemas.service_tasks.embed_schemas import EmbedRequest, EmbedResponse
from app.utils.pika_utils import pika_utils
from app.utils.response_hold_utils import response_hold


def handle_embed(decoded_message_body):
    task_request = TaskRequest.model_validate(decoded_message_body)
    job_data = json.loads(task_request.job_data)
    embed_request = EmbedRequest.model_validate(job_data)

    embeddings = generate_embeddings(embed_request.text)

    embed_response = EmbedResponse(embedding=embeddings)

    job_data.update(embed_response.model_dump())
    response_hold.stash_job_data(task_request.task_id, job_data)

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
