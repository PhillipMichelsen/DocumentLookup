import json

from app.handlers.minio_message_handler import handle_minio_message


def minio_message_callback(ch, method, properties, body):
    decoded_message_body = json.loads(body.decode('utf-8'))
    handle_minio_message(decoded_message_body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
