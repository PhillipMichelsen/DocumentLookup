import json

from app.config import settings
from app.schemas.task_schemas import TaskRequest, TaskResponse
from app.schemas.service_tasks.retrieve_closest_entries_schemas import RetrieveClosestEntriesRequest, RetrieveClosestEntriesResponse
from app.utils.pika_utils import pika_utils
from app.utils.weaviate_utils import weaviate_utils
from app.utils.response_hold_utils import response_hold


def handle_retrieve_closest_entries(decoded_message_body):
    task_request = TaskRequest.model_validate(decoded_message_body)
    job_data = json.loads(task_request.job_data)
    retrieve_request = RetrieveClosestEntriesRequest.model_validate(job_data)

    closest_entries = weaviate_utils.retrieve_closest_entries(
        vector=retrieve_request.embedding[0],
        top_n=retrieve_request.top_n,
        type_filter=retrieve_request.type_filter,
        document_id=retrieve_request.document_id
    )

    closest_text = [entry['text'] for entry in closest_entries['data']['Get']['Text']]

    retrieve_response = RetrieveClosestEntriesResponse(entries=closest_text)
    job_data.update(retrieve_response.model_dump())
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
