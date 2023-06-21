import datetime
import mimetypes
import uuid

from app.utils.minio_connection import minio_client


def get_upload_presigned_url(filename: str) -> str:
    uuid_name = str(uuid.uuid4())
    content_type, _ = mimetypes.guess_type(filename)

    presigned_url = minio_client.get_presigned_url(
        method='PUT',
        bucket_name='test',
        object_name=uuid_name,
        expires=datetime.timedelta(minutes=10),
        response_headers={'response-content-type': content_type},
        extra_query_params={'X-Amz-Meta-Original-Filename': filename}
    )

    return presigned_url


def get_download_presigned_url(object_name: str) -> str:
    presigned_url = minio_client.get_presigned_url(
        method='GET',
        bucket_name='test',
        object_name=object_name,
        expires=datetime.timedelta(minutes=10),
    )

    return presigned_url
