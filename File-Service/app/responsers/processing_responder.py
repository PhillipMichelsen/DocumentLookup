import json

from app.handlers.processing_handler import handle_process_file
from app.utils.pika_handler import pika_handler


def on_message_process_file(ch, method, properties, body):
    data = json.loads(body.decode('utf-8'))

    handle_process_file(data)

    ch.basic_ack(delivery_tag=method.delivery_tag)




