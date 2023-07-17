from app.config import settings
from app.utils.task_utils import task_utils
from app.utils.job_utils import job_utils
from app.utils.pika_utils import pika_utils
from app.utils.redis_utils import job_redis, task_redis
from app.listeners.job_response_listener import job_response_callback
from app.listeners.task_request_listener import task_request_callback


def initialize():
    pika_utils.init_connection(
        host=settings.rabbitmq_host,
        username=settings.rabbitmq_username,
        password=settings.rabbitmq_password
    )

    pika_utils.declare_exchanges(settings.exchanges_file)

    task_redis.init_connection(
        host=settings.redis_host,
        port=settings.redis_port,
        db=0
    )
    job_redis.init_connection(
        host=settings.redis_host,
        port=settings.redis_port,
        db=1
    )

    task_utils.load_tasks(settings.task_file)
    job_utils.load_jobs(settings.job_file)


initialize()
pika_utils.register_consumer('task_request_queue', 'task_request', task_request_callback)
pika_utils.register_consumer('job_response_queue', 'job_response', job_response_callback)

pika_utils.start_consuming()
