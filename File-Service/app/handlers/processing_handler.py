import json
import uuid

from app.config import settings
from app.modules.processing_module import grobid_fulltext_pdf, parse_grobid_output
from app.schemas.service_tasks.processing_schemas import ProcessFileRequest, ProcessFileResponse
from app.schemas.task_schemas import TaskRequest
from app.utils.pika_utils import pika_utils
from app.utils.postgres_utils import postgres_utils
from app.utils.service_utils import send_handler_messages
from app.utils.weaviate_utils import weaviate_utils


def handle_process_file(decoded_message_body):
    task_request = TaskRequest.model_validate(decoded_message_body)
    job_data = json.loads(task_request.job_data)
    process_file_request = ProcessFileRequest.model_validate(job_data)

    object_name = process_file_request.Records[0]['s3']['object']['key']
    bucket_name = process_file_request.Records[0]['s3']['bucket']['name']

    grobid_output = grobid_fulltext_pdf(bucket_name, object_name)
    divs, paragraphs = parse_grobid_output(grobid_output)
    entry_count = len(divs) + len(paragraphs)

    file_data = {
        "document_id": object_name,
        "original_file_name": 'test.pdf',
        "user_id": 'testing',
        "total_entries": entry_count,
    }

    postgres_utils.add_file(file_data)

    entries = [
        (paragraphs, 'paragraph', object_name),
        (divs, 'div', object_name)
    ]

    process_file_response = ProcessFileResponse(entries=entries)

    send_handler_messages(task_request.task_id, job_data, process_file_response)
