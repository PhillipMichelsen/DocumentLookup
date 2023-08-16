import json

from app.config import settings
from app.modules.embed_module import generate_embeddings
from app.schemas.task_schemas import TaskRequest, TaskResponse
from app.schemas.service_tasks.embed_store_schemas import EmbedStoreRequest
from app.utils.pika_utils import pika_utils
from app.utils.weaviate_utils import weaviate_utils
from app.utils.response_hold_utils import response_hold


def handle_embed_store(decoded_message_body):
    task_request = TaskRequest.model_validate(decoded_message_body)
    job_data = json.loads(task_request.job_data)
    embed_store_request = EmbedStoreRequest.model_validate(job_data)

    embeddings = generate_embeddings(embed_store_request.text)
    embeddings_with_uuid = [(embeddings[i], embed_store_request.uuid[i]) for i in range(len(embeddings))]

    for embedding, uuid in embeddings_with_uuid:
        weaviate_utils.add_vector_to_entry(uuid, embedding)

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