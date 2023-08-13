from app.schemas.tasks.processing_schemas import ProcessFileRequest, ProcessFileResponse
from app.schemas.task_schemas import TaskRequest, TaskResponse
from app.utils.minio_utils import minio_utils
from app.utils.response_hold_utils import response_hold
from app.utils.pika_utils import pika_utils
from app.modules.processing_module import grobid_fulltext_pdf, parse_grobid_output
from app.config import settings
import json


def handle_process_file(decoded_message_body):
    task_request = TaskRequest.model_validate(decoded_message_body)
    process_file_request = ProcessFileRequest.model_validate(task_request.request_content)

    object_name = process_file_request.Records[0]['s3']['object']['key']
    bucket_name = process_file_request.Records[0]['s3']['bucket']['name']
    event_name = process_file_request.Records[0]['eventName']
    original_filename = process_file_request.Records[0]['s3']['object']['userMetadata']['X-Amz-Meta-Original-Filename']
    presigned_url_download = minio_utils.generate_download_url('test', object_name)

    grobid_output = grobid_fulltext_pdf(presigned_url_download)
    paragraphs, sentences = parse_grobid_output(grobid_output)

    process_file_response = ProcessFileResponse(paragraphs=paragraphs, sentences=sentences)

    response_hold.stash_response(task_request.task_id, process_file_response)

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
