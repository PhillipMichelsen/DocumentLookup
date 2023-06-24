import json

from app.handlers.upload_handler import handle_get_presigned_url_upload, handle_file_uploaded
from app.utils.pika_handler import pika_handler


def on_message_get_presigned_url(ch, method, properties, body):
    data = json.loads(body.decode('utf-8'))

    response = handle_get_presigned_url_upload(data)
    response_encoded_json = response.json().encode('utf-8')

    pika_handler.send_response(
        reply_to=properties.reply_to,
        correlation_id=properties.correlation_id,
        message=response_encoded_json,
    )

    ch.basic_ack(delivery_tag=method.delivery_tag)


def on_message_file_uploaded(ch, method, properties, body):
    data = json.loads(body.decode('utf-8'))

    handle_file_uploaded(data)

    ch.basic_ack(delivery_tag=method.delivery_tag)
