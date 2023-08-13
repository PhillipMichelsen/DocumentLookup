from app.config import settings
from app.listeners.job_request_listener import job_request_callback
from app.listeners.task_response_listener import task_response_callback
from app.listeners.task_route_response_listener import task_route_response_callback
from app.utils.job_utils import job_utils
from app.utils.pika_utils import pika_utils
from app.utils.redis_utils import job_redis, task_redis
from app.utils.task_utils import task_utils

# Prepare pika connection and declare exchanges
pika_utils.init_connection(
    host=settings.rabbitmq_host,
    username=settings.rabbitmq_username,
    password=settings.rabbitmq_password
)
pika_utils.declare_exchanges(settings.exchanges_file)

# Prepare redis connections
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

# Load tasks and jobs
task_utils.load_tasks(settings.task_file)
job_utils.load_jobs(settings.job_file)

# Register consumer for job request
pika_utils.register_consumer(
    queue_name=settings.job_request_queue,
    exchange=settings.service_exchange,
    routing_key=settings.job_request_queue_routing_key,
    on_message_callback=job_request_callback,
    auto_delete=False
)

# Register consumer for task route response
pika_utils.register_consumer(
    queue_name=settings.task_route_response_queue,
    exchange=settings.service_exchange,
    routing_key=settings.task_route_response_queue_routing_key,
    on_message_callback=task_route_response_callback,
    auto_delete=False
)

# Register consumer for task response
pika_utils.register_consumer(
    queue_name=settings.task_response_queue,
    exchange=settings.service_exchange,
    routing_key=settings.task_response_queue_routing_key,
    on_message_callback=task_response_callback,
    auto_delete=False
)

# Start consuming messages, this is a blocking call
pika_utils.start_consuming()
