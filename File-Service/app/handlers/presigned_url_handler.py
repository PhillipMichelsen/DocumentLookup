import json

from app.config import settings
from app.schemas.task_schemas import TaskRequest, TaskResponse
from app.schemas.servicve_tasks.presigned_url_schemas import PresignedURLUploadRequest, PresignedURLUploadResponse
from app.utils.minio_utils import minio_utils
from app.utils.pika_utils import pika_utils
from app.utils.response_hold_utils import response_hold


def handle_get_presigned_url_upload(decoded_message_body):
    task_request = TaskRequest.model_validate(decoded_message_body)
    job_data = json.loads(task_request.job_data)
    presigned_url_upload_request = PresignedURLUploadRequest.model_validate(job_data)

    presigned_url_upload, _ = minio_utils.generate_upload_url(
        bucket_name='test',
        filename=presigned_url_upload_request.filename
    )

    presigned_url_response = PresignedURLUploadResponse(presigned_url=presigned_url_upload)

    job_data.update(presigned_url_response.model_dump())
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
