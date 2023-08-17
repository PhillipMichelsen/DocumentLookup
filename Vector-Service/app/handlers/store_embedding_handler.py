import json

from app.schemas.service_tasks.store_embedding_schemas import StoreEmbeddingRequest, StoreEmbeddingResponse
from app.schemas.task_schemas import TaskRequest
from app.utils.postgres_utils import postgres_utils
from app.utils.service_utils import send_handler_messages
from app.utils.weaviate_utils import weaviate_utils


def handle_store_embedding(decoded_message_body):
    task_request = TaskRequest.model_validate(decoded_message_body)
    job_data = json.loads(task_request.job_data)
    store_vector_request = StoreEmbeddingRequest.model_validate(job_data)

    for embedding, uuid in zip(store_vector_request.embedding, store_vector_request.uuid):
        weaviate_utils.add_vector_to_entry(uuid, embedding)

    postgres_utils.increment_entries_processed(store_vector_request.document_id, len(store_vector_request.uuid))

    store_embedding_response = StoreEmbeddingResponse(uuid=store_vector_request.uuid)

    send_handler_messages(task_request.task_id, job_data, store_embedding_response)
