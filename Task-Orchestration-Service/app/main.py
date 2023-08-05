from app.config import settings
from app.listeners.job_request_listener import job_request_callback
from app.listeners.task_response_listener import task_response_callback
from app.listeners.task_route_response_listener import task_route_response_callback
from app.utils.job_utils import job_utils
from app.utils.pika_utils import pika_utils
from app.utils.redis_utils import job_redis, task_redis
from app.utils.task_utils import task_utils


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
pika_utils.register_consumer(settings.task_response_queue, settings.task_response_queue_routing_key,
                             task_response_callback)
pika_utils.register_consumer(settings.job_request_queue, settings.job_request_queue_routing_key, job_request_callback)
pika_utils.register_consumer(settings.task_route_response_queue, settings.task_route_response_queue_routing_key,
                             task_route_response_callback)

pika_utils.start_consuming()
