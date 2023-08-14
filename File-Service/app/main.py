from app.config import settings
from app.listeners.file_presigned_url_listener import on_message_get_presigned_url_upload
from app.listeners.file_processing_listener import on_message_process_file
from app.listeners.route_request_listener import on_message_route_request
from app.utils.minio_utils import minio_utils
from app.utils.pika_utils import pika_utils

minio_utils.init_connection(
    endpoint=settings.minio_host,
    access_key=settings.minio_access_key,
    secret_key=settings.minio_secret_key
)

# Prepare pika connection and declare exchanges
pika_utils.init_connection(
    host=settings.rabbitmq_host,
    username=settings.rabbitmq_username,
    password=settings.rabbitmq_password
)
pika_utils.declare_exchanges(settings.exchanges_file)

# Register presigned url upload consumer
pika_utils.register_consumer(
    queue_name=settings.file_queue_presigned_url_upload,
    exchange=settings.service_exchange,
    routing_key=settings.file_queue_presigned_url_upload_routing_key,
    on_message_callback=on_message_get_presigned_url_upload,
    auto_delete=False
)

pika_utils.register_consumer(
    queue_name=settings.file_queue_process_file,
    exchange=settings.service_exchange,
    routing_key=settings.file_queue_process_file_routing_key,
    on_message_callback=on_message_process_file,
    auto_delete=False
)

# Register route request consumer
pika_utils.register_consumer(
    queue_name=f'{pika_utils.service_id}_{settings.route_request_queue}',
    exchange=settings.task_routing_exchange,
    routing_key=f'{pika_utils.service_id}_{settings.route_request_queue_routing_key}',
    on_message_callback=on_message_route_request,
    auto_delete=True
)

# Start consuming messages
pika_utils.start_consuming()
