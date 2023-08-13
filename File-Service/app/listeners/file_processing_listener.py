import json

from app.handlers.processing_handler import handle_process_file


def on_message_process_file(ch, method, properties, body):
    decoded_message_body = json.loads(body.decode('utf-8'))
    handle_process_file(decoded_message_body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
