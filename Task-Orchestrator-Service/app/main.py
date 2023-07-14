import logging

from app.utils.pika_utils import pika_helper
from app.utils.redis_utils import job_redis, task_redis
from app.utils.task_utils import task_utils
from app.utils.job_utils import job_utils

from app.listeners.task_request_listener import task_request_callback
from app.listeners.job_response_listener import job_response_callback

logging.basicConfig(level=logging.INFO)


def initialize():
    pika_helper.init_connection()
    pika_helper.declare_exchanges()

    job_redis.init_connection()
    task_redis.init_connection()

    task_utils.load_tasks()
    job_utils.load_jobs()

    logging.info("[*] Initialized!")


initialize()
pika_helper.register_consumer('task_request_queue', 'task_request', task_request_callback)
pika_helper.register_consumer('job_response_queue', 'job_response', job_response_callback)

pika_helper.start_consuming()


