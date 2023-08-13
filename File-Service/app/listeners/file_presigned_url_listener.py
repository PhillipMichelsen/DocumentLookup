import json
from app.handlers.presigned_url_handler import handle_get_presigned_url_upload


def on_message_get_presigned_url_upload(ch, method, properties, body):
    decoded_message_body = json.loads(body.decode('utf-8'))
    handle_get_presigned_url_upload(decoded_message_body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
