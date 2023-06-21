from app.responsers.upload_responder import on_message_get_presigned_url, on_message_file_uploaded
from app.responsers.processing_responder import on_message_process_file
from app.utils.pika_handler import pika_handler

# External queues
pika_handler.register_consumer('file_queue_get_presigned_url', 'get_presigned_url', on_message_get_presigned_url)

# Internal queues
pika_handler.register_consumer('file_queue_file_uploaded', 'file_uploaded', on_message_file_uploaded)
pika_handler.register_consumer('file_queue_process_file', 'process_file', on_message_process_file)


pika_handler.start_consuming()
