from app.config import settings
from app.listeners.clear_job_data_listener import on_message_clear_job_data
from app.listeners.file_presigned_url_listener import on_message_get_presigned_url_upload
from app.listeners.file_processing_listener import on_message_process_file
from app.listeners.get_files_listener import on_message_get_files
from app.listeners.route_request_listener import on_message_route_request
from app.utils.minio_utils import minio_utils
from app.utils.pika_utils import pika_utils
from app.utils.postgres_utils import postgres_utils
from app.utils.weaviate_utils import weaviate_utils

postgres_utils.init_connection('postgresql://postgres:postgres@postgres-service:5432/documentlookup')
postgres_utils.create_tables()

minio_utils.init_connection(
    endpoint=settings.minio_host,
    access_key=settings.minio_access_key,
    secret_key=settings.minio_secret_key
)

weaviate_utils.init_connection(
    host=settings.weaviate_host,
    port=settings.weaviate_port
)

# Prepare pika connection and declare exchanges
pika_utils.init_connection(
    host=settings.rabbitmq_host,
    username=settings.rabbitmq_username,
    password=settings.rabbitmq_password
)
pika_utils.declare_exchanges()

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

pika_utils.register_consumer(
    queue_name=settings.get_files_queue,
    exchange=settings.service_exchange,
    routing_key=settings.get_files_queue_routing_key,
    on_message_callback=on_message_get_files,
    auto_delete=False,
    priority=10
)

# Register route request consumer
pika_utils.register_consumer(
    queue_name=f'{pika_utils.service_id}_{settings.route_request_queue}',
    exchange=settings.service_exchange,
    routing_key=f'{pika_utils.service_id}_{settings.route_request_queue_routing_key}',
    on_message_callback=on_message_route_request,
    auto_delete=True
)

# Register clear job data consumer
pika_utils.register_consumer(
    queue_name=f'{pika_utils.service_id}_{settings.clear_job_data_queue}',
    exchange=settings.service_exchange,
    routing_key=f'{pika_utils.service_id}_{settings.clear_job_data_queue_routing_key}',
    on_message_callback=on_message_clear_job_data,
    auto_delete=True
)

# Start consuming messages
pika_utils.start_consuming()
