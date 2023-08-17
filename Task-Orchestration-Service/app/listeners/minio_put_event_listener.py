import json

from app.handlers.minio_put_event_handler import handle_minio_put_event


def on_message_minio_put_event(ch, method, properties, body):
    decoded_message_body = json.loads(body.decode('utf-8'))
    handle_minio_put_event(decoded_message_body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
