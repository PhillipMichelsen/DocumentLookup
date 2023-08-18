import json
import uuid

from app.config import settings
from app.modules.processing_module import grobid_fulltext_pdf, parse_grobid_output
from app.schemas.job_schemas import JobRequest
from app.schemas.jobs import embed_store_schemas
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
    entries = len(divs) + len(paragraphs)

    file_data = {
        "document_id": object_name,
        "original_file_name": 'test.pdf',
        "user_id": 'testing',
        "total_entries": entries,
        "entries_processed": 0
    }

    postgres_utils.add_file(file_data)

    def process_items(items, item_type):
        for i in range(0, len(items), settings.batch_size):
            group = items[i:i + settings.batch_size]
            uuids = []

            for item in group:
                entry_uuid = weaviate_utils.add_entry(item, item_type, object_name)
                uuids.append(entry_uuid)

            job = JobRequest(
                job_name='embed_store_text',
                requesting_service_exchange=settings.service_exchange,
                requesting_service_return_queue_routing_key='None',
                requesting_service_id=pika_utils.service_id,
                job_id=str(uuid.uuid4()),
                job_data=json.dumps(embed_store_schemas.EmbedStoreRequest(
                    document_id=object_name,
                    text=group,
                    uuid=uuids
                ).model_dump())
            )

            task_message = json.dumps(job.model_dump())
            pika_utils.publish_message(
                exchange_name=settings.task_orchestrator_exchange,
                routing_key=settings.task_orchestrator_job_request_routing_key,
                message=task_message.encode('utf-8')
            )

    process_items(divs, "div")
    process_items(paragraphs, "paragraph")

    process_file_response = ProcessFileResponse(paragraphs=paragraphs)

    send_handler_messages(task_request.task_id, job_data, process_file_response)
