import json

from app.schemas.service_tasks.get_files_schemas import GetFilesRequest, GetFilesResponse
from app.schemas.task_schemas import TaskRequest
from app.utils.postgres_utils import file_table_utils
from app.utils.postgres_utils import postgres_utils
from app.utils.weaviate_utils import weaviate_utils
from app.utils.service_utils import send_handler_messages


def handle_get_files_handler(decoded_message_body):
    task_request = TaskRequest.model_validate(decoded_message_body)
    job_data = json.loads(task_request.job_data)
    get_files_request = GetFilesRequest.model_validate(job_data)

    document_ids = postgres_utils.get_all_document_ids()
    files = [postgres_utils.get_file_by_document_id(doc_id) for doc_id in document_ids]

    response_document_ids = []
    response_filenames = []
    response_file_statuses = []

    for file in files:
        embedded_entries = weaviate_utils.retrieve_count_by_document_id(file.document_id)

        response_document_ids.append(file.document_id)
        response_filenames.append(file.original_file_name)
        response_file_statuses.append(
            file_table_utils.determine_processing_status(file.total_entries, embedded_entries)
        )

    get_files_response = GetFilesResponse(
        document_id=response_document_ids,
        filename=response_filenames,
        file_status=response_file_statuses
    )

    send_handler_messages(task_request.task_id, job_data, get_files_response)
