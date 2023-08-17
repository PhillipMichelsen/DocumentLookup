import json

from app.schemas.service_tasks.presigned_url_schemas import PresignedURLUploadRequest, PresignedURLUploadResponse
from app.schemas.task_schemas import TaskRequest
from app.utils.minio_utils import minio_utils
from app.utils.service_utils import send_handler_messages


def handle_get_presigned_url_upload(decoded_message_body):
    task_request = TaskRequest.model_validate(decoded_message_body)
    job_data = json.loads(task_request.job_data)
    presigned_url_upload_request = PresignedURLUploadRequest.model_validate(job_data)

    presigned_url_upload, _ = minio_utils.generate_upload_url(
        bucket_name='test',
        filename=presigned_url_upload_request.filename
    )

    presigned_url_response = PresignedURLUploadResponse(presigned_url=presigned_url_upload)

    send_handler_messages(task_request.task_id, job_data, presigned_url_response)
