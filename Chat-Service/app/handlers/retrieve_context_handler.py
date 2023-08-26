import json

from app.schemas.service_tasks.retrieve_context_schemas import RetrieveContextRequest, RetrieveContextResponse
from app.schemas.task_schemas import TaskRequest
from app.utils.weaviate_utils import weaviate_utils
from app.utils.service_utils import send_handler_messages


def handle_retrieve_context(decoded_message_body):
    task_request = TaskRequest.model_validate(decoded_message_body)
    job_data = json.loads(task_request.job_data)
    retrieve_context_request = RetrieveContextRequest.model_validate(job_data)

    closest_entries = weaviate_utils.retrieve_closest_entries(
        retrieve_context_request.context_query,
        retrieve_context_request.top_n,
        retrieve_context_request.text_type,
        retrieve_context_request.document_ids
    )

    closest_entries = [entry['text'] for entry in closest_entries['data']['Get']['Text']]

    retrieve_context_response = RetrieveContextResponse(context=closest_entries)

    send_handler_messages(task_request.task_id, job_data, retrieve_context_response)
