import json
import uuid
from app.config import settings
from app.modules.processing_module import grobid_fulltext_pdf, parse_grobid_output
from app.schemas.task_schemas import TaskRequest, TaskResponse
from app.schemas.tasks.processing_schemas import ProcessFileRequest
from app.schemas.job_schemas import JobRequest
from app.utils.minio_utils import minio_utils
from app.utils.pika_utils import pika_utils
from app.utils.weaviate_utils import weaviate_utils


def handle_process_file(decoded_message_body):
    task_request = TaskRequest.model_validate(decoded_message_body)
    process_file_request = ProcessFileRequest.model_validate(json.loads(task_request.request_content))

    object_name = process_file_request.Records[0]['s3']['object']['key']
    bucket_name = process_file_request.Records[0]['s3']['bucket']['name']

    grobid_output = grobid_fulltext_pdf(bucket_name, object_name)
    divs, paragraphs = parse_grobid_output(grobid_output)

    def process_items(items, item_type):
        for i in range(0, len(items), 20):
            group = items[i:i + 20]
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
                initial_request_content=json.dumps({"text": group, "uuid": uuids})
            )

            task_message = json.dumps(job.model_dump())
            pika_utils.publish_message(
                exchange_name=settings.task_orchestrator_exchange,
                routing_key=settings.task_orchestrator_job_request_routing_key,
                message=task_message.encode('utf-8')
            )

    process_items(divs, "div")
    process_items(paragraphs, "paragraph")

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
