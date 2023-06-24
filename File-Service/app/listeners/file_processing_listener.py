import json

from app.handlers.processing_handler import handle_process_file
from app.utils.pika_helper import pika_helper


def on_message_process_file(ch, method, properties, body):
    """This function is called when a message is received from the queue

    Decodes the message and passes it to the handler function
    """
    data = json.loads(body.decode('utf-8'))

    handle_process_file(data)

    ch.basic_ack(delivery_tag=method.delivery_tag)
