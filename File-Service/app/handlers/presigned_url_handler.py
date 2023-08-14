import json

from app.config import settings
from app.schemas.task_schemas import TaskRequest, TaskResponse
from app.schemas.tasks.presigned_url_schemas import PresignedURLUploadRequest, PresignedURLUploadResponse
from app.utils.minio_utils import minio_utils
from app.utils.pika_utils import pika_utils
from app.utils.response_hold_utils import response_hold


def handle_get_presigned_url_upload(decoded_message_body):
    task_request = TaskRequest.model_validate(decoded_message_body)
    presigned_url_upload_request = PresignedURLUploadRequest.model_validate(json.loads(task_request.request_content))

    presigned_url_upload, _ = minio_utils.generate_upload_url(
        bucket_name='test',
        filename=presigned_url_upload_request.filename
    )

    presigned_url_response = PresignedURLUploadResponse(presigned_url=presigned_url_upload)

    response_hold.stash_response(task_request.task_id, presigned_url_response)

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
