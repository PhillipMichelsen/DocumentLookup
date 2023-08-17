import json

from app.handlers.get_files_handler import handle_get_files_handler


def on_message_get_files(ch, method, properties, body):
    decoded_message_body = json.loads(body.decode('utf-8'))
    handle_get_files_handler(decoded_message_body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
