from app.listeners.file_upload_listener import on_message_get_presigned_url, on_message_file_uploaded
from app.listeners.file_processing_listener import on_message_process_file
from app.utils.pika_helper import pika_helper

# External queues
pika_helper.register_consumer('file_queue_get_presigned_url', 'get_presigned_url', on_message_get_presigned_url)

# Internal queues
pika_helper.register_consumer('file_queue_file_uploaded', 'file_uploaded', on_message_file_uploaded)
pika_helper.register_consumer('file_queue_process_file', 'process_file', on_message_process_file)


pika_helper.start_consuming()
