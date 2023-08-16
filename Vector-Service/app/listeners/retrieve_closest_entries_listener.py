import json

from app.handlers.retrieve_closest_entries_handler import handle_retrieve_closest_entries


def on_message_retrieve_closest_entries(ch, method, properties, body):
    decoded_message_body = json.loads(body.decode('utf-8'))
    handle_retrieve_closest_entries(decoded_message_body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
