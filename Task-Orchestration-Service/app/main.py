from app.config import settings
from app.listeners.job_request_listener import on_message_job_request
from app.listeners.minio_put_event_listener import on_message_minio_put_event
from app.listeners.task_response_listener import on_message_task_response
from app.listeners.task_route_response_listener import on_message_task_route_response
from app.listeners.add_tasks_to_job_listener import on_message_add_tasks_to_job
from app.utils.job_utils import job_utils
from app.utils.pika_utils import pika_utils
from app.utils.redis_utils import job_redis, task_redis
from app.utils.task_utils import task_utils

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
task_utils.load_tasks()
job_utils.load_jobs()

# Prepare pika connection and declare exchanges
pika_utils.init_connection(
    host=settings.rabbitmq_host,
    username=settings.rabbitmq_username,
    password=settings.rabbitmq_password
)
pika_utils.declare_exchanges()

# Register consumer for job request
pika_utils.register_consumer(
    queue_name=settings.job_request_queue,
    exchange=settings.service_exchange,
    routing_key=settings.job_request_queue_routing_key,
    on_message_callback=on_message_job_request,
    auto_delete=False
)

pika_utils.register_consumer(
    queue_name=settings.minio_put_event_queue,
    exchange=settings.service_exchange,
    routing_key=settings.minio_put_event_queue_routing_key,
    on_message_callback=on_message_minio_put_event,
    auto_delete=False
)

pika_utils.register_consumer(
    queue_name=settings.add_tasks_to_job_queue,
    exchange=settings.service_exchange,
    routing_key=settings.add_tasks_to_job_queue_routing_key,
    on_message_callback=on_message_add_tasks_to_job,
    auto_delete=False,
    priority=10
)

# Register consumer for task route response
pika_utils.register_consumer(
    queue_name=settings.task_route_response_queue,
    exchange=settings.service_exchange,
    routing_key=settings.task_route_response_queue_routing_key,
    on_message_callback=on_message_task_route_response,
    auto_delete=False
)

# Register consumer for task response
pika_utils.register_consumer(
    queue_name=settings.task_response_queue,
    exchange=settings.service_exchange,
    routing_key=settings.task_response_queue_routing_key,
    on_message_callback=on_message_task_response,
    auto_delete=False
)

# Start consuming messages, this is a blocking call
pika_utils.start_consuming()
