import json

from app.schemas.job_schemas import JobRequest, JobResponse
from app.utils.pika_utils import pika_utils
from app.utils.redis_utils import job_redis_utils


def handle_health_check(decoded_message_body):
    # TODO: Implement health check handler
    raise NotImplementedError
