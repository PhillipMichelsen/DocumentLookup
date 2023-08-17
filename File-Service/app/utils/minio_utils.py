import uuid
from typing import Tuple

from minio import Minio


class MinioUtils:
    def __init__(self):
        self.minio = None

    def init_connection(self, endpoint: str, access_key: str, secret_key: str) -> None:
        """Initialize connection to Minio

        :param endpoint: The endpoint of the Minio server
        :param access_key: The access key of the Minio server
        :param secret_key: The secret key of the Minio server
        :return: None
        """
        self.minio = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=False
        )

    def generate_upload_url(self, bucket_name: str, filename: str) -> Tuple[str, str]:
        """Generates a presigned upload URL and returns it along with a generated UUID for the object.

        :param bucket_name: The name of the bucket
        :param filename: The original filename of the object
        :return: Presigned upload URL and object UUID
        """
        object_name = str(uuid.uuid4())

        presigned_url = self.minio.get_presigned_url(
            method='PUT',
            bucket_name=bucket_name,
            object_name=object_name,
        )

        return presigned_url, object_name

    def generate_download_url(self, bucket_name: str, object_name: str) -> str:
        """Generates a presigned download URL for the object.

        :param bucket_name: The name of the bucket
        :param object_name: The name of the object
        :return: Presigned download URL
        """
        presigned_url = self.minio.get_presigned_url(
            method='GET',
            bucket_name=bucket_name,
            object_name=object_name,
        )

        return presigned_url

    def delete_object(self, bucket_name: str, object_name: str) -> None:
        """Deletes an object from a bucket.

        :param bucket_name: The name of the bucket
        :param object_name: The name of the object
        :return: None
        """
        self.minio.remove_object(bucket_name, object_name)


minio_utils = MinioUtils()
