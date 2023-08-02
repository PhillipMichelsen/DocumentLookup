import json

from app.schemas.task_schemas import JobRequest, JobResponse
from app.utils.pika_utils import pika_utils


def handle_health_check(decoded_message_body):
    # TODO: Implement health check handler
    raise NotImplementedError
