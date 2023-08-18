import json

from app.schemas.service_tasks.add_entries_schemas import AddEntriesRequest, AddEntriesResponse
from app.schemas.task_schemas import TaskRequest
from app.utils.weaviate_utils import weaviate_utils
from app.utils.service_utils import send_handler_messages
from app.utils.postgres_utils import postgres_utils


def handle_add_entries(decoded_message_body):
    task_request = TaskRequest.model_validate(decoded_message_body)
    job_data = json.loads(task_request.job_data)
    add_entry_request = AddEntriesRequest.model_validate(job_data)

    for entry_type in add_entry_request.entries:
        postgres_utils.append_weaviate_uuids(entry_type[2], weaviate_utils.batch_add_entries(
            entry_type[0],
            entry_type[1],
            entry_type[2],
        ))

    add_entries_response = AddEntriesResponse(entries_added=len(add_entry_request.entries))

    send_handler_messages(task_request.task_id, job_data, add_entries_response)
