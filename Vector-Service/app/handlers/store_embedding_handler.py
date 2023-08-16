import json

from app.config import settings
from app.schemas.task_schemas import TaskRequest, TaskResponse
from app.schemas.service_tasks.store_embedding_schemas import StoreEmbeddingRequest
from app.utils.pika_utils import pika_utils
from app.utils.weaviate_utils import weaviate_utils


def handle_store_embedding(decoded_message_body):
    task_request = TaskRequest.model_validate(decoded_message_body)
    job_data = json.loads(task_request.job_data)
    store_vector_request = StoreEmbeddingRequest.model_validate(job_data)

    for embedding, uuid in zip(store_vector_request.embedding, store_vector_request.uuid):
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
