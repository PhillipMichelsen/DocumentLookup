from pydantic import ValidationError

from app.utils.pika_handler import pika_handler
from app.modules.upload_module import get_upload_presigned_url, get_download_presigned_url
from app.schemas.upload_schemas import \
    GetPresignedURLUploadRequest, GetPresignedURLUploadResponse, \
    FileUploadedRequest, FileUploadedResponse


def handle_get_presigned_url_upload(raw_payload: dict) -> GetPresignedURLUploadResponse:
    try:
        request = GetPresignedURLUploadRequest(**raw_payload)
        presigned_url_upload = get_upload_presigned_url(request.filename)
        response = GetPresignedURLUploadResponse(presigned_url=presigned_url_upload)

    except ValidationError as e:
        response = GetPresignedURLUploadResponse(error=e.json())

    return response


def handle_file_uploaded(raw_payload: dict):
    request = FileUploadedRequest(**raw_payload)

    object_name = request.Records[0]['s3']['object']['key']
    bucket_name = request.Records[0]['s3']['bucket']['name']
    event_name = request.Records[0]['eventName']
    original_filename = request.Records[0]['s3']['object']['userMetadata']['X-Amz-Meta-Original-Filename']
    presigned_url_download = get_download_presigned_url(object_name)

    response = FileUploadedResponse(presigned_url=presigned_url_download)
    response_encoded_json = response.json().encode('utf-8')

    pika_handler.send_message_internal(
        exchange_name='file_exchange',
        routing_key='process_file',
        message=response_encoded_json
    )


