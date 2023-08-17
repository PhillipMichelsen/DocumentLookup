import json

from app.schemas.service_tasks.retrieve_closest_entries_schemas import RetrieveClosestEntriesRequest, \
    RetrieveClosestEntriesResponse
from app.schemas.task_schemas import TaskRequest
from app.utils.service_utils import send_handler_messages
from app.utils.weaviate_utils import weaviate_utils


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

    send_handler_messages(task_request.task_id, job_data, retrieve_response)
