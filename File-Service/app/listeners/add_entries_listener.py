import json

from app.handlers.add_entries_handler import handle_add_entries


def on_message_add_entries(ch, method, properties, body):
    decoded_message_body = json.loads(body.decode('utf-8'))
    handle_add_entries(decoded_message_body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
